import logging
import os

class AppLogger:
    def __init__(self, name: str):
        """
        Initializes the logger. 
        Requires a 'name' (usually __name__ from the calling file) to track where logs come from.
        """
        self.logger = logging.getLogger(name)
        
        # Set the minimum logging level
        self.logger.setLevel(logging.DEBUG)
        # Define the log directory and file
        log_dir = "data/selpy_app/system/logs"
        log_file = f"{name}.log"

        # CRITICAL: Check if handlers already exist to prevent duplicate log entries
        if not self.logger.handlers:
            
            # 1. Ensure the log directory exists
            os.makedirs(log_dir, exist_ok=True)
            log_path = os.path.join(log_dir, log_file)

            # 2. Define the format for your logs
            formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")

            # 3. Setup File Handler (writes to file)
            file_handler = logging.FileHandler(log_path)
            file_handler.setFormatter(formatter)

            # 4. Setup Stream Handler (prints to console)
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)

            # 5. Add handlers to the logger instance
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

            # Optional: Prevent log messages from being passed to the root logger
            self.logger.propagate = False

    def get_logger(self):
        """Returns the configured logger instance."""
        return self.logger