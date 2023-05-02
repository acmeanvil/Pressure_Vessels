"""
Copyright 2023 Acmeanvil

Use of this source code is governed by an MIT-style
license that can be found in the LICENSE file or at
https://opensource.org/licenses/MIT.

A variety of pressure vessel related functions
assumptions:
    -vessel is cylindrical with capped ends and is a fully closed volume
    -uniform external pressure on all surface
"""

import streamlit as st
import materials.materials as mt
import pressure_vessel.ext_presure_vessel_functions as epv
import pressure_vessel.vessel as vsl
import layout.st_layout as stl
import layout.figures as fgs
import plotly.graph_objects as go
import pandas as pd


st.markdown("<h1 style='text-align: center; color: gray;'>Pressure Vessel Design</h1>", unsafe_allow_html=True)

#import material choices from csv and convert each to a material class object
matl_table=mt.import_matl_table("material_table.csv")
#create a material category list (this is for the future to allow for generic categories
#such as "metal", "ceramic", "GFRP/CFRP", etc., etc.)
matl_category=mt.generate_matl_category_index(matl_table)
#create list of material types within a category ie "aluminum", "steel", "stainles steel, etc."
matl_type=mt.generate_matl_type_index(matl_table)

df_mt=pd.read_csv("material_table.csv")

#set flags for switching between plot based on pressure or depth
depth_switch=True
pressure_switch=False
#streamlit layout for 2x tabs each with 2x columns, 4x output boxes and an expander
container_1=st.container()
with container_1:
    col_1, col_2 = st.columns(2)        
    with col_1:
        depth_switch=st.button("Depth", use_container_width=True, type="primary")
    with col_2:
        pressure_switch=st.button("Pressure", use_container_width=True, type="primary")


#setup selection box
category_selection=st.sidebar.selectbox("Material Category", matl_category)
#setup selection box
type_selection=st.sidebar.selectbox("Material Type", matl_type)

#create list of available materials that fall into the selected category and type
matl_index=mt.generate_matl_index(matl_table, type_selection)
#setup selection box
matl_selection=st.sidebar.selectbox("Material", matl_index)

#setup selection number input boxes for the primary inputs
length_choice=st.sidebar.number_input("Vessel Length (in)", min_value=1.0)
diameter_choice=st.sidebar.number_input("Vessel Diameter (in)", min_value=1.0)
thickness_choice=st.sidebar.number_input("Vessel Wall Thickness (in)", min_value=0.01)
percent_choice=st.sidebar.number_input("Percent of wall Thickness (%) (for thick walled vessels oly, 100%=OD 0%=ID)", min_value=1)

depth_choice=st.sidebar.number_input("Vessel Depth Rating (ft)", min_value=100)
pressure_max=epv.depth_to_pressure(depth_choice)
st.sidebar.info(f"Pressure = {round(pressure_max,1)} psi")

#create aan empty material object and assign the selected material object to it  
vessel_matl=mt.material()
for matl in matl_table:
    if matl.matl_label==matl_selection:
        vessel_matl.assign_matl(matl)

#create a pressure vessel class object and all particulars
vessel_1=vsl.vessel(matl_label="Vessel 1", matl=vessel_matl, length=length_choice, diameter=diameter_choice, wall_thickness=thickness_choice)
thickness_ratio=vessel_1.thickness_ratio()["ratio"]
thickness_type=vessel_1.thickness_ratio()["type"]
length_ratio=vessel_1.length_ratio()

#calc maximum values and get the Handcalcs rendered versions
hs_latex_max, hs_value_max=epv.thin_hoop_stress(vessel_1, pressure_max)
ls_latex_max, ls_value_max=epv.thin_longitudinal_stress(vessel_1, pressure_max)

hs_tk_latex_max, hs_tk_value_max=epv.thick_hoop_stress(vessel_1, pressure_max, percent_choice)
ls_tk_latex_max, ls_tk_value_max=epv.thick_longitudinal_stress(vessel_1, pressure_max)

#put together figures required for display
figures=fgs.thin_display_hoop_and_long_figures(vessel_1, depth_choice)
figures_tk=fgs.thick_display_hoop_and_long_figures(vessel_1, depth_choice, percent_choice)

#diameter and length reductions at max pressure
dia_reduc_latex, dia_reduc=epv.thin_diameter_reduction(vessel_1,  epv.depth_to_pressure(depth_choice))
length_reduc_latex, length_reduc=epv.thin_length_reduction(vessel_1, epv.depth_to_pressure(depth_choice))

tk_dia_reduc_latex, tk_dia_reduc=epv.thick_outer_diameter_reduction(vessel_1,  epv.depth_to_pressure(depth_choice))
tk_length_reduc_latex, tk_length_reduc=epv.thick_length_reduction(vessel_1, epv.depth_to_pressure(depth_choice))

#build the main page with two tabs each with two columns
tab_1, tab_2, tab_3= st.tabs(["Elastic Stress", "Elastic Stability", "Materials"])
with tab_1:
    container_2=st.container()
    with container_2:
        col_3, col_4 = st.columns(2)
        with col_3:
            if thickness_ratio>=10:
                if depth_switch==True:
                    st.plotly_chart(figures["fig_hs_d"], use_container_width=True)
                else:
                    st.plotly_chart(figures["fig_hs_p"], use_container_width=True)
                st.info(f"Max Hoop Stress = {round(hs_value_max,0)} psi")
            elif thickness_ratio<10:
                if depth_switch==True:
                    st.plotly_chart(figures_tk["fig_tk_hs_d"], use_container_width=True)
                else:
                    st.plotly_chart(figures_tk["fig_tk_hs_p"], use_container_width=True)
                st.info(f"Max Hoop Stress = {round(hs_tk_value_max,0)} psi")                
            exp_1=st.expander("Expanded Hoop Stress Calculations")
            if thickness_ratio>=10:
                with exp_1:
                    st.latex(hs_latex_max)
                st.info(f"Diameter Reduction = {round(dia_reduc,4)} in")
            elif thickness_ratio<10:
                with exp_1:
                    st.latex(hs_tk_latex_max)
                st.info(f"Diameter Reduction = {round(tk_dia_reduc,4)} in")               
            exp_2=st.expander("Expanded Diameter Reduction Calculations")
            with exp_2:
                if thickness_ratio>=10:
                    st.latex(dia_reduc_latex)
                elif thickness_ratio<10:
                    st.latex(tk_dia_reduc_latex)
            st.info(f"Thickness Ratio (R/t) = {round(thickness_ratio,3)}  (Pressure Vesssl is {thickness_type})")
        
        with col_4:
            if thickness_ratio>=10:
                if depth_switch==True:
                    st.plotly_chart(figures["fig_ls_d"], use_container_width=True)
                else:
                    st.plotly_chart(figures["fig_ls_p"], use_container_width=True)
                st.info(f"Max Longitudinal Stress = {round(ls_value_max,0)} psi")
            elif thickness_ratio<10:
                if depth_switch==True:
                    st.plotly_chart(figures_tk["fig_tk_ls_d"], use_container_width=True)
                else:
                    st.plotly_chart(figures_tk["fig_tk_ls_p"], use_container_width=True)
                st.info(f"Max Longitudinal Stress = {round(ls_tk_value_max,0)} psi")
            exp_3=st.expander("Expanded Longitudional Stress Calculations")
            if thickness_ratio>=10:
                with exp_3:
                    st.latex(ls_latex_max)
                st.info(f"Length Reduction = {round(length_reduc,4)} in")
            elif thickness_ratio<10:
                with exp_3:
                    st.latex(ls_tk_latex_max)
                st.info(f"Length Reduction = {round(tk_length_reduc,4)} in")
            exp_4=st.expander("Expanded Length Reduction Calculations")
            with exp_4:
                if thickness_ratio>=10:
                    st.latex(length_reduc_latex)
                elif thickness_ratio<10:
                    st.latex(tk_length_reduc_latex)
            st.info(f"Length to Thickness Ratio (L/t) = {round(length_ratio,3)}")
with tab_2:
    container_3=st.container()
    with container_3:
        col_5, col_6 = st.columns(2)
        with col_5:
             st.write()
        with col_6:
             st.write()
        exp_5=st.expander("Handcalc")
        with exp_5:
            st.write("")

with tab_3:
    container_4=st.container()
    with container_4:
        st.markdown("<h2 style='text-align: center; color: white;'>Available Materials</h2>", unsafe_allow_html=True)
        st.dataframe(df_mt, use_container_width=True)