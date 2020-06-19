from typing import Dict, List
import requests
import csv


def fetch_data(url_dir: str, dataIndex: List[Dict]) -> Dict[str, Dict]:
    """
    Loops over a list of dictionaries and fetches CSV data.

    Args:
        url_dir (str): Url where data is located, without the filename. Eg.
            "http://interactives.data.spotlightpa.org/2020/coronavirus/data/inquirer"
        dataIndex (list): List of dictionaries that includes a filename key and a name key, describing the type of
            data contained in the file.

    Returns:
        A dictionary of ordered dictionaries with the fetched data.
    """
    data = {}
    for item in dataIndex:
        csv_url = f"{url_dir}/{item['filename']}"
        with requests.get(csv_url, stream=True) as r:
            lines = (line.decode("utf-8") for line in r.iter_lines())
            reader = csv.DictReader(lines)
            csv_data = [x for x in reader]
        data[item.name] = csv_data
    return data
