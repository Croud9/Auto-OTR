import sys
import logging
from logic import logicUIMainApp

logging.basicConfig(filename='Data/System/log_info.log', 
                    level=logging.INFO,
                    filemode='w', 
                    format='%(asctime)s:%(levelname)s:%(message)s')
logger = logging.getLogger(__name__)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_exception

if __name__ == '__main__':
    logicUIMainApp.main()