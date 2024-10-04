# -*- coding: utf-8 -*-
__title__   = "03.02 - Element Properties"
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

rvt_year = int(app.VersionNumber)
selection = uidoc.Selection                     #type: Selection



# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝
#==================================================

ref_picked_object = selection.PickObject(ObjectType.Element)
elem = doc.GetElement(ref_picked_object)

level_id = elem.LevelId
level = doc.GetElement(level_id)

if type(elem) != Room:
    print('This is not a Room. Please Select a room!')
    import sys
    sys.exit()

if elem.GroupId ==ElementId(-1):
    group = 'None'
else:
    group = elem.GroupId

# Prints
print('ElementID: {}'.format(elem.Id))
print('GroupID: {}'.format(group))
print("Category: {}".format(elem.Category.Name))
print("Category: {}".format(elem.Category.BuiltInCategory))
print("Level: {}".format(level.Name))
print('XYZ: {}'.format(elem.Location.Point))
print('Area: {}'.format(elem.Area))
print('Number: {}'.format(elem.Number))
print('Perimeter: {}'.format(elem.Perimeter))

perimeter_m = convert_internal_units(elem.Perimeter, get_internal=False)
area_m = convert_internal_units(elem.Area, get_internal=False, unit='m2')
print('#'*10)
print('Area: {} m2'.format(area_m))
print('Perimeter: {} m'.format(perimeter_m))

