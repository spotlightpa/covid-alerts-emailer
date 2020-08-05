import inflect


def rank_text(rank_from_top: int, rank_from_bottom: int,) -> str:
    """
    Generates a text fragment describing a value's rank within the total range.

    Args
        rank_from_top (int): Rank of item from highest (eg. 1) to lowest (eg. 67).
        rank_from_bottom (int): Rank of item from lowest (eg. 67) to highest (eg. 1).

    Returns:
        str: Text fragment
    """
    p = inflect.engine()
    if rank_from_top <= rank_from_bottom:
        if rank_from_top == 1:
            return "highest"
        else:
            return f"{p.ordinal(rank_from_top)} highest"
    else:
        if rank_from_bottom == 1:
            return "lowest"
        else:
            return f"{p.ordinal(rank_from_bottom)} lowest"
