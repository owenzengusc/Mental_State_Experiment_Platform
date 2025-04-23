import tkinter as tk

def get_optimal_window_size(scale_factor=0.85, min_width=800, min_height=600):
    """Calculate the optimal window size based on screen resolution.
    
    Args:
        scale_factor: Proportion of screen to use (0.0-1.0)
        min_width: Minimum window width
        min_height: Minimum window height
        
    Returns:
        Tuple of (width, height) for the window
    """
    root = tk.Tk()
    root.withdraw()  # Hide the temporary window
    
    # Get screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Calculate optimal size (85% of screen by default)
    width = max(int(screen_width * scale_factor), min_width)
    height = max(int(screen_height * scale_factor), min_height)
    
    # Some OSes report weird screen sizes, add safety constraints
    width = min(width, screen_width)
    height = min(height, screen_height)
    
    root.destroy()
    return width, height

def calculate_center_position(window, width, height):
    """Calculate the center position for a window.
    
    Args:
        window: Tkinter window object
        width: Window width
        height: Window height
        
    Returns:
        Tuple of (x, y) for window positioning
    """
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    
    return x, y

def get_responsive_window_size(window_type="test"):
    """Get responsive window size based on window type.
    
    Args:
        window_type: Type of window ("test", "main", or "small")
        
    Returns:
        Tuple of (width, height) for the window
    """
    if window_type == "test":
        # Test windows need more space (85% of screen)
        return get_optimal_window_size(0.85, 1200, 800)
    elif window_type == "main":
        # Main windows are slightly smaller (75% of screen)
        return get_optimal_window_size(0.75, 1000, 700)
    else:  # "small" or any other value
        # Small dialogs and instruction screens (60% of screen)
        return get_optimal_window_size(0.6, 800, 600)

def set_responsive_geometry(window, window_type="test"):
    """Set responsive window geometry based on screen size.
    
    Args:
        window: Tkinter window object
        window_type: Type of window ("test", "main", or "small")
        
    Returns:
        Tuple of (width, height) that was set
    """
    width, height = get_responsive_window_size(window_type)
    x, y = calculate_center_position(window, width, height)
    
    window.geometry(f"{width}x{height}+{x}+{y}")
    
    # Set reasonable min/max sizes
    window.update_idletasks()  # Ensure window is updated
    window.minsize(min(width, 800), min(height, 600))
    window.maxsize(window.winfo_screenwidth(), window.winfo_screenheight())
    
    return width, height 