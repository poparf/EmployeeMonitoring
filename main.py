from capturing.StartTrackers import start_trackers, stop_trackers, start_system_tracker, systemTracker
if __name__ == '__main__':
    start_trackers()
    start_system_tracker()
    print(systemTracker.system_info)
    input("here...")
    stop_trackers()