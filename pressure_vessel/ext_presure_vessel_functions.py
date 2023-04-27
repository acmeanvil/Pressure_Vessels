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

from __future__ import annotations

import math
import pressure_vessel.vessel as pv
from handcalcs.decorator import handcalc


def depth_to_pressure(depth: float)->float:
    """ 
    takes a depth in ft and returns a pressure in psi
    """
    pressure=14.7*(depth/33.0)
    return pressure

@handcalc()
def thin_hoop_stress(vessel: pv.vessel, pressure: float)->float:
    """ 
    Roarks 7, pp. 593 table 13.1, case 1c
    hoop stress, assumes that there is no radial stress and hoop stress
    is the uniform through out wall thickness
    """
    hoop=((pressure*(vessel.diameter/2))/(2*vessel.wall_thickness)) #hoop stress
    return hoop

@handcalc()
def thin_longitudinal_stress(vessel: pv.vessel, pressure: float)->float:
    """ 
    Roarks 7, pp. 593 table 13.1, case 1c longitudinal stress,
    assumes that there is no radial stress and longitudinal stress
    is the uniform through out wall thickness
    """
    long=((pressure*(vessel.diameter/2))/(vessel.wall_thickness)) #longitudinal stress
    return long

@handcalc()
def thin_diameter_reduction(vessel: pv.vessel, pressure: float)->float:
    """ 
    Roarks 7, pp. 593 table 13.1, case 1c
    reduction in diameter of a pressure vessel under uniform external pressure
    """
    r=vessel.diameter/2
    E=float(vessel.matl.E)
    t=vessel.wall_thickness
    v=float(vessel.matl.v)
    p=pressure
    dia=(((p*(r**2))/(E*t))*(1-(v/2)))*2 #reduction in diameter
    return dia

@handcalc()
def thin_length_reduction(vessel: pv.vessel, pressure: float)->float:
    """ 
    Roarks 7, pp. 593 table 13.1, case 1c
    reduction in length of a pressure vessel under uniform external pressure
    """
    r=vessel.diameter/2
    E=float(vessel.matl.E)
    t=vessel.wall_thickness
    v=float(vessel.matl.v)
    p=pressure
    l=vessel.length
    len=(((p*r*l)/(E*t))*(0.5-v)) #reduction in length
    return len

def thin_critical_buckling_pressure(vessel: pv.vessel, pressure: float, mode: int)->float:
    """ 
    Roarks 7, pp. 736 table 15.2, case 20a
    """
    r=vessel.diameter/2
    E=float(vessel.matl.E)
    t=vessel.wall_thickness
    v=float(vessel.matl.v)
    p=pressure
    l=vessel.length
    n=mode
    #break apart main equation into 4 parts for convienience
    q1=(E*(t/r))/(1+(.5*(((math.pi*r)/(n*l))**2)))
    q2=(1/((n**2)*(1+((n*l)/(math.pi*r))**2)**2))
    q3=((n**2)*(t**2))/(12*(r**2)*(1-(v**2)))
    q4=(1+((math.pi*r)/(n*l))**2)**2
    p_crit=q1*(q2+(q3*q4))  #critical buckling pressure
    return p_crit
   
def thick_hoop_stress(vessel: pv.vessel, pressure: float, percent: float)->float:
    """ 
    Roarks 7, pp. 683 table 13.5, case 1c
    hoop stress at some point in the vessel wall thickness
    specified by a percentage of wall thickness where 0%=ID and 100%=OD
    """
    t=vessel.wall_thickness
    a=vessel.diameter/2         #outer radius
    b=a-t                       #inner radius
    r=b+(t*(percent/100))       #radial distance to stress
    p=pressure
    hoop=(-p*(a**2)*((b**2)+(r**2)))/((r**2)*((a**2)-(b**2)))
    return hoop

def thick_hoop_stress_max(vessel: pv.vessel, pressure: float)->float:
    """ 
    Roarks 7, pp. 683 table 13.5, case 1c
    maximum hoop stress at ID
    """
    t=vessel.wall_thickness     
    a=vessel.diameter/2                 #outer radius
    b=a-t                               #inner radius
    p=pressure
    hoop=(-p*2*(a**2))/((a**2)-(b**2))  #hoop stress @ radial dist, "r"
    return hoop

def thick_longitudinal_stress(vessel: pv.vessel, pressure: float)->float:
    """ 
    Roarks 7, pp. 683 table 13.5, case 1d
    longitudinal (axial) stress, uniform across the cross section
    """
    t=vessel.wall_thickness
    a=vessel.diameter/2               #outer radius
    b=a-t                             #inner radius
    p=pressure
    long=(-p*(a**2))/((a**2)-(b**2))  #longitudinal stress 
    return long

def thick_radial_stress(vessel: pv.vessel, pressure: float, percent: float)->float:
    """
    Roarks 7, pp. 683 table 13.5, case 1c 
    radial stress at some point in the vessel wall thickness
    specified by a percentage of wall thickness where 0%=ID and 100%=OD
    """
    t=vessel.wall_thickness
    a=vessel.diameter/2                                       #outer radius
    b=a-t                                                     #inner radius
    r=b+(t*(percent/100))                                     #radial distance to stress
    p=pressure
    rad=(-p*(a**2)*((r**2)-(b**2)))/((r**2)*((a**2)-(b**2)))  #radial stress
    return rad

def thick_radial_stress_max(vessel: pv.vessel, pressure: float)->float:
    """ 
    Roarks 7, pp. 683 table 13.5, case 1d
    max radial stres is outer surface of vessel and equal to external pressure
    """
    rad=-pressure
    return rad

def thick_shear_stress(vessel: pv.vessel, pressure: float, percent: float)->float:
    """ 
    Roarks 7, pp. 683 table 13.5, case 1c
    internal shear stress at some point in the vessel wall thickness
    specified by a percentage of wall thickness where 0%=ID and 100%=OD
    """
    t=vessel.wall_thickness
    a=vessel.diameter/2                  #outer radius
    b=a-t                                #inner radius
    r=b+(t*(percent/100))                #radial distance to stress
    p=pressure
    shear=(-p*(a**2))/(((a**2)-(b**2)))  #internal shear stress
    return shear

def thick_outer_diameter_reduction(vessel: pv.vessel, pressure: float)->float:
    """
    Roarks 7, pp. 683 table 13.5, case 1d 
    reduction in outer diameter due to external pressure
    """
    t=vessel.wall_thickness
    a=vessel.diameter/2
    b=a-t 
    E=float(vessel.matl.E)
    v=float(vessel.matl.v)
    p=pressure
    dia=(((-p*a)/E)*((((a**2)*(1-(2*v)))+((b**2)*(1+v)))/((a**2)-(b**2))))*2
    return dia

def thick_inner_diameter_reduction(vessel: pv.vessel, pressure: float)->float:
    """
    Roarks 7, pp. 683 table 13.5, case 1d
    reduction in inner diameter due to external pressure
    """
    t=vessel.wall_thickness
    a=vessel.diameter/2
    b=a-t 
    E=float(vessel.matl.E)
    v=float(vessel.matl.v)
    p=pressure
    dia=(((-p*b)/E)*(((a**2)*(2-v))/((a**2)-(b**2))))*2
    return dia

def thick_length_reduction(vessel: pv.vessel, pressure: float)->float:
    """ 
    Roarks 7, pp. 683 table 13.5, case 1d
    reduction in overall length due to external pressure
    """
    t=vessel.wall_thickness
    a=vessel.diameter/2
    b=a-t 
    E=float(vessel.matl.E)
    v=float(vessel.matl.v)
    p=pressure
    l=vessel.length
    len=((-p*l)/E)*(((a**2)*(1-(2*v)))/((a**2)-(b**2)))
    return len

