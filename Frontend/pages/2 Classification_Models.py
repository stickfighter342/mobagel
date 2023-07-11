import streamlit as st
import requests

st.title('Classification Models')
st.write('#### Statistical classification is **identifying**, out of a list of classifications, which one an observation belongs to.')


st.subheader('Examples:')

col1, col2 = st.columns([0.04, 1])

# Display icon image in the first column
icon_path = "person.jpeg"  # Replace with the actual path to your icon image
col1.image(icon_path, width = 20)  # Adjust the width as per your preference

# Display text in the second column
col2.write("###### Age Group Classification")
col2.markdown('- Josh: Sex = Male, Height = 185 cm, Weight = 85 kg, Ethnicity: White -> **Age = 18 - 21 years old**')
col2.markdown('- Alice: Sex = Female, Height = 158 cm, Weight = 52 kg, Ethnicity: Asian -> **Age = 13 - 17 years old**')

col1, col2 = st.columns([0.04, 1])
icon_path = "email.jpeg"  # Replace with the actual path to your icon image
col1.image(icon_path, width = 20)  # Adjust the width as per your preference
col2.write("###### Email Spam Classification")
col2.markdown('- Email 1: Suspicious Address? = No, Links/Files? = Yes, Suspicious Words? = No -> **Spam = No**')
col2.markdown('- Email 2: Suspicious Address? = Yes, Links/Files? = Yes, Suspicious Words? = Yes -> **Spam = Yes**')





