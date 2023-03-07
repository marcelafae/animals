import pandas as pd

#color name substitution
def replace_colors(color_list: list,
                   new_color: str,
                   series: pd.Series) -> pd.Series:
    series = series.copy()
    for color in color_list:
        series = series.str.replace(color, new_color)
    return series

#check for duplicate values separated by "/"
def is_duplicate_value(color: str) -> str:
    color_list = color.split("/")
    if len(color_list) != 2:
        return color
    if color_list[0] == color_list[1]:
        return color_list[0]
    else:
        return color

#defining all tricolor animals in tricolor
def is_tricolor(in_color: str) -> str:
    colors = ["Calico", "Tricolor"]
    color_list = " ".join(in_color.split("/")).split(" ")
    for color in colors:
        if color in color_list:
            return "Tricolor"
    return in_color

#defining all animals in striped
def has_stripes(in_color: str) -> str:
    colors = ["Torbie", "Striped", "Tabby", "Tortie", "Tiger", "Brindle", "Sable"]
    color_list = " ".join(in_color.split("/")).split(" ")
    for color in colors:
        if color in color_list:
            return "Striped"
    return in_color

#defining all animals with spots
def has_spots(in_color: str) -> str:
    colors = ["Merle", "Spotted"]
    color_list = " ".join(in_color.split("/")).split(" ")
    for color in colors:
        if color in color_list:
            return "Spotted"
    return in_color

#function for performing all of the above operations at once!
def perform_all_color_cleaning(series: pd.Series) -> pd.Series:
    color_map = {
        "": [" Tick"],
        "Brown": ["Chocolate", "Liver", "Ruddy"],
        "White": ["Flame Point", "Lilac Point"],
        "Beige": ["Buff", "Tan", "Fawn", "Yellow", "Gold", "Cream", "Seal Point", "Lynx Point", "Brown Point", "Apricot", "Pink"],
        "Orange": ["Orange Tabby", "Red"],
        "Tricolor": ["Tricolor", "Calico"],
        "Spotted": ["Black Merle", "Brown Merle", "Gray Merle", "Orange Merle" ],
        "Striped": ["Tiger", "Tabby"],
        "Gray": ["Black Smoke", "Gray Smoke", "Gray Point", "Silver Lynx Point", "Silver", "Agouti", "Grey", "Blue", "Gray Beige"],
    }
    for key, val in color_map.items():
        series = replace_colors(val, key, series)
    series = series.map(is_duplicate_value)
    series = series.map(has_spots)
    series = series.map(has_stripes)
    series = series.map(is_tricolor)
    return series
