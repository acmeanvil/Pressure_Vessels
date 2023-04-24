"""
Copyright 2023 Acmeanvil

Use of this source code is governed by an MIT-style
license that can be found in the LICENSE file or at
https://opensource.org/licenses/MIT.

Generic material properties class object with support functions
"""

from __future__ import annotations

from dataclasses import dataclass
import csv

matl_file_read_flag=0

@dataclass
class material:
    """
    Generic materials class
    """
    label: str=""
    matl_type: str=""
    matl_cat: str=""
    spec: str=""
    spec_number: str=""
    DIN_num: str="" 
    density: float=0
    fy: float=0
    fu: float=0
    E: float=0
    G: float=0
    v: float=0
    elongation: float=0
    area_reduc: float=0

def psi_to_mpa(stress: float)->float:
    """ 
    convert pounds per squarein ch to meg Pascals 
    """
    stress_si=stress/145.04
    return stress_si
    
def cubic_in_cubic_mm(dens: float)->float:
    """  
    converts cubic inches to cubic millimeter
    """
    density_si=dens*(25.4**3)
    return density_si

def convert_to_material(matl_list: list(str,float))->material:
    """ 
    converts a list to a "material" class object
    """
    matl=material(label=matl_list[0],
                  matl_type=matl_list[1],
                  matl_cat=matl_list[2],
                  spec=matl_list[3],
                  spec_number=matl_list[4],
                  DIN_num=matl_list[5],
                  density=matl_list[6],
                  fy=matl_list[7],
                  fu=matl_list[8],
                  E=matl_list[9],
                  G=matl_list[10],
                  v=matl_list[11],
                  elongation=matl_list[12],
                  area_reduc=matl_list[13]
                  )  
    return matl

def import_matl_table(matl_file: str)->list(material):
    """  
    imports a csv file of materials and converts each line to a "material" class object
    """
    if matl_file_read_flag==0:
        matl_acc = [] 
        with open(matl_file, "r") as csv_file:
            csv_reader = csv.reader(csv_file)
            for line in csv_reader[1:]:
                matl=convert_to_material(line)
                matl_acc.append(matl)
        return matl_acc
    else:
        return

def generate_matl_index(matl_list: list(material), matl_type: str)->list(str):
    """ 
    generates a list of names of all material objects in matl_list with a matl_type
    equal to the included string    
    """
    matl_index=[]
    for matl in matl_list:
        if matl.matl_type==matl_type:
            if matl.label not in matl_index:
                 matl_index.append(matl.label)
        if matl_type=="all" or matl_type=="All":
            if matl.label not in matl_index:
                matl_index.append(matl.label)       
    return matl_index

def generate_matl_type_index(matl_list: list(material))->list(str):
    """ 
    generates a list of all material typess in matl_list
    """
    matl_type_index=[]
    for matl in matl_list:
        if matl.matl_cat not in matl_type_index:
            matl_type_index.append(matl.matl_cat)
    return matl_type_index

    