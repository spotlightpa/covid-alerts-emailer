### Covid alerts

An app that sends out emails to subscribers with updates on COVID-19 cases, deaths and other data in their county.

View an example email [here](https://interactives.data.spotlightpa.org/2020/covid-email-alerts/assets/2020-11-09/newsletter_Dauphin_2020-11-09.html).

[Click here](https://email-alerts.data.spotlightpa.org/form.html) to sign up for the mailing list.

#### Requirements

- Python 3.6.
- This project uses [Selenium](https://www.selenium.dev/selenium/docs/api/py/), which requires Chrome and
 [chromedriver](https://chromedriver.chromium.org/) to be installed. Here's a chromedriver install guide for [Ubuntu 16.04 and 18.04](https://tecadmin.net/setup-selenium-chromedriver-on-ubuntu/)
 and for [Mac](http://jonathansoma.com/lede/foundations-2017/classes/more-scraping/selenium/).
- This project uses geopandas, which may require certain [additional dependencies](https://geopandas.org/install.html
) depending on your OS.
- A SendGrid account, with API key stored in .env file in project root (see .env.example).
- A AWS S3 bucket set up, with AWS IAM credentials stored in .env in project root (see .env.example) or in ~/.aws
/credentials


#### Install

- Run `./setup.sh`. To use specific version of Python, run `PATH=PATH_TO_PYTHON:$PATH ./setup.sh`.

- Create a .env file in the project root and add API keys and associated variables. Use .env.example as a template.

#### Run

- `./run.sh`
