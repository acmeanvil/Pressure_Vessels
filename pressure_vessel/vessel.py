"""
Copyright 2023 Acmeanvil

Use of this source code is governed by an MIT-style
license that can be found in the LICENSE file or at
https://opensource.org/licenses/MIT.

Pressure vessel class object
assumptions:
    -material properties are inherited form the "material" class
    -vessel is cylindrical with capped ends and is a fully closed volume
    -uniform external pressure on all surface
"""

from __future__ import annotations

from dataclasses import dataclass
import materials.materials as mt

@dataclass
class vessel(mt.material):
    """ 
    generic cylindrical pressure vessel class
    """
    label: str=""
    matl: mt.material=mt.material()
    length: float=0
    diameter: float=0
    wall_thickness: float=0

    def thickness_ratio(self)->dict(float,str):
        """ 
        ratio of radius to thickness (R/t)
        used to define a thin versus thick walled cylinder
        R/t>10 = thin walled
        returns a dictionary with the ratio and whether

        """
        ratio_dict={"ratio":0.0,"type":""}
        ratio=(self.diameter/2)/self.wall_thickness
        ratio_dict.update({"ratio":ratio})
        if ratio<10:
            type="Thick Walled"
            ratio_dict.update({"type":type})
        else:
            type="Thin Walled"
            ratio_dict.update({"type":type})
        return ratio_dict
    
    def length_ratio(self)->float:
        """ 
        ratio of cylinder length to radius (L/R)
        """
        ratio=self.length/(self.diameter/2)
        return ratio