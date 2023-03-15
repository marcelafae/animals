import os
import pandas as pd
import numpy as np
from .data_all import get_data_all
from .data_cats import get_merge_cats
from .preproc_colors import perform_all_color_cleaning
from .preproc_intake_conditions import fix_age, drop_under_8_aged
from .data_dog import get_data_dogs
# nothing from and import from the data_dog.py because it is already inside 


def separate_dataframe(df, column_name, unique_value):
    grouped = df.groupby(column_name)
    filtered_df = grouped.get_group(unique_value)
    #other_df= df.loc[df[column_name] != unique_value]
    return filtered_df


def get_data(animal_type):
    """
    Its values should be pandas.DataFrames loaded from csv files
    """
    # Challenge to merge together
    if animal_type == "Cat":
        data_cats= get_merge_cats()
        return data_cats
    else:
        return get_data_dogs()

def classify_value(value):
    if 0 <= value < 1:
        return 'after several hours'
    elif 1 <= value <=5:
        return 'between 1 and 5 days'
    elif 5< value <= 10:
        return 'between 6 and 10 days'
    elif 10 < value <= 15:
        return 'between 11 and 15 days'
    elif 15 < value <= 20:
        return 'between 16 and 20 days'
    elif 20 < value <=25:
        return 'between 21 and 25 days'
    elif 25 < value <= 30:
        return 'between 26 and 30 days'
    else:
        return 'higher than 30 days'

# relable the column 'breed'
def get_breed (series: pd.Series) -> pd.Series:
    def cleaning(d: str):
        ## remove whitespaces
        d = d.strip()
        ## lowercasing
        d = d.lower()
        ## remove the word 'mix'-> doesn't work -> data['breed']= data.breed.str.replace('mix', '')
        d = d.replace('mix', '')
        return d
    series = series.map(cleaning)
    breed_map = {
        "small": ["pit bull", "chihuahua","terrier", "dachshund", "miniature poodle", "beagle", "miniature schnauzer", "bulldog", "shih tzu", "pug", "australian kelpie", "maltese", "chow chow", "spaniel", "cardigan welsh corgi","miniature pinscher", "chinese sharpei", "queensland heeler", "pomeranian", "lhasa apso"],
        "big": ["retriever", "shepherd", "australian cattle dog", "collie", "hound", "boxer", "catahoula", "siberian husky", "great pyrenees","rottweiler", "pointer", "staffordshire", "black mouth cur", "doberman pinsch", "blue lacy"],
        "short_hair": ["domestic shorthair", "shorthair", "short hair", "american shorthair", "siamese"],
        "medium_hair": ["domestic medium hair", "medium hair"],
        "long_hair": ["domestic longhair", "long hair", "longhair"],
        "uncommon": get_uncommon_breeds(series),
    }

    for key, val in breed_map.items():
        series = replace_breeds(val, key, series)
    return series

def replace_breeds(breed_list: list,
                   new_breed: str,
                   series: pd.Series) -> pd.Series:
    def helper(breed, new_breed):
        def inner(x):
            return new_breed if breed in x else x
        return inner
    series = series.copy()
    for breed in breed_list:
        mapper = helper(breed, new_breed)
        series = series.map(mapper)
    return series

# delete the separated breeds-> /
def breeds_separated(in_breed: pd.Series) -> pd.Series:
    breed_list = []
    for row in in_breed:
        breed_list += row.split('/')
    breed_list = np.array([breed.strip() for breed in breed_list])
    return pd.Series(breed_list)

def get_uncommon_breeds(breeds: pd.Series) -> list:
    return breeds_separated(breeds).value_counts()[44:].index

