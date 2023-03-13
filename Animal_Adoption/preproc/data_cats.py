import os
import pandas as pd


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

def get_merge_cats():
    """"function to merge the aac_shelter_cat_outcome_eng.csv with our clean dataframe"""
     #load both dataframes

    csv_path = os.path.join("../../raw_data", "aac_intakes_outcomes.csv")
    data= pd.read_csv(os.path.join(csv_path))
    csv_path_cats = os.path.join("../../raw_data", "aac_shelter_cat_outcome_eng.csv")
    data_cats= pd.read_csv(os.path.join(csv_path_cats))
    #drop all dogs from main dataframe
    data.drop(data[data['animal_type'] == 'Dog'].index, inplace = True)

    #merge to dataframes into one with only cats but all information
    data_cats.merge(data, left_on='animal_id', right_on='animal_id_outcome')

    # call the second function 'select_and_rename_columns' into the first function
    data_cats = select_and_rename_columns(data_cats)
    
    return data_cats

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



