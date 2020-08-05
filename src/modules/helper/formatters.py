def format_commas(number: int):
    """
    Takes int, adds commas between 1000s. eg. converts 10000 to 10,000
    """
    return "{:,}".format(number)
