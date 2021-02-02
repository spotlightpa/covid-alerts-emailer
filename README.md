### Covid alerts

An app that sends out emails to subscribers with updates on COVID-19 cases, deaths and other data in their county.

View an example email [here](https://interactives.data.spotlightpa.org/2020/covid-email-alerts/assets/2020-11-09/newsletter_Dauphin_2020-11-09.html).

[Click here](https://email-alerts.data.spotlightpa.org/form.html) to sign up for the mailing list.

#### Requirements

- Python 3.6 or higher.
- This project uses [Selenium](https://www.selenium.dev/selenium/docs/api/py/), which requires Chrome and
 [chromedriver](https://chromedriver.chromium.org/) to be installed. Here's a chromedriver install guide for [Ubuntu 16.04 and 18.04](https://tecadmin.net/setup-selenium-chromedriver-on-ubuntu/) 
 and for [Mac](http://jonathansoma.com/lede/foundations-2017/classes/more-scraping/selenium/).
- This project uses geopandas, which may require certain [additional dependencies](https://geopandas.org/install.html
) depending on your OS.
- A SendGrid account, with API key stored in .env file in project root (see .env.example).
- A AWS S3 bucket set up, with AWS IAM credentials stored in .env in project root (see .env.example) or in ~/.aws
/credentials

#### Install

1. Open the terminal. Clone the project repo.

2. If you don't have pipenv installed on your machine, install it. On Mac, using you homebrew, run:

    `brew install pipenv`

3. Navigate into the project directory.
     
4. Use pipenv to create a virtual environment and install the project 
dependencies. Run:

    `pipenv install`

5. Create a .env file in the project root and add API keys and associated variables. Use .env.example as a template.

#### Run

`pipenv run python src/covid_email_alerts.py`
