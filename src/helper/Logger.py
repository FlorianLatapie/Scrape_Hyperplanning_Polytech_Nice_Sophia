import logging
import os

path_logs = os.path.dirname(os.path.abspath(__file__)) + "/../../logs/"

if not os.path.exists(path_logs):
    os.makedirs(path_logs)

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO,
                    filename=path_logs + "app.log",
                    filemode="a",
                    format='%(asctime)s - %(levelname)s - %(filename)s - %(message)s')
