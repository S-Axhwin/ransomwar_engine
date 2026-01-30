import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

logger = logging.getLogger(__name__)

class RansomwareHandler(FileSystemEventHandler):
    def __init__(self, decoy_ledger, alert_callback):
        self.decoy_ledger = decoy_ledger # Map of absolute path -> canary
        self.alert_callback = alert_callback

    def on_modified(self, event):
        if event.is_directory:
            return
        
        # Check if the modified file is a decoy
        if event.src_path in self.decoy_ledger:
            logger.critical(f"🚨 DECOY TOUCHED: {event.src_path} was modified!")
            self.alert_callback(event.src_path, "DECOY_MODIFIED")
    
    def on_deleted(self, event):
        if event.is_directory:
            return
        
        if event.src_path in self.decoy_ledger:
             logger.critical(f"🚨 DECOY DELETED: {event.src_path} was deleted!")
             self.alert_callback(event.src_path, "DECOY_DELETED")
            
    def on_moved(self, event):
        if event.is_directory:
            return

        if event.src_path in self.decoy_ledger:
             logger.critical(f"🚨 DECOY RENAMED: {event.src_path} -> {event.dest_path}")
             self.alert_callback(event.src_path, "DECOY_RENAMED")

class FIMMonitor:
    def __init__(self, watch_dir, decoy_ledger, alert_callback):
        self.watch_dir = watch_dir
        self.event_handler = RansomwareHandler(decoy_ledger, alert_callback)
        self.observer = Observer()
        self.is_running = False

    def start(self):
        self.observer.schedule(self.event_handler, self.watch_dir, recursive=True)
        self.observer.start()
        self.is_running = True
        logger.info(f"FIM Monitor started on {self.watch_dir}")

    def stop(self):
        self.observer.stop()
        self.observer.join()
        self.is_running = False
        logger.info("FIM Monitor stopped")

if __name__ == "__main__":
    # Test stub
    logging.basicConfig(level=logging.INFO)
    
    def simple_alert(path, reason):
        print(f"ALERT TRIGGERED: {reason} on {path}")

    # Dummy ledger
    import os
    test_file = os.path.abspath("test_decoys/salary_report_2024.docx")
    ledger = {test_file: "dummy_canary"}
    
    fim = FIMMonitor(".", ledger, simple_alert)
    fim.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        fim.stop()
