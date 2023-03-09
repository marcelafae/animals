import os
import pandas as pd


class Animals:
    def get_data(self):
        """
        Its values should be pandas.DataFrames loaded from csv files
        """
        # load the dataset
        root_dir = os.path.dirname(os.path.dirname(__file__))
        csv_path = os.path.join(root_dir, "data", "aac_intakes_outcomes.csv")
        data= pd.read_csv(os.path.join(csv_path))

        # Drop duplicates in place
        data.drop_duplicates(inplace=True)

        # convert several columns in another type
        data['date_of_birth'] = pd.to_datetime(data['date_of_birth'])
        data['outcome_datetime'] = pd.to_datetime(data['outcome_datetime'])
        data['intake_datetime'] = pd.to_datetime(data['intake_datetime'])

        # drop columns (meaningless, missing values or correlated to another column)
        data.drop(['outcome_subtype', 'outcome_number', 'found_location', 'intake_type', 'time_in_shelter', 'time_in_shelter_days', 'age_upon_outcome_age_group', 'age_upon_intake_age_group', 'dob_year', 'dob_month', 'dob_monthyear'], axis=1, inplace= True)

        # drop the values 'Bird', 'Livestock' and 'Other' in the column 'animal_type'
        data.drop(data[data['animal_type'] == 'Bird'].index, inplace = True)
        data.drop(data[data['animal_type'] == 'Other'].index, inplace = True)
        data.drop(data[data['animal_type'] == 'Livestock'].index, inplace = True)

        # drop the animal_id_outcome, that appears more than once in the column '???'
        data.drop_duplicates(subset=["animal_id_outcome"], keep="first", inplace=True)
        data[data["animal_id_outcome"].duplicated()]["animal_id_outcome"].unique()

        # relabled colums: split the column 'sex_upon_outcome' into a column 'sex' and a column 'sex_type'
        data['sex_type']= data.sex_upon_outcome.apply(lambda x : x.split(" ")[0])
        data['sex']= data.sex_upon_outcome.apply(lambda x : x.split(" ")[-1])
        # relabel the values of the new column 'sex' to value 'Neutered' and value 'Intact' and value 'NaN'(unknown)
        data.sex_type.replace(['Neutered', 'Spayed', 'Intact', 'Unknown'], ['Neutered', 'Neutered', 'Intact', 'Unknown'], inplace=True)
        data.sex.replace(['Male', 'Female', 'Unknown', 'nan'], ['Male', 'Female', 'Unknown', 'nan'], inplace=True)

        # relabled columns: column 'color'
        #color name substitution
        data['color'].apply(perform_all_color_cleaning)
        # relabled columns: column 'breed'
        data['breed'].apply(get_breed)
        # try loading the datatset and getting an error if not
        try:
            return data
        except:
            return "Data can't be loaded."

# relable the column 'breed'
def get_breed (series: pd.Series) -> pd.Series:
    breed = self.data['breed']

    breed_map = {
        "small": ["pit bull", "chihuahua","terrier", "dachshund", "miniature poodle", "beagle", "miniature schnauzer", "bulldog", "shih tzu", "pug", "australian kelpie", "maltese", "chow chow", "spaniel", "cardigan welsh corgi","miniature pinscher", "chinese sharpei", "queensland heeler", "pomeranian", "lhasa apso"],
        "big": ["retriever", "shepherd", "australian cattle dog", "collie", "hound", "boxer", "catahoula", "siberian husky", "great pyrenees","rottweiler", "pointer", "staffordshire", "black mouth cur", "doberman pinsch", "blue lacy"],
        "short_hair": ["domestic shorthair", "american shorthair", "siamese"],
        "medium_hair": ["domestic medium hair"],
        "long_hair": ["domestic longhair", "siamese"],
        #"uncommon": [???],
    }
    for key, val in breed_map.items():
        series = replace_breeds(val, key, series)
        series = series.map(cleaning)
        # series = series.map(uncommon???)
    return series

    def cleaning(d):
        ## remove whitespaces
        d = d.strip()
        ## lowercasing
        d = d.lower()
        ## remove the word 'mix'-> doesn't work -> data['breed']= data.breed.str.replace('mix', '')
        d = d.replace('mix', '')
        return d

    # def unknown(d):
