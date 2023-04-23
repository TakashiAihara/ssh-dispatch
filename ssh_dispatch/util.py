from os.path import expanduser


def convert_tilde_to_home_path(path: str) -> str:
    return path.replace("~", expanduser("~"))
