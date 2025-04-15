# -*- coding: utf-8 -*-
__title__   = "IFC verschieben"
__doc__     = """Version = 1.0
Date    = 09.04.2025

________________________________________________________________
Author: Daniel Förster"""


# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
#==================================================
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import *
from Snippets._selection import *
import math
from pyrevit import forms


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

filter_cats       = ISelectionFilter_Categories([BuiltInCategory.OST_RvtLinks])
ifc = selection.PickObject(ObjectType.Element, filter_cats, "Wählen sie die IFC")
ifc = doc.GetElement(ifc)

point = selection.PickPoint('Wählen sie die Mitte des Schachts') #type: XYZ

#print(point.X, point.Y, point.Z)

trans_vec = XYZ(-point.X, -point.Y, 0)

t = Transaction(doc, __title__)
t.Start()

ifc.Location.Move(trans_vec)

t.Commit()