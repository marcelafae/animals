import streamlit as st
import numpy as np
import pandas as pd
import requests
import os

curr_path = os.path.dirname(__file__)


st.set_page_config(
    page_title = 'Animals deserve a home',
    page_icon = '🐶🐱',
    layout = 'wide', #centered
    initial_sidebar_state = 'auto', # collapsed

)


CSS_dog = """
.block-container {
    background-color: rgba(255, 255, 255, 0.5);
    color: rgba(0, 0, 0, 1);
}
.stApp {
    background-image: url(https://tractive.com/blog/wp-content/uploads/2016/04/puppy-care-guide-for-new-parents.jpg);
    background-size: cover;
}
"""

CSS_cat = """
.block-container {
    background-color: rgba(255, 255, 255, 0.5);
    color: rgba(0, 0, 0, 1);
}
.stApp {
    background-image: url('https://wallpapercave.com/wp/CKJtGTz.jpg');
    background-size: cover;
}
"""

#Title
'''# 🐕🐩 Animals deserve a home 🐈‍⬛🐈'''

#Rest
st.markdown('#### A project to help animal shelters worldwide')

st.write(' ###### By providing some information, our website can assist you in determining how long a dog or cat will stay in your shelter')
st.write('First, you need to specify if the animal is a dog or a cat.')
choose = st.radio('',('','🐩 Dog','🐈 Cat'))

if choose == '':
    pass
elif choose == '🐩 Dog':
    st.write(f'<style>{CSS_dog}</style>', unsafe_allow_html=True)
    animal_type = 'Dog'
elif choose == '🐈 Cat':
    st.write(f'<style>{CSS_cat}</style>', unsafe_allow_html=True)
    animal_type = 'Cat'


#THIS PART NEEDS TO BE 100% AN ACCURATE MATCH W THE MODEL!!!!!!!!!!!!!!!!!!!!!!!!

# Conditions
st.write("### Can you tell me more about how this animal was found?")

col1, col2, col3 = st.columns((2,2,3))

#check the column name and what I wrote here
intake_type = col1.selectbox("Pick one of those options about how this animal ended up in your shelter?",\
    ('Public Assist', 'Owner Surrender', 'Stray', 'Euthanasia Request','Abandoned'))

intake_condition = col2.selectbox("Now plase tell us about this animal health conditions",\
    ('Normal', 'Injured', 'Aged', 'Sick', 'Other', 'Medical', 'Feral', 'Pregnant', 'Nursing', 'Behavior'))



st.write("### The age of this animal in years and months")
col1, col2, col3 = st.columns((1.5,1.5,5))

years = col1.number_input('Years',min_value = 0, max_value = 28,step=1,value=0)

if years == 0:
    months = col2.number_input('Months',min_value = 1, max_value = 11,step=1,value=1)
else:
    months = col2.number_input('Months',min_value = 0, max_value = 11,step=1,value=1)

age_upon_intake_months = years * 12 + months



st.write("### Animal Characteristics")
col1, col2, col3, col4, col5= st.columns((2,1.5,1.5,3,5))



good_with_other_dogs = col1.selectbox("Friendliness with dogs",('1','2', '3', '4', '5'))

color = col2.selectbox("Color or pattern",('Black', 'White', 'Brown', 'Beige','Has Spots', 'Tabby or Brindle', 'Tricolor'))

gender = ("Female", "Male")
options = list(range(len(gender)))
male_or_female_intake = col3.selectbox("Sex", options, format_func=lambda x: gender[x])

if male_or_female_intake == 0:
    spayed = ("Intact", "Spayed")
    options = list(range(len(spayed)))
    neutered_or_spayed_intake = col4.selectbox("Intact, Spayed or Neutered?", options, format_func=lambda x: spayed[x])
else:
    neutered = ("Intact", "Neutered")
    options = list(range(len(neutered)))
    neutered_or_spayed_intake = col5.selectbox("Intact, Spayed or Neutered?", options, format_func=lambda x: neutered[x])


st.write(f"### Please press the button to check if the animal will stay longer than 7 days in the shelter.")

# Prediction

url = 'https://animal-api-gzsqtwobpa-lz.a.run.app/predict'

if st.button('Click here'):
    if choose == '':
        st.warning('You forgot to choose an animal!')
    else: #please make sure this is correct with the model!!!!!
        params = {"intake_type": intake_type,
            "animal_type": animal_type,
            "intake_condition": intake_condition,
            "breed": breed,
            "age_upon_intake_months": age_upon_intake_months,
            "neutered_or_spayed_intake": neutered_or_spayed_intake,
            "male_or_female_intake": male_or_female_intake,
            "color": color
        }

        response = requests.get(url, params=params)
        if response.json()["prediction"] == 0:
            st.success("This animal is likely to stay less than one week in your shelter!")
        else:
            st.info('''
            This animal is likely to stay longer 😿 Here are some things you can try:
            - Take photos and videos of this animal to show their personality;
            - Contact local newspapers, radio stations, and TV channels to see if they are willing to do a feature on the animal;
            - artner with rescue groups;
            - Social media can always be helpful! Make sure to use hashtags to increase reach.
            '''
            )




 #---------
 # TaxiFareModel front

# This front queries the Le Wagon [taxi fare model API](https://taxifare.lewagon.ai/predict?pickup_datetime=2012-10-06%2012:10:20&pickup_longitude=40.7614327&pickup_latitude=-73.9798156&dropoff_longitude=40.6513111&dropoff_latitude=-73.8803331&passenger_count=2)
# '''

# with st.form(key='params_for_api'):

#     pickup_date = st.date_input('pickup datetime', value=datetime.datetime(2012, 10, 6, 12, 10, 20))
#     pickup_time = st.time_input('pickup datetime', value=datetime.datetime(2012, 10, 6, 12, 10, 20))
#     pickup_datetime = f'{pickup_date} {pickup_time}'
#     pickup_longitude = st.number_input('pickup longitude', value=40.7614327)
#     pickup_latitude = st.number_input('pickup latitude', value=-73.9798156)
#     dropoff_longitude = st.number_input('dropoff longitude', value=40.6413111)
#     dropoff_latitude = st.number_input('dropoff latitude', value=-73.7803331)
#     passenger_count = st.number_input('passenger_count', min_value=1, max_value=8, step=1, value=1)

#     st.form_submit_button('Make prediction')

# params = dict(
#     pickup_datetime=pickup_datetime,
#     pickup_longitude=pickup_longitude,
#     pickup_latitude=pickup_latitude,
#     dropoff_longitude=dropoff_longitude,
#     dropoff_latitude=dropoff_latitude,
#     passenger_count=passenger_count)

# wagon_cab_api_url = 'https://taxifare.lewagon.ai/predict'
# response = requests.get(wagon_cab_api_url, params=params)

# prediction = response.json()

# pred = prediction['fare']

# st.header(f'Fare amount: ${round(pred, 2)}')
