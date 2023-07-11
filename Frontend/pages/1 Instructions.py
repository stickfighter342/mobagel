import streamlit as st

st.title('Instructions')
st.write("To begin using the Machine Learning Helper, select the type of data processing.")

classification, _, regression = st.columns([9, 2, 9])


with classification:
    st.write("### Classification Models")
    st.write("Classification refers to the blah blah blah.")

with regression:
    st.write("### Regression Models")
    st.write("Regression refers to the blah blah blah.")

