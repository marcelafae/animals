import streamlit as st
import requests
import os
import pickle
import pandas as pd

curr_path = os.path.dirname(__file__)


st.set_page_config(
    page_title = 'Animals deserve a home',
    page_icon = '🐶🐱',
    layout = 'wide', #centered
    initial_sidebar_state = 'auto', # collapsed
    )

CSS_hero = """
.block-container {
    background-color: rgba(253,252,245, 0.4);
    color: rgba(0, 0, 0, 1);
}
.stApp {
    background-image: url('https://www.vmamodesto.com/images/page-heroes/hero-puppykitten.jpg');
    background-size: cover;
}
"""

CSS_dog = """
.block-container {
    background-color: rgba(253,252,245, 0.4);
    color: rgba(0, 0, 0, 1);
}
.stApp {
    background-image: url('https://wallpapercave.com/uwp/uwp1908294.jpeg');
    background-size: cover;
}
"""

CSS_cat = """
.block-container {
    background-color: rgba(253,252,245, 0.4);
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


st.write('### First, you need to specify if the animal is a dog or a cat.')
choose = st.radio('',('🐩 Dog','🐈 Cat'))
if choose == '':
    st.write(f'<style>{CSS_hero}</style>', unsafe_allow_html=True)
    animal_type = ''
elif choose == '🐩 Dog':
    st.write(f'<style>{CSS_dog}</style>', unsafe_allow_html=True)
    animal_type = 'Dog'
elif choose == '🐈 Cat':
    st.write(f'<style>{CSS_cat}</style>', unsafe_allow_html=True)
    animal_type = 'Cat'


#THIS PART NEEDS TO BE 100% AN ACCURATE MATCH W THE MODEL!!!!!!!!!!!!!!!!!!!!!!!!

# Conditions
#st.write("### Can you tell me more about how this animal was found?")

#col1, col2, col3 = st.columns((2,2,3))

#check the column name and what I wrote here
# intake_type = col1.selectbox("Pick one of those options about how this animal ended up in your shelter?",\
#     ('Public Assist', 'Owner Surrender', 'Stray', 'Euthanasia Request','Abandoned'))


st.write("### How old is this animal and what does it look like?")
col1, col2, col3, col4 = st.columns((1,1,1.5,2))

years = col1.number_input('Years',min_value = 0, max_value = 28,step=1,value=0)

if years == 0:
    months = col2.number_input('Months',min_value = 1, max_value = 11,step=1,value=1)
else:
    months = col2.number_input('Months',min_value = 0, max_value = 11,step=1,value=1)

age_upon_intake_years = years+ months/12
color = col3.selectbox("Color or pattern",('Black', 'White', 'Brown', 'Beige','Has Spots', 'Tabby or Brindle', 'Tricolor'))

if animal_type == 'Dog':
    root_dir = os.path.dirname(os.path.dirname(__file__))
    breed_path = os.path.join(root_dir, "breeds.csv")
    breed_tuple = pd.read_csv(os.path.join(breed_path), index_col=0).index
    breed = col4.selectbox("Breed", breed_tuple)
else:
    breed = "Domestic Shorthair Mix"




st.write("### General Characteristics")
col1, col2, col3= st.columns((1,1,1))
#good_with_other_dogs = col1.selectbox("Friendliness with dogs",('1','2', '3', '4', '5'))


intake_condition = col1.selectbox("Animal's condition",\
    ('Normal', 'Injured', 'Aged', 'Sick', 'Other', 'Medical', 'Feral', 'Pregnant', 'Nursing', 'Behavior'))

gender = ("Female", "Male")
options = list(range(len(gender)))
male_or_female_intake = col2.selectbox("Sex", options, format_func=lambda x: gender[x])

if male_or_female_intake == 0:
    spayed = ("Intact", "Spayed")
    options = list(range(len(spayed)))
    neutered_or_spayed_intake = col3.selectbox("Intact, Spayed or Neutered?", options, format_func=lambda x: spayed[x])
else:
    neutered = ("Intact", "Neutered")
    options = list(range(len(neutered)))
    neutered_or_spayed_intake = col3.selectbox("Intact, Spayed or Neutered?", options, format_func=lambda x: neutered[x])




st.write(f"### Please press the button to check how long this animal will need to wait to find a home.")

# Prediction

url = 'https://animal-api-gzsqtwobpa-lz.a.run.app/predict'
url_local = "http://127.0.0.1:8000/predict"
if st.button('Click here'):
    if choose == '':
        st.warning("No, no, no. You need to pick 'Dog' or 'Cat'")
    else: #please make sure this is correct with the model!!!!!
        params = {
            "age_upon_intake_y": age_upon_intake_years,
            "animal_type": animal_type,
            "intake_condition": intake_condition,
            "breed": breed,
            "sex": male_or_female_intake,
            "sex_type": neutered_or_spayed_intake,
            "color": color
        }

        response = requests.get(url, params=params)
        # st.write(response)
        # st.write(response.json())
        days = round(response.json()['days_in_shelter'], 1)
        st.balloons()

        st.write(f'# The animal will stay around {days} days')
        # if response.json()['days_in_shelter'] == 0:
        #     st.success("This animal is likely to stay less than one week in your shelter!")
        # else:
        #     st.info('''
        #     This animal is likely to stay longer 😿 Here are some things you can try:
        #     - Take photos and videos of this animal to show their personality;
        #     - Contact local newspapers, radio stations, and TV channels to see if they are willing to do a feature on the animal;
        #     - artner with rescue groups;
        #     - Social media can always be helpful! Make sure to use hashtags to increase reach.
        #     '''
        #     )
