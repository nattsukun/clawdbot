#!/usr/bin/env python3
"""
Clawdbot Setup Wizard - macOS Edition
Protected Installer with Native GUI
"""

import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import threading
import json
from pathlib import Path
import plistlib

# Configuration
APP_NAME = "Clawdbot"
APP_VERSION = "2026.1.25"
CONFIG_DIR = Path.home() / ".clawdbot"
NODE_MIN_VERSION = 22
BUNDLE_IDENTIFIER = "bot.clawd.installer"

class Color:
    """ANSI color codes for terminal"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class MacSetupWizard:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{APP_NAME} Setup Wizard")
        
        # macOS native window style
        self.root.geometry("750x600")
        self.root.resizable(False, False)
        
        # Set macOS appearance
        try:
            # Use native macOS appearance
            self.root.tk.call('tk::unsupported::MacWindowStyle', 'style', self.root._w, 'moveableModal', '')
        except:
            pass
        
        # Variables
        self.install_type = tk.StringVar(value="current")
        self.gateway_mode = tk.StringVar(value="local")
        self.provider_name = tk.StringVar(value="skip")
        self.api_key = tk.StringVar()
        self.log_level = tk.StringVar(value="info")
        self.install_path = tk.StringVar(value=str(Path.home() / "clawdbot"))
        self.repo_url = tk.StringVar(value="https://github.com/clawdbot/clawdbot.git")
        self.create_app_bundle = tk.BooleanVar(value=True)
        self.add_to_dock = tk.BooleanVar(value=True)
        self.create_launchd = tk.BooleanVar(value=True)
        
        # Pages
        self.pages = []
        self.current_page = 0
        
        # Create UI
        self.create_widgets()
        self.show_page(0)
        
    def create_widgets(self):
        """Create all UI widgets"""
        # Header with macOS style
        header_frame = tk.Frame(self.root, bg="#f5f5f7", height=90)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text=f"📦 {APP_NAME} Setup",
            font=("SF Pro Display", 24, "bold"),
            bg="#f5f5f7",
            fg="#1d1d1f"
        ).pack(pady=30)
        
        # Content frame
        self.content_frame = tk.Frame(self.root, bg="white")
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Navigation buttons (macOS style)
        nav_frame = tk.Frame(self.root, bg="#f5f5f7", height=70)
        nav_frame.pack(fill=tk.X, side=tk.BOTTOM)
        nav_frame.pack_propagate(False)
        
        self.prev_btn = tk.Button(
            nav_frame,
            text="← Go Back",
            command=self.prev_page,
            width=12,
            state=tk.DISABLED,
            relief=tk.FLAT,
            bg="#e8e8ed",
            fg="#1d1d1f"
        )
        self.prev_btn.pack(side=tk.LEFT, padx=30, pady=20)
        
        self.next_btn = tk.Button(
            nav_frame,
            text="Continue →",
            command=self.next_page,
            width=15,
            relief=tk.FLAT,
            bg="#007aff",
            fg="white",
            font=("SF Pro Display", 11, "bold")
        )
        self.next_btn.pack(side=tk.RIGHT, padx=30, pady=20)
        
        # Create pages
        self.create_welcome_page()
        self.create_prerequisites_page()
        self.create_install_type_page()
        self.create_macos_options_page()
        self.create_configuration_page()
        self.create_installation_page()
        self.create_completion_page()
        
    def create_welcome_page(self):
        """Welcome page with macOS style"""
        frame = tk.Frame(self.content_frame, bg="white")
        
        # App icon area (placeholder)
        icon_frame = tk.Frame(frame, bg="white", width=100, height=100)
        icon_frame.pack(pady=20)
        
        tk.Label(
            frame,
            text=f"Welcome to {APP_NAME}",
            font=("SF Pro Display", 20, "bold"),
            bg="white",
            fg="#1d1d1f"
        ).pack(pady=10)
        
        tk.Label(
            frame,
            text="A powerful messaging gateway with AI capabilities",
            font=("SF Pro Text", 13),
            bg="white",
            fg="#86868b"
        ).pack(pady=5)
        
        # Features box
        features_frame = tk.Frame(frame, bg="#f5f5f7", relief=tk.FLAT)
        features_frame.pack(pady=20, padx=40, fill=tk.X)
        
        features = [
            ("💬", "Multi-Channel Support", "WhatsApp, Telegram, Discord, Slack & more"),
            ("🤖", "AI-Powered Agent", "Advanced RPC mode with multiple providers"),
            ("🔌", "Plugin System", "Extensible architecture for custom features"),
            ("🌐", "Gateway Server", "Remote access and control capabilities")
        ]
        
        for emoji, title, desc in features:
            feature_row = tk.Frame(features_frame, bg="#f5f5f7")
            feature_row.pack(fill=tk.X, padx=20, pady=10)
            
            tk.Label(
                feature_row,
                text=emoji,
                font=("SF Pro Text", 24),
                bg="#f5f5f7"
            ).pack(side=tk.LEFT, padx=(0, 15))
            
            text_frame = tk.Frame(feature_row, bg="#f5f5f7")
            text_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            tk.Label(
                text_frame,
                text=title,
                font=("SF Pro Text", 12, "bold"),
                bg="#f5f5f7",
                fg="#1d1d1f",
                anchor="w"
            ).pack(fill=tk.X)
            
            tk.Label(
                text_frame,
                text=desc,
                font=("SF Pro Text", 10),
                bg="#f5f5f7",
                fg="#86868b",
                anchor="w"
            ).pack(fill=tk.X)
        
        tk.Label(
            frame,
            text="Click Continue to begin installation",
            font=("SF Pro Text", 11),
            bg="white",
            fg="#86868b"
        ).pack(pady=20)
        
        self.pages.append(frame)
        
    def create_prerequisites_page(self):
        """Prerequisites check page"""
        frame = tk.Frame(self.content_frame, bg="white")
        
        tk.Label(
            frame,
            text="System Requirements",
            font=("SF Pro Display", 18, "bold"),
            bg="white",
            fg="#1d1d1f"
        ).pack(pady=20)
        
        tk.Label(
            frame,
            text="Checking your system for required software...",
            font=("SF Pro Text", 11),
            bg="white",
            fg="#86868b"
        ).pack(pady=5)
        
        self.prereq_text = scrolledtext.ScrolledText(
            frame,
            height=15,
            width=70,
            font=("SF Mono", 10),
            bg="#f5f5f7",
            relief=tk.FLAT
        )
        self.prereq_text.pack(pady=15)
        
        tk.Button(
            frame,
            text="Check Requirements",
            command=self.check_prerequisites,
            relief=tk.FLAT,
            bg="#34c759",
            fg="white",
            font=("SF Pro Text", 11)
        ).pack(pady=10)
        
        self.pages.append(frame)
        
    def create_install_type_page(self):
        """Installation type selection"""
        frame = tk.Frame(self.content_frame, bg="white")
        
        tk.Label(
            frame,
            text="Installation Type",
            font=("SF Pro Display", 18, "bold"),
            bg="white",
            fg="#1d1d1f"
        ).pack(pady=20)
        
        tk.Label(
            frame,
            text="Choose how you want to install Clawdbot",
            font=("SF Pro Text", 11),
            bg="white",
            fg="#86868b"
        ).pack(pady=5)
        
        options_frame = tk.Frame(frame, bg="white")
        options_frame.pack(pady=20, fill=tk.BOTH, expand=True)
        
        # Radio button style for macOS
        for value, text, desc in [
            ("current", "📁 Current Directory", "Install from the current location (for development)"),
            ("global", "🌐 Global Installation", "Install system-wide using npm"),
            ("clone", "📥 Clone Repository", "Download and install from GitHub")
        ]:
            option_frame = tk.Frame(options_frame, bg="#f5f5f7", relief=tk.FLAT)
            option_frame.pack(fill=tk.X, padx=20, pady=5)
            
            rb = tk.Radiobutton(
                option_frame,
                text=text,
                variable=self.install_type,
                value=value,
                bg="#f5f5f7",
                font=("SF Pro Text", 12, "bold"),
                anchor="w"
            )
            rb.pack(fill=tk.X, padx=15, pady=5)
            
            tk.Label(
                option_frame,
                text=desc,
                font=("SF Pro Text", 10),
                bg="#f5f5f7",
                fg="#86868b",
                anchor="w"
            ).pack(fill=tk.X, padx=40, pady=(0, 10))
        
        # Path configuration
        path_frame = tk.Frame(frame, bg="white")
        path_frame.pack(pady=15, fill=tk.X, padx=30)
        
        tk.Label(
            path_frame,
            text="Installation Path:",
            font=("SF Pro Text", 11),
            bg="white",
            anchor="w"
        ).pack(fill=tk.X)
        
        path_entry_frame = tk.Frame(path_frame, bg="white")
        path_entry_frame.pack(fill=tk.X, pady=5)
        
        tk.Entry(
            path_entry_frame,
            textvariable=self.install_path,
            font=("SF Mono", 11),
            relief=tk.FLAT,
            bg="#f5f5f7"
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)
        
        tk.Button(
            path_entry_frame,
            text="Browse...",
            command=self.browse_path,
            relief=tk.FLAT,
            bg="#e8e8ed"
        ).pack(side=tk.RIGHT, padx=(5, 0))
        
        self.pages.append(frame)
        
    def create_macos_options_page(self):
        """macOS-specific options"""
        frame = tk.Frame(self.content_frame, bg="white")
        
        tk.Label(
            frame,
            text="macOS Integration",
            font=("SF Pro Display", 18, "bold"),
            bg="white",
            fg="#1d1d1f"
        ).pack(pady=20)
        
        tk.Label(
            frame,
            text="Configure macOS-specific features",
            font=("SF Pro Text", 11),
            bg="white",
            fg="#86868b"
        ).pack(pady=5)
        
        options_frame = tk.Frame(frame, bg="#f5f5f7", relief=tk.FLAT)
        options_frame.pack(pady=20, padx=30, fill=tk.BOTH, expand=True)
        
        # Checkboxes with descriptions
        for var, text, desc in [
            (self.create_app_bundle, "📦 Create App Bundle", "Create Clawdbot.app in /Applications"),
            (self.add_to_dock, "🎯 Add to Dock", "Pin Clawdbot to your Dock for easy access"),
            (self.create_launchd, "🚀 Launch at Startup", "Start gateway automatically when you log in")
        ]:
            option_row = tk.Frame(options_frame, bg="#f5f5f7")
            option_row.pack(fill=tk.X, padx=20, pady=10)
            
            cb = tk.Checkbutton(
                option_row,
                text=text,
                variable=var,
                bg="#f5f5f7",
                font=("SF Pro Text", 12, "bold"),
                anchor="w"
            )
            cb.pack(fill=tk.X)
            
            tk.Label(
                option_row,
                text=desc,
                font=("SF Pro Text", 10),
                bg="#f5f5f7",
                fg="#86868b",
                anchor="w"
            ).pack(fill=tk.X, padx=25)
        
        self.pages.append(frame)
        
    def create_configuration_page(self):
        """Configuration page"""
        frame = tk.Frame(self.content_frame, bg="white")
        
        tk.Label(
            frame,
            text="Configuration",
            font=("SF Pro Display", 18, "bold"),
            bg="white",
            fg="#1d1d1f"
        ).pack(pady=20)
        
        config_frame = tk.Frame(frame, bg="#f5f5f7", relief=tk.FLAT)
        config_frame.pack(pady=10, padx=30, fill=tk.BOTH, expand=True)
        
        # Gateway mode
        self.create_config_row(config_frame, "Gateway Mode:", self.gateway_mode, 
                               ["local", "remote"], 0)
        
        # AI Provider
        self.create_config_row(config_frame, "AI Provider:", self.provider_name,
                               ["openai", "anthropic", "google", "skip"], 1)
        
        # API Key
        tk.Label(
            config_frame,
            text="API Key:",
            font=("SF Pro Text", 11, "bold"),
            bg="#f5f5f7",
            anchor="w"
        ).grid(row=2, column=0, sticky="w", padx=20, pady=10)
        
        tk.Entry(
            config_frame,
            textvariable=self.api_key,
            show="•",
            font=("SF Mono", 11),
            relief=tk.FLAT,
            bg="white"
        ).grid(row=2, column=1, sticky="ew", padx=20, pady=10, ipady=5)
        
        # Log level
        self.create_config_row(config_frame, "Log Level:", self.log_level,
                               ["debug", "info", "warn", "error"], 3)
        
        config_frame.columnconfigure(1, weight=1)
        
        self.pages.append(frame)
        
    def create_config_row(self, parent, label_text, variable, values, row):
        """Helper to create configuration row"""
        tk.Label(
            parent,
            text=label_text,
            font=("SF Pro Text", 11, "bold"),
            bg="#f5f5f7",
            anchor="w"
        ).grid(row=row, column=0, sticky="w", padx=20, pady=10)
        
        combo = ttk.Combobox(
            parent,
            textvariable=variable,
            values=values,
            state="readonly",
            font=("SF Pro Text", 11)
        )
        combo.grid(row=row, column=1, sticky="ew", padx=20, pady=10)
        
    def create_installation_page(self):
        """Installation progress page"""
        frame = tk.Frame(self.content_frame, bg="white")
        
        tk.Label(
            frame,
            text="Installing Clawdbot",
            font=("SF Pro Display", 18, "bold"),
            bg="white",
            fg="#1d1d1f"
        ).pack(pady=20)
        
        self.install_status = tk.Label(
            frame,
            text="Preparing installation...",
            font=("SF Pro Text", 11),
            bg="white",
            fg="#86868b"
        )
        self.install_status.pack(pady=5)
        
        self.progress = ttk.Progressbar(
            frame,
            length=600,
            mode='indeterminate'
        )
        self.progress.pack(pady=15)
        
        self.install_text = scrolledtext.ScrolledText(
            frame,
            height=15,
            width=70,
            font=("SF Mono", 10),
            bg="#f5f5f7",
            relief=tk.FLAT
        )
        self.install_text.pack(pady=10)
        
        self.pages.append(frame)
        
    def create_completion_page(self):
        """Completion page"""
        frame = tk.Frame(self.content_frame, bg="white")
        
        tk.Label(
            frame,
            text="✓",
            font=("SF Pro Display", 48),
            bg="white",
            fg="#34c759"
        ).pack(pady=20)
        
        tk.Label(
            frame,
            text="Installation Complete!",
            font=("SF Pro Display", 20, "bold"),
            bg="white",
            fg="#1d1d1f"
        ).pack(pady=10)
        
        tk.Label(
            frame,
            text=f"{APP_NAME} has been successfully installed on your Mac",
            font=("SF Pro Text", 12),
            bg="white",
            fg="#86868b"
        ).pack(pady=5)
        
        # Next steps
        steps_frame = tk.Frame(frame, bg="#f5f5f7", relief=tk.FLAT)
        steps_frame.pack(pady=20, padx=40, fill=tk.X)
        
        tk.Label(
            steps_frame,
            text="Next Steps:",
            font=("SF Pro Text", 12, "bold"),
            bg="#f5f5f7",
            anchor="w"
        ).pack(fill=tk.X, padx=20, pady=(15, 5))
        
        steps = [
            "1. Run 'clawdbot login' to connect to WhatsApp",
            "2. Start gateway with 'clawdbot gateway run'",
            "3. Check status with 'clawdbot channels status'",
            "",
            "Documentation available at:",
            "• ~/clawdbot/INSTALLATION-TH.md",
            "• ~/clawdbot/USER-GUIDE-TH.md",
            "• https://docs.clawd.bot"
        ]
        
        for step in steps:
            tk.Label(
                steps_frame,
                text=step,
                font=("SF Pro Text", 10),
                bg="#f5f5f7",
                fg="#1d1d1f" if step and step[0].isdigit() else "#86868b",
                anchor="w"
            ).pack(fill=tk.X, padx=30, pady=2)
        
        # Action buttons
        button_frame = tk.Frame(frame, bg="white")
        button_frame.pack(pady=20)
        
        tk.Button(
            button_frame,
            text="🚀 Start Gateway Now",
            command=self.start_gateway,
            relief=tk.FLAT,
            bg="#007aff",
            fg="white",
            font=("SF Pro Text", 12)
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="📱 Open in Finder",
            command=self.open_in_finder,
            relief=tk.FLAT,
            bg="#e8e8ed",
            font=("SF Pro Text", 12)
        ).pack(side=tk.LEFT, padx=5)
        
        self.pages.append(frame)
    
    def show_page(self, page_num):
        """Show specific page"""
        for page in self.pages:
            page.pack_forget()
        
        if 0 <= page_num < len(self.pages):
            self.pages[page_num].pack(fill=tk.BOTH, expand=True)
            self.current_page = page_num
            
            self.prev_btn.config(state=tk.NORMAL if page_num > 0 else tk.DISABLED)
            
            if page_num == len(self.pages) - 1:
                self.next_btn.config(text="Finish", command=self.finish)
            else:
                self.next_btn.config(text="Continue →", command=self.next_page)
                
    def next_page(self):
        """Go to next page"""
        if self.current_page == 2:  # Install type page
            self.current_page = 3  # Go to macOS options
        elif self.current_page == 4:  # Config page
            self.current_page = 5
            self.show_page(5)
            self.run_installation()
            return
        else:
            self.current_page += 1
            
        self.show_page(self.current_page)
        
    def prev_page(self):
        """Go to previous page"""
        if self.current_page > 0:
            self.current_page -= 1
            self.show_page(self.current_page)
    
    def browse_path(self):
        """Browse for installation path"""
        path = filedialog.askdirectory(
            initialdir=str(Path.home()),
            title="Choose Installation Directory"
        )
        if path:
            self.install_path.set(path)
            
    def check_prerequisites(self):
        """Check system prerequisites"""
        self.prereq_text.delete(1.0, tk.END)
        
        def check():
            self.log_prereq("Checking macOS system requirements...\n\n")
            
            # Check macOS version
            self.log_prereq("➤ Checking macOS version...")
            try:
                result = subprocess.run(['sw_vers', '-productVersion'], capture_output=True, text=True)
                macos_version = result.stdout.strip()
                self.log_prereq(f" {macos_version}\n  ✓ macOS compatible\n\n")
            except:
                self.log_prereq(" ✗ Unable to detect\n\n")
            
            # Check Homebrew
            self.log_prereq("➤ Checking Homebrew...")
            brew_installed, _ = self.check_command("brew")
            if brew_installed:
                self.log_prereq(" ✓ Found\n\n")
            else:
                self.log_prereq(" ⚠ Not installed (optional)\n")
                self.log_prereq("  Install: /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"\n\n")
            
            # Check Node.js
            self.log_prereq("➤ Checking Node.js...")
            node_installed, node_version = self.check_command("node")
            if node_installed:
                self.log_prereq(f" {node_version}\n  ✓ Node.js found\n\n")
            else:
                self.log_prereq(" ✗ Not found!\n")
                self.log_prereq("  Install: brew install node\n")
                self.log_prereq("  Or download from: https://nodejs.org/\n\n")
            
            # Check pnpm
            self.log_prereq("➤ Checking pnpm...")
            pnpm_installed, pnpm_version = self.check_command("pnpm")
            if pnpm_installed:
                self.log_prereq(f" {pnpm_version}\n  ✓ pnpm found\n\n")
            else:
                self.log_prereq(" ⚠ Not installed\n")
                if messagebox.askyesno("Install pnpm?", "pnpm is required. Install now?"):
                    self.log_prereq("  Installing pnpm...\n")
                    self.run_command("npm install -g pnpm")
                    self.log_prereq("  ✓ pnpm installed!\n\n")
            
            # Check Git
            self.log_prereq("➤ Checking Git...")
            git_installed, git_version = self.check_command("git")
            if git_installed:
                self.log_prereq(f" {git_version}\n  ✓ Git found\n\n")
            else:
                self.log_prereq(" ⚠ Not found (optional for cloning)\n\n")
            
            self.log_prereq("✓ System check complete!\n")
        
        threading.Thread(target=check, daemon=True).start()
        
    def log_prereq(self, message):
        """Log to prerequisites text widget"""
        self.prereq_text.insert(tk.END, message)
        self.prereq_text.see(tk.END)
        self.prereq_text.update()
        
    def log_install(self, message):
        """Log to installation text widget"""
        self.install_text.insert(tk.END, message + "\n")
        self.install_text.see(tk.END)
        self.install_text.update()
        
    def update_status(self, message):
        """Update installation status label"""
        self.install_status.config(text=message)
        self.install_status.update()
        
    def check_command(self, command):
        """Check if command exists"""
        try:
            result = subprocess.run([command, "--version"], capture_output=True, text=True, timeout=5)
            return True, result.stdout.strip()
        except:
            return False, None
            
    def run_command(self, command, cwd=None):
        """Run shell command"""
        try:
            result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
            return result.returncode == 0, result.stdout
        except Exception as e:
            return False, str(e)
            
    def run_installation(self):
        """Run installation process"""
        self.progress.start()
        
        def install():
            try:
                install_type = self.install_type.get()
                install_path = Path(self.install_path.get())
                
                if install_type == "current":
                    self.update_status("Installing from current directory...")
                    self.log_install("Installing dependencies...")
                    self.run_command("pnpm install")
                    
                    self.log_install("Building project...")
                    self.run_command("pnpm build")
                    
                elif install_type == "global":
                    self.update_status("Installing globally...")
                    self.log_install("Installing clawdbot from npm...")
                    self.run_command("npm install -g clawdbot")
                    
                elif install_type == "clone":
                    self.update_status("Cloning repository...")
                    repo_url = self.repo_url.get()
                    
                    self.log_install(f"Cloning from {repo_url}...")
                    self.run_command(f'git clone {repo_url} "{install_path}"')
                    
                    self.log_install("Installing dependencies...")
                    self.run_command("pnpm install", cwd=str(install_path))
                    
                    self.log_install("Building project...")
                    self.run_command("pnpm build", cwd=str(install_path))
                
                # Apply configuration
                self.update_status("Configuring...")
                self.log_install("\nApplying configuration...")
                self.apply_config()
                
                # macOS-specific setup
                if self.create_app_bundle.get():
                    self.update_status("Creating app bundle...")
                    self.log_install("\nCreating Clawdbot.app...")
                    self.create_mac_app_bundle()
                
                if self.create_launchd.get():
                    self.update_status("Setting up auto-start...")
                    self.log_install("\nCreating LaunchAgent...")
                    self.create_launchd_plist()
                
                if self.add_to_dock.get():
                    self.log_install("\nAdding to Dock...")
                    self.add_app_to_dock()
                
                self.update_status("Installation complete!")
                self.log_install("\n✓ Installation completed successfully!")
                self.progress.stop()
                
                self.root.after(1000, lambda: self.show_page(6))
                
            except Exception as e:
                self.update_status("Installation failed")
                self.log_install(f"\n✗ Installation failed: {str(e)}")
                self.progress.stop()
                messagebox.showerror("Installation Failed", str(e))
        
        threading.Thread(target=install, daemon=True).start()
        
    def apply_config(self):
        """Apply configuration"""
        commands = [
            f"pnpm clawdbot config set gateway.mode {self.gateway_mode.get()}",
            f"pnpm clawdbot config set logging.level {self.log_level.get()}"
        ]
        
        if self.provider_name.get() != "skip":
            commands.append(f"pnpm clawdbot config set provider.name {self.provider_name.get()}")
            if self.api_key.get():
                commands.append(f"pnpm clawdbot config set provider.apiKey {self.api_key.get()}")
        
        for cmd in commands:
            self.log_install(f"  {cmd}")
            self.run_command(cmd)
            
    def create_mac_app_bundle(self):
        """Create macOS .app bundle"""
        app_path = Path("/Applications/Clawdbot.app")
        contents = app_path / "Contents"
        macos = contents / "MacOS"
        resources = contents / "Resources"
        
        # Create directories
        macos.mkdir(parents=True, exist_ok=True)
        resources.mkdir(parents=True, exist_ok=True)
        
        # Create Info.plist
        plist_data = {
            'CFBundleName': 'Clawdbot',
            'CFBundleDisplayName': 'Clawdbot',
            'CFBundleIdentifier': BUNDLE_IDENTIFIER,
            'CFBundleVersion': APP_VERSION,
            'CFBundleShortVersionString': APP_VERSION,
            'CFBundleExecutable': 'clawdbot',
            'CFBundlePackageType': 'APPL',
            'LSMinimumSystemVersion': '11.0',
            'NSHighResolutionCapable': True,
        }
        
        with open(contents / "Info.plist", 'wb') as f:
            plistlib.dump(plist_data, f)
        
        # Create launcher script
        launcher = macos / "clawdbot"
        launcher.write_text(f"""#!/bin/bash
cd "{self.install_path.get()}"
pnpm clawdbot gateway run
""")
        launcher.chmod(0o755)
        
        self.log_install(f"  Created: {app_path}")
        
    def create_launchd_plist(self):
        """Create LaunchAgent plist"""
        plist_path = Path.home() / "Library/LaunchAgents/bot.clawd.gateway.plist"
        plist_path.parent.mkdir(parents=True, exist_ok=True)
        
        plist_data = {
            'Label': 'bot.clawd.gateway',
            'ProgramArguments': [
                '/usr/local/bin/pnpm',
                'clawdbot',
                'gateway',
                'run'
            ],
            'WorkingDirectory': str(self.install_path.get()),
            'RunAtLoad': True,
            'KeepAlive': True,
            'StandardOutPath': str(Path.home() / '.clawdbot/logs/gateway.log'),
            'StandardErrorPath': str(Path.home() / '.clawdbot/logs/gateway-error.log'),
        }
        
        with open(plist_path, 'wb') as f:
            plistlib.dump(plist_data, f)
        
        # Load LaunchAgent
        subprocess.run(['launchctl', 'load', str(plist_path)])
        self.log_install(f"  Created: {plist_path}")
        
    def add_app_to_dock(self):
        """Add app to Dock"""
        applescript = '''
        tell application "System Events"
            tell dock preferences
                set properties to {dock apps to (dock apps & "/Applications/Clawdbot.app")}
            end tell
        end tell
        '''
        subprocess.run(['osascript', '-e', applescript])
        
    def start_gateway(self):
        """Start gateway"""
        subprocess.Popen(
            ['open', '/Applications/Clawdbot.app']
        )
        messagebox.showinfo("Gateway Started", "Clawdbot gateway is starting...")
        
    def open_in_finder(self):
        """Open installation directory in Finder"""
        subprocess.run(['open', self.install_path.get()])
        
    def finish(self):
        """Finish installation"""
        self.root.destroy()

def main():
    """Main entry point"""
    root = tk.Tk()
    app = MacSetupWizard(root)
    root.mainloop()

if __name__ == "__main__":
    main()
