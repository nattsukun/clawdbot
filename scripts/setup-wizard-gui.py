#!/usr/bin/env python3
"""
Clawdbot Setup Wizard - Python Edition
Protected Installer with GUI
"""

import os
import sys
import subprocess
import platform
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import json
from pathlib import Path

# Configuration
APP_NAME = "Clawdbot"
APP_VERSION = "2026.1.25"
CONFIG_DIR = Path.home() / ".clawdbot"
NODE_MIN_VERSION = 22

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

class SetupWizard:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{APP_NAME} Setup Wizard")
        self.root.geometry("700x550")
        self.root.resizable(False, False)
        
        # Variables
        self.install_type = tk.StringVar(value="current")
        self.gateway_mode = tk.StringVar(value="local")
        self.provider_name = tk.StringVar(value="skip")
        self.api_key = tk.StringVar()
        self.log_level = tk.StringVar(value="info")
        self.install_path = tk.StringVar(value=str(Path.cwd()))
        self.repo_url = tk.StringVar(value="https://github.com/clawdbot/clawdbot.git")
        
        # Pages
        self.pages = []
        self.current_page = 0
        
        # Create UI
        self.create_widgets()
        self.show_page(0)
        
    def create_widgets(self):
        """Create all UI widgets"""
        # Header
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text=f"{APP_NAME} Setup Wizard",
            font=("Arial", 18, "bold"),
            bg="#2c3e50",
            fg="white"
        ).pack(pady=25)
        
        # Content frame
        self.content_frame = tk.Frame(self.root, bg="white")
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Navigation buttons
        nav_frame = tk.Frame(self.root, bg="#ecf0f1", height=60)
        nav_frame.pack(fill=tk.X, side=tk.BOTTOM)
        nav_frame.pack_propagate(False)
        
        self.prev_btn = tk.Button(
            nav_frame,
            text="← Previous",
            command=self.prev_page,
            width=12,
            state=tk.DISABLED
        )
        self.prev_btn.pack(side=tk.LEFT, padx=20, pady=15)
        
        self.next_btn = tk.Button(
            nav_frame,
            text="Next →",
            command=self.next_page,
            width=12,
            bg="#3498db",
            fg="white"
        )
        self.next_btn.pack(side=tk.RIGHT, padx=20, pady=15)
        
        # Create pages
        self.create_welcome_page()
        self.create_prerequisites_page()
        self.create_install_type_page()
        self.create_configuration_page()
        self.create_installation_page()
        self.create_completion_page()
        
    def create_welcome_page(self):
        """Welcome page"""
        frame = tk.Frame(self.content_frame, bg="white")
        
        tk.Label(
            frame,
            text=f"Welcome to {APP_NAME} Setup Wizard",
            font=("Arial", 14, "bold"),
            bg="white"
        ).pack(pady=20)
        
        tk.Label(
            frame,
            text=f"This wizard will guide you through the installation of {APP_NAME}.",
            font=("Arial", 10),
            bg="white",
            wraplength=600
        ).pack(pady=10)
        
        features = [
            "✓ Multiple messaging channels (WhatsApp, Telegram, Discord, etc.)",
            "✓ Powerful AI agent with RPC mode",
            "✓ Modular plugin system",
            "✓ Gateway server for remote access",
            "✓ Cross-platform support"
        ]
        
        for feature in features:
            tk.Label(
                frame,
                text=feature,
                font=("Arial", 10),
                bg="white",
                anchor="w"
            ).pack(anchor="w", padx=50, pady=5)
        
        tk.Label(
            frame,
            text="\nClick 'Next' to begin installation.",
            font=("Arial", 10, "italic"),
            bg="white"
        ).pack(pady=20)
        
        self.pages.append(frame)
        
    def create_prerequisites_page(self):
        """Prerequisites check page"""
        frame = tk.Frame(self.content_frame, bg="white")
        
        tk.Label(
            frame,
            text="Checking Prerequisites",
            font=("Arial", 14, "bold"),
            bg="white"
        ).pack(pady=20)
        
        self.prereq_text = scrolledtext.ScrolledText(
            frame,
            height=15,
            width=70,
            font=("Courier", 9),
            bg="#f8f9fa"
        )
        self.prereq_text.pack(pady=10)
        
        tk.Button(
            frame,
            text="Check Now",
            command=self.check_prerequisites,
            bg="#2ecc71",
            fg="white"
        ).pack(pady=10)
        
        self.pages.append(frame)
        
    def create_install_type_page(self):
        """Installation type selection"""
        frame = tk.Frame(self.content_frame, bg="white")
        
        tk.Label(
            frame,
            text="Choose Installation Type",
            font=("Arial", 14, "bold"),
            bg="white"
        ).pack(pady=20)
        
        options_frame = tk.Frame(frame, bg="white")
        options_frame.pack(pady=20)
        
        tk.Radiobutton(
            options_frame,
            text="Install from current directory (Development)",
            variable=self.install_type,
            value="current",
            bg="white",
            font=("Arial", 10)
        ).pack(anchor="w", pady=5)
        
        tk.Radiobutton(
            options_frame,
            text="Install globally from npm",
            variable=self.install_type,
            value="global",
            bg="white",
            font=("Arial", 10)
        ).pack(anchor="w", pady=5)
        
        tk.Radiobutton(
            options_frame,
            text="Clone from repository",
            variable=self.install_type,
            value="clone",
            bg="white",
            font=("Arial", 10)
        ).pack(anchor="w", pady=5)
        
        # Repository URL field (for clone option)
        repo_frame = tk.Frame(frame, bg="white")
        repo_frame.pack(pady=10, fill=tk.X, padx=50)
        
        tk.Label(repo_frame, text="Repository URL:", bg="white").pack(anchor="w")
        tk.Entry(repo_frame, textvariable=self.repo_url, width=60).pack(fill=tk.X, pady=5)
        
        tk.Label(repo_frame, text="Install Path:", bg="white").pack(anchor="w", pady=(10, 0))
        tk.Entry(repo_frame, textvariable=self.install_path, width=60).pack(fill=tk.X, pady=5)
        
        self.pages.append(frame)
        
    def create_configuration_page(self):
        """Configuration page"""
        frame = tk.Frame(self.content_frame, bg="white")
        
        tk.Label(
            frame,
            text="Configuration",
            font=("Arial", 14, "bold"),
            bg="white"
        ).pack(pady=20)
        
        config_frame = tk.Frame(frame, bg="white")
        config_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Gateway mode
        tk.Label(config_frame, text="Gateway Mode:", bg="white", font=("Arial", 10, "bold")).grid(
            row=0, column=0, sticky="w", pady=5
        )
        ttk.Combobox(
            config_frame,
            textvariable=self.gateway_mode,
            values=["local", "remote"],
            state="readonly",
            width=30
        ).grid(row=0, column=1, sticky="w", padx=10, pady=5)
        
        # AI Provider
        tk.Label(config_frame, text="AI Provider:", bg="white", font=("Arial", 10, "bold")).grid(
            row=1, column=0, sticky="w", pady=5
        )
        ttk.Combobox(
            config_frame,
            textvariable=self.provider_name,
            values=["openai", "anthropic", "google", "skip"],
            state="readonly",
            width=30
        ).grid(row=1, column=1, sticky="w", padx=10, pady=5)
        
        # API Key
        tk.Label(config_frame, text="API Key:", bg="white", font=("Arial", 10, "bold")).grid(
            row=2, column=0, sticky="w", pady=5
        )
        tk.Entry(config_frame, textvariable=self.api_key, show="*", width=33).grid(
            row=2, column=1, sticky="w", padx=10, pady=5
        )
        
        # Log level
        tk.Label(config_frame, text="Log Level:", bg="white", font=("Arial", 10, "bold")).grid(
            row=3, column=0, sticky="w", pady=5
        )
        ttk.Combobox(
            config_frame,
            textvariable=self.log_level,
            values=["debug", "info", "warn", "error"],
            state="readonly",
            width=30
        ).grid(row=3, column=1, sticky="w", padx=10, pady=5)
        
        self.pages.append(frame)
        
    def create_installation_page(self):
        """Installation progress page"""
        frame = tk.Frame(self.content_frame, bg="white")
        
        tk.Label(
            frame,
            text="Installing...",
            font=("Arial", 14, "bold"),
            bg="white"
        ).pack(pady=20)
        
        self.progress = ttk.Progressbar(
            frame,
            length=600,
            mode='indeterminate'
        )
        self.progress.pack(pady=10)
        
        self.install_text = scrolledtext.ScrolledText(
            frame,
            height=15,
            width=70,
            font=("Courier", 9),
            bg="#f8f9fa"
        )
        self.install_text.pack(pady=10)
        
        self.pages.append(frame)
        
    def create_completion_page(self):
        """Completion page"""
        frame = tk.Frame(self.content_frame, bg="white")
        
        tk.Label(
            frame,
            text="✓ Installation Complete!",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#2ecc71"
        ).pack(pady=30)
        
        tk.Label(
            frame,
            text=f"{APP_NAME} has been successfully installed!",
            font=("Arial", 11),
            bg="white"
        ).pack(pady=10)
        
        instructions = [
            "Next steps:",
            "1. Run 'clawdbot login' to login to WhatsApp",
            "2. Run 'clawdbot gateway run' to start the gateway",
            "3. Check status with 'clawdbot channels status'",
            "",
            "Documentation:",
            "• Installation Guide: INSTALLATION-TH.md",
            "• User Guide: USER-GUIDE-TH.md",
            "• Online: https://docs.clawd.bot"
        ]
        
        for instruction in instructions:
            tk.Label(
                frame,
                text=instruction,
                font=("Arial", 9),
                bg="white",
                anchor="w"
            ).pack(anchor="w", padx=100, pady=2)
        
        tk.Button(
            frame,
            text="Start Gateway Now",
            command=self.start_gateway,
            bg="#3498db",
            fg="white",
            font=("Arial", 10)
        ).pack(pady=20)
        
        self.pages.append(frame)
    
    def show_page(self, page_num):
        """Show specific page"""
        # Hide all pages
        for page in self.pages:
            page.pack_forget()
        
        # Show current page
        if 0 <= page_num < len(self.pages):
            self.pages[page_num].pack(fill=tk.BOTH, expand=True)
            self.current_page = page_num
            
            # Update navigation buttons
            self.prev_btn.config(state=tk.NORMAL if page_num > 0 else tk.DISABLED)
            
            if page_num == len(self.pages) - 1:
                self.next_btn.config(text="Finish", command=self.finish)
            else:
                self.next_btn.config(text="Next →", command=self.next_page)
                
    def next_page(self):
        """Go to next page"""
        if self.current_page == 2:  # Install type page
            self.current_page = 3  # Skip to config
        elif self.current_page == 3:  # Config page
            # Start installation
            self.current_page = 4
            self.show_page(4)
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
            
    def check_prerequisites(self):
        """Check system prerequisites"""
        self.prereq_text.delete(1.0, tk.END)
        
        def check():
            self.log_prereq("Checking prerequisites...\n")
            
            # Check Node.js
            self.log_prereq("➤ Checking Node.js...")
            node_installed, node_version = self.check_command("node")
            if node_installed:
                self.log_prereq(f"  ✓ Node.js found: {node_version}\n", "green")
            else:
                self.log_prereq("  ✗ Node.js not found!\n", "red")
                self.log_prereq("  Please install from: https://nodejs.org/\n")
            
            # Check pnpm
            self.log_prereq("➤ Checking pnpm...")
            pnpm_installed, pnpm_version = self.check_command("pnpm")
            if pnpm_installed:
                self.log_prereq(f"  ✓ pnpm found: {pnpm_version}\n", "green")
            else:
                self.log_prereq("  ⚠ pnpm not found\n", "yellow")
                if messagebox.askyesno("Install pnpm?", "pnpm is not installed. Install now?"):
                    self.log_prereq("  Installing pnpm...\n")
                    self.run_command("npm install -g pnpm")
                    self.log_prereq("  ✓ pnpm installed!\n", "green")
            
            # Check Git
            self.log_prereq("➤ Checking Git...")
            git_installed, git_version = self.check_command("git")
            if git_installed:
                self.log_prereq(f"  ✓ Git found: {git_version}\n", "green")
            else:
                self.log_prereq("  ⚠ Git not found (optional)\n", "yellow")
            
            self.log_prereq("\n✓ Prerequisites check complete!\n", "green")
        
        threading.Thread(target=check, daemon=True).start()
        
    def log_prereq(self, message, color=None):
        """Log to prerequisites text widget"""
        self.prereq_text.insert(tk.END, message)
        self.prereq_text.see(tk.END)
        self.prereq_text.update()
        
    def log_install(self, message):
        """Log to installation text widget"""
        self.install_text.insert(tk.END, message + "\n")
        self.install_text.see(tk.END)
        self.install_text.update()
        
    def check_command(self, command):
        """Check if command exists and get version"""
        try:
            result = subprocess.run(
                [command, "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return True, result.stdout.strip()
        except:
            return False, None
            
    def run_command(self, command, cwd=None):
        """Run shell command"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                capture_output=True,
                text=True
            )
            return result.returncode == 0, result.stdout
        except Exception as e:
            return False, str(e)
            
    def run_installation(self):
        """Run installation process"""
        self.progress.start()
        
        def install():
            try:
                install_type = self.install_type.get()
                
                if install_type == "current":
                    self.log_install("Installing from current directory...")
                    self.log_install("Installing dependencies...")
                    self.run_command("pnpm install")
                    
                    self.log_install("Building project...")
                    self.run_command("pnpm build")
                    
                elif install_type == "global":
                    self.log_install("Installing globally from npm...")
                    self.run_command("npm install -g clawdbot")
                    
                elif install_type == "clone":
                    self.log_install(f"Cloning repository...")
                    install_path = self.install_path.get()
                    repo_url = self.repo_url.get()
                    
                    self.run_command(f'git clone {repo_url} "{install_path}"')
                    
                    self.log_install("Installing dependencies...")
                    self.run_command("pnpm install", cwd=install_path)
                    
                    self.log_install("Building project...")
                    self.run_command("pnpm build", cwd=install_path)
                
                # Apply configuration
                self.log_install("\nApplying configuration...")
                self.apply_config()
                
                self.log_install("\n✓ Installation completed successfully!")
                self.progress.stop()
                
                # Move to completion page
                self.root.after(1000, lambda: self.show_page(5))
                
            except Exception as e:
                self.log_install(f"\n✗ Installation failed: {str(e)}")
                self.progress.stop()
                messagebox.showerror("Installation Failed", str(e))
        
        threading.Thread(target=install, daemon=True).start()
        
    def apply_config(self):
        """Apply user configuration"""
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
            
    def start_gateway(self):
        """Start gateway server"""
        if messagebox.askyesno("Start Gateway", "Start Clawdbot gateway now?"):
            subprocess.Popen(
                "pnpm clawdbot gateway run",
                shell=True,
                creationflags=subprocess.CREATE_NEW_CONSOLE if platform.system() == "Windows" else 0
            )
            messagebox.showinfo("Gateway Started", "Gateway is starting in a new window...")
            
    def finish(self):
        """Finish installation"""
        self.root.destroy()

def main():
    """Main entry point"""
    root = tk.Tk()
    app = SetupWizard(root)
    root.mainloop()

if __name__ == "__main__":
    main()
