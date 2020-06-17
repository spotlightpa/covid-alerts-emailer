from definitions import DIR_DATA
from src.init.init_program import init_program
from jinja2 import Template
from jinja2 import Environment, FileSystemLoader
import altair as alt
from vega_datasets import data
from altair_saver import save
import requests


def main():

    # init
    init_program()

    # rget data

    # data

    # Create altair graphic
    cars = data.cars()
    chart = (
        alt.Chart(cars)
        .mark_point()
        .encode(x="Horsepower", y="Miles_per_Gallon", color="Origin",)
    )
    # chart.show()
    path = DIR_DATA / "chart.svg"
    save(chart, str(path))

    # produce newsletter
    file_loader = FileSystemLoader("src/templates")
    env = Environment(loader=file_loader)
    template = env.get_template("base.html")
    output = template.render(title="Page Title!!!", body="New covid case data")
    html_path = DIR_DATA / "test.html"
    with open(html_path, "w") as fout:
        fout.writelines(output)


if __name__ == "__main__":
    main()
