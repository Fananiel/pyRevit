# -*- coding: utf-8 -*-
__title__   = "Maße Höhe"
__doc__     = """Version = 2.0
Date    = 26.03.2025
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

view = doc.ActiveView

#Ebenen

# Schachtgrube
ebenen  = FilteredElementCollector(doc, view.Id).OfCategory(BuiltInCategory.OST_Levels).WhereElementIsNotElementType().ToElements()
Ebene_SG = [eb for eb in ebenen if eb.Name == 'Schachtgrube']

if len(Ebene_SG) == 0:
    forms.alert('Die Ebene Schachtgrube wurde nicht gefunden.', exitscript=True)

Ebene_SG = Ebene_SG[0].GetPlaneReference()

# Schachtkopf
Ebene_SK = [eb for eb in ebenen if eb.Name == 'Schachtkopf']

if len(Ebene_SK) == 0:
    forms.alert('Die Ebene Schachtkopf wurde nicht gefunden.', exitscript=True)

Ebene_SK = Ebene_SK[0].GetPlaneReference()

cats = ISelectionFilter_Categories([BuiltInCategory.OST_Levels])
Ebene_0 = selection.PickObject(ObjectType.Element, cats,'Wählen sie die untere Haltestelle')
Ebene_1 = selection.PickObject(ObjectType.Element, cats,'Wählen sie die obere Haltestelle')

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

Test_ref = ReferenceArray()
Test_ref.Append(Ebene_SG)
Test_ref.Append(Ebene_0)
Test_ref.Append(Ebene_1)
Test_ref.Append(Ebene_SK)

"""
# Let user pick a view
selected_view = forms.select_views(title='Select View', multiple=False)
if not selected_view:
    print("No view was selected. Exiting.")
    import sys
    sys.exit()

print("Selected view: {}".format(selected_view.Title))
print(selected_view.Origin)
print(selected_view.SketchPlane)
print(selected_view.CropBox)


# Referenzebene auswählen
filter_cats_ref = ISelectionFilter_Categories([BuiltInCategory.OST_CLines])
Ebene_ref = selection.PickObject(ObjectType.Element, filter_cats_ref, "Wählen sie die Referenzebene!")
elem = doc.GetElement(Ebene_ref)
print(elem.Direction)



"""
# points for dimline

view_origin = view.Origin
view_rdir = view.RightDirection
view_udir = view.UpDirection
view_cp = view.CropBox

point_1 = view_cp.Max - 5 * view_rdir

#point_1 = view_origin
point_2 = point_1 + 10 * view_udir

dimline = Line.CreateBound(point_1, point_2)

offset = convert_internal_units(0.5, True, 'm')
dimline_sh = dimline.CreateOffset(offset, XYZ(1,0,0))
dimline_test = dimline_sh.CreateOffset(offset, XYZ(1,0,0))


# Transaction
t = Transaction(doc, __title__)
t.Start()
try:
    #Changes

    SH_Dim = doc.Create.NewDimension(doc.ActiveView, dimline_sh, SH_ref)  # type: Dimension
    SH_Dim.Prefix = "SH"

    test_dim = doc.Create.NewDimension(doc.ActiveView, dimline, Test_ref)  # type: Dimension
    segments = test_dim.Segments
    count = 0
    prefixes = ["HSG", "FH", "HSK"]
    for seg in segments:
        seg.Prefix = prefixes[count]
        count += 1

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

