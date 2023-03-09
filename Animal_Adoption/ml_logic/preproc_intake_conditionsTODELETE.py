import pandas as pd


#functions to fix the age dtype from srt to floats and transform all the formats to years
def fix_age(x: str)  -> float:

    x1=x.split(' ')
    if 'year' in x1[1]:
        return float(x1[0])

    elif 'month' in x1[1]:
        x1[0] = int(x1[0])/12
        return float(x1[0])

    elif 'week' in x1[1]:
        x1[0] = int(x1[0])/52
        return float(x1[0])

    else:
        x1[0] = int(x1[0])/365
        return float(x1[0])


#drop all animals under 8 considered AGED on the normal df

def drop_under_8_aged(df: pd.DataFrame)  -> pd.DataFrame:

    condition_1 = df['age_upon_intake'] > 8
    condition_2 = df['intake_condition'] != 'Aged'
    new_df = df[(condition_1) & (condition_2)]
    return new_df
