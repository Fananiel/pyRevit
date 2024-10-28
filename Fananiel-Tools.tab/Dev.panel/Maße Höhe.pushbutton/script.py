# -*- coding: utf-8 -*-
__title__   = "Maße Höhe"
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

filter_cats       = ISelectionFilter_Categories([BuiltInCategory.OST_Levels])
Ebene_SG = selection.PickObject(ObjectType.Element, filter_cats, "Wählen sie die Ebene der Schachtgrube!")
Ebene_0 = selection.PickObject(ObjectType.Element, filter_cats, "Wählen sie die Ebene der unteren Haltestelle!")
Ebene_1 = selection.PickObject(ObjectType.Element, filter_cats, "Wählen sie die Ebene der oberen Haltestelle!")
Ebene_SK = selection.PickObject(ObjectType.Element, filter_cats, "Wählen sie die Ebene des Schachtkopfs!")


# Reference Arrays

SG_ref = ReferenceArray()
SG_ref.Append(Ebene_SG)
SG_ref.Append(Ebene_0)

FH_ref = ReferenceArray()
FH_ref.Append(Ebene_0)
FH_ref.Append(Ebene_1)

SK_ref = ReferenceArray()
SK_ref.Append(Ebene_1)
SK_ref.Append(Ebene_SK)

SH_ref = ReferenceArray()
SH_ref.Append(Ebene_SG)
SH_ref.Append(Ebene_SK)


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
    SG_Dim = doc.Create.NewDimension(doc.ActiveView, dimline, SG_ref) #type: Dimension
    SG_Dim.Prefix = "HSG"

    FH_Dim = doc.Create.NewDimension(doc.ActiveView, dimline, FH_ref)  # type: Dimension
    FH_Dim.Prefix = "FH"

    SK_Dim = doc.Create.NewDimension(doc.ActiveView, dimline, SK_ref)  # type: Dimension
    SK_Dim.Prefix = "HSK"

    SH_Dim = doc.Create.NewDimension(doc.ActiveView, dimline_sh, SH_ref)  # type: Dimension
    SH_Dim.Prefix = "SH"

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

