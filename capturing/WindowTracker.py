import pygetwindow as gw
import time
from threading import Thread, Event
import logging

class WindowTracker(Thread):
    def __init__(self, interval=0.5, logger=None):
        """
        Initialize the WindowTracker.
        
        :param interval: Time between window state checks (default 0.5 seconds)
        :param logger: Optional logger for tracking events
        """
        super().__init__()
        self.interval = interval
        self.logger = logger or logging.getLogger(__name__)
        
        self.stop_event = Event()
        self.window_history = []
        self.current_window_start = None
        self.current_window_title = None

    def run(self):
        """
        Main tracking method. Continuously monitors active windows.
        """
        try:
            while not self.stop_event.is_set():
                active_window = gw.getActiveWindow()
                
                if active_window:
                    if active_window.title != self.current_window_title:
                        # Window has changed
                        self._log_window_change(active_window)
                
                time.sleep(self.interval)
        
        except Exception as e:
            self.logger.error(f"Window tracking error: {e}")
    
    def _log_window_change(self, new_window):
        """
        Log window changes and track time spent.
        
        :param new_window: Newly active window
        """
        current_time = time.time()
        
        # Log previous window's duration if exists
        if self.current_window_title and self.current_window_start:
            duration = current_time - self.current_window_start
            self.window_history.append({
                'title': self.current_window_title,
                'start_time': self.current_window_start,
                'duration': duration
            })
            self.logger.info(f"Window '{self.current_window_title}' active for {duration:.2f} seconds")
        
        # Update current window tracking
        self.current_window_title = new_window.title
        self.current_window_start = current_time
        
    
    def stop(self):
        """
        Gracefully stop the window tracking.
        """
        self.stop_event.set() # Sets the flag to true to stop the thread
        # Log the final window
        if self.current_window_title and self.current_window_start:
            final_duration = time.time() - self.current_window_start
            
            
            self.window_history.append({
                'title': self.current_window_title,
                'start_time': self.current_window_start,
                'duration': final_duration
            })
        self.join()
        return self.window_history


# def main():
#     # Configure logging
#     logging.basicConfig(
#         level=logging.INFO, 
#         format='%(asctime)s - %(levelname)s: %(message)s'
#     )
    
#     try:
#         # Create and start the window tracker
#         tracker = WindowTracker()
#         tracker.start()
        
#         # Let it run for a while (e.g., 5 minutes)
#         input("Press Enter to stop tracking...")
        
#         # Stop tracking and get results
#         results = tracker.stop()
        
#         # Display detailed results
#         print("\n--- Window Tracking Results ---")
#         for entry in results:
#             print(f"Window: {entry['title']}")
#             print(f"Duration: {entry['duration']:.2f} seconds")
#             print(f"Started at: {time.ctime(entry['start_time'])}\n")
    
#     except Exception as e:
#         logging.error(f"Tracking failed: {e}")
        
# main()
