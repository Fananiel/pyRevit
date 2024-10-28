# -*- coding: utf-8 -*-
__title__   = "04.02 - Get Parameters"
__doc__     = """Version = 1.0
Date    = 04.10.2024
________________________________________________________________
Author: Daniel Förster"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
#==================================================
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import Room
from Autodesk.Revit.UI.Selection import *
from Snippets._parameters import get_param_value
from Snippets._convert import convert_internal_units

#.NET Imports
import clr
clr.AddReference('System')
from System.Collections.Generic import List


# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝
#==================================================
app    = __revit__.Application
uidoc  = __revit__.ActiveUIDocument
doc    = __revit__.ActiveUIDocument.Document    #type:Document
selection = uidoc.Selection                     #type: Selection

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝
#==================================================

#🔷 Pick Object
ref_picked_object = selection.PickObject(ObjectType.Element)
picked_object     = doc.GetElement(ref_picked_object)

# ✅ Get Built-In Parameters
comments = picked_object.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS)
mark     = picked_object.get_Parameter(BuiltInParameter.ALL_MODEL_MARK)
el_type  = picked_object.get_Parameter(BuiltInParameter.ELEM_TYPE_PARAM)
#area     = picked_object.get_Parameter(BuiltInParameter.HOST_AREA_COMPUTED)
#b_offset = picked_object.get_Parameter(BuiltInParameter.WALL_BASE_OFFSET)
height =    picked_object.get_Parameter(BuiltInParameter.INSTANCE_ELEVATION_PARAM)


# ✅ Get Shared/Project Parameters
# p_text     = picked_object.LookupParameter("p_text")
# s_bool     = picked_object.LookupParameter("s_bool")
# s_material = picked_object.LookupParameter("s_material")
# s_number   = picked_object.LookupParameter("s_number")
# s_area     = picked_object.LookupParameter("s_area")

def read_param(p):
    """Read properties of a Parameter"""
    print("Name: {}".format(p.Definition.Name))
    print("ParameterGroup: {}".format(p.Definition.ParameterGroup))
    print("BuiltInParameter: {}".format(p.Definition.BuiltInParameter))
    print("IsReadOnly: {}".format(p.IsReadOnly))
    print("HasValue: {}".format(p.HasValue))
    print("IsShared: {}".format(p.IsShared))
    print("StorageType: {}".format(p.StorageType))
    print("Value: {}".format(get_param_value(p)))
    if p == height:
        height_meters = convert_internal_units(get_param_value(p), get_internal=False, unit='m')
        print('Value in m: {}'.format(height_meters))
    print("AsValueString(): {}".format(p.AsValueString()))
    print('-'*100)


# 👀 READ PARAMETERS
read_param(comments)
read_param(mark)
read_param(el_type)
#read_param(area)
#read_param(b_offset)
#read_param(p_text)
#read_param(s_bool)
#read_param(s_material)
#read_param(s_number)
#read_param(s_area)
read_param(height)