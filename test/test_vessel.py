"""
Copyright 2023 Acmeanvil

Use of this source code is governed by an MIT-style
license that can be found in the LICENSE file or at
https://opensource.org/licenses/MIT.

test functions related to "vessel" class support functions
"""

from pressure_vessel.vessel import vessel
from materials.materials import material

def test_thickness_ratio():
    matl_1=material()
    vessel_1=vessel(label="vessel_1", matl=matl_1, length=10.0, diameter=5.0, wall_thickness=0.1)
    vessel_2=vessel(label="vessel_2", matl=matl_1, length=40.0, diameter=36.0, wall_thickness=0.1)
    assert vessel_1.thickness_ratio()==25
    assert vessel_2.thickness_ratio()==180

def test_length_ratio():
    matl_1=material()
    vessel_1=vessel(label="vessel_1", matl=matl_1, length=10.0, diameter=5.0, wall_thickness=0.1)
    vessel_2=vessel(label="vessel_2", matl=matl_1, length=40.0, diameter=16.0, wall_thickness=0.1)
    assert vessel_1.length_ratio()==4.0
    assert vessel_2.length_ratio()==5.0