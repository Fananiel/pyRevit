# -*- coding: utf-8 -*-
__title__   = "03.01 - Selection"
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

# 1. Get selected Elements
"""
selected_element_ids = selection.GetElementIds()

for e_id in selected_element_ids:
    print(e_id)
    e = doc.GetElement(e_id)
    print(e)

    if type(e) == Room:
        print("It's a room!")
    elif type(e) == Wall:
        print("It's a wall!")

"""

# 2. Pick Elements by rectangle

# selected_elements = selection.PickElementsByRectangle('Select some elements')
# print(selected_elements)


# 3. Pick object

# ref_picked_object = selection.PickObject(ObjectType.Element)
# picked_object = doc.GetElement(ref_picked_object)
# print(picked_object)


# 4. Pick Objects (Multiple)

#ref_picked_objects = selection.PickObjects(ObjectType.Element)
#picked_objects = [doc.GetElement(ref) for ref in ref_picked_objects]

"""
same as:
picked_objects = []

for ref in ref_picked_objects:
    e = doc.GetElement(ref)
    picked_objects.append(e)
"""

#for el in picked_objects:
    #print(el)


# 5. Pick Point

#selected_point = selection.PickPoint()
#print(selected_point)


# 6. PickBox

# picked_box = selection.PickBox(PickBoxStyle.Directional)
# print(picked_box)
# print(picked_box.Max)
# print(picked_box.Min)


# 7. Set Selection in Revit UI

new_selection = List[ElementId]()
new_selection.Add(ElementId(9771))
new_selection.Add(ElementId(9772))
new_selection.Add(ElementId(9773))
new_selection.Add(ElementId(9774))

selection.SetElementIds(new_selection)


#==================================================
