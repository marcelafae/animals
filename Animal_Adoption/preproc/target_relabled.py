import pandas as pd

def breed_2class(df, column_name):
    breeds = []
    for breed in df.loc[:,column_name]:
        if 'Mix' in breed or '/' in breed or 'Domestic' in breed:
            breeds.append('mixed')
        else:
            breeds.append('non_mixed')
    df['breed_mix_nonmix'] = breeds
    return df.reset_index(drop=True)

# new name!!!
def time_in_shelter_days_round_5classes(df, column_name):
    classes_5= []
    for value in df.loc[:, column_name]:
        if 0 <= value < 1:
            classes_5.append('several hours')
        elif 1 <= value <=5: 
            classes_5.append('between 1 and 5 days')
        elif 5< value <= 10:
            classes_5.append('between 6 and 10 days')
        elif 10 < value <= 15:
            classes_5.append('between 11 and 15 days')
        elif 15 < value <= 20:
            classes_5.append('between 16 and 20 days')
        elif 20 < value <=25:
            classes_5.append('between 21 and 25 days')
        elif 25 < value <= 30:
            classes_5.append('between 26 and 30 days')
        else:
            classes_5.append('higher than 30 days')
    df['time_in_shelter_days_round_5classes']= classes_5
    return df.reset_index(drop=True)

# new_name!!!
def time_in_shelter_days_round_2classes(df, column_name):
    classes_2= []
    for value in df.loc[:, column_name]:
        if value <=7:
            classes_2.append('one week')
        else:
            classes_2.append('more than one week')
    df['time_in_shelter_days_round_2classes']=classes_2
    return df.reset_index(drop=True)



# relable the colum 'outcome_type' into two classes 'adopted' or 'not adopted'   
def outcome_type_2classes(df, column_name):
    classes_2= []
    for value in df.loc[:, column_name]:
        if value == 'Return to Owner':
            classes_2.append('not adopted')
        elif value == 'Transfer': 
            classes_2.append('adopted')
        elif value == 'Adoption':
            classes_2.append('adopted')
        elif value == 'Euthanasia':
            classes_2.append('not adopted')
        elif value == 'Died':
            classes_2.append('not adopted')
        elif value == 'Rto-Adopt':
            classes_2.append('adopted')
        elif value == 'Missing':
            classes_2.append('not adopted')
        else:
            classes_2.append('not adopted')
    df['outcome_type_2classes']= classes_2
    return df.reset_index(drop=True)