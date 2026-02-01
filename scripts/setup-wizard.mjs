#!/usr/bin/env node
// Clawdbot Setup Wizard - Node.js Version
// Cross-platform interactive installer

import { createInterface } from 'readline';
import { exec, spawn } from 'child_process';
import { promisify } from 'util';
import { existsSync, writeFileSync, appendFileSync } from 'fs';
import { join, dirname } from 'path';
import { homedir } from 'os';
import { fileURLToPath } from 'url';

const execAsync = promisify(exec);
const __dirname = dirname(fileURLToPath(import.meta.url));

// Colors for terminal output
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  dim: '\x1b[2m',
  cyan: '\x1b[36m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  red: '\x1b[31m',
  magenta: '\x1b[35m',
};

// Helper functions
function colorize(text, color) {
  return `${colors[color]}${text}${colors.reset}`;
}

function header(text) {
  console.log('\n' + colorize('═'.repeat(60), 'magenta'));
  console.log(colorize(`  ${text}`, 'bright'));
  console.log(colorize('═'.repeat(60), 'magenta') + '\n');
}

function step(text) {
  console.log(colorize(`➤ ${text}`, 'cyan'));
}

function success(text) {
  console.log(colorize(`✓ ${text}`, 'green'));
}

function error(text) {
  console.log(colorize(`✗ ${text}`, 'red'));
}

function warning(text) {
  console.log(colorize(`⚠ ${text}`, 'yellow'));
}

// Create readline interface
const rl = createInterface({
  input: process.stdin,
  output: process.stdout,
});

function question(query) {
  return new Promise((resolve) => rl.question(query, resolve));
}

async function confirm(message) {
  const answer = await question(`${message} (Y/n): `);
  return !answer || answer.toLowerCase() === 'y';
}

async function select(message, options, defaultOption = 0) {
  console.log(`\n${message}`);
  options.forEach((opt, i) => {
    console.log(`  ${i + 1}. ${opt}`);
  });
  
  const answer = await question(`\nChoose (1-${options.length}) [${defaultOption + 1}]: `);
  const choice = parseInt(answer) - 1;
  
  return isNaN(choice) || choice < 0 || choice >= options.length 
    ? defaultOption 
    : choice;
}

async function checkCommand(command) {
  try {
    await execAsync(`${command} --version`);
    return true;
  } catch {
    return false;
  }
}

async function getVersion(command) {
  try {
    const { stdout } = await execAsync(`${command} --version`);
    return stdout.trim();
  } catch {
    return null;
  }
}

async function runCommand(command, cwd = process.cwd()) {
  return new Promise((resolve, reject) => {
    const child = spawn(command, [], {
      shell: true,
      cwd,
      stdio: 'inherit',
    });
    
    child.on('close', (code) => {
      if (code === 0) {
        resolve();
      } else {
        reject(new Error(`Command failed with code ${code}`));
      }
    });
  });
}

// Main setup wizard
async function main() {
  try {
    header('Clawdbot Setup Wizard');
    console.log('Welcome to Clawdbot installation wizard!\n');
    
    // Step 1: Check Prerequisites
    header('Step 1: Checking Prerequisites');
    
    // Check Node.js
    step('Checking Node.js installation...');
    if (await checkCommand('node')) {
      const nodeVersion = await getVersion('node');
      success(`Node.js found: ${nodeVersion}`);
      
      const versionMatch = nodeVersion.match(/v?(\d+)\./);
      if (versionMatch && parseInt(versionMatch[1]) < 22) {
        warning(`Node.js version 22 or higher is recommended. Current: ${nodeVersion}`);
        if (!(await confirm('Continue anyway?'))) {
          console.log('Please upgrade Node.js and run setup again.');
          process.exit(1);
        }
      }
    } else {
      error('Node.js not found!');
      console.log('\nPlease install Node.js 22+ from: https://nodejs.org/');
      process.exit(1);
    }
    
    // Check pnpm
    step('Checking pnpm installation...');
    if (await checkCommand('pnpm')) {
      const pnpmVersion = await getVersion('pnpm');
      success(`pnpm found: ${pnpmVersion}`);
    } else {
      warning('pnpm not found!');
      if (await confirm('Install pnpm now?')) {
        step('Installing pnpm...');
        await runCommand('npm install -g pnpm');
        success('pnpm installed successfully!');
      } else {
        console.log('pnpm is required. Please install it manually: npm install -g pnpm');
        process.exit(1);
      }
    }
    
    // Check Git
    step('Checking Git installation...');
    if (await checkCommand('git')) {
      const gitVersion = await getVersion('git');
      success(`Git found: ${gitVersion}`);
    } else {
      warning('Git not found (optional for development)');
    }
    
    // Step 2: Installation Type
    header('Step 2: Installation Type');
    const installChoice = await select(
      'Choose installation type:',
      [
        'Install from current directory (development)',
        'Install globally from npm',
        'Clone from repository',
      ]
    );
    
    let installPath = process.cwd();
    
    switch (installChoice) {
      case 0: {
        // Install from current directory
        header('Step 3: Installing from Current Directory');
        
        if (!existsSync('package.json')) {
          error('package.json not found in current directory!');
          process.exit(1);
        }
        
        step('Installing dependencies...');
        await runCommand('pnpm install');
        success('Dependencies installed!');
        
        step('Building project...');
        await runCommand('pnpm build');
        success('Build completed!');
        
        installPath = process.cwd();
        break;
      }
      
      case 1: {
        // Install globally
        header('Step 3: Installing Globally');
        
        step('Installing clawdbot from npm...');
        await runCommand('npm install -g clawdbot');
        success('Clawdbot installed globally!');
        
        const { stdout } = await execAsync('npm root -g');
        installPath = stdout.trim();
        break;
      }
      
      case 2: {
        // Clone from repository
        header('Step 3: Cloning Repository');
        
        const repoUrl = await question('Repository URL [https://github.com/clawdbot/clawdbot.git]: ');
        const finalRepoUrl = repoUrl || 'https://github.com/clawdbot/clawdbot.git';
        
        const installDir = await question(`Installation directory [${join(homedir(), 'clawdbot')}]: `);
        installPath = installDir || join(homedir(), 'clawdbot');
        
        step('Cloning repository...');
        await runCommand(`git clone ${finalRepoUrl} "${installPath}"`);
        
        step('Installing dependencies...');
        await runCommand('pnpm install', installPath);
        success('Dependencies installed!');
        
        step('Building project...');
        await runCommand('pnpm build', installPath);
        success('Build completed!');
        break;
      }
    }
    
    // Step 4: Configuration
    header('Step 4: Initial Configuration');
    
    if (await confirm('Configure Clawdbot now?')) {
      // Gateway mode
      const modeChoice = await select(
        '\nGateway Mode:',
        ['local - Run gateway on this machine', 'remote - Connect to remote gateway']
      );
      const mode = modeChoice === 0 ? 'local' : 'remote';
      
      await runCommand(`pnpm clawdbot config set gateway.mode ${mode}`, installPath);
      success(`Gateway mode set to: ${mode}`);
      
      // AI Provider
      if (await confirm('\nConfigure AI Provider?')) {
        const providerChoice = await select(
          '\nAvailable Providers:',
          [
            'openai - OpenAI (GPT)',
            'anthropic - Anthropic (Claude)',
            'google - Google (Gemini)',
            'skip - Configure later',
          ],
          3
        );
        
        const providers = ['openai', 'anthropic', 'google'];
        
        if (providerChoice < 3) {
          const provider = providers[providerChoice];
          await runCommand(`pnpm clawdbot config set provider.name ${provider}`, installPath);
          
          const apiKey = await question('\nEnter API Key (or press Enter to skip): ');
          if (apiKey) {
            await runCommand(`pnpm clawdbot config set provider.apiKey ${apiKey}`, installPath);
            success(`Provider configured: ${provider}`);
          }
        }
      }
      
      // Logging level
      const logChoice = await select(
        '\nLog Level:',
        ['debug - Verbose logging', 'info - Standard logging', 'warn - Warnings only', 'error - Errors only'],
        1
      );
      
      const logLevels = ['debug', 'info', 'warn', 'error'];
      const logLevel = logLevels[logChoice];
      
      await runCommand(`pnpm clawdbot config set logging.level ${logLevel}`, installPath);
      success(`Log level set to: ${logLevel}`);
    }
    
    // Step 5: Shell configuration
    header('Step 5: Shell Configuration');
    
    if (await confirm('Add shortcuts to shell profile?')) {
      const shellConfigPath = process.platform === 'win32'
        ? null // Windows uses PowerShell profile
        : join(homedir(), '.bashrc'); // Linux/Mac
      
      if (shellConfigPath && existsSync(shellConfigPath)) {
        const shortcuts = `
# Clawdbot Shortcuts (Added by setup wizard)
alias clawdbot='pnpm --dir "${installPath}" clawdbot'
alias clawdbot-start='pnpm --dir "${installPath}" clawdbot gateway run --force'
alias clawdbot-status='pnpm --dir "${installPath}" clawdbot channels status --all'
alias cb='clawdbot'

`;
        
        appendFileSync(shellConfigPath, shortcuts);
        success('Shortcuts added to shell profile!');
        console.log('  - clawdbot         : Run clawdbot command');
        console.log('  - clawdbot-start   : Start gateway');
        console.log('  - clawdbot-status  : Check status');
        console.log('  - cb               : Alias for clawdbot');
      } else if (process.platform === 'win32') {
        warning('Shell shortcuts should be added via PowerShell profile');
        console.log('Run setup-wizard.ps1 for Windows-specific setup');
      }
    }
    
    // Step 6: Completion
    header('Installation Complete!');
    
    console.log(colorize('Clawdbot has been successfully installed!\n', 'green'));
    
    console.log(colorize('Next steps:', 'yellow'));
    console.log("  1. Restart terminal to load new shortcuts");
    console.log("  2. Run 'clawdbot login' to login to WhatsApp");
    console.log("  3. Run 'clawdbot gateway run' to start the gateway");
    console.log("  4. Check status with 'clawdbot channels status'\n");
    
    console.log(colorize('Useful commands:', 'cyan'));
    console.log('  clawdbot --help           - Show help');
    console.log('  clawdbot config list      - View configuration');
    console.log('  clawdbot channels status  - Check channels\n');
    
    console.log(colorize('Documentation:', 'cyan'));
    console.log('  Installation Guide: INSTALLATION-TH.md');
    console.log('  User Guide: USER-GUIDE-TH.md');
    console.log('  Online Docs: https://docs.clawd.bot\n');
    
    if (await confirm('Start gateway now?')) {
      step('Starting gateway...');
      process.chdir(installPath);
      await runCommand('pnpm clawdbot gateway run');
    } else {
      console.log(colorize('\nSetup complete! Run clawdbot when ready.', 'green'));
    }
    
  } catch (err) {
    error(`Setup failed: ${err.message}`);
    process.exit(1);
  } finally {
    rl.close();
  }
}

// Run setup wizard
main().catch((err) => {
  error(`Fatal error: ${err.message}`);
  process.exit(1);
});
