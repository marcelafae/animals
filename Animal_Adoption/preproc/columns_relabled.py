import pandas as pd

#relabled column 'breed' into column 'breed_2class' with values 'mixed' and 'non mixed'
def breed_2classes(df, column_name):
    breeds = []
    for breed in df.loc[:,column_name]:
        if 'Mix' in breed or '/' in breed or 'Domestic' in breed:
            breeds.append('mixed')
        else:
            breeds.append('not mixed')
    df['breed_2classes'] = breeds
    return df


# relable the colum 'outcome_type' into column 'outcome_type_2classes' with values 'adopted' and 'not adopted'   
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
    return df

# relable the colum 'intake_condition' into column 'intake_condition_2classes' with values 'normal' and 'not normal'
def intake_condition_2classes(df,col):
    normal_dict = {'Normal': 'normal', 'Injured': 'not normal', 'Sick': 'not normal', 'Nursing': 'not normal', 'Aged': 'not normal', 'Other': 'not normal', 'Feral': 'not normal'}
    df['intake_condition_2classes'] = df[col].map(normal_dict)
    return df

# relable the colum 'color' into column 'color_3classes' with values 'monocolor', 'bicolor' and 'tricolor'
def color_3classes (df, column_name):
    classes3= []
    for value in df[column_name]:
        if '/' in value:
            classes3.append('Bicolor')
        elif 'Tricolor' in value or 'Calico' in value or 'Torbie' in value or 'Tortie' in value:
            classes3.append('Tricolor')
        else: 
            classes3.append('Monocolor') 
    df['color_3classes'] = classes3    
    return df