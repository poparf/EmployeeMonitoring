import pygetwindow as gw
import time
from threading import Thread, Event
import logging
from db.repository.WindowTrackerRepository import WindowTrackerRepository
from capturing.SystemTracker import SystemTracker
import win32gui
import win32process
import psutil
from kafkadir.KafkaProducerWrapper import KafkaProducerWrapper
#from kafkadir.KafkaConnectionChecker import KafkaConnectionChecker

class WindowTracker(Thread):
    def __init__(self, interval=0.5, logger=None):
        """
        interval: Time between window state checks (default 0.5 seconds)
        logger: Optional logger for tracking events
        """
        super().__init__()
        self.interval = interval
        self.logger = logger or logging.getLogger(__name__)

        self.stop_event = Event()
        self.window_history = []
        self.current_window_start = None
        self.current_window_title = None
        
        self.producer = None
        self.window_tracker_repository = None
        self.producer = KafkaProducerWrapper(['localhost:9092'])

    def run(self):
        """
        Main tracking method. Continuously monitors active windows.
        """
        try:
            while not self.stop_event.is_set():
                active_window = gw.getActiveWindow()
                
                if active_window:
                    self.logger.info(f"Active window: {active_window.title}")
                    if active_window.title != self.current_window_title:
                        # Window has changed

                        self._log_window_change(active_window)
                
                time.sleep(self.interval)
                self.logger.info("I slept enough...")
        
        except Exception as e:
            self.logger.error(f"Window tracking error: {e}")
    
    def _log_window_change(self, new_window):
        current_time = time.time()
        
        # Log previous window's duration if exists
        if self.current_window_title and self.current_window_start:
            duration = current_time - self.current_window_start
        
            window = win32gui.GetForegroundWindow()
            
            _, pid = win32process.GetWindowThreadProcessId(window)
            # Get process name from ID
            try:
                process = psutil.Process(pid)
                process_name = process.name()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                print("Error when capturing the process name!")
                
            new_window_history = {
                "process_id": pid,
                "process_name": process_name,
                'title': self.current_window_title,
                'start_time': self.current_window_start,
                'duration': duration
            }
            self.window_history.append(new_window_history)
            window_tracker_repository = WindowTrackerRepository()
            window_tracker_repository.insert(new_window_history)
            self.producer.send_message(KafkaProducerWrapper.ACTIVE_WINDOW_TOPIC, new_window_history)
                            
            self.logger.info(f"Window '{self.current_window_title}' active for {duration:.2f} seconds")
            
                
        # Update current window tracking
        self.current_window_title = new_window.title
        self.current_window_start = current_time
        
    
    def stop(self):
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
