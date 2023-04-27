import streamlit as st
import materials.materials as mt
import pressure_vessel.ext_presure_vessel_functions as epv
import pressure_vessel.vessel as vsl
import layout.st_layout as stl
import plotly.graph_objects as go
from plotly.subplots import make_subplots as msp
import numpy as np

st.markdown("<h1 style='text-align: center; color: white;'>Pressure Vessel Design</h1>", unsafe_allow_html=True)

#import material choices from csv and convert each to a material class object
matl_table=mt.import_matl_table("material_table.csv")

#create a material category list (this is for the future to allow for generic categories
# such as "metal", "ceramic", "GFRP/CFRP", etc., etc.)
matl_category=mt.generate_matl_category_index(matl_table)
#setup selection box
category_selection=st.sidebar.selectbox("Material Category", matl_category)

#create list of material types within a category ie "aluminum", "steel", "stainles steel, etc."
matl_type=mt.generate_matl_type_index(matl_table)
#setup selection box
type_selection=st.sidebar.selectbox("Material Type", matl_type)

#create list of available materials that fall into the selected category and type
matl_index=mt.generate_matl_index(matl_table, type_selection)
#setup selection box
matl_selection=st.sidebar.selectbox("Material", matl_index)

#setup selection number input boxes for the primary inputs
length_choice=st.sidebar.number_input("Vessel Length", min_value=0.01)
diameter_choice=st.sidebar.number_input("Vessel Diameter", min_value=0.01)
thickness_choice=st.sidebar.number_input("Vessel Wall Thickness", min_value=0.01)
depth_choice=st.sidebar.number_input("Vessel Depth Rating", min_value=10)
#debug
# st.write("Material=",matl_selection)
# st.write("Length=",length_choice)
# st.write("Diameter=",diameter_choice)
# st.write("Wall Thickness=",thickness_choice)

#create aan empty material object and assign the selected material object to it  
vessel_matl=mt.material()
for matl in matl_table:
    if matl.matl_label==matl_selection:
        vessel_matl.assign_matl(matl)

#create a pressure vessel class object 
vessel_1=vsl.vessel(matl_label="Vessel 1", matl=vessel_matl, length=length_choice, diameter=diameter_choice, wall_thickness=thickness_choice)
pressure=epv.depth_to_pressure(depth_choice)

#create lists for X and Y values for plots
depth_values = list(range(1, int(round(depth_choice+1,0)), int(round((depth_choice+1)/15,0))))

pressure_values=[]
for depth in depth_values:
    pressure_values.append(epv.depth_to_pressure(depth))

hoop_stress_values=[]
for pressure in pressure_values:
    hs_latex, hs_value=epv.thin_hoop_stress(vessel_1, pressure)
    hoop_stress_values.append(hs_value)
hs_latex, hs_value=epv.thin_hoop_stress(vessel_1, max(pressure_values))

long_stress_values=[]
for pressure in pressure_values:
    ls_latex, ls_value=epv.thin_longitudinal_stress(vessel_1, pressure)
    long_stress_values.append(ls_value)
ls_latex, ls_value=epv.thin_longitudinal_stress(vessel_1, max(pressure_values))

#create plots for hoop and longitudinal stress vs depth and pressure
fig_hs_d = go.Figure()
fig_hs_p = go.Figure()

fig_ls_d = go.Figure()
fig_ls_p = go.Figure()

#hoop stress vs depth
fig_hs_d.add_trace(
    go.Scatter(
        name="Hoop Stress",
        x=depth_values,
        y=hoop_stress_values,
        fill="tonexty")
)
#graph a line at vessel material yield stress
fig_hs_d.add_trace(
    go.Scatter(
        name="Yield Stress",
        x=[0, depth_choice],
        y=[vessel_1.matl.fy, vessel_1.matl.fy],
        fill="tonexty")
)

#pretty up hoop stress vs depth plot
fig_hs_d.update_layout(title_text="<b>Hoop Stress at Depth<b>", title_x=0.35, font_size=32)
fig_hs_d.update_xaxes(title=dict(text="<b>Depth (ft)<b>",font=dict(size=14)), range=[0, max(depth_values)*1.02] ,title_standoff = 20)
fig_hs_d.update_yaxes(title=dict(text="<b>Hoop Stress (psi)<b>",font=dict(size=14)), title_standoff = 20)
fig_hs_d.update_layout(legend=dict( yanchor="top", y=0.90, xanchor="left", x=0.01))

#hoop stress vs pressure
fig_hs_p.add_trace(
    go.Scatter(
        name="Hoop Stress",
        x=pressure_values,
        y=hoop_stress_values,
        fill="tonexty")
)
#graph a line at vessel material yield stress
fig_hs_p.add_trace(
    go.Scatter(
        name="Yield Stress",
        x=[0, max(pressure_values)],
        y=[vessel_1.matl.fy, vessel_1.matl.fy],
        fill="tonexty")
)
#pretty up hoop stress vs pressure plot
fig_hs_p.update_layout(title_text="<b>Hoop Stress at Pressure<b>", title_x=0.35, font_size=32)
fig_hs_p.update_xaxes(title=dict(text="<b>Pressure (psi)<b>",font=dict(size=14)), range=[0, max(pressure_values)*1.02], title_standoff = 20)
fig_hs_p.update_yaxes(title=dict(text="<b>Hoop Stress (psi)<b>",font=dict(size=14)), title_standoff = 20)
fig_hs_p.update_layout(legend=dict( yanchor="top", y=0.90, xanchor="left", x=0.01))

#longitudinal stress vs depth
fig_ls_d.add_trace(
    go.Scatter(
        name="Longitudinal Stress",
        x=depth_values,
        y=long_stress_values,
        fill="tonexty")
)
#graph a line at vessel material yield stress
fig_ls_d.add_trace(
    go.Scatter(
        name="Yield Stress",
        x=[0, max(depth_values)],
        y=[vessel_1.matl.fy, vessel_1.matl.fy],
        fill="tonexty")
)
#pretty up longitudinal stress vs depth plot
fig_ls_d.update_layout(title_text="<b>Longituduinal Stress at Depth<b>", title_x=0.25, font_size=20)
fig_ls_d.update_xaxes(title=dict(text="<b>Depth (ft)<b>",font=dict(size=14)), range=[0, max(depth_values)*1.02], title_standoff = 20)
fig_ls_d.update_yaxes(title=dict(text="<b>Longitudinal Stress (psi)<b>",font=dict(size=14)), title_standoff = 20)
fig_ls_d.update_layout(legend=dict( yanchor="top", y=0.90, xanchor="left", x=0.01))

#longitudinal stress vs pressure
fig_ls_p.add_trace(
    go.Scatter(
        name="Longitudinal Stress",
        x=pressure_values,
        y=long_stress_values,
        fill="tonexty")
)
#graph a line at vessel material yield stress
fig_ls_p.add_trace(
    go.Scatter(
        name="Yield Stress",
        x=[0, max(pressure_values)],
        y=[vessel_1.matl.fy, vessel_1.matl.fy],
        fill="tonexty")
)
#pretty up longitudinal stress vs pressure plot
fig_ls_p.update_layout(title_text="<b>Longitudinal Stress at Pressure<b>", title_x=0.25, font_size=14)
fig_ls_p.update_xaxes(title=dict(text="<b>Pressure (psi)<b>",font=dict(size=14)), range=[0, max(pressure_values)*1.02], title_standoff = 20)
fig_ls_p.update_yaxes(title=dict(text="<b>Longitudinal Stress (psi)<b>",font=dict(size=14)), title_standoff = 20)
fig_ls_p.update_layout(legend=dict( yanchor="top", y=0.90, xanchor="left", x=0.01))

#set flags for switching between plot based on pressure or depth
depth_switch=True
pressure_switch=False

#diameter and length reductions at max pressure
dia_reduc_latex, dia_reduc=epv.thin_diameter_reduction(vessel_1,  epv.depth_to_pressure(depth))
length_reduc_latex, length_reduc=epv.thin_length_reduction(vessel_1, epv.depth_to_pressure(depth))

#streamlit layout for 2x tabs each with 2x columns, 4x output boxes and an expander
container_1=st.container()
with container_1:
    col_1, col_2 = st.columns(2)        
    with col_1:
        depth_switch=st.button("Depth", use_container_width=True)
    with col_2:
        pressure_switch=st.button("Pressure", use_container_width=True)

tab_1, tab_2, tab_3, tab_4, tab_5= st.tabs(["Thin Walled Stress", "Thin Walled Stability", "        ","Thick Wall Stress", "Thick Walled Stability"])

with tab_1:
    container_2=st.container()
    with container_2:
        col_3, col_4 = st.columns(2)
        with col_3:
            if depth_switch==True:
                st.plotly_chart(fig_hs_d, use_container_width=True)
            else:
                st.plotly_chart(fig_hs_p, use_container_width=True)
            st.info(f"Max Hoop Stress = {round(max(hoop_stress_values),0)} psi")
            st.info(f"Diameter Reduction = {round(dia_reduc,4)} in")
        with col_4:
            if depth_switch==True:
                st.plotly_chart(fig_ls_d, use_container_width=True)
            else:
                st.plotly_chart(fig_ls_p, use_container_width=True)
            st.info(f"Max Longitudinal Stress = {round(max(long_stress_values),0)} psi")
            st.info(f"Length Reduction = {round(length_reduc,4)} in")
        exp_1=st.expander("Handcalc")
        with exp_1:
            st.latex(hs_latex)
            st.latex(ls_latex)
            st.latex(dia_reduc_latex)
            st.latex(length_reduc_latex)
with tab_2:
    container_3=st.container()
    with container_3:
        col_5, col_6 = st.columns(2)
        with col_5:
             st.write()
        with col_6:
             st.write()
        exp_2=st.expander("Handcalc")
        with exp_2:
            st.write("")

with tab_3:
    st.write()

with tab_4:
    container_4=st.container()
    with container_4:
        col_7, col_8 = st.columns(2)
        with col_7:
             st.write()
        with col_8:
             st.write()
        exp_3=st.expander("Handcalc")
        with exp_3:
            st.write("")

with tab_5:
    container_5=st.container()
    with container_5:
        col_9, col_10 = st.columns(2)
        with col_9:
             st.write()
        with col_10:
             st.write()
        exp_4=st.expander("Handcalc")
        with exp_4:
            st.write("")


