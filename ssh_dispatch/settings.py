import os
from util import convert_tilde_to_home_path
from dotenv import load_dotenv

load_dotenv()


class Settings(object):
    ssh_config_file = convert_tilde_to_home_path(os.environ.get("SSH_CONFIG_FILE") or "~")
    ssh_keys_path = convert_tilde_to_home_path(os.environ.get("SSH_KEYS_PATH") or "~")
    ssh_key_prefix = convert_tilde_to_home_path(os.environ.get("SSH_KEY_PREFIX") or "~")

    logs_path = convert_tilde_to_home_path(os.environ.get("LOGS_PATH") or "logs")
    log_name = convert_tilde_to_home_path(os.environ.get("LOG_NAME") or "ssh_dispatch.log")

    rsa_bits = int(os.environ.get("RSA_BITS") or "4096")
