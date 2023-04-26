import streamlit as st
import plotly.graph_objects as go
import materials.materials as mt
import pressure_vessel.ext_presure_vessel_functions as epv
import pressure_vessel.vessel as vsl
import layout.st_layout as stl
import plotly.graph_objects as go
from plotly.subplots import make_subplots as msp
import numpy as np

st.header("Pressure Vessel Design")

matl_table=mt.import_matl_table("material_table.csv")

matl_category=mt.generate_matl_category_index(matl_table)
category_selection=st.sidebar.selectbox("Material Category", matl_category)

matl_type=mt.generate_matl_type_index(matl_table)
type_selection=st.sidebar.selectbox("Material Type", matl_type)

matl_index=mt.generate_matl_index(matl_table, type_selection)
matl_selection=st.sidebar.selectbox("Material", matl_index)

length_choice=st.sidebar.number_input("Vessel Length", min_value=0.01)
diameter_choice=st.sidebar.number_input("Vessel Diameter", min_value=0.01)
thickness_choice=st.sidebar.number_input("Vessel Wall Thickness", min_value=0.01)
depth_choice=st.sidebar.number_input("Vessel Depth Rating", min_value=0.01)

vessel_matl=mt.material()
for matl in matl_table:
    if matl.matl_label==matl_selection:
        vessel_matl.assign_matl(matl)

vessel_1=vsl.vessel(matl_label="Vessel 1", matl=vessel_matl, length=length_choice, diameter=diameter_choice, wall_thickness=thickness_choice)
pressure=epv.depth_to_pressure(depth_choice)
depth_values = list(range(1, int(round(depth_choice+1,0)), int(round((depth_choice+1)/100,0))))
#st.write(depth_values)

pressure_values=[]
for depth in depth_values:
    pressure_values.append(epv.depth_to_pressure(depth))
#st.write(pressure_values)

hoop_stress_values=[]
for pressure in pressure_values:
    hoop_stress_values.append(epv.thin_hoop_stress(vessel_1, pressure))
#st.write(hoop_stress_values)

long_stress_values=[]
for pressure in pressure_values:
    long_stress_values.append(epv.thin_longitudinal_stress(vessel_1, pressure))
#st.write(long_stress_values)


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
fig_hs_d.add_trace(
    go.Scatter(
        name="Yield Stress",
        x=[0, depth_choice],
        y=[vessel_1.matl.fy, vessel_1.matl.fy],
        fill="tonexty")
)

fig_hs_d.update_layout(title_text="<b>Hoop Stress at Depth<b>", title_x=0.25, font_size=20)
fig_hs_d.update_xaxes(title=dict(text="<b>Depth (ft)<b>",font=dict(size=14)), range=[0, max(depth_values)*1.02] ,title_standoff = 20)
fig_hs_d.update_yaxes(title=dict(text="<b>Hoop Stress (psi)<b>",font=dict(size=14)), range=[0, max(hoop_stress_values)*1.02], title_standoff = 20)
fig_hs_d.update_layout(legend=dict( yanchor="top", y=0.90, xanchor="left", x=0.01))

fig_hs_p.add_trace(
    go.Scatter(
        name="Hoop Stress",
        x=pressure_values,
        y=hoop_stress_values,
        fill="tonexty")
)

fig_hs_p.add_trace(
    go.Scatter(
        name="Yield Stress",
        x=[0, max(pressure_values)],
        y=[vessel_1.matl.fy, vessel_1.matl.fy],
        fill="tonexty")
)

fig_hs_p.update_layout(title_text="<b>Hoop Stress at Pressure<b>", title_x=0.25, font_size=14)
fig_hs_p.update_xaxes(title=dict(text="<b>Pressure (psi)<b>",font=dict(size=14)), range=[0, max(pressure_values)*1.02], title_standoff = 20)
fig_hs_p.update_yaxes(title=dict(text="<b>Hoop Stress (psi)<b>",font=dict(size=14)), range=[0, max(hoop_stress_values)*1.02], title_standoff = 20)
fig_hs_p.update_layout(legend=dict( yanchor="top", y=0.90, xanchor="left", x=0.01))

fig_ls_d.add_trace(
    go.Scatter(
        name="Longitudinal Stress",
        x=depth_values,
        y=long_stress_values,
        fill="tonexty")
)

fig_ls_d.add_trace(
    go.Scatter(
        name="Yield Stress",
        x=[0, max(depth_values)],
        y=[vessel_1.matl.fy, vessel_1.matl.fy],
        fill="tonexty")
)

fig_ls_d.update_layout(title_text="<b>Longituduinal Stress at Depth<b>", title_x=0.25, font_size=20)
fig_ls_d.update_xaxes(title=dict(text="<b>Depth (ft)<b>",font=dict(size=14)), range=[0, max(depth_values)*1.02], title_standoff = 20)
fig_ls_d.update_yaxes(title=dict(text="<b>Longitudinal Stress (psi)<b>",font=dict(size=14)), range=[0, max(long_stress_values)*1.02], title_standoff = 20)
fig_ls_d.update_layout(legend=dict( yanchor="top", y=0.90, xanchor="left", x=0.01))

fig_ls_p.add_trace(
    go.Scatter(
        name="Longitudinal Stress",
        x=pressure_values,
        y=long_stress_values,
        fill="tonexty")
)

fig_ls_p.add_trace(
    go.Scatter(
        name="Yield Stress",
        x=[0, max(pressure_values)],
        y=[vessel_1.matl.fy, vessel_1.matl.fy],
        fill="tonexty")
)

fig_ls_p.update_layout(title_text="<b>Longitudinal Stress at Pressure<b>", title_x=0.25, font_size=14)
fig_ls_p.update_xaxes(title=dict(text="<b>Pressure (psi)<b>",font=dict(size=14)), range=[0, max(pressure_values)*1.02], title_standoff = 20)
fig_ls_p.update_yaxes(title=dict(text="<b>Longitudinal Stress (psi)<b>",font=dict(size=14)), range=[0, max(long_stress_values)*1.02], title_standoff = 20)
fig_ls_p.update_layout(legend=dict( yanchor="top", y=0.90, xanchor="left", x=0.01))

depth_switch=True
pressure_switch=False
dia_reduc=epv.thin_diameter_reduction(vessel_1,  epv.depth_to_pressure(depth))
length_reduc=epv.thin_length_reduction(vessel_1, epv.depth_to_pressure(depth))


tab_1, tab_2 = st.tabs(["Elastic Stress", "Elastic Stability"])
with tab_1:
    container_1=st.container()
    with container_1:
        col_1, col_2 = st.columns(2)        
        with col_1:
            depth_switch=st.button("Depth", use_container_width=True)
        with col_2:
            pressure_switch=st.button("Pressure", use_container_width=True)
    container_2=st.container()
    with container_2:
        col_3, col_4 = st.columns(2)
        with col_3:
            if depth_switch==True:
                st.plotly_chart(fig_hs_d, use_container_width=True)
            else:
                st.plotly_chart(fig_hs_p, use_container_width=True)
            st.info(f"Max Hoop Stress = {round(max(hoop_stress_values),0)} psi")
            st.info(f"Diameter Reduction = {round(max(dia_reduc),4)} in")
        with col_4:
            if depth_switch==True:
                st.plotly_chart(fig_ls_d, use_container_width=True)
            else:
                st.plotly_chart(fig_ls_p, use_container_width=True)
            st.info(f"Max Longitudinal Stress = {round(max(long_stress_values),0)} psi")
            st.info(f"Length Reduction = {round(max(length_reduc),4)} in")
        exp_1=st.expander("Handcalc")
        with exp_1:
            st.write("Test 1")

with tab_2:
    container_3=st.container()
    with container_3:
        col_5, col_6 = st.columns(2)
        with col_5:
            st.write(depth_choice)
            st.write(float(vessel_1.matl.fy))
        with col_6:
            st.write("i am here 4")
        exp_2=st.expander("Handcalc")
        with exp_2:
            st.write("Test 2")



# st.write("Material=",matl_selection)
# st.write("Length=",length_choice)
# st.write("Diameter=",diameter_choice)
# st.write("Wall Thickness=",thickness_choice)
