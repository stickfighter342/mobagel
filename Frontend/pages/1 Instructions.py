import streamlit as st

st.title('Instructions')
st.write("To begin using the Machine Learning Helper, select the type of data processing.")

classification, _, regression = st.columns([9, 1, 9])


with classification:
    goto_classification = st.button("#### Classification Models")

    

with regression:
    st.button("#### Regression Models")
    

