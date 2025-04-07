# -*- coding: utf-8 -*-
__title__   = "Ankerschienen Maße"
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
from Snippets._parameters import get_param_value
from Snippets._convert import convert_internal_units


# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝
#==================================================
app    = __revit__.Application
uidoc  = __revit__.ActiveUIDocument
doc    = __revit__.ActiveUIDocument.Document    #type:Document
selection = uidoc.Selection                     #type: Selection


def check_family(element, keyword):
    el_type = element.get_Parameter(BuiltInParameter.ELEM_FAMILY_PARAM).AsValueString()
    if keyword.lower() in el_type.lower():
        return True


# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝
#==================================================
# Ansicht
view = doc.ActiveView


# Bemaßungsstil
dim_type_group = ElementTypeGroup.SpotElevationType
p = BuiltInParameter.ALL_MODEL_TYPE_NAME
alle_stile = FilteredElementCollector(doc).WhereElementIsElementType().ToElements()
bm_stil = [dt for dt in FilteredElementCollector(doc).OfClass(DimensionType) if dt.get_Parameter(p).AsString() == 'Standard 3mm'][0]

# Schienenbügel filtern

all_allgmodel   = FilteredElementCollector(doc, view.Id).OfCategory(BuiltInCategory.OST_GenericModel).WhereElementIsNotElementType().ToElements()
all_brackets    = [m for m in all_allgmodel if check_family(m,"DB_Ankerschiene")]

if len(all_brackets) == 0:
    forms.alert('Es wurden keine Schienenbügel gefunden.', exitscript=True)

# Z-Referenz der Schienenbügel auslesen

elevations = []
for b in all_brackets:
    sch_bef = b.LookupParameter("Schienenbügelbefestigung")
    if sch_bef:
        sch_bef = get_param_value(sch_bef)
        if sch_bef == 1:
            ref = b.GetReferenceByName('Mittenebene')
            if ref:
                elevations.append(ref)

# Ebenen filtern

ebenen  = FilteredElementCollector(doc, view.Id).OfCategory(BuiltInCategory.OST_Levels).WhereElementIsNotElementType().ToElements()
Ebene_SG = [eb for eb in ebenen if eb.Name == 'Schachtgrube']

if len(Ebene_SG) == 0:
    forms.alert('Die Ebene Schachtgrube wurde nicht gefunden.', exitscript=True)

Ebene_SG = Ebene_SG[0].GetPlaneReference()

# Reference Arrays

SG_ref = ReferenceArray()
SG_ref.Append(Ebene_SG)


for el in elevations:
    SG_ref.Append(el)

# curve for dimline

brack1 = all_brackets[0]
pos_b1 = brack1.get_BoundingBox(view).Max
point_1 = pos_b1 + XYZ(0, 20, 0)
point_2 = point_1 + XYZ(0, 0, 10)
dimline = Line.CreateBound(point_1, point_2)


# Transaction
t = Transaction(doc, __title__)
t.Start()
try:
    #Changes
    SG_Dim = doc.Create.NewDimension(view, dimline, SG_ref, bm_stil) #type: Dimension
    t.Commit()
except Exception as e:
    print(e)
    t.RollBack()

###########################################################################################
