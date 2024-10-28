# -*- coding: utf-8 -*-
__title__   = "03.04 - Sum Rooms"
__doc__     = """Version = 1.0
Date    = 08.10.2024
________________________________________________________________
Author: Daniel Förster"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
#==================================================
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import Room, RoomTag
from Autodesk.Revit.UI.Selection import *
from Snippets._selection import ISelectionFilter_Classes, ISelectionFilter_Categories
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

# Get Rooms

selected_elements = [doc.GetElement(e_id) for e_id in selection.GetElementIds()]
selected_rooms = [el for el in selected_elements if type(el) == Room]

if not selected_rooms:
    filter_types = ISelectionFilter_Classes([Room])
    ref_picked_rooms = selection.PickObjects(ObjectType.Element, filter_types)
    selected_rooms = [doc.GetElement(ref) for ref in ref_picked_rooms]

if not selected_rooms:
    print('There were no Rooms selected. Please Try Again.')
    import sys
    sys.exit()

# Get Values
total = 0
for room in selected_rooms:
    room_name = room.get_Parameter(BuiltInParameter.ROOM_NAME).AsString()
    area_m2 = convert_internal_units(room.Area,get_internal=False, unit='m2')
    area_m2_rounded = round(area_m2, 2)

    total += area_m2_rounded

    print("{}: {}m2".format(room_name, area_m2_rounded))

# Print Results
print('-'*20)
print("Total: {}m2".format(total))
print("Selected {} Rooms".format(len(selected_rooms)))

