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
    matl_label: str=""
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

    def assign_matl(self, matl: material):
        """  
        Takes in a material class object and assigns its
        values to another material class object
        """
        self.matl_label=matl.matl_label
        self.matl_type=matl.matl_type
        self.matl_cat=matl.matl_cat
        self.spec=matl.spec
        self.spec_number=matl.spec_number
        self.DIN_num=matl.DIN_num
        self.density=matl.density
        self.fy=matl.fy
        self.fu=matl.fu
        self.E=matl.E
        self.G=matl.G
        self.v=matl.v
        self.elongation=matl.elongation
        self.area_reduc=matl.area_reduc

    def clear_matl(self):
        """ 
        Clears the valuse of a material class object
            floats -> 0
            strings -> empty
        """
        self.matl_label=""
        self.matl_type=""
        self.matl_cat=""
        self.spec=""
        self.spec_number=""
        self.DIN_num=""
        self.density=0
        self.fy=0
        self.fu=0
        self.E=0
        self.G=0
        self.v=0
        self.elongation=0
        self.area_reduc=0

    def imp_to_si(self):
        """ 
        Coverts Imperial values to SI values
        assumes:
            psi -> MPa
            lb/in^2 -> kg/mm^2
        """
        self.density=lbin2_to_kgmm2(self.density)
        self.fy=psi_to_mpa(self.fy)
        self.fu=psi_to_mpa(self.fu)
        self.E=psi_to_mpa(self.E)
        self.G=psi_to_mpa(self.G)


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

def lbin2_to_kgmm2(lbin2: float)->float:
    """ 
    Takes lb/in^2 and returns kg/mm^2
    """
    kgmm2=lbin2*((25.4**2)/2.2)
    return kgmm2 

def convert_to_material(matl_list: list(str,float))->material:
    """ 
    converts a list to a "material" class object
    """
    for element in matl_list[6:]:
         if isinstance(element, str) and element.replace(",","").replace(".","").isnumeric():
            element=float(element)
            
    matl=material(matl_label=matl_list[0],
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
            for line in csv_reader:
                matl=convert_to_material(line)
                matl_acc.append(matl)
            matl_acc.pop(0)
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
            if matl.matl_label not in matl_index:
                 matl_index.append(matl.label)
        if matl_type=="all" or matl_type=="All":
            if matl.matl_label not in matl_index:
                matl_index.append(matl.matl_label)  
    matl_index.insert(0, "---")   
    return matl_index

def generate_matl_type_index(matl_list: list(material))->list(str):
    """ 
    generates a list of all material typess in matl_list
    """
    matl_type_index=[]
    for matl in matl_list:
        if matl.matl_type not in matl_type_index:
            matl_type_index.append(matl.matl_type)
    matl_type_index.insert(0, "All")
    return matl_type_index

def generate_matl_category_index(matl_list: list(material))->list(str):
    """ 
    generates a list of all material typess in matl_list
    """
    matl_type_index=[]
    for matl in matl_list:
        if matl.matl_cat not in matl_type_index:
            matl_type_index.append(matl.matl_cat)
    matl_type_index.insert(0, "All")
    return matl_type_index

    