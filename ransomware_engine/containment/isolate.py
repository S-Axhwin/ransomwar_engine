import logging
import psutil
import os
import time

logger = logging.getLogger(__name__)

class Containment:
    def __init__(self, safe_mode=True):
        self.safe_mode = safe_mode
        self.triggered = False

    def isolate_network(self):
        """
        Disable network interfaces.
        In Safe Mode, this just logs the action.
        """
        if self.triggered:
            return

        logger.critical("🚨 CONTAINMENT TRIGGERED: Network Isolation Requested")
        
        if self.safe_mode:
            logger.warning("SAFE MODE ACTIVE: Network isolation skipped. Would have executed 'pfctl -e' or similar.")
        else:
            # Dangerous! Only enable if sure.
            # Example for Mac: os.system("sudo ifconfig en0 down")
            logger.critical("CORE ACTION: Disabling network interfaces (simulated for now even in non-safe mode to prevent lockout)")
            # In a real tool: 
            # subprocess.run(["sudo", "ifconfig", "en0", "down"])

        self.triggered = True

    def kill_process(self, pid: int):
        """
        Terminates a suspicious process.
        """
        logger.critical(f"🚨 CONTAINMENT TRIGGERED: Kill Process PID={pid}")

        if self.safe_mode:
            logger.warning(f"SAFE MODE ACTIVE: Process {pid} would be killed.")
            return

        try:
            p = psutil.Process(pid)
            p.terminate() # or p.kill()
            logger.critical(f"Process {pid} terminated.")
        except psutil.NoSuchProcess:
            logger.error(f"Process {pid} not found.")
        except psutil.AccessDenied:
            logger.error(f"Access denied to kill process {pid}. (Run as root?)")

    def shutdown_system(self):
        """
        Last resort.
        """
        logger.critical("🚨 CONTAINMENT TRIGGERED: SYSTEM SHUTDOWN")
        if self.safe_mode:
            logger.warning("SAFE MODE ACTIVE: Shutdown skipped.")
        else:
            # os.system("sudo shutdown -h now")
            pass

if __name__ == "__main__":
    # Test
    logging.basicConfig(level=logging.INFO)
    c = Containment(safe_mode=True)
    c.isolate_network()
    c.kill_process(12345)
