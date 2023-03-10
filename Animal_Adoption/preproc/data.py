import os
import pandas as pd
import numpy as np
from .preproc_colors import perform_all_color_cleaning
from.preproc_intake_conditions import fix_age


def separate_dataframe(df, column_name, unique_value):
    grouped = df.groupby(column_name)
    filtered_df = grouped.get_group(unique_value)
    #other_df= df.loc[df[column_name] != unique_value]
    return filtered_df

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
        'outcome_hour', 'age_upon_intake_(days)',
        'intake_monthyear', 'outcome_datetime', 'outcome_type'
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
    
    # relabled columns: column 'breed'
    data['breed']= get_breed(data['breed'])


    data = separate_dataframe(data,'animal_type', animal_type)
    
    return data



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

if __name__ == "__main__":
    print(get_data())
