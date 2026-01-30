import logging
import json
import time
import os
from logging.handlers import RotatingFileHandler

def setup_logger(name="ransomware_engine", log_file="ransomware_events.log", level=logging.INFO):
    """
    Sets up a structured logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # File Handler
    file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=5)
    file_handler.setFormatter(formatter)
    
    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
    return logger

class EventLogger:
    def __init__(self, log_file="events.jsonl"):
        self.log_file = log_file

    def log_event(self, event_type: str, details: dict):
        """
        Logs a structured event to a JSONL file for easy parsing by dashboard.
        """
        event = {
            "timestamp": time.time(),
            "event_type": event_type,
            "details": details
        }
        try:
            with open(self.log_file, "a") as f:
                f.write(json.dumps(event) + "\n")
        except Exception as e:
            print(f"Failed to log event: {e}")

if __name__ == "__main__":
    # Test
    l = setup_logger()
    l.info("Logger initialized")
    
    el = EventLogger()
    el.log_event("TEST_EVENT", {"foo": "bar", "severity": "low"})
