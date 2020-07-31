from typing import Union
from css_html_js_minify import html_minify
from pathlib import Path


def minify_email_html(html: str, save_path: Union[str, Path] = None) -> str:
    """
    Minifies provided html.

    Args:
        html (str): Source html to minified.
        save_path (Union[str, Path], optional): Path to save file to. Defaults to None. Minified file will not be saved.

    Returns:
        str: minified version of provided HTML
    """
    minified_html = html_minify(html)
    if save_path:
        save_path = str(save_path)
        with open(save_path, "w") as fout:
            fout.writelines(minified_html)
    return minified_html
