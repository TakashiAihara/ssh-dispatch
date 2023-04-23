import click
from ssh_dispatch.ssh import (
    get_or_generate_private_key,
    generate_ssh_client,
    get_key_for_use,
    detect_already_save,
    save_pkey,
)
from ssh_dispatch.settings import Settings
from ssh_dispatch.logger import logger, console


@click.command()
@click.option(
    "--hostname",
    "-h",
    default="localhost",
    help="Remote server IP address. default=localhost",
)
@click.option(
    "--username",
    "-u",
    default="root",
    help="Username for remote server. default=root",
)
@click.option(
    "--password",
    "-p",
    required=False,
    hide_input=True,
    help="Password for remote server. default=None",
)
@click.option(
    "--key",
    "-k",
    required=False,
    help="Private key for remote server.",
)
@click.option(
    "--area",
    "-a",
    required=False,
    default="home",
    help="Network area name. home/gcp/aws/oci/other",
)
@click.option(
    "--debug",
    "-d",
    required=False,
    is_flag=True,
    help="Debug mode.",
)
def ssh_key_dispatch(
    hostname: str, username: str, password: str | None, key: str | None, area: str, debug: bool
) -> None:
    ssh_client = generate_ssh_client()
    if debug:
        logger.setLevel("DEBUG")
        console.setLevel("DEBUG")

    logger.debug(f"hostname={str(hostname)}")
    logger.debug(f"username={str(username)}")
    logger.debug(f"password={str(password)}")
    logger.debug(f"key={str(key)}")
    logger.debug(f"area={str(area)}")

    reg_key = get_or_generate_private_key(Settings(), area)
    reg_pkey = reg_key.get_base64()

    if key is not None:
        ssh_client.connect(hostname, username=username, password=password, pkey=get_key_for_use(key))
    else:
        ssh_client.connect(hostname, username=username, password=password)

    if detect_already_save(ssh_client, reg_pkey):
        logger.info("Already saved. exit.")

    else:
        logger.info("Public key Not found from authorized_keys. Save public key.")
        save_pkey(ssh_client, reg_pkey)
        logger.info("Saved")

    # SSHセッションを終了
    ssh_client.close()


if __name__ == "__main__":
    ssh_key_dispatch()
