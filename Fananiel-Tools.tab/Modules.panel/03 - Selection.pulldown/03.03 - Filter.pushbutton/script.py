# -*- coding: utf-8 -*-
__title__   = "03.03 - Filter"
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

#1️⃣ ISelectionFilter - Classes
# filter_types    = ISelectionFilter_Classes([Room, RoomTag])
# selected_elements_ = selection.PickObjects(ObjectType.Element, filter_types)
#
el_list = []
# for ref in selected_elements_:
#     el_list.append(doc.GetElement(ref))

#2️⃣ ISelectionFilter - Categories
filter_cats       = ISelectionFilter_Categories([BuiltInCategory.OST_Walls])
selected_elements = selection.PickObjects(ObjectType.Element, filter_cats)

for ref in selected_elements:
    el_list.append(doc.GetElement(ref))

print(el_list)
