import altair as alt


def spotlight():
    # la times typography
    titleFont = "Benton Gothic Bold, sans-serif"
    titleFontSize = 22
    titleFontWeight = "normal"
    labelFont = "Benton Gothic, sans-serif"
    labelFontSize = 11.5
    labelFontWeight = "normal"
    legendFontSize = 16
    legendFontWeight = "normal"
    font = "Benton Gothic, sans-serif"

    # Axes
    axisColor = "#000000"
    gridColor = "#DEDDDD"
    return {
        "width": 600,
        "height": 380,
        "autosize": {"type": "fit", "contains": "padding"},
        "config": {
            "title": {
                "fontSize": titleFontSize,
                "font": titleFont,
                "fontWeight": titleFontWeight,
                "anchor": "start",  # equivalent of left-aligned.
                "fontColor": "#000000",
            },
            "axis": {
                "labelFont": labelFont,
                "labelFontSize": labelFontSize,
                "labelFontWeight": labelFontWeight,
                "titleFont": titleFont,
                "titleFontSize": titleFontSize,
                "titleFontWeight": titleFontWeight,
            },
            "axisX": {
                "domain": True,
                "domainColor": axisColor,
                "domainWidth": 1,
                "grid": False,
                "labelAngle": 0,
                "tickSize": 5,
                "tickColor": axisColor,
                "labelOverlap": True,
                "titlePadding": 10,  # guessing, not specified in styleguide
                "title": "X Axis Title (units)",
                "tickCount": 5,
            },
            "axisY": {
                "domain": False,
                "grid": True,
                "gridColor": gridColor,
                "gridWidth": 1,
                "labelFont": labelFont,
                "labelFontSize": 12,
                "labelAngle": 0,
                "ticks": False,  # even if you don't have a "domain" you need to turn these off.
                "titleFont": font,
                "titleFontSize": 12,
                "titlePadding": 10,  # guessing, not specified in styleguide
                "title": "Y Axis Title (units)",
                "tickCount": 5,
                # titles are by default vertical left of axis so we need to hack this
                "titleAngle": 0,  # horizontal
                "titleY": -10,  # move it up
                "titleX": 18,  # move it to the right so it aligns with the labels
            },
            "legend": {
                "labelColor": "black",
                "labelFont": font,
                "labelFontSize": labelFontSize,
                "symbolType": "square",  # just 'cause
                "symbolSize": 100,  # default
                "titleFont": font,
                "titleFontSize": legendFontSize,
                "titleFontWeight": legendFontWeight,
                # "orientation": "vertical",
                "orient": "top",
                "padding": 0,
                # "title": "",  # set it to no-title by default
            },
            "view": {
                "stroke": "transparent",  # altair uses gridlines to box the area where the data is visualized. This
                # takes that off.
            },
        },
    }
