"""
Copyright 2023 Acmeanvil

Use of this source code is governed by an MIT-style
license that can be found in the LICENSE file or at
https://opensource.org/licenses/MIT.

test functions related to "material" class support functions
"""

import materials.materials as mt

def test_convert_to_material():
    matl=["6061-t6","Aluminum","metal","UNS","A96061",1,0.098,35000,42000,10000000,3800000,0.33,2,3]
    matl_conv=mt.convert_to_material(matl)
    assert matl_conv.matl_label=="6061-t6"
    assert matl_conv.matl_type=="Aluminum"
    assert matl_conv.matl_cat=="metal"
    assert matl_conv.spec=="UNS"
    assert matl_conv.spec_number=="A96061"
    assert matl_conv.DIN_num==1
    assert matl_conv.density==0.098
    assert matl_conv.fy==35000
    assert matl_conv.fu==42000
    assert matl_conv.E==10000000
    assert matl_conv.G==3800000
    assert matl_conv.v==0.33
    assert matl_conv.elongation==2
    assert matl_conv.area_reduc==3

def test_psi_to_mpa():
    stress=145040
    assert mt.psi_to_mpa(stress)==1000.0

def test_cubic_in_cubic_mm():
    dens=0.1
    assert mt.cubic_in_cubic_mm(dens)==0.1*(25.4**3.0)

def test_lbin2_to_kgmm2():
    lbin2=0.1
    assert round(mt.lbin2_to_kgmm2(lbin2),8)==round(29.3254545454,8)

def test_generate_matl_index():
    matl_list=[]
    matl_1=mt.material(matl_label="test_6061", matl_type="test_Aluminum", matl_cat="test_metal_1")
    matl_list.append(matl_1)
    matl_list.append(mt.material(matl_label="test_7075", matl_type="test_Aluminum", matl_cat="test_metal_1"))   
    matl_list.append(mt.material(matl_label="test_4140", matl_type="test_Steel", matl_cat="test_metal_2"))
    matl_list.append(mt.material(matl_label="test_316", matl_type="test_Stainless Steel", matl_cat="test_metal_3"))
    matl_list.append(mt.material(matl_label="test_316", matl_type="test_Stainless Steel", matl_cat="test_metal_4"))
    
    assert mt.generate_matl_index(matl_list, "all")==["test_6061","test_7075","test_4140","test_316"]
    assert mt.generate_matl_index(matl_list, "All")==["test_6061","test_7075","test_4140","test_316"]
    assert mt.generate_matl_index(matl_list, "test_Aluminum")==["test_6061","test_7075"]
    assert mt.generate_matl_index(matl_list, "test_Steel")==["test_4140"]

def test_generate_matl_type_index():
    matl_list=[]
    matl_list.append(mt.material(matl_label="test_6061", matl_type="test_Aluminum", matl_cat="test_metal_1"))
    matl_list.append(mt.material(matl_label="test_7075", matl_type="test_Aluminum", matl_cat="test_metal_1"))   
    matl_list.append(mt.material(matl_label="test_4140", matl_type="test_Steel", matl_cat="test_metal_2"))
    matl_list.append(mt.material(matl_label="test_316", matl_type="test_Stainless Steel", matl_cat="test_metal_3"))
    matl_list.append(mt.material(matl_label="test_316", matl_type="test_Stainless Steel", matl_cat="test_metal_4"))
    
    assert mt.generate_matl_type_index(matl_list)==["All","test_Aluminum","test_Steel","test_Stainless Steel"]