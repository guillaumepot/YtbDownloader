from src.LoggerManager import LoggerManager



def main():
    console_logger = LoggerManager.configure_logger(name='script', verbose=True)

    console_logger.debug('Hello, World!')


if __name__ == "__main__":
    main()