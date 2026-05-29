# src/system/heartbeat_writer.py
import time
from pathlib import Path
import logging

# Set up a basic logger for this module
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger(__name__)

class HeartbeatWriter:
    """
    Manages writing a timestamp to a file for external monitoring.
    """
    def __init__(self, file_path="runtime/heartbeat.txt"):
        self.heartbeat_path = Path(file_path)
        # Ensure the directory exists
        try:
            self.heartbeat_path.parent.mkdir(parents=True, exist_ok=True)
            logger.info(f"Heartbeat file path ensured: {self.heartbeat_path}")
        except Exception as e:
            logger.error(f"Failed to create heartbeat directory: {e}")
            # Depending on severity, you might want to raise the exception here

    def ping(self):
        """
        Updates the heartbeat file with the current timestamp.
        """
        try:
            timestamp = str(time.time())
            self.heartbeat_path.write_text(timestamp)
            logger.debug(f"Pinged heartbeat at {timestamp}")
        except IOError as e:
            logger.error(f"Failed to write to heartbeat file: {e}")

if __name__ == "__main__":
    # Example: run as a standalone process to ping every 30 seconds
    writer = HeartbeatWriter()
    logger.info("Starting standalone HeartbeatWriter (pinging every 30s)... Press Ctrl+C to stop.")
    try:
        while True:
            writer.ping()
            time.sleep(30)
    except KeyboardInterrupt:
        logger.info("Heartbeat writer stopped manually.")
