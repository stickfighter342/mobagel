import streamlit as st

def main():
    st.title("Machine Learning Helper")
    st.write("##### Welcome to the Machine Learning Helper homepage! We make machine learning fast and easy for you.")
    st.write("Simply submit your data file, and leave the nitty-gritty coding to us!")
    container = st.container()

    # Content within the container
    with container:
        st.header("Container")
        st.text("This is inside the container")
        st.button("Button inside the container")

    # Create an expander
    expander = st.expander("Expander")

    # Content within the expander
    with expander:
        st.text("This is inside the expander")
        st.checkbox("Checkbox inside the expander")

if __name__ == '__main__':
    main()
