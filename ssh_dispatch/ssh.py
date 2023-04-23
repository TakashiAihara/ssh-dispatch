from os.path import join
import paramiko
from ssh_dispatch.settings import Settings
from ssh_dispatch.util import convert_tilde_to_home_path
from ssh_dispatch.logger import logger


def get_or_generate_private_key(settings: Settings, area: str) -> paramiko.RSAKey:
    reg_key_path = join(settings.ssh_keys_path, settings.ssh_key_prefix + area)
    reg_key_data: paramiko.RSAKey

    try:
        logger.info("Reading key for dispatch: " + reg_key_path)
        reg_key_data = paramiko.RSAKey.from_private_key_file(reg_key_path)

    except FileNotFoundError:
        logger.info("Key not found. generating: " + reg_key_path)
        reg_key_data = paramiko.RSAKey.generate(settings.rsa_bits)
        reg_key_data.write_private_key_file(reg_key_path)

    logger.debug(reg_key_data.get_base64())
    return reg_key_data


def generate_ssh_client() -> paramiko.SSHClient:
    logger.debug("generate ssh client.")
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    return ssh_client


def get_key_for_use(key: str) -> paramiko.RSAKey:
    return paramiko.RSAKey.from_private_key_file(convert_tilde_to_home_path(key))


def detect_already_save(ssh_client: paramiko.SSHClient, pkey: str) -> bool:
    logger.debug("detect already save.")
    stdin, stdout, stderr = ssh_client.exec_command('grep "' + pkey + '" ~/.ssh/authorized_keys')
    output = stdout.read().decode()
    logger.debug("count line: " + str(output.count("\n")))
    is_saved = output.count("\n") > 1
    logger.debug("is saved: " + str(is_saved))
    return is_saved


def save_pkey(ssh_client: paramiko.SSHClient, pkey: str) -> None:
    logger.debug("save pkey.")
    stdin, stdout, stderr = ssh_client.exec_command('echo "ssh-rsa ' + pkey + '" >> ~/.ssh/authorized_keys')
