### Covid alerts

An app that sends out emails to subscribers with updates on COVID-19 cases, deaths and other data in their county.

[Click here](https://email-alerts.data.spotlightpa.org/form.html) to sign up for the mailing list.

#### Requirements

- Python >3.6
- This project uses [selenium](https://www.selenium.dev/selenium/docs/api/py/), which requires
 [chromedriver](https://chromedriver.chromium.org/) or [geckodriver](https://firefox-source-docs.mozilla.org/testing/geckodriver/) 
 to be installed. Here's a chromedriver install guide for [Ubuntu 16.04 and 18.04](https://tecadmin.net/setup-selenium-chromedriver-on-ubuntu/) 
 and for [Mac](http://jonathansoma.com/lede/foundations-2017/classes/more-scraping/selenium/).
- This project uses geopandas, which may require certain [additional dependencies](https://geopandas.org/install.html) depending on your OS.

#### Install

1. Open the terminal. Clone the project repo.

2. If you don't have pipenv installed on your machine, install it. On Mac, using you homebrew, run:

    `brew install pipenv`

3. Navigate into the project directory.
     
4. Use pipenv to create a virtual environment and install the project 
dependencies. Run:

    `pipenv install`

5. Create a .env file in the project root and add API keys and associated variables. Use .env.example as a template.