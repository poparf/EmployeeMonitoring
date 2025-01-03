import psutil
import platform
import time

def get_active_window_info():
    system = platform.system()
    
    if system == 'Windows':
        import win32gui
        import win32process
        
        # Get the window handle
        window = win32gui.GetForegroundWindow()
        # Get window title
        window_title = win32gui.GetWindowText(window)
        
        # Get process ID
        _, pid = win32process.GetWindowThreadProcessId(window)
        # Get process name from ID
        try:
            process = psutil.Process(pid)
            process_name = process.name()
            return {
                'window_title': window_title,
                'process_name': process_name,
                'pid': pid
            }
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return None
            
    elif system == 'Darwin':  # macOS
        try:
            from AppKit import NSWorkspace
            active_app = NSWorkspace.sharedWorkspace().activeApplication()
            return {
                'window_title': active_app['NSApplicationName'],
                'process_name': active_app['NSApplicationName'],
                'pid': active_app['NSApplicationProcessIdentifier']
            }
        except ImportError:
            print("Please install pyobjc-framework-Cocoa for macOS support")
            return None
            
    elif system == 'Linux':
        try:
            import Xlib.display
            import Xlib.X
            
            display = Xlib.display.Display()
            window = display.get_input_focus().focus
            wmname = window.get_wm_name()
            
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if proc.connections():  # Check if process has window connections
                        return {
                            'window_title': wmname,
                            'process_name': proc.name(),
                            'pid': proc.pid
                        }
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            return None
            
        except ImportError:
            print("Please install python-xlib for Linux support")
            return None
            
    return None

# Example usage
if __name__ == "__main__":
    while(True):
        info = get_active_window_info()
        if info:
            print(f"Window Title: {info['window_title']}")
            print(f"Process Name: {info['process_name']}")
            print(f"Process ID: {info['pid']}")
        else:
            print("Could not get window/process information")
        time.sleep(1)