import time
import os
import argparse
import logging
from ransomware_engine.decoy.generator import DecoyGenerator
from ransomware_engine.detector.fim import FIMMonitor
from ransomware_engine.containment.isolate import Containment
from ransomware_engine.logger.logger import setup_logger, EventLogger

# Setup Global Logger
logger = setup_logger()
event_logger = EventLogger()

def handle_alert(path, reason):
    """
    Callback when FIM detects a modification.
    """
    logger.critical(f"ALERT: {reason} on {path}")
    event_logger.log_event("ALERT", {"reason": reason, "path": path})
    
    # Trigger Containment
    containment = Containment(safe_mode=True) # Start in safe mode
    containment.isolate_network()
    # In a real scenario, we might find the PID:
    # containment.kill_process(pid) 

def main():
    parser = argparse.ArgumentParser(description="Ransomware Detector Engine")
    parser.add_argument("--watch", default=".", help="Directory to watch")
    parser.add_argument("--decoys", default="decoys", help="Directory to store decoys")
    args = parser.parse_args()

    # 1. Initialize Decoys
    logger.info("Initializing Decoy System...")
    decoy_gen = DecoyGenerator(args.decoys)
    
    # Generate a few decoys if they don't exist
    for name in ["salary_data", "passwords", "strategic_plan"]:
        path = decoy_gen.generate_decoy(name, ".docx", overwrite=False)
        logger.info(f"Deployed decoy: {path}")

    # Build Ledger
    # For now, we trust all files in the decoy_dir are ours if we just created them.
    # But FIM needs full paths.
    ledger = {}
    for root, dirs, files in os.walk(args.decoys):
        for file in files:
            full_path = os.path.abspath(os.path.join(root, file))
            # In a real app, we persist the ledger. Re-reading here implies we trust them currently.
            # We should probably re-verify them or just load from a DB.
            # For this MVP, we assume newly created ones are valid.
            ledger[full_path] = "canary_placeholder"
    
    # 2. Start FIM
    logger.info(f"Starting FIM on {args.watch}...")
    fim = FIMMonitor(args.watch, ledger, handle_alert)
    fim.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Stopping engine...")
        fim.stop()

if __name__ == "__main__":
    main()
