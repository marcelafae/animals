import os
import pandas as pd
from .data_all import get_data_all
def get_merge_cats():
    """"function to merge the aac_shelter_cat_outcome_eng.csv with our clean dataframe"""
     #load both dataframes
    data= get_data_all()
    csv_path_cats = os.path.join("../../raw_data", "aac_shelter_cat_outcome_eng.csv")
    data_cats= pd.read_csv(os.path.join(csv_path_cats))
    #drop all dogs from main dataframe
    data.drop(data[data['animal_type'] != 'Cat'].index, inplace = True)

    #merge to dataframes into one with only cats but all information
    data_cats = data_cats.merge(data, left_on='animal_id', right_on='animal_id_outcome')
    data_cats = select_and_rename_columns(data_cats)
    return data_cats

#keep only the useful columns and rename them
def select_and_rename_columns(df):
    # list of columns to keep
    columns_to_keep = ['animal_id','animal_type_x', 'breed_x', 'color_y', 'intake_condition', 'intake_type',
                       'sex_upon_intake', 'age_upon_intake_(years)', 'intake_datetime',
                       'time_in_shelter_days', 'Cat/Kitten (outcome)', 'cfa_breed', 'domestic_breed',
                       'sex_y', 'Spay/Neuter', 'breed_y', 'outcome_type_2classes',
                        'time_in_shelter_days_round', 'time_in_shelter_class',
                        'time_in_shelter_days_round_8classes',
                        'time_in_shelter_days_round_2classes', 'intake_condition_2classes',
                        'color_3classes'
    ]

    # select columns and rename them
    df_selected = df[columns_to_keep].rename(columns={'animal_type_x': 'animal_type',
                                                      'color_y': 'color',
                                                     'breed_x': 'breed',
                                                     'sex_y': 'sex',
                                                      'Cat/Kitten (outcome)': 'Cat/Kitten',
                                                      'breed_y': 'hair length'})

    # return new dataframe with selected and renamed columns
    return df_selected




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
        "": [" Tick", " Point"],
        "Brown": ["Chocolate", "Liver", "Ruddy"],
        "White": ["Flame", "Lilac"],
        "Beige": ["Buff", "Tan", "Fawn", "Yellow", "Gold", "Cream", "Seal", "Lynx", "Brown", "Apricot", "Pink"],
        "Orange": ["Orange Tabby", "Red"],
        "Tricolor": ["Tricolor", "Calico"],
        "Spotted": ["Black Merle", "Brown Merle", "Gray Merle", "Orange Merle" ],
        "Striped": ["Tiger", "Tabby"],
        "Gray": ["Black Smoke", "Gray Smoke", "Silver Smoke", "Blue Smoke", "Silver Lynx", "Silver", "Agouti", "Grey", "Blue", "Gray Beige"],
    }
    for key, val in color_map.items():
        series = replace_colors(val, key, series)
    series = series.map(is_duplicate_value)
    series = series.map(has_spots)
    series = series.map(has_stripes)
    series = series.map(is_tricolor)
    return series
