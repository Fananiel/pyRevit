# -*- coding: utf-8 -*-
__title__   = "Winkel"
__doc__     = """Version = 1.0
Date    = 09.04.2025

Beschreibung: 

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

filter_cats       = ISelectionFilter_Categories([BuiltInCategory.OST_Lines])
d_line = selection.PickObject(ObjectType.Element, filter_cats, "Wählen sie eine Linie")
d_line = doc.GetElement(d_line)

filter_cats       = ISelectionFilter_Categories([BuiltInCategory.OST_CLines, BuiltInCategory.OST_Grids])
r_line = selection.PickObject(ObjectType.Element, filter_cats, "Wählen sie die Referenzebene")
r_line = doc.GetElement(r_line)

#filter_cats       = ISelectionFilter_Categories([BuiltInCategory.OST_RvtLinks])
#ifc = selection.PickObject(ObjectType.Element, filter_cats)
#ifc = doc.GetElement(ifc)

d_line_dir_vec = d_line.Location.Curve.Direction #type:XYZ
r_line_dir_vec = r_line.Direction #type:XYZ

winkel = d_line_dir_vec.AngleTo(r_line_dir_vec)

winkel_g = winkel * 180 / math.pi

forms.alert("Winkel: {}".format(winkel_g))

