import logging
import os



class LoggerManager:
    @staticmethod
    def configure_logger(name:str =' default', log_dir:str = './logs/', verbose:bool = False) -> logging.Logger:

        # Log Directory
        if not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # log Level
        log_level = logging.DEBUG if verbose else logging.INFO

        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        # File Handler
        file_handler = logging.FileHandler(os.path.join(log_dir, f'{name}.log'))
        file_handler.setFormatter(formatter)

    
        # Create logger
        logger = logging.getLogger(name)
        # Add Handlers to Logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        # Set Level
        logger.setLevel(log_level)
        # Propagate
        logger.propagate = False


        return logger