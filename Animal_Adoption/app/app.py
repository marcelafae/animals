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

st.markdown('## This is a h2 ##')

st.markdown('This is still need to be pretty. Right now working on functional.')

# This front queries from our API [Animals_API](http://127.0.0.1:8000/predict?vgg_cat_or_dog=%E2%80%98Cat%E2%80%99&vgg_color=%E2%80%98Black%E2%80%99&vgg_breed=%E2%80%99Sheperd%E2%80%99&sex=%E2%80%98Female%E2%80%99&condition=%E2%80%99Normal%E2%80%99&age_animal=2&castraded=%E2%80%98Yes%27')
# '''

st.header('Photo')
st.markdown('Now upload the photo of the new animal')


uploaded_photo = st.file_uploader('here is how ppl can upload a photo')


st.header('Questions')
st.markdown('**Before** pressing submit, make sure you fill all fields below')

with st.form(key='params_for_api'):
    vgg_cat_or_dog=st.selectbox('Is this a cat or a dog?', ['Dog', 'Cat'])
    vgg_color=st.multiselect('Choose the color of this animal. If more than 2 pick only "Tricolor"', ['Black', 'White', 'Brown', 'Beige', 'Tricolor'])
    vgg_breed=st.selectbox('More information about this animal. Pick one', ['Big House Dog', 'Small House Dog', 'Long hair Cat', 'Short Hair Cat'])
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

animals_api_url = 'https://taxifare.lewagon.ai/predict'
response = requests.get(animals_api_url, params=params)

prediction = response.json()

pred = prediction['Days_in_shelter']

st.header(f'Days in Shelter: ${round(pred, 2)}')
