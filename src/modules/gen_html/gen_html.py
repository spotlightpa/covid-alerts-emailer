from jinja2 import Template
from jinja2 import Environment, FileSystemLoader
from definitions import DIR_DATA


def gen_html(templates_path, template_vars):
    """
    Generates HTML from templates using jinja2.

    Args:
        templates_path (str): Path to directory that has html templates
        template_vars (dict): Variables for templates

    Returns:
        A string of HTML.
    """
    file_loader = FileSystemLoader(templates_path)
    env = Environment(loader=file_loader)
    template = env.get_template("base.html")
    output = template.render(**template_vars)
    return output
