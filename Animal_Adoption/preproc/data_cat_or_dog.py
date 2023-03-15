import os
import pandas as pd
import numpy as np
from .preproc_colors import perform_all_color_cleaning
from .columns_relabled import breed_2classes
from .columns_relabled import outcome_type_2classes
from .columns_relabled import intake_condition_2classes
from .columns_relabled import color_3classes
from .target_relabled import time_in_shelter_days_round_2classes, time_in_shelter_days_round_8classes
# from preproc.data_all import get_data_all
# from preproc.preproc_colors import perform_all_color_cleaning
# from preproc.preproc_intake_conditions import fix_age, drop_under_8_aged

# nothing from and import from the data_dog.py because it is already inside 


def separate_dataframe(df, column_name, unique_value):
    grouped = df.groupby(column_name)
    filtered_df = grouped.get_group(unique_value)
    #other_df= df.loc[df[column_name] != unique_value]
    return filtered_df

#keep only the useful columns and rename them
def select_and_rename_columns(df):
    # list of columns to keep
    columns_to_keep = ['animal_id','animal_type_x', 'breed_x', 'color_y', 'intake_condition', 'intake_type',
                       'sex_upon_intake', 'age_upon_intake_(years)', 'intake_datetime',
                       'time_in_shelter_days', 'Cat/Kitten (outcome)', 'cfa_breed', 'domestic_breed',
                       'sex_y', 'Spay/Neuter', 'breed_y']

    # select columns and rename them
    df_selected = df[columns_to_keep].rename(columns={'animal_type_x': 'animal_type',
                                                      'color_y': 'color',
                                                     'breed_x': 'breed',
                                                     'sex_y': 'sex',
                                                      'Cat/Kitten (outcome)': 'Cat/Kitten',
                                                      'breed_y': 'hair length'})

    # return new dataframe with selected and renamed columns
    return df_selected


def get_data(animal_type):
    """
    Its values should be pandas.DataFrames loaded from csv files
    """
    # load the dataset
    root_dir = os.path.dirname(os.path.dirname(__file__))
    csv_path = os.path.join(root_dir, "../raw_data", "aac_intakes_outcomes.csv")
    data= pd.read_csv(os.path.join(csv_path))

    # Drop duplicates in place
    data.drop_duplicates(inplace=True)

    # convert several columns in another type
    data['date_of_birth'] = pd.to_datetime(data['date_of_birth'])
    data['outcome_datetime'] = pd.to_datetime(data['outcome_datetime'])
    data['intake_datetime'] = pd.to_datetime(data['intake_datetime'])

    # drop columns (meaningless, missing values or correlated to another column)
    data.drop([
        'outcome_subtype', 'outcome_number', 'found_location',
        'time_in_shelter', 'age_upon_outcome_age_group', 'age_upon_intake_age_group',
        'dob_year', 'dob_month', 'dob_monthyear', "age_upon_outcome",
        'age_upon_intake_(days)', 'count', 'age_upon_outcome_(days)',
        'age_upon_outcome_(years)', 'outcome_month',
        'outcome_year', 'outcome_monthyear', 'outcome_weekday',
        'outcome_hour', 'outcome_datetime', 'age_upon_intake_(days)',
        'intake_monthyear'
        ], axis=1, inplace= True)
    data.dropna(inplace=True)
    # drop the values 'Bird' and 'Other' in the column 'animal_type'
    data.drop(data[data['animal_type'] == 'Bird'].index, inplace = True)
    data.drop(data[data['animal_type'] == 'Other'].index, inplace = True)

    # relabled colums: split the column 'sex_upon_outcome' into a column 'sex' and a column 'sex_type'
    data['sex_type']= data.sex_upon_outcome.map(lambda x : x.split(" ")[0])
    data['sex']= data.sex_upon_outcome.map(lambda x : x.split(" ")[-1])
    # relabel the values of the new column 'sex' to value 'Neutered' and value 'Intact' and value 'NaN'(unknown)
    data.sex_type.replace(['Neutered', 'Spayed', 'Intact', 'Unknown'], ['Neutered', 'Neutered', 'Intact', 'Unknown'], inplace=True)
    data.sex.replace(['Male', 'Female', 'Unknown', 'nan'], ['Male', 'Female', 'Unknown', 'nan'], inplace=True)

    # relabled columns: column 'color'
    #color name substitution
    data['color']= perform_all_color_cleaning(data['color'])
    # data['color_new']= data.


    # relabled column 'breed_new' with values 'small', 'big', 'uncommon'
    data['breed_new']= get_breed(data['breed'])
    # relabled column 'breed_mix_nonmix' with values 'mix' and 'non_mix'
    data = breed_2classes(data,'breed')

    # relabled column 'outcome_type_2classes' with values 'adopted' and 'not adopted'
    data= outcome_type_2classes(data,'outcome_type')


    # relabled columns: time_in_shelter, mean is 17 days
    data['time_in_shelter_days_round']= data['time_in_shelter_days'].apply(lambda x: round(x))
    data['time_in_shelter_class']= data['time_in_shelter_days'].apply(classify_value)
    # 'time_in_shelter_days_5' -> 5 classes
    data= time_in_shelter_days_round_8classes(data, 'time_in_shelter_days_round')
    # 'time_in_shelter_days_2' -> 2 classes (one week, more than one week)
    data= time_in_shelter_days_round_2classes(data,'time_in_shelter_days_round')

    # relabled column: 'intake_condition' into 'intake_condition_2classes with the values 'normal' and 'not normal'
    data = intake_condition_2classes(data,'intake_condition')

    data= color_3classes(data, 'color')
    
    data = separate_dataframe(data,'animal_type', animal_type)
    
    # Challenge to merge together
    if animal_type == "Cat":
        csv_path_cats = os.path.join("../../raw_data", "aac_shelter_cat_outcome_eng.csv")
        data_cats= pd.read_csv(os.path.join(csv_path_cats))
        #merge to dataframes into one with only cats but all information
        data_cats = data_cats.merge(data, left_on='animal_id', right_on='animal_id_outcome')
         # call the second function 'select_and_rename_columns' into the first function
        data_cats = select_and_rename_columns(data_cats)
        return data_cats
    else:
        return data
    return data

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

