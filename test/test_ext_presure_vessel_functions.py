"""
Copyright 2023 Acmeanvil

Use of this source code is governed by an MIT-style
license that can be found in the LICENSE file or at
https://opensource.org/licenses/MIT.

pressure vessel test functions related to "vessel" class
"""

from pressure_vessel.vessel import vessel
from materials.materials import material
import pressure_vessel.ext_presure_vessel_functions as epv

def test_depth_to_pressure():
    depth=100
    assert round(epv.depth_to_pressure(depth), 8)==round(44.5454545454, 8)

def test_pressure_to_depth():
    pressure=100
    assert round(epv.pressure_to_depth(pressure), 8)==round(224.489795919, 8)

def test_thin_hoop_stress():
    matl_1=material()
    vessel_1=vessel(label="vessel_1", matl=matl_1, length=10.0, diameter=5.0, wall_thickness=0.1)
    vessel_2=vessel(label="vessel_2", matl=matl_1, length=40.0, diameter=36.0, wall_thickness=0.4)
    pressure=100

    latex_1, value_1=epv.thin_hoop_stress(vessel_1, pressure)
    latex_2, value_2=epv.thin_hoop_stress(vessel_2, pressure)

    assert value_1==1250.0
    assert value_2==2250.0

def test_thin_longitudinal_stress():
    matl_1=material()
    vessel_1=vessel(label="vessel_1", matl=matl_1, length=10.0, diameter=5.0, wall_thickness=0.1)
    vessel_2=vessel(label="vessel_2", matl=matl_1, length=40.0, diameter=36.0, wall_thickness=0.4)
    pressure=100

    latex_1, value_1=epv.thin_longitudinal_stress(vessel_1, pressure)
    latex_2, value_2=epv.thin_longitudinal_stress(vessel_2, pressure)
    
    assert value_1==2500.0
    assert value_2==4500.0

def test_thin_diameter_reduction():
    matl_1=material(E=10000000, v=0.3)
    vessel_1=vessel(label="vessel_1", matl=matl_1, length=10.0, diameter=5.0, wall_thickness=0.1, E=10000000, v=0.3)
    vessel_2=vessel(label="vessel_2", matl=matl_1, length=40.0, diameter=36.0, wall_thickness=0.4, E=10000000, v=0.3)
    pressure=100

    latex_1, value_1=epv.thin_diameter_reduction(vessel_1, pressure)
    latex_2, value_2=epv.thin_diameter_reduction(vessel_2, pressure)

    assert value_1==0.0010625 
    assert value_2==0.01377

def test_thin_length_reduction():
    matl_1=material(E=10000000, v=0.3)
    vessel_1=vessel(label="vessel_1", matl=matl_1, length=10.0, diameter=5.0, wall_thickness=0.1, E=10000000, v=0.3)
    vessel_2=vessel(label="vessel_2", matl=matl_1, length=40.0, diameter=36.0, wall_thickness=0.4, E=10000000, v=0.3)
    pressure=100  

    latex_1, value_1=epv.thin_length_reduction(vessel_1, pressure)

    assert value_1==0.0005

def test_thin_critical_buckling_pressure():
    matl_1=material(E=10000000, v=0.3)
    vessel_1=vessel(label="vessel_1", matl=matl_1, length=10.0, diameter=5.0, wall_thickness=0.1, E=10000000, v=0.3)
    vessel_2=vessel(label="vessel_2", matl=matl_1, length=40.0, diameter=36.0, wall_thickness=0.4, E=10000000, v=0.3)
    pressure=100 
    mode=1

    assert round(epv.thin_critical_buckling_pressure(vessel_1, pressure, mode),8)==round(44614.12796007,8)
    assert round(epv.thin_critical_buckling_pressure(vessel_2, pressure, mode),8)==round(49422.11933874,8)

def test_thick_hoop_stress():
    matl_1=material(E=10000000, v=0.3)
    vessel_1=vessel(label="vessel_1", matl=matl_1, length=10.0, diameter=5.0, wall_thickness=0.1, E=10000000, v=0.3)
    vessel_2=vessel(label="vessel_2", matl=matl_1, length=40.0, diameter=36.0, wall_thickness=0.4, E=10000000, v=0.3)
    pressure=100 
    percent=50 

    assert round(epv.thick_hoop_stress(vessel_1, pressure, percent),8)==round(-2499.4900084148608,8)
    assert round(epv.thick_hoop_stress(vessel_2, pressure, percent),8)==round(-4499.719136586164,8)

def test_thick_hoop_stress_max():
    matl_1=material(E=10000000, v=0.3)
    vessel_1=vessel(label="vessel_1", matl=matl_1, length=10.0, diameter=5.0, wall_thickness=0.1, E=10000000, v=0.3)
    vessel_2=vessel(label="vessel_2", matl=matl_1, length=40.0, diameter=36.0, wall_thickness=0.4, E=10000000, v=0.3)
    pressure=100 
    percent=50 

    assert round(epv.thick_hoop_stress_max(vessel_1, pressure),8)==round(-2551.020408163264,8)
    assert round(epv.thick_hoop_stress_max(vessel_2, pressure),8)==round(-4550.5617977528245,8)

def test_thick_longitudinal_stress():
    matl_1=material(E=10000000, v=0.3)
    vessel_1=vessel(label="vessel_1", matl=matl_1, length=10.0, diameter=5.0, wall_thickness=0.1, E=10000000, v=0.3)
    vessel_2=vessel(label="vessel_2", matl=matl_1, length=40.0, diameter=36.0, wall_thickness=0.4, E=10000000, v=0.3)
    pressure=100 
    
    assert round(epv.thick_longitudinal_stress(vessel_1,pressure),8)==round(-1275.510204081630,8)
    assert round(epv.thick_longitudinal_stress(vessel_2,pressure),8)==round(-2275.280898876410,8)

def test_thick_radial_stress():
    matl_1=material(E=10000000, v=0.3)
    vessel_1=vessel(label="vessel_1", matl=matl_1, length=10.0, diameter=5.0, wall_thickness=0.1, E=10000000, v=0.3)
    vessel_2=vessel(label="vessel_2", matl=matl_1, length=40.0, diameter=36.0, wall_thickness=0.4, E=10000000, v=0.3)
    pressure=100
    percent=50

    assert round(epv.thick_radial_stress(vessel_1,pressure,percent),8)==round(-51.530399748404,8)
    assert round(epv.thick_radial_stress(vessel_2,pressure,percent),8)==round(-50.842661166661,8)

def test_thick_radial_stress_max():
    matl_1=material(E=10000000, v=0.3)
    vessel_1=vessel(label="vessel_1", matl=matl_1, length=10.0, diameter=5.0, wall_thickness=0.1, E=10000000, v=0.3)
    vessel_2=vessel(label="vessel_2", matl=matl_1, length=40.0, diameter=36.0, wall_thickness=0.4, E=10000000, v=0.3)
    pressure=100

    assert epv.thick_radial_stress_max(vessel_1, pressure)==-pressure 

def test_thick_shear_stress():
    matl_1=material(E=10000000, v=0.3)
    vessel_1=vessel(label="vessel_1", matl=matl_1, length=10.0, diameter=5.0, wall_thickness=0.1, E=10000000, v=0.3)
    vessel_2=vessel(label="vessel_2", matl=matl_1, length=40.0, diameter=36.0, wall_thickness=0.4, E=10000000, v=0.3)
    pressure=100
    percent=50

    assert round(epv.thick_shear_stress(vessel_1,pressure,percent),8)==round(-1275.510204081630,8)
    assert round(epv.thick_shear_stress(vessel_2,pressure,percent),8)==round(-2275.280898876410,8)

def test_thick_outer_diameter_reduction():
    matl_1=material(E=10000000, v=0.3)
    vessel_1=vessel(label="vessel_1", matl=matl_1, length=10.0, diameter=5.0, wall_thickness=0.1, E=10000000, v=0.3)
    vessel_2=vessel(label="vessel_2", matl=matl_1, length=40.0, diameter=36.0, wall_thickness=0.4, E=10000000, v=0.3)
    pressure=100

    assert round(epv.thick_outer_diameter_reduction(vessel_1,pressure),8)==round(-0.001019183673,8)
    assert round(epv.thick_outer_diameter_reduction(vessel_2,pressure),8)==round(-0.013456719101,8)

def test_thick_inner_diameter_reduction():
    matl_1=material(E=10000000, v=0.3)
    vessel_1=vessel(label="vessel_1", matl=matl_1, length=10.0, diameter=5.0, wall_thickness=0.1, E=10000000, v=0.3)
    vessel_2=vessel(label="vessel_2", matl=matl_1, length=40.0, diameter=36.0, wall_thickness=0.4, E=10000000, v=0.3)
    pressure=100

    assert round(epv.thick_inner_diameter_reduction(vessel_1,pressure),8)==round(-0.001040816327,8)
    assert round(epv.thick_inner_diameter_reduction(vessel_2,pressure),8)==round(-0.013615280899,8)

def test_thick_length_diameter_reduction():
    matl_1=material(E=10000000, v=0.3)
    vessel_1=vessel(label="vessel_1", matl=matl_1, length=10.0, diameter=5.0, wall_thickness=0.1, E=10000000, v=0.3)
    vessel_2=vessel(label="vessel_2", matl=matl_1, length=40.0, diameter=36.0, wall_thickness=0.4, E=10000000, v=0.3)
    pressure=100

    assert round(epv.thick_length_reduction(vessel_1,pressure),8)==round(-0.000510204082,8)
    assert round(epv.thick_length_reduction(vessel_2,pressure),8)==round(-0.003640449438,8)