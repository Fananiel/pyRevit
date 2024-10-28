# -*- coding: utf-8 -*-
__title__   = "Maße Tür"
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

selected_views = forms.select_views()

#Ebenen

filter_cats       = ISelectionFilter_Categories([BuiltInCategory.OST_Levels])
Ebene_0 = selection.PickObject(ObjectType.Element, filter_cats, "Wählen sie die Ebene einer Haltestelle!")
moobject = selection.PickObject(ObjectType.Face, "Wählen sie die Oberkante der MÖH")


# Reference Arrays
ref = ReferenceArray()
ref.Append(moobject)
ref.Append(Ebene_0)

# Pick point for dimline

selected_point = selection.PickPoint("Platzieren sie die Maßlinien")
point_2 = selected_point + XYZ(0,0,10)
dimline = Line.CreateBound(selected_point, point_2)

offset = convert_internal_units(0.5, True, 'm')
dimline_sh = dimline.CreateOffset(offset, XYZ(-1, 0, 0))

# Transaction

t = Transaction(doc, __title__)
t.Start()
try:
    #Changes
    MOH_Dim = doc.Create.NewDimension(doc.ActiveView, dimline, ref) #type: Dimension
    MOH_Dim.Prefix = "MÖH"

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

