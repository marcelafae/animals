import streamlit as st
import numpy as np
import pandas as pd
import requests
import os

curr_path = os.path.dirname(__file__)

with open(os.path.join(curr_path, 'style.css'), encoding='utf-8') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)



# st.markdown(
#     f"""
#     <style>
#         {open("style.css").read()}
#     </style>
#     """,
#     unsafe_allow_html=True
# )


st.title('Animals deserve a home')
st.markdown('## A project to help animal shelters worldwide')

# This front queries from our API [Animals_API](http://127.0.0.1:8000/predict?vgg_cat_or_dog=%E2%80%98Cat%E2%80%99&vgg_color=%E2%80%98Black%E2%80%99&vgg_breed=%E2%80%99Sheperd%E2%80%99&sex=%E2%80%98Female%E2%80%99&condition=%E2%80%99Normal%E2%80%99&age_animal=2&castraded=%E2%80%98Yes%27')
# '''

st.header('Photo')
st.markdown('Now upload the photo of the new animal')

uploaded_photo = st.file_uploader('here is how ppl can upload a photo')


st.header('Questions')
st.markdown('**Before** pressing submit, make sure you fill all fields below')

with st.form(key='params_for_api'):
    vgg_cat_or_dog=st.selectbox('Is this a cat or a dog?', ['Dog', 'Cat'])
    vgg_color=st.multiselect('Choose the color of this animal.', ['Black', 'White', 'Brown', 'Beige','Has Spots', 'Tabby or Brindle' 'Tricolor'])
    st.markdown('**Make sure you only select 1 or 2 colors. If the animal has 3 colors or spots or stripes/pattern, pick just 1 category')
    vgg_breed=st.selectbox('More information about this animal. Pick one', ['Big House Dog', 'Small House Dog', 'Long hair Cat', 'Short Hair Cat', 'Uncommon'])
    sex=st.selectbox('Sex of the animal', ['Male', 'Female'])
    condition=st.selectbox('Animal condition', ['Normal', 'Sick', 'Injured', 'Nursing', 'Pregnant', 'Senior', 'Feral'])
    age_animal=st.number_input('What is the age of this animal? If below 0 years, say 0', min_value=0, max_value=25, step=1, value=1)
    castraded=st.checkbox('This animal has been castrated')


    submitted = st.form_submit_button("Lets see how many days...")


params = dict(
    vgg_cat_or_dog=vgg_cat_or_dog,
    vgg_color=vgg_color,
    vgg_breed=vgg_breed,
    sex=sex,
    condition=condition,
    age_animal=age_animal,
    castraded=castraded)

animals_api_url = 'https://animal-api-gzsqtwobpa-lz.a.run.app/predict'
response = requests.get(animals_api_url, params=params)

prediction = response.json()

pred = prediction['Days_in_shelter']

st.header(f'Days in Shelter: ${round(pred, 2)}')

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
