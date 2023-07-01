import logging
import colorlog

class Logger:

    def __init__(self, logger_name = "my_logger", level = "debug") -> None:
        """
        Create a logger.
        Example: logger = Logger(logger_name = "my_logger", level = "debug").
        level: debug < info < warning < error < critical.
        """
        # Create a Logger object
        self.logger = logging.getLogger(logger_name)
        self.handler = logging.StreamHandler() # Default handler
        self.handler_type = "console"
        self.format = "%(log_color)s%(asctime)s - %(levelname)s - %(message)s" # Default format
        self.log_colors = {
        'DEBUG': 'blue',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white'
        }

        if level == "debug":
            self.level = logging.DEBUG
        elif level == "info":
            self.level = logging.INFO
        elif level == "warning":
            self.level = logging.WARNING
        elif level == "error":
            self.level = logging.ERROR
        elif level == "critical":
            self.level = logging.CRITICAL
        self.logger.setLevel(self.level)
    
    def setHandler(self, handler_type = "console", txt_file = "my_log.txt"):
        """
        Set the handler type.
        Example: setHandler(handler_type = "txt", txt_file = "my_log.txt").
        handler_type: "console" or "txt".
        """
        # Create a handler object
        if handler_type == "console":
            handler = logging.StreamHandler()
        elif handler_type == "txt":
            handler = logging.FileHandler(txt_file)
            self.setFormat(color=False)
        handler.setLevel(self.level)
        self.handler = handler
        self.handler_type = handler_type
    
    def setFormat(self, color = True, time = True, name = False, join = "-"):
        """
        Set the logger's format.
        Example: setFormat(name = True, join = "|").
        Default format: time - level - message.
        """
        format_str = ""
        if color:
            format_str = format_str + "%(log_color)s"
        if time:
            format_str = format_str + "%(asctime)s " + join + " "
        if name:
            format_str = format_str + "%(name)s " + join + " "
        format_str = format_str + "%(levelname)s " + join + " " + "%(message)s"
        self.format = format_str
    
    def setLogColor(self, color_dict):
        """
        Set the specified log color.
        Default: {
        'DEBUG': 'blue',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white'
        }.
        """
        self.log_colors = color_dict
    
    def launch(self):
        """
        Launch the logger.
        """
        if self.handler_type == "txt":
            self.formatter = logging.Formatter(self.format)
        elif self.handler_type == "console":
            self.formatter = colorlog.ColoredFormatter(self.format, log_colors=self.log_colors)
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)

    def debug(self, message):
        self.logger.debug(message)
    
    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)
    
    def error(self, message):
        self.logger.error(message)
    
    def critical(self, message):
        self.logger.critical(message)


if __name__ == "__main__":
    logger = Logger()
    #logger.setFormat(name=True, join="") # Please complete setting before launch
    #logger.setFormat(color=False)
    #logger.setHandler(handler_type="txt", txt_file="log.txt")
    logger.launch()
    # Record different levels of log messages
    logger.debug('This is a DEBUG level log message')
    logger.info('This is an INFO level log message')
    logger.warning('This is a WARNING level log message')
    logger.error('This is an ERROR level log message')
    logger.critical('This is a CRITICAL level log message')