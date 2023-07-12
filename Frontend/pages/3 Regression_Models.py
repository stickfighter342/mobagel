import streamlit as st

st.title('Regression Models')
st.write('##### Regression analysis is **estimating** the relationship between a predictor variable and a response (observation) variable.')


st.write('##### Examples:')

col1, col2 = st.columns([0.04, 1])

# Display icon image in the first column
icon_path = "house.jpeg"  # Replace with the actual path to your icon image
col1.image(icon_path, width = 20)  # Adjust the width as per your preference

# Display text in the second column
col2.write("###### Price of Houses")
col2.markdown('- House 1: Size: 4500 sq ft, Nearest MRT Station: 550 m, Bedrooms: 3 -> **Price = $725,300**')
col2.markdown('- House 2: Size: 2200 sq ft, Nearest MRT Station: 3.4 km, Bedrooms: 1 -> **Price = $358,000**')

col1, col2 = st.columns([0.04, 1])
icon_path = "email.jpeg"  # Replace with the actual path to your icon image
col1.image(icon_path, width = 20)  # Adjust the width as per your preference
col2.write("###### Email Spam Classification")
col2.markdown('- Email 1: Suspicious Address? = No, Links/Files? = Yes, Suspicious Words? = No -> **Spam = No**')
col2.markdown('- Email 2: Suspicious Address? = Yes, Links/Files? = Yes, Suspicious Words? = Yes -> **Spam = Yes**')

