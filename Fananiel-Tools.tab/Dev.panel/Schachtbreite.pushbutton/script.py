# -*- coding: utf-8 -*-
__title__   = "Schachtbreite"
__doc__     = """Version = 1.0
Date    = 28.10.2024
________________________________________________________________
Author: Daniel Förster"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
#==================================================
from Autodesk.Revit.DB import *
from pyrevit import forms
from Autodesk.Revit.UI.Selection import *
from Snippets._selection import ISelectionFilter_Categories
from Snippets._convert import convert_internal_units

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

#Ebenen

Schacht_l = selection.PickObject(ObjectType.Face, "Wählen sie die linke Seite des Schachts")
Schacht_r    = selection.PickObject(ObjectType.Face, "Wählen sie die rechte Seite des Schachts")

filter_cats       = ISelectionFilter_Categories([BuiltInCategory.OST_CLines])
Schacht_m    = selection.PickObject(ObjectType.Element, filter_cats, "Wählen sie die Mitte des Schachts")


# Reference Arrays
ref = ReferenceArray()
ref.Append(Schacht_l)
ref.Append(Schacht_r)

ref1 = ReferenceArray()
ref1.Append(Schacht_l)
ref1.Append(Schacht_m)

ref2 = ReferenceArray()
ref2.Append(Schacht_m)
ref2.Append(Schacht_r)

# Pick point for dimline

selected_point = selection.PickPoint("Platzieren sie die Maßlinien")
point_2 = selected_point + XYZ(0, 10, 0)
dimline = Line.CreateBound(selected_point, point_2)

offset = convert_internal_units(0.5, True, 'm')
dimline_2 = dimline.CreateOffset(offset, XYZ(-1, 0, 0))

# Transaction

t = Transaction(doc, __title__)
t.Start()
try:
    #Changes
    TS_Dim = doc.Create.NewDimension(doc.ActiveView, dimline, ref) #type: Dimension
    TS_Dim.Prefix = "TS"

    TS1_Dim = doc.Create.NewDimension(doc.ActiveView, dimline_2, ref1)  # type: Dimension
    TS1_Dim.Prefix = "Mitte Aufzug"

    TS2_Dim = doc.Create.NewDimension(doc.ActiveView, dimline_2, ref2)  # type: Dimension

    t.Commit()
except:
    t.RollBack()


###########################################################################################

#selected_views = forms.select_views()

# # Get Levels
# levels = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Levels)
#
# # OfClass
# levels_ = FilteredElementCollector(doc).OfClass(Level).ToElements()

# for level in levels_:
#     levels_ref.Append(level.GetPlaneReference())

