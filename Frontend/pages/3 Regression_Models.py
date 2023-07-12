import streamlit as st
import requests


API_URL = 'http://localhost:8000'

response =  requests.get(API_URL + "/login")
if response.status_code == 200:
    data = response.json()
    st.write(data["message"])
else:
    st.error("Failed to fetch data from the API.")


st.title('Regression Models')
st.write('##### **Estimating** the relationship between a predictor variable and a response (observation) variable.')

expander = st.expander('Details of Regression Models')

with expander:
    st.write('In regression analysis, we try and find a relationship between X (predictor) and Y (response) that minimizes a scale of the amount of error, i.e. the discrepancy between the predicted relationship and the given observed relationship.')
    st.write('In most regression models, this scale is called the mean squared error (MSE), defined as')
    st.latex(r'\text{MSE} = \sum_i (\text{obs} - \text{pred})^2 = \sum_i (Y_i - \hat Y_i)^2')
    st.write('where **obs** $$= Y_i$$ represents your observation, and **pred** $$= \hat Y_i$$ represents your prediction based on the predictor variables.')
    st.write("To obtain the estimates $$\\hat Y_i$$, we define a relationship function $$f(X_i, \\beta) = \\hat Y_i$$. The goal is to be able to find $$\\beta$$ such that the MSE is minimized. In other words,")
    st.latex(r'\text{find} \ \beta \ \text{such that} \ \beta = \arg \min_{\beta} \ \text{MSE} = \arg \min_{\beta} \ \sum_i (Y_i - f(X_i, \beta))^2.')

expander2 = st.expander("Click Here to View Examples")

# Content within the expander
with expander2:
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



st.subheader('Create Your Own Classification Model Here!')
X_train = st.file_uploader('Insert Predictor Data')
y_train = st.file_uploader('Insert Response Data')



