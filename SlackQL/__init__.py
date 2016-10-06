import logging
logger = logging.getLogger('')
console = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)-4s: %(message)s', "%Y-%m-%d %H:%M:%S")
console.setFormatter(formatter)
logger.addHandler(console)
logger.setLevel(logging.INFO)
