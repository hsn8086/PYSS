import logging

import util
from config_loader import Config
from server import Server

logging.basicConfig(level=logging.INFO, format='[%(asctime)s][%(name)s][%(levelname)s] %(message)s')
logging.getLogger().addFilter(util.FlaskLoggerFilter())
config = Config()
s = Server(config)
s.start()
