import os
import pandas as pd
import numpy as np
import requests
pd.set_option('display.max_rows', None)
from .preproc_colors import *

#only gets the data from the acc_intakes_outcomes, transform some columsn into datetime and drop useless columns
def get_data_dogs():
    """
    Its values should be pandas.DataFrames loaded from csv files
    """
    # load the dataset
    csv_path = os.path.join("../../raw_data", "aac_intakes_outcomes.csv")
    data= pd.read_csv(os.path.join(csv_path))

    data['date_of_birth'] = pd.to_datetime(data['date_of_birth'])
    data['outcome_datetime'] = pd.to_datetime(data['outcome_datetime'])
    data['intake_datetime'] = pd.to_datetime(data['intake_datetime'])

    # drop the values 'Bird' and 'Other' in the column 'animal_type'
    data.drop(data[data['animal_type'] == 'Bird'].index, inplace = True)
    data.drop(data[data['animal_type'] == 'Other'].index, inplace = True)
    data.drop(data[data['animal_type'] == 'Cat'].index, inplace = True)
    data.drop([
        'outcome_subtype', 'animal_id_outcome','outcome_number',
        'found_location', 'animal_id_intake',
        'age_upon_outcome_age_group', 'age_upon_intake_age_group',
        'dob_year', 'dob_month', 'dob_monthyear', "age_upon_outcome",
        'age_upon_intake_(days)', 'count', 'age_upon_outcome_(days)',
        'age_upon_outcome_(years)', 'outcome_month',
        'outcome_year', 'outcome_monthyear', 'outcome_weekday',
        'outcome_hour', 'age_upon_intake_(days)',
        'intake_monthyear', 'outcome_datetime', 'outcome_type'
        ], axis=1, inplace= True)
    return data


# relable the column 'breed'
def get_breed_dogs(series: pd.Series) -> pd.Series:
    def cleaning(d: str):
       ## lowercasing
        d = d.lower()
    # remove the word 'mix', 'toy', etc...->
        d = d.replace("rhod", "")
        d = d.replace("mix", "")
        d = d.replace("eng", "")
        d = d.replace("shorthair", "")
        d = d.replace("longhair", "")
        d = d.replace("smooth", "")
        d = d.replace("queensland", "")
        d = d.replace("old lish", "")
        d = d.replace("wirehair", "")
        d = d.replace("anatol", "")
        d = d.replace("lish", "")
        d = d.replace("rough", "")
        d = d.replace("old", "")

        ## fix the breeds for the api
        d = d.replace("pitbull", "American Staffordshire Terrier")
        d = d.replace("patterdale terr", "patterdale Terrier")
        d = d.replace("bluetick hound", "Bluetick Coonhound")
        d = d.replace("standard poodle", "Poodle (Standard)")
        d = d.replace("miniature poodle", "Poodle (Miniature)")
        d = d.replace("toy poodle", "Poodle (Toy)")
        d = d.replace("german  pointer", "German Shorthaired Pointer")
        d = d.replace("wire hair fox terrier", "Wire Fox Terrier")
        d = d.replace("cavalier span", "Cavalier King Charles Spaniel")
        d = d.replace("jack russell terrier", "terrier")
        d = d.replace("st. bernard rough coat", "saint bernard")
        d = d.replace("st. bernard smooth coat", "saint bernard")
        d = d.replace("flat coat retriever", "Flat-Coated Retriever")
        d = d.replace("tan hound", "Black and Tan Coonhound")
        d = d.replace("redbone hound", "Redbone Coonhound")
        d = d.replace("black mouth cur", "Catahoula")
        d = d.replace("mexican hairless", "American Hairless Terrier")
        d = d.replace("landseer", "Newfoundland")
        d = d.replace("schnauzer giant", "Giant Schnauzer")

        ## remove whitespaces
        d = d.strip()
        return d
    series = series.map(cleaning)

    return series


# delete the separated breeds-> /
def breeds_separated_dogs(in_breed: str) -> str:
    breed_list = in_breed.split('/')
    return breed_list[0]


# relabled colums: split the column 'sex_upon_outcome' into a column 'sex' and a column 'sex_type'
def split_sex_from_castrate(data: pd.DataFrame)-> pd.DataFrame:
    data.dropna(inplace=True)
    data['sex_type']= data.sex_upon_outcome.map(lambda x : x.split(" ")[0])
    data['sex']= data.sex_upon_outcome.map(lambda x : x.split(" ")[-1])
    return data


# gets the dog breed info from the API in the correct way
def get_breeds_info_from_dataframe(df):
    dic_breed_dic ={}
    fail_breed_list = []
    for breed_name in df['breed'].unique():
        api_url = 'https://api.api-ninjas.com/v1/dogs?name={}'.format(breed_name)
        response = requests.get(api_url, headers={'X-Api-Key': os.environ.get("API_KEY", "")})
        response_json = response.json()
        # print(response_json
        # if response_json:
        #     dic_breed_list.append(response_json[0])
        if response_json and type(response_json) == list:
            dic_breed_dic[breed_name] = response_json[0]
        else:
            #fail_breed_list.append()
            print(fail_breed_list)
            print(response_json)
            print(type(response_json))

    breed_info = pd.DataFrame(dic_breed_dic.values(), index=dic_breed_dic.keys())
    return breed_info

      #  breed_info.append(response_df)
   # print(breed_info)
    #return breed_info



# if __name__ == "__main__":
#     print(get_data_dogs())
