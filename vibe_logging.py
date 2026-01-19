# ResoniteLink AI World Builder v5.0
# logging_utils.py - Logging and JSON export

"""
Logging utilities for debug output and JSON command export.
"""

import datetime
import json
import os


class Logger:
    """Handles logging to console, file, and JSON export."""
    
    def __init__(self, log_dir="."):
        self.log_dir = log_dir
        self.log_file = None
        self.json_file = None
        self.json_first_entry = True
        self.log_filename = None
        self.json_filename = None
        self.start_time = None
    
    def init(self):
        """Initialize logging files with timestamp-based names."""
        self.start_time = datetime.datetime.now()
        date_str = self.start_time.strftime("%y%m%d_%H%M")
        
        # Create log directory if needed
        if self.log_dir and not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        
        # Open log file
        self.log_filename = f"resonite_debug_{date_str}.log"
        log_path = os.path.join(self.log_dir, self.log_filename)
        self.log_file = open(log_path, "a", encoding="utf-8")
        
        # Open JSON file
        self.json_filename = f"resonite_builder_{date_str}.json"
        json_path = os.path.join(self.log_dir, self.json_filename)
        self.json_file = open(json_path, "w", encoding="utf-8")
        self.json_file.write("[\n")
        
        # Log header
        self.log("=" * 60)
        self.log("ResoniteLink AI World Builder v5.0")
        self.log(f"Started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.log(f"Log file: {self.log_filename}")
        self.log(f"JSON file: {self.json_filename}")
        self.log("=" * 60)
    
    def log(self, message):
        """Log a message to console and file.
        
        Args:
            message: Message to log
        """
        timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        line = f"[{timestamp}] {message}"
        print(line)
        if self.log_file:
            self.log_file.write(line + "\n")
            self.log_file.flush()
    
    def log_json(self, label, data):
        """Log JSON data with a label.
        
        Args:
            label: Label prefix (e.g., "SENDING:", "RECEIVED:")
            data: Data to log (will be JSON formatted)
        """
        formatted = json.dumps(data, indent=2)
        self.log(f"{label}\n{formatted}")
    
    def log_prompt(self, prompt):
        """Log a user prompt with visual separators.
        
        Args:
            prompt: User's prompt text
        """
        self.log("*" * 60)
        self.log(f"PROMPT: {prompt}")
        self.log("*" * 60)
    
    def log_plan(self, plan):
        """Log the AI's build plan.
        
        Args:
            plan: Plan description
        """
        self.log(f"Plan: {plan}")
    
    def log_mapping(self, placeholder, real_id):
        """Log ID mapping.
        
        Args:
            placeholder: Placeholder ID (e.g., $SLOT_0)
            real_id: Real generated ID
        """
        self.log(f"Mapping {placeholder} -> {real_id}")
    
    def log_ok(self, operation, detail=None):
        """Log successful operation.
        
        Args:
            operation: Operation name (e.g., "addSlot")
            detail: Optional detail string
        """
        if detail:
            self.log(f"OK {operation}: {detail}")
        else:
            self.log(f"OK {operation}")
    
    def log_fail(self, operation, error):
        """Log failed operation.
        
        Args:
            operation: Operation name
            error: Error message
        """
        self.log(f"FAILED {operation}: {error}")
    
    def log_warning(self, message):
        """Log a warning message.
        
        Args:
            message: Warning message
        """
        self.log(f"WARNING: {message}")
    
    def log_error(self, message):
        """Log an error message.
        
        Args:
            message: Error message
        """
        self.log(f"ERROR: {message}")
    
    def write_json(self, data):
        """Write command data to JSON export file.
        
        Args:
            data: Command data to export
        """
        if self.json_file:
            if not self.json_first_entry:
                self.json_file.write(",\n")
            self.json_first_entry = False
            self.json_file.write(json.dumps(data, indent=2))
            self.json_file.flush()
    
    def close(self):
        """Close all log files."""
        if self.json_file:
            self.json_file.write("\n]\n")
            self.json_file.close()
            self.json_file = None
        
        if self.log_file:
            self.log("Goodbye!")
            elapsed = datetime.datetime.now() - self.start_time
            self.log(f"Session duration: {elapsed}")
            self.log_file.close()
            self.log_file = None


# Global logger instance
_logger = None


def get_logger():
    """Get the global logger instance.
    
    Returns:
        Logger: Global logger instance
    """
    global _logger
    if _logger is None:
        _logger = Logger()
    return _logger


def init_logging(log_dir="."):
    """Initialize the global logger.
    
    Args:
        log_dir: Directory for log files
    """
    global _logger
    _logger = Logger(log_dir)
    _logger.init()
    return _logger


def log(message):
    """Log a message using the global logger.
    
    Args:
        message: Message to log
    """
    get_logger().log(message)


def log_json(label, data):
    """Log JSON data using the global logger."""
    get_logger().log_json(label, data)


def log_prompt(prompt):
    """Log a prompt using the global logger."""
    get_logger().log_prompt(prompt)


def close_logging():
    """Close the global logger."""
    global _logger
    if _logger:
        _logger.close()
        _logger = None
