import os
import pandas as pd


class Animals:
    def get_data(self):
        """
        Its values should be pandas.DataFrames loaded from csv files
        """
        # load the dataset
        file_path= 'code/JeanneDuPre/project/data/aac_intakes_outcomes.csv'
        data= pd.read_csv(file_path, delimiter= ",")
        # cwd = os.getcwd()  # Get the current working directory (cwd)
        # files = os.listdir(cwd)  # Get all the files in that directory
        # print("Files in %r: %s" % (cwd, files))
        
        
        # root_dir = os.path.dirname(os.path.dirname(__file__))
        # csv_path = os.path.join(root_dir, "data", "csv")
        # # data= pd.read_csv(os.path.join(csv_path))

        # file_names = [f for f in os.listdir(csv_path) if f.endswith(".csv")]
        # for f in file_names:
        #     data= pd.read_csv(os.path.join(csv_path),f)
        # key_names = [
        #     key_name.replace("aac_", "").replace("_dataset", "").replace(".csv", "")
        #     for key_name in file_names
        # ]

        # # Create the dictionary
        # data = {}
        # for k, f in zip(key_names, file_names):
        #     data[k] = pd.read_csv(os.path.join(csv_path, f))
        
        # Drop duplicates in place
        data.drop_duplicates(inplace=True)
        
        # convert several columns in another type
        data['date_of_birth'] = pd.to_datetime(data['date_of_birth'])
        data['outcome_datetime'] = pd.to_datetime(data['outcome_datetime'])
        data['intake_datetime'] = pd.to_datetime(data['intake_datetime'])
        data["sex_upon_outcome"] = data.sex_upon_outcome.astype(str)
    
        # drop columns (meaningless, missing values or correlated to another column)
        data.drop(['outcome_subtype', 'outcome_number', 'found_location', 'intake_type', 'time_in_shelter', 'time_in_shelter_days', 'age_upon_outcome_age_group', 'age_upon_intake_age_group', 'dob_year', 'dob_month', 'dob_monthyear'], axis=1, inplace= True)
        
        # drop the values 'Bird' and 'Other' in the column 'animal_type'
        data.drop(data[data['animal_type'] == 'Bird'].index, inplace = True)
        data.drop(data[data['animal_type'] == 'Other'].index, inplace = True)
        
        # drop the animal_id_outcome, that appears more than once in the column '???'
        data.drop_duplicates(subset=["animal_id_outcome"], keep="first", inplace=True)
        data[data["animal_id_outcome"].duplicated()]["animal_id_outcome"].unique()
        
        # relabled colums: split the column 'sex_upon_outcome' into a column 'sex' and a column 'sex_type' 
        data['sex_type']= data.sex_upon_outcome.apply(lambda x : x.split(" ")[0])
        data['sex']= data.sex_upon_outcome.apply(lambda x : x.split(" ")[-1])
        # relabel the values of the new column 'sex' to value 'Neutered' and value 'Intact' and value 'NaN'(unknown)
        data.sex_type.replace(['Neutered', 'Spayed', 'Intact', 'Unknown'], ['Neutered', 'Neutered', 'Intact', 'NaN'], inplace=True)
        data.sex.replace(['Male', 'Female', 'Unknown', 'nan'], ['Male', 'Female', 'nan', 'nan'], inplace=True)
        
        # relabled columns: column 'color'
        
        # relabled columns: column 'breed'
        
        # try loading the datatset and getting an error if not
        try:
            return data
        except: 
            return "Data can't be loaded."
        
    # def get_training_data(self):
        # please copy the training_data
    