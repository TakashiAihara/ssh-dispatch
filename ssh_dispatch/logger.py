import logging
from os import makedirs
from os.path import join
from settings import Settings

makedirs(Settings.logs_path, exist_ok=True)

logging.basicConfig(
    filename=join(Settings.logs_path, Settings.log_name),
    level=logging.INFO,
    format="[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)

formatter = logging.Formatter("%(name)-12s: %(levelname)-8s %(message)s")
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(formatter)
logging.getLogger("").addHandler(console)

logger = logging.getLogger(__name__)
