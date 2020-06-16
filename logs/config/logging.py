import logging
import logging.config
import os
import yaml
from definitions import DIR_LOGS_OUTPUT, PATH_LOGS_CONFIG


def logs_config(
    default_path=PATH_LOGS_CONFIG, default_level=logging.INFO, env_key="LOG_CFG"
):
    """
    Setup logging configuration
    @default_path: path of logging config file, eg. config/logging.yaml
    @default_level: default level that logs are logged at.
    @env_key: If env_key is detected among env variables, this will be used as path to config file
    """

    path = default_path

    # if file path is set using LOG_CFG env as path to config file
    value = os.getenv(env_key, None)
    if value:
        path = value

    # load config
    if os.path.exists(path):
        with open(path, "rt") as f:
            config = yaml.safe_load(f.read())  # convert yaml to dict
            # we get the path in config file then append it to our log directory
            for handler in config["handlers"]:
                if "FileHandler" in config["handlers"][handler]["class"]:
                    config["handlers"][handler]["filename"] = (
                        DIR_LOGS_OUTPUT / config["handlers"][handler]["filename"]
                    )
                    config["handlers"][handler]["filename"].parent.mkdir(
                        exist_ok=True, parents=True
                    )  # create parent
                    # directories of path if they don't exist
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
