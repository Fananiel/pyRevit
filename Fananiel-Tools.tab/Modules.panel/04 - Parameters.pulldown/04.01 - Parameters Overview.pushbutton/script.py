# -*- coding: utf-8 -*-
__title__   = "04.01 - Parameters Overview"
__doc__     = """Version = 1.0
Date    = 08.10.2024
________________________________________________________________
Author: Daniel Förster"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
#==================================================
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import ObjectType, Selection
from Snippets._parameters import get_param_value

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝
#==================================================
uidoc  = __revit__.ActiveUIDocument
doc    = __revit__.ActiveUIDocument.Document    #type:Document
selection = uidoc.Selection                     #type: Selection

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝
#==================================================

# Pick object

ref_picked_object = selection.PickObject(ObjectType.Element)
picked_object = doc.GetElement(ref_picked_object)
#print(picked_object.Parameters)

for p in picked_object.Parameters:
    print('Name: {}'.format(p.Definition.Name))
    print('ParameterGroup: {}'.format(p.Definition.ParameterGroup))
    print('BuiltInParameter: {}'.format(p.Definition.BuiltInParameter))
    print('IsReadOnly: {}'.format(p.IsReadOnly))
    print('HasValue: {}'.format(p.HasValue))
    print('IsShared: {}'.format(p.IsShared))
    print('StorageType: {}'.format(p.StorageType))
    print('Value: {}'.format(get_param_value(p)))
    print('AsValueString: {}'.format(p.AsValueString()))
    print('-'*100)

