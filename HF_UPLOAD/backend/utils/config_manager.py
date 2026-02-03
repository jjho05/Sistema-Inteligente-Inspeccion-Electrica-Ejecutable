"""
Configuration manager for standalone executable.
Handles API key and settings with GUI dialog.
"""

import json
import os
from pathlib import Path
from typing import Dict, Optional
import tkinter as tk
from tkinter import messagebox, simpledialog


class ConfigManager:
    """Manage application configuration."""
    
    def __init__(self, config_file: str = "config.json"):
        """Initialize config manager."""
        self.config_file = Path(config_file)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """Load configuration from file."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")
                return {}
        return {}
    
    def _save_config(self):
        """Save configuration to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get_api_key(self) -> Optional[str]:
        """Get API key, prompt if not configured."""
        api_key = self.config.get('GEMINI_API_KEY')
        
        if not api_key:
            api_key = self._prompt_api_key()
            if api_key:
                self.config['GEMINI_API_KEY'] = api_key
                self._save_config()
        
        return api_key
    
    def _prompt_api_key(self) -> Optional[str]:
        """Show GUI dialog to get API key."""
        root = tk.Tk()
        root.withdraw()
        
        # Show info message
        messagebox.showinfo(
            "Configuración Inicial",
            "Bienvenido al Sistema de Inspección Eléctrica.\n\n"
            "Para usar el sistema, necesitas una API Key de Google Gemini.\n\n"
            "Obtén tu clave en: https://makersuite.google.com/app/apikey"
        )
        
        # Prompt for API key
        api_key = simpledialog.askstring(
            "API Key de Gemini",
            "Ingresa tu API Key de Google Gemini:",
            show='*'
        )
        
        root.destroy()
        
        if api_key and api_key.strip():
            return api_key.strip()
        
        messagebox.showerror(
            "Error",
            "No se proporcionó una API Key válida.\n"
            "El sistema no puede funcionar sin ella."
        )
        return None
    
    def update_api_key(self, new_key: str):
        """Update API key."""
        self.config['GEMINI_API_KEY'] = new_key
        self._save_config()
    
    def get(self, key: str, default=None):
        """Get configuration value."""
        return self.config.get(key, default)
    
    def set(self, key: str, value):
        """Set configuration value."""
        self.config[key] = value
        self._save_config()


def get_config_manager() -> ConfigManager:
    """Get singleton config manager instance."""
    if not hasattr(get_config_manager, 'instance'):
        get_config_manager.instance = ConfigManager()
    return get_config_manager.instance
