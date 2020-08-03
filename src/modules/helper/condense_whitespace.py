import re
from typing import Union
from pathlib import Path


def condense_whitespace(
    text: str, replace: str = " ", save_path: Union[str, Path] = None
) -> str:
    """
    Replaces whitespace

    Args:
        text (str): Text to change.
        replace (str, optional): Characters to replace white space with. Defaults to a single space: " "
        save_path (Union[str, Path], optional): Path to save file to. Defaults to None. Minified file will not be saved.
    Return:
        str: Text stripped of white space.

    """
    stripped_text = re.sub(r"\s+", replace, text)
    if save_path:
        save_path = str(save_path)
        with open(save_path, "w") as fout:
            fout.writelines(stripped_text)
    return stripped_text
