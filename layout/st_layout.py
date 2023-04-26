import streamlit as st

def generate_layout():    
    tab_1, tab_2 = st.tabs(["Elastic Stress", "Elastic Stability"])
    with tab_1:
        container_1=st.container()
        with container_1:
            col_1, col_2 = st.columns(2)
            with col_1:
                st.write("i am here")
            with col_2:
                st.write("i am here 2")
            exp_1=st.expander("Handcalc")
            with exp_1:
                st.write("Testicicle 1")

    with tab_2:
        container_2=st.container()
        with container_2:
            col_3, col_4 = st.columns(2)
            with col_3:
                st.write("i am here 3")
            with col_4:
                st.write("i am here 4")
            exp_2=st.expander("Handcalc")
            with exp_2:
                st.write("Testicicles 2")

# number_input_list={"length":"Vessel Length","diameter":"Vessel Diameter","thickness":"Vessel Wall Thickness"}
