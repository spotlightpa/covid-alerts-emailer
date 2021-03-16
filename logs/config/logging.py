import logging
import logging.config
import os
import yaml
from src.definitions import DIR_LOGS_OUTPUT, PATH_LOGS_CONFIG


def logs_config(
    default_path=PATH_LOGS_CONFIG, default_level=logging.INFO, env_key="LOG_CFG"
):
    """
    Setup logging configuration
    @default_path: path of logging config file, eg. config/logging.yaml
    @default_level: default level that logs are logged at.
    @env_key: If env_key is detected among env variables, this will be used as path to config file
    """
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s (%(filename)s:%(lineno)s): %(message)s",
        datefmt='%b %-d, %Y %-H:%M:%S %p'
    )
