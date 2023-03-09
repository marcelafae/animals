import os
import pandas as pd
import numpy as np
from .preproc_colors import perform_all_color_cleaning

def get_data():
    """
    Its values should be pandas.DataFrames loaded from csv files
    """
    # load the dataset
    #root_dir = os.path.dirname(os.path.dirname(__file__))
    csv_path = os.path.join("../../raw_data", "aac_intakes_outcomes.csv")
    data= pd.read_csv(os.path.join(csv_path))

    # Drop duplicates in place
    data.drop_duplicates(inplace=True)

    # convert several columns in another type
    data['date_of_birth'] = pd.to_datetime(data['date_of_birth'])
    data['outcome_datetime'] = pd.to_datetime(data['outcome_datetime'])
    data['intake_datetime'] = pd.to_datetime(data['intake_datetime'])

    # drop columns (meaningless, missing values or correlated to another column)
    data.drop(['outcome_subtype', 'outcome_number', 'found_location', 'intake_type', 'time_in_shelter', 'time_in_shelter_days', 'age_upon_outcome_age_group', 'age_upon_intake_age_group', 'dob_year', 'dob_month', 'dob_monthyear'], axis=1, inplace= True)
    data.dropna(inplace=True)
    # drop the values 'Bird' and 'Other' in the column 'animal_type'
    data.drop(data[data['animal_type'] == 'Bird'].index, inplace = True)
    data.drop(data[data['animal_type'] == 'Other'].index, inplace = True)

    # drop the animal_id_outcome, that appears more than once in the column '???'
    data.drop_duplicates(subset=["animal_id_outcome"], keep="first", inplace=True)
    data[data["animal_id_outcome"].duplicated()]["animal_id_outcome"].unique()

    # relabled colums: split the column 'sex_upon_outcome' into a column 'sex' and a column 'sex_type' 
    data['sex_type']= data.sex_upon_outcome.map(lambda x : x.split(" ")[0])
    data['sex']= data.sex_upon_outcome.map(lambda x : x.split(" ")[-1])
    # relabel the values of the new column 'sex' to value 'Neutered' and value 'Intact' and value 'NaN'(unknown)
    data.sex_type.replace(['Neutered', 'Spayed', 'Intact', 'Unknown'], ['Neutered', 'Neutered', 'Intact', 'Unknown'], inplace=True)
    data.sex.replace(['Male', 'Female', 'Unknown', 'nan'], ['Male', 'Female', 'Unknown', 'nan'], inplace=True)

    # relabled columns: column 'color'
    #color name substitution
    data['color']= perform_all_color_cleaning(data['color'])
    # relabled columns: column 'breed'
    data['breed']= get_breed(data['breed'])
    # try loading the datatset and getting an error if not
    return data
    # if data:
    #     return data
    # else: 
    #     return "Data can't be loaded."
        
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
        # series = series.map(uncommon???)
    return series
    
    # def unknown(d):

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