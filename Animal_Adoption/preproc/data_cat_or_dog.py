import os
import pandas as pd
import numpy as np
from preproc.data_all import get_data_all
from preproc.preproc_colors import perform_all_color_cleaning
from preproc.preproc_intake_conditions import fix_age, drop_under_8_aged

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
    data = get_data_all()
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

