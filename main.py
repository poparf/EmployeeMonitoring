print("Importing")
from capturing.StartTrackers import start_trackers, stop_trackers, SystemTracker

if __name__ == "__main__":
    print("Started")
    systemTracker = SystemTracker.get_instance()
    print(systemTracker.system_info)
    # We will use the PC username, computer name and OS as the key for the computer we're monitoring
    # since the ip is subject to change !
    """
    The payload that we will send thourgh kafka will be in the folowing format:
    {
        user: {
            username: str,
            computer_name: str,
            os: str,
            ip: str
        },
        data: {
            active_window: {
                ...
            },
            OR !!
            keyboard: {
                ...
            },
            OR !!
            screen: {
                ...
            }
        }
    }
    """
    start_trackers()
    input("\nCapturing...")
    stop_trackers()