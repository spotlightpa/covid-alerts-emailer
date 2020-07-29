import logging
from dotenv import load_dotenv
from definitions import DIR_OUTPUT
from logs.config.logging import logs_config
from src.modules.gen_chart.themes import spotlight
from src.modules.helper.misc import delete_dir_contents
from src.modules.helper.time import utc_now
from src.modules.init.pandas_opts import pandas_opts
import altair as alt


def init_program():
    # Load env vars
    load_dotenv()

    # init logging
    program_start_time = utc_now()
    timezone = program_start_time.tzinfo
    logs_config()
    logging.info(f"Begin program run: {program_start_time} ({timezone} time)")

    # create or clean download dir
    if DIR_OUTPUT.is_dir():
        # delete files from previous run
        delete_dir_contents(DIR_OUTPUT)
    else:
        logging.info("Data directory doesn't exist - building")
        DIR_OUTPUT.mkdir()

    # Set pandas options
    pandas_opts()

    # set Altair themes
    alt.themes.register("spotlight", spotlight)
    alt.themes.enable("spotlight")

    return program_start_time
