#!/usr/bin/env python3
"""
Final Script - Audiobook Production System Setup Script
======================================================

This script automates the setup process for the Final Script audiobook production system.
It handles dependency installation, environment configuration, and system validation.

Usage:
    python setup.py [options]

Options:
    --check-only    Only check system requirements without installing
    --skip-redis    Skip Redis installation (assume it's already installed)
    --dev           Install development dependencies
    --help          Show this help message
"""

import os
import sys
import subprocess
import platform
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

class SetupManager:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.requirements_file = self.project_root / "requirements.txt"
        self.env_template = self.project_root / ".env.template"
        self.env_file = self.project_root / ".env"
        self.system_info = self._get_system_info()
        
    def _get_system_info(self) -> Dict:
        """Get system information"""
        return {
            "os": platform.system(),
            "os_version": platform.version(),
            "python_version": sys.version,
            "architecture": platform.architecture()[0],
            "python_executable": sys.executable
        }
    
    def print_header(self):
        """Print setup header"""
        print(f"{Colors.CYAN}{Colors.BOLD}")
        print("=" * 80)
        print("🚀 FINAL SCRIPT - AUDIOBOOK PRODUCTION SYSTEM SETUP")
        print("=" * 80)
        print(f"{Colors.END}")
        print(f"{Colors.WHITE}Setting up your audiobook production pipeline...{Colors.END}\n")
    
    def print_step(self, step: str, description: str):
        """Print a setup step"""
        print(f"{Colors.BLUE}📋 {step}: {description}{Colors.END}")
    
    def print_success(self, message: str):
        """Print success message"""
        print(f"{Colors.GREEN}✅ {message}{Colors.END}")
    
    def print_warning(self, message: str):
        """Print warning message"""
        print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")
    
    def print_error(self, message: str):
        """Print error message"""
        print(f"{Colors.RED}❌ {message}{Colors.END}")
    
    def check_python_version(self) -> bool:
        """Check if Python version is compatible"""
        self.print_step("Python Version Check", "Verifying Python compatibility")
        
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            self.print_error(f"Python 3.8+ required, found {version.major}.{version.minor}")
            return False
        
        self.print_success(f"Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    
    def check_pip(self) -> bool:
        """Check if pip is available"""
        self.print_step("Pip Check", "Verifying pip availability")
        
        try:
            import pip
            self.print_success("Pip is available")
            return True
        except ImportError:
            self.print_error("Pip is not available. Please install pip first.")
            return False
    
    def install_dependencies(self, dev: bool = False) -> bool:
        """Install Python dependencies"""
        self.print_step("Dependencies", "Installing Python packages")
        
        if not self.requirements_file.exists():
            self.print_error(f"Requirements file not found: {self.requirements_file}")
            return False
        
        try:
            cmd = [sys.executable, "-m", "pip", "install", "-r", str(self.requirements_file)]
            if dev:
                cmd.extend(["--dev"])
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            self.print_success("Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            self.print_error(f"Failed to install dependencies: {e.stderr}")
            return False
    
    def check_redis(self) -> bool:
        """Check if Redis is available"""
        self.print_step("Redis Check", "Verifying Redis availability")
        
        try:
            import redis
            r = redis.Redis(host='localhost', port=6379, decode_responses=True)
            r.ping()
            self.print_success("Redis is running and accessible")
            return True
        except ImportError:
            self.print_error("Redis Python package not installed")
            return False
        except redis.ConnectionError:
            self.print_error("Redis server is not running")
            return False
        except Exception as e:
            self.print_error(f"Redis check failed: {e}")
            return False
    
    def install_redis(self) -> bool:
        """Install Redis based on operating system"""
        self.print_step("Redis Installation", f"Installing Redis for {self.system_info['os']}")
        
        system = self.system_info['os']
        
        try:
            if system == "Linux":
                # Try different package managers
                if self._run_command(["which", "apt-get"]):
                    subprocess.run(["sudo", "apt-get", "update"], check=True)
                    subprocess.run(["sudo", "apt-get", "install", "-y", "redis-server"], check=True)
                elif self._run_command(["which", "yum"]):
                    subprocess.run(["sudo", "yum", "install", "-y", "redis"], check=True)
                elif self._run_command(["which", "dnf"]):
                    subprocess.run(["sudo", "dnf", "install", "-y", "redis"], check=True)
                elif self._run_command(["which", "pacman"]):
                    subprocess.run(["sudo", "pacman", "-S", "--noconfirm", "redis"], check=True)
                else:
                    self.print_warning("No supported package manager found. Please install Redis manually.")
                    return False
                    
            elif system == "Darwin":  # macOS
                if self._run_command(["which", "brew"]):
                    subprocess.run(["brew", "install", "redis"], check=True)
                else:
                    self.print_warning("Homebrew not found. Please install Redis manually or install Homebrew first.")
                    return False
                    
            elif system == "Windows":
                self.print_warning("Windows Redis installation not automated. Please install Redis manually:")
                self.print_warning("1. Download Redis from https://github.com/microsoftarchive/redis/releases")
                self.print_warning("2. Or use WSL with Linux installation steps")
                return False
            else:
                self.print_warning(f"Unsupported operating system: {system}")
                return False
            
            self.print_success("Redis installed successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            self.print_error(f"Failed to install Redis: {e}")
            return False
    
    def start_redis(self) -> bool:
        """Start Redis service"""
        self.print_step("Redis Service", "Starting Redis service")
        
        system = self.system_info['os']
        
        try:
            if system == "Linux":
                subprocess.run(["sudo", "systemctl", "start", "redis"], check=True)
                subprocess.run(["sudo", "systemctl", "enable", "redis"], check=True)
            elif system == "Darwin":  # macOS
                subprocess.run(["brew", "services", "start", "redis"], check=True)
            else:
                self.print_warning("Please start Redis manually for your system")
                return True
            
            self.print_success("Redis service started")
            return True
            
        except subprocess.CalledProcessError as e:
            self.print_error(f"Failed to start Redis: {e}")
            return False
    
    def create_env_file(self) -> bool:
        """Create .env file from template"""
        self.print_step("Environment", "Setting up environment configuration")
        
        if not self.env_template.exists():
            self.print_error(f"Environment template not found: {self.env_template}")
            return False
        
        if self.env_file.exists():
            self.print_warning(".env file already exists, skipping creation")
            return True
        
        try:
            # Copy template to .env
            with open(self.env_template, 'r') as template:
                content = template.read()
            
            with open(self.env_file, 'w') as env:
                env.write(content)
            
            self.print_success("Environment file created")
            self.print_warning("Please edit .env file with your actual API keys")
            return True
            
        except Exception as e:
            self.print_error(f"Failed to create .env file: {e}")
            return False
    
    def validate_setup(self) -> bool:
        """Validate the complete setup"""
        self.print_step("Validation", "Validating complete setup")
        
        checks = [
            ("Python Version", self.check_python_version),
            ("Pip", self.check_pip),
            ("Dependencies", lambda: self._check_dependencies()),
            ("Redis", self.check_redis),
            ("Environment", lambda: self.env_file.exists()),
        ]
        
        all_passed = True
        for check_name, check_func in checks:
            try:
                if not check_func():
                    all_passed = False
            except Exception as e:
                self.print_error(f"{check_name} check failed: {e}")
                all_passed = False
        
        if all_passed:
            self.print_success("Setup validation completed successfully!")
            return True
        else:
            self.print_error("Setup validation failed. Please fix the issues above.")
            return False
    
    def _check_dependencies(self) -> bool:
        """Check if all dependencies are installed"""
        required_packages = [
            "langgraph", "langchain", "openai", "redis", 
            "pydantic", "python-dotenv", "reportlab"
        ]
        
        missing_packages = []
        for package in required_packages:
            try:
                __import__(package.replace("-", "_"))
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            self.print_error(f"Missing packages: {', '.join(missing_packages)}")
            return False
        
        self.print_success("All dependencies are installed")
        return True
    
    def _run_command(self, cmd: List[str]) -> bool:
        """Run a command and return True if successful"""
        try:
            subprocess.run(cmd, capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def print_system_info(self):
        """Print system information"""
        print(f"{Colors.PURPLE}System Information:{Colors.END}")
        print(f"  OS: {self.system_info['os']} {self.system_info['os_version']}")
        print(f"  Architecture: {self.system_info['architecture']}")
        print(f"  Python: {self.system_info['python_version']}")
        print(f"  Executable: {self.system_info['python_executable']}")
        print()
    
    def print_next_steps(self):
        """Print next steps after setup"""
        print(f"{Colors.CYAN}{Colors.BOLD}")
        print("🎉 SETUP COMPLETE!")
        print("=" * 50)
        print(f"{Colors.END}")
        print(f"{Colors.WHITE}Next steps:{Colors.END}")
        print(f"1. {Colors.YELLOW}Edit .env file{Colors.END} with your OpenRouter API key")
        print(f"2. {Colors.YELLOW}Start Redis{Colors.END} if not already running: redis-server")
        print(f"3. {Colors.YELLOW}Run Station 1{Colors.END}: python -m app.agents.station_01_seed_processor")
        print(f"4. {Colors.YELLOW}Or run full automation{Colors.END}: python full_automation.py")
        print()
        print(f"{Colors.GREEN}For more information, see:{Colors.END}")
        print(f"  • README.md - Complete documentation")
        print(f"  • QUICK_START.md - Quick start guide")
        print(f"  • STATION_COMMANDS.md - Individual station commands")
        print()

def main():
    """Main setup function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Setup Final Script audiobook production system")
    parser.add_argument("--check-only", action="store_true", help="Only check requirements")
    parser.add_argument("--skip-redis", action="store_true", help="Skip Redis installation")
    parser.add_argument("--dev", action="store_true", help="Install development dependencies")
    
    args = parser.parse_args()
    
    setup = SetupManager()
    setup.print_header()
    setup.print_system_info()
    
    # Check-only mode
    if args.check_only:
        setup.print_step("Check Mode", "Only checking system requirements")
        success = setup.validate_setup()
        sys.exit(0 if success else 1)
    
    # Setup steps
    steps = [
        ("Python Version", setup.check_python_version),
        ("Pip Check", setup.check_pip),
        ("Dependencies", lambda: setup.install_dependencies(args.dev)),
    ]
    
    if not args.skip_redis:
        steps.extend([
            ("Redis Installation", setup.install_redis),
            ("Redis Service", setup.start_redis),
        ])
    
    steps.extend([
        ("Environment Setup", setup.create_env_file),
        ("Final Validation", setup.validate_setup),
    ])
    
    # Execute setup steps
    for step_name, step_func in steps:
        if not step_func():
            setup.print_error(f"Setup failed at step: {step_name}")
            sys.exit(1)
    
    setup.print_next_steps()

if __name__ == "__main__":
    main()
