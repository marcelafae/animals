import streamlit as st
import numpy as np
import pandas as pd



st.title('Animals deserve a home')

st.markdown('## This is a h2 ##')

st.markdown('This is still need to be pretty. Right now working on functional.')

# This front queries from our API [Animals_API](http://127.0.0.1:8000/predict?vgg_cat_or_dog=%E2%80%98Cat%E2%80%99&vgg_color=%E2%80%98Black%E2%80%99&vgg_breed=%E2%80%99Sheperd%E2%80%99&sex=%E2%80%98Female%E2%80%99&condition=%E2%80%99Normal%E2%80%99&age_animal=2&castraded=%E2%80%98Yes%27')
# '''

st.header('Photo')
st.markdown('Now upload the photo of the new animal')



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

uploaded_photo = st.file_uploader('here is how ppl can upload a photo')


st.header('Questions')
st.markdown('**Before** pressing submit, make sure you fill all fields below')

with st.form(key='params_for_api'):
    vgg_cat_or_dog=st.selectbox('Is this a cat or a dog', ['Dog', 'Cat'])
    vgg_color=st.multiselect('Choose the color of this animal. If more than 2 pick only "Tricolor"', ['Black', 'White', 'Brown', 'Beige', 'Tricolor'])
    vgg_breed=st.selectbox('More information about this animal. Pick one', ['Big House Dog', 'Small House Dog', 'Long hair Cat', 'Short Hair Cat'])
    sex=st.selectbox('Sex of the animal', ['Male', 'Female'])
    condition=st.selectbox('Animal condition', ['Normal', 'Sick', 'Injured', 'Nursing', 'Pregnant', 'Senior', 'Feral'])
    age_animal=st.number_input('What is the age of this animal? If below 0 years, say 0', min_value=0, max_value=25, step=1, value=1)
    castraded=st.checkbox('This animal has been castrated')


    submitted = st.form_submit_button("Lets see how many days...")




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
