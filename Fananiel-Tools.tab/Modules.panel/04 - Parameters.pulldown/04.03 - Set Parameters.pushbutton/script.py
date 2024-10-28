# -*- coding: utf-8 -*-
__title__   = "04.03 - Set Parameters"
__doc__     = """Version = 1.0
Date    = 10.10.2024
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

# Pick Object
ref_picked_object = selection.PickObject(ObjectType.Element)
picked_object     = doc.GetElement(ref_picked_object)

# Get Built-In Parameters
comments = picked_object.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS)
mark     = picked_object.get_Parameter(BuiltInParameter.ALL_MODEL_MARK)
el_type  = picked_object.get_Parameter(BuiltInParameter.ELEM_TYPE_PARAM)
area     = picked_object.get_Parameter(BuiltInParameter.HOST_AREA_COMPUTED)
b_offset = picked_object.get_Parameter(BuiltInParameter.WALL_BASE_OFFSET)


# Get Shared/Project Parameters
p_text     = picked_object.LookupParameter("p_text")
s_bool     = picked_object.LookupParameter("s_bool")
s_material = picked_object.LookupParameter("s_material")
s_number   = picked_object.LookupParameter("s_number")
s_area     = picked_object.LookupParameter("s_area")

# Set Parameter Values
with Transaction(doc, __title__) as t:
    t.Start()

    comments.Set('Random comment')
    mark.Set(str(picked_object.Id))
    el_type.Set(ElementId(712306))
    b_offset.Set(-1.5)
    p_text.Set('some text')
    s_bool.Set(1)
    s_material.Set(ElementId(1204710))
    s_number.Set(15.55)
    s_area.Set(15.55)

    t.Commit()

