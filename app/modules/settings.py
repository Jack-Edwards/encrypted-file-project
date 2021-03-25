from os import path
from pathlib import Path
from configparser import ConfigParser


def load_from_file(project_directory: str, filename: str = 'settings.ini'):
    """Load application settings"""
    settings_filepath = path.join(project_directory, filename)

    config = ConfigParser()
    config.read(settings_filepath)
    return config
