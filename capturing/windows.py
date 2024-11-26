import pygetwindow as gw
import time
from threading import Thread

class CaptureWindow(Thread):
    def __init__(self):
        super().__init__()

        self.time_with_active_window = []
        self.start_time = None
        self.is_running = True
    
    def run(self):
        try:
            # Get the initial active window
            initial_window = gw.getActiveWindow()
            
            # Check if an active window exists
            if initial_window is None:
                print("No active window found.")
                return
            
            # Store the initial window title
            initial_title = initial_window.title
            self.start_time = time.time()
            
            # Continue monitoring while the thread is running
            while self.is_running:
                # Get the current active window
                current_window = gw.getActiveWindow()
                
                # If no window is active or the window has changed, break the loop
                if current_window is None or current_window.title != initial_title:
                    end_time = time.time()
                    self.time_with_active_window.append({
                        "title": initial_title, 
                        "duration": end_time - self.start_time
                    })
                    break
                
                # Sleep to prevent high CPU usage
                time.sleep(1)
        
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def stop(self):
        """Method to stop the thread"""
        self.is_running = False

# Example usage
def main():
    # Create and start the window capture thread
    cw = CaptureWindow()
    cw.start()
    
    # Wait for the thread to complete
    cw.join()
    
    # Print the tracked window time
    print("Window Time Tracking Results:")
    for window in cw.time_with_active_window:
        print(f"Window: {window['title']}")
        print(f"Duration: {window['duration']:.2f} seconds")

if __name__ == "__main__":
    main()