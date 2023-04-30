"""
Copyright 2023 Acmeanvil

Use of this source code is governed by an MIT-style
license that can be found in the LICENSE file or at
https://opensource.org/licenses/MIT.

Functions for plotting graphs pressure or depth verse hoop or longitudinal stress
"""
from __future__ import annotations

import pressure_vessel.ext_presure_vessel_functions as epv
import pressure_vessel.vessel as vsl
import plotly.graph_objects as go

def thin_display_hoop_and_long_figures(vessel: vsl.vessel, depth_choice: float)->dict(fig):
    """ 
    Takes a Vessel class object and a depth, assembles and returns plots for:
        -Thin Walled Hoop stress verse depth
        -Thin Walled Hoop stress verse pressure
        -Thin Walled Longitudinal stress verse depth
        -Thin Walled Longitudinal stress verse pressure
    """
    figures={"fig_hs_d":None, "fig_hs_p":None, "fig_ls_d":None, "fig_ls_p":None}
    
    pressure=epv.depth_to_pressure(depth_choice)

    #create lists for X and Y values for plots
    depth_values = list(range(1, int(round(depth_choice+1,0)), int(round((depth_choice+1)/30,0))))
    pressure_values=[]
    for depth in depth_values:
        pressure_values.append(epv.depth_to_pressure(depth))

    hoop_stress_values=[]
    for pressure in pressure_values:
        hs_latex, hs_value=epv.thin_hoop_stress(vessel, pressure)
        hoop_stress_values.append(hs_value)
 

    long_stress_values=[]
    for pressure in pressure_values:
        ls_latex, ls_value=epv.thin_longitudinal_stress(vessel, pressure)
        long_stress_values.append(ls_value)

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
            line_color="white")
    )
    #graph a line at vessel material yield stress
    fig_hs_d.add_trace(
        go.Scatter(
            name="Under Yield Stress",
            x=[0, max(depth_values)],
            y=[vessel.matl.fy, vessel.matl.fy], fill="tozeroy" ,line_color="#A0E095")
    )
    if max(hoop_stress_values) > float(vessel.matl.fy):
        fig_hs_d.add_trace(
            go.Scatter(
                name="Over Yield Stress",
                x=[0, max(depth_values)],
                y=[max(hoop_stress_values), max(hoop_stress_values)], fill="tonexty" ,line_color="#EF8282")
        )

    #pretty up hoop stress vs depth plot
    fig_hs_d.update_layout(title_text="<b>Hoop Stress at Depth<b>", margin=dict(l=20, r=20, t=20, b=20), title_x=0.40, title_y=0.95, font_size=32)
    fig_hs_d.update_xaxes(title=dict(text="<b>Depth (ft)<b>",font=dict(size=14)), range=[0, max(depth_values)*1.02] ,title_standoff = 20)
    fig_hs_d.update_yaxes(title=dict(text="<b>Hoop Stress (psi)<b>",font=dict(size=14)), title_standoff = 20)
    fig_hs_d.update_layout(legend=dict( yanchor="top", y=0.90, xanchor="left", x=0.01))
    figures.update({"fig_hs_d":fig_hs_d})

    #hoop stress vs pressure
    fig_hs_p.add_trace(
        go.Scatter(
            name="Hoop Stress",
            x=pressure_values,
            y=hoop_stress_values,
            line_color="white")
    )
    #graph a line at vessel material yield stress
    fig_hs_p.add_trace(
        go.Scatter(
            name="Under Yield Stress",
            x=[0, max(pressure_values)],
            y=[vessel.matl.fy, vessel.matl.fy], fill="tozeroy" ,line_color="#A0E095")
    )
    if max(hoop_stress_values) > float(vessel.matl.fy):
        fig_hs_p.add_trace(
            go.Scatter(
                name="Over Yield Stress",
                x=[0, max(pressure_values)],
                y=[max(hoop_stress_values), max(hoop_stress_values)], fill="tonexty" ,line_color="#EF8282")
        )

    #pretty up hoop stress vs pressure plot
    fig_hs_p.update_layout(title_text="<b>Hoop Stress at Pressure<b>", margin=dict(l=20, r=20, t=20, b=20), title_x=0.40, title_y=0.95, font_size=32)
    fig_hs_p.update_xaxes(title=dict(text="<b>Pressure (psi)<b>",font=dict(size=14)), range=[0, max(pressure_values)*1.02], title_standoff = 20)
    fig_hs_p.update_yaxes(title=dict(text="<b>Hoop Stress (psi)<b>",font=dict(size=14)), title_standoff = 20)
    fig_hs_p.update_layout(legend=dict( yanchor="top", y=0.90, xanchor="left", x=0.01))
    figures.update({"fig_hs_p":fig_hs_p})

    #longitudinal stress vs depth
    fig_ls_d.add_trace(
        go.Scatter(
            name="Longitudinal Stress",
            x=depth_values,
            y=long_stress_values,
            line_color="white")
    )
    #graph a line at vessel material yield stress
    fig_ls_d.add_trace(
        go.Scatter(
            name="Yield Stress",
            x=[0, max(depth_values)],
            y=[vessel.matl.fy, vessel.matl.fy], fill="tozeroy" ,line_color="#A0E095")
    )
    if max(long_stress_values) > float(vessel.matl.fy):
        fig_ls_d.add_trace(
            go.Scatter(
                name="Over Yield Stress",
                x=[0, max(depth_values)],
                y=[max(long_stress_values), max(long_stress_values)], fill="tonexty" ,line_color="#EF8282")
        )
    #pretty up longitudinal stress vs depth plot
    fig_ls_d.update_layout(title_text="<b>Longituduinal Stress at Depth<b>", margin=dict(l=20, r=20, t=20, b=20), title_x=0.35, title_y=0.95,  font_size=20)
    fig_ls_d.update_xaxes(title=dict(text="<b>Depth (ft)<b>",font=dict(size=14)), range=[0, max(depth_values)*1.02], title_standoff = 20)
    fig_ls_d.update_yaxes(title=dict(text="<b>Longitudinal Stress (psi)<b>",font=dict(size=14)), title_standoff = 20)
    fig_ls_d.update_layout(legend=dict( yanchor="top", y=0.90, xanchor="left", x=0.01))
    figures.update({"fig_ls_d":fig_ls_d})

    #longitudinal stress vs pressure
    fig_ls_p.add_trace(
        go.Scatter(
            name="Longitudinal Stress",
            x=pressure_values,
            y=long_stress_values,
            line_color="white")
    )
    #graph a line at vessel material yield stress
    fig_ls_p.add_trace(
        go.Scatter(
            name="Yield Stress",
            x=[0, max(pressure_values)],
            y=[vessel.matl.fy, vessel.matl.fy], fill="tozeroy" ,line_color="#A0E095")
    )
    if max(long_stress_values) > float(vessel.matl.fy):
        fig_ls_p.add_trace(
            go.Scatter(
                name="Over Yield Stress",
                x=[0, max(pressure_values)],
                y=[max(long_stress_values), max(long_stress_values)], fill="tonexty" ,line_color="#EF8282")
        )
    #pretty up longitudinal stress vs pressure plot
    fig_ls_p.update_layout(title_text="<b>Longitudinal Stress at Pressure<b>", margin=dict(l=20, r=20, t=20, b=20), title_x=0.35, title_y=0.95, font_size=14)
    fig_ls_p.update_xaxes(title=dict(text="<b>Pressure (psi)<b>",font=dict(size=14)), range=[0, max(pressure_values)*1.02], title_standoff = 20)
    fig_ls_p.update_yaxes(title=dict(text="<b>Longitudinal Stress (psi)<b>",font=dict(size=14)), title_standoff = 20)
    fig_ls_p.update_layout(legend=dict( yanchor="top", y=0.90, xanchor="left", x=0.01))
    figures.update({"fig_ls_p":fig_ls_p})
    
    return figures

def thick_display_hoop_and_long_figures(vessel: vsl.vessel, depth_choice: float, percent: float)->dict(fig):
    """ 
    Takes a Vessel class object and a depth, assembles and returns plots for:
        -Thin Walled Hoop stress verse depth
        -Thin Walled Hoop stress verse pressure
        -Thin Walled Longitudinal stress verse depth
        -Thin Walled Longitudinal stress verse pressure
    """
    figures={"fig_tk_hs_d":None, "fig_tk_hs_p":None, "fig_tk_ls_d":None, "fig_tk_ls_p":None}
    
    pressure=epv.depth_to_pressure(depth_choice)

    #create lists for X and Y values for plots
    depth_values = list(range(1, int(round(depth_choice+1,0)), int(round((depth_choice+1)/30,0))))
    pressure_values=[]
    for depth in depth_values:
        pressure_values.append(epv.depth_to_pressure(depth))

    hoop_stress_values=[]
    for pressure in pressure_values:
        hs_latex, hs_value=epv.thick_hoop_stress(vessel, pressure, percent)
        hoop_stress_values.append(hs_value)
 

    long_stress_values=[]
    for pressure in pressure_values:
        ls_latex, ls_value=epv.thick_longitudinal_stress(vessel, pressure)
        long_stress_values.append(ls_value)

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
            line_color="white")
    )
    #graph a line at vessel material yield stress
    fig_hs_d.add_trace(
        go.Scatter(
            name="Under Yield Stress",
            x=[0, max(depth_values)],
            y=[vessel.matl.fy, vessel.matl.fy], fill="tozeroy" ,line_color="#A0E095")
    )
    if max(hoop_stress_values) > float(vessel.matl.fy):
        fig_hs_d.add_trace(
            go.Scatter(
                name="Over Yield Stress",
                x=[0, max(depth_values)],
                y=[max(hoop_stress_values), max(hoop_stress_values)], fill="tonexty" ,line_color="#EF8282")
        )

    #pretty up hoop stress vs depth plot
    fig_hs_d.update_layout(title_text="<b>Hoop Stress at Depth<b>", margin=dict(l=20, r=20, t=20, b=20), title_x=0.40, title_y=0.95, font_size=32)
    fig_hs_d.update_xaxes(title=dict(text="<b>Depth (ft)<b>",font=dict(size=14)), range=[0, max(depth_values)*1.02] ,title_standoff = 20)
    fig_hs_d.update_yaxes(title=dict(text="<b>Hoop Stress (psi)<b>",font=dict(size=14)), title_standoff = 20)
    fig_hs_d.update_layout(legend=dict( yanchor="top", y=0.90, xanchor="left", x=0.01))
    figures.update({"fig_tk_hs_d":fig_hs_d})

    #hoop stress vs pressure
    fig_hs_p.add_trace(
        go.Scatter(
            name="Hoop Stress",
            x=pressure_values,
            y=hoop_stress_values,
            line_color="white")
    )
    #graph a line at vessel material yield stress
    fig_hs_p.add_trace(
        go.Scatter(
            name="Under Yield Stress",
            x=[0, max(pressure_values)],
            y=[vessel.matl.fy, vessel.matl.fy], fill="tozeroy" ,line_color="#A0E095")
    )
    if max(hoop_stress_values) > float(vessel.matl.fy):
        fig_hs_p.add_trace(
            go.Scatter(
                name="Over Yield Stress",
                x=[0, max(pressure_values)],
                y=[max(hoop_stress_values), max(hoop_stress_values)], fill="tonexty" ,line_color="#EF8282")
        )

    #pretty up hoop stress vs pressure plot
    fig_hs_p.update_layout(title_text="<b>Hoop Stress at Pressure<b>", margin=dict(l=20, r=20, t=20, b=20), title_x=0.40, title_y=0.95, font_size=32)
    fig_hs_p.update_xaxes(title=dict(text="<b>Pressure (psi)<b>",font=dict(size=14)), range=[0, max(pressure_values)*1.02], title_standoff = 20)
    fig_hs_p.update_yaxes(title=dict(text="<b>Hoop Stress (psi)<b>",font=dict(size=14)), title_standoff = 20)
    fig_hs_p.update_layout(legend=dict( yanchor="top", y=0.90, xanchor="left", x=0.01))
    figures.update({"fig_tk_hs_p":fig_hs_p})

    #longitudinal stress vs depth
    fig_ls_d.add_trace(
        go.Scatter(
            name="Longitudinal Stress",
            x=depth_values,
            y=long_stress_values,
            line_color="white")
    )
    #graph a line at vessel material yield stress
    fig_ls_d.add_trace(
        go.Scatter(
            name="Yield Stress",
            x=[0, max(depth_values)],
            y=[vessel.matl.fy, vessel.matl.fy], fill="tozeroy" ,line_color="#A0E095")
    )
    if max(long_stress_values) > float(vessel.matl.fy):
        fig_ls_d.add_trace(
            go.Scatter(
                name="Over Yield Stress",
                x=[0, max(depth_values)],
                y=[max(long_stress_values), max(long_stress_values)], fill="tonexty" ,line_color="#EF8282")
        )
    #pretty up longitudinal stress vs depth plot
    fig_ls_d.update_layout(title_text="<b>Longituduinal Stress at Depth<b>", margin=dict(l=20, r=20, t=20, b=20), title_x=0.35, title_y=0.95,  font_size=20)
    fig_ls_d.update_xaxes(title=dict(text="<b>Depth (ft)<b>",font=dict(size=14)), range=[0, max(depth_values)*1.02], title_standoff = 20)
    fig_ls_d.update_yaxes(title=dict(text="<b>Longitudinal Stress (psi)<b>",font=dict(size=14)), title_standoff = 20)
    fig_ls_d.update_layout(legend=dict( yanchor="top", y=0.90, xanchor="left", x=0.01))
    figures.update({"fig_tk_ls_d":fig_ls_d})

    #longitudinal stress vs pressure
    fig_ls_p.add_trace(
        go.Scatter(
            name="Longitudinal Stress",
            x=pressure_values,
            y=long_stress_values,
            line_color="white")
    )
    #graph a line at vessel material yield stress
    fig_ls_p.add_trace(
        go.Scatter(
            name="Yield Stress",
            x=[0, max(pressure_values)],
            y=[vessel.matl.fy, vessel.matl.fy], fill="tozeroy" ,line_color="#A0E095")
    )
    if max(long_stress_values) > float(vessel.matl.fy):
        fig_ls_p.add_trace(
            go.Scatter(
                name="Over Yield Stress",
                x=[0, max(pressure_values)],
                y=[max(long_stress_values), max(long_stress_values)], fill="tonexty" ,line_color="#EF8282")
        )
    #pretty up longitudinal stress vs pressure plot
    fig_ls_p.update_layout(title_text="<b>Longitudinal Stress at Pressure<b>", margin=dict(l=20, r=20, t=20, b=20), title_x=0.35, title_y=0.95, font_size=14)
    fig_ls_p.update_xaxes(title=dict(text="<b>Pressure (psi)<b>",font=dict(size=14)), range=[0, max(pressure_values)*1.02], title_standoff = 20)
    fig_ls_p.update_yaxes(title=dict(text="<b>Longitudinal Stress (psi)<b>",font=dict(size=14)), title_standoff = 20)
    fig_ls_p.update_layout(legend=dict( yanchor="top", y=0.90, xanchor="left", x=0.01))
    figures.update({"fig_tk_ls_p":fig_ls_p})
    
    return figures