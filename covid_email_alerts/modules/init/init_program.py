import logging
from dotenv import load_dotenv
from covid_email_alerts.definitions import DIR_OUTPUT
from logs.config.logging import logs_config
from covid_email_alerts.modules.gen_chart.themes import spotlight
from covid_email_alerts.modules.helper.misc import delete_dir_contents
from covid_email_alerts.modules.helper.time import utc_now
from covid_email_alerts.modules.init.pandas_opts import pandas_opts
import altair as alt
import os


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

    # this fixes a strange bug with botocore/moto not recognizing AWS credentials: https://github.com/spulec/moto/issues/1941
    os.environ["AWS_ACCESS_KEY_ID"] = os.environ.get("KEY_ID")
    os.environ["AWS_SECRET_ACCESS_KEY"] = os.environ.get("SECRET_KEY_ID")

    # set Altair themes
    alt.themes.register("spotlight", spotlight)
    alt.themes.enable("spotlight")

    return program_start_time
