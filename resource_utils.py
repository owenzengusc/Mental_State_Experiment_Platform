import sys
import os

def get_resource_path(relative_path):
    """
    Get the absolute path to a resource file.
    This works for both development and PyInstaller executable environments.
    
    Args:
        relative_path (str): The relative path to the resource file
        
    Returns:
        str: The absolute path to the resource file
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # If not running as executable, use the script's directory
        base_path = os.path.dirname(__file__)
    
    return os.path.join(base_path, relative_path)