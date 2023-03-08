import streamlit as st
import numpy as np
import pandas as pd



st.title('Animals deserve a home')
st.title('This is where we add some description of the project (title)')

st.markdown('# This is a h1 #')
st.markdown('## This is a h2 ##')

st.markdown('markdown to separate the fields and I can use **bold by adding 2 stars around the text**')

st.header('Photo')
st.markdown('Now upload the photo of the new animal')

uploaded_photo = st.file_uploader('here is how ppl can upload a photo')
#uploaded_csv = st.file_uploader('here is where ppl can also upload their csv')
#if uploaded_csv:
    # st.header('This is a csv')
    # df = pd.read_csv(uploaded_csv)
    # st.write(df.describe())

st.header('Questions')
st.markdown('**Before** pressing submit, make sure you fill all fields below')


st.selectbox('Male or Female', ['Male', 'Female'])
st.multiselect('Condition', ['Normal', 'Sick', 'Injured', 'Nursing', 'Pregnant', 'Senior', 'Feral'])
st.number_input('Please add the age in years', 0, 25)
st.selectbox('Is this animal castrated?', ['Yes', 'No'])

st.button('Click me to see how many days')
