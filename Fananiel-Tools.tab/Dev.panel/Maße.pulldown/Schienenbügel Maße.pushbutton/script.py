# -*- coding: utf-8 -*-
__title__   = "Schienenbügel Maße"
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

# classes
class FamilyLoadOptions(IFamilyLoadOptions):
    'A Class implementation for loading families'

    def OnFamilyFound(self, familyInUse, overwriteParameterValues):
        'Defines behavior when a family is found in the model.'
        overwriteParameterValues = True
        return True

    def OnSharedFamilyFound(self, sharedFamily, familyInUse, source, overwriteParameterValues):
        'Defines behavior when a shared family is found in the model.'
        source = FamilySource.Project
        # source = FamilySource.Family
        overwriteParameterValues = True
        return True

# Functions

def check_type(element, keyword):
    el_type = element.get_Parameter(BuiltInParameter.ELEM_TYPE_PARAM).AsValueString()
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
all_brackets    = [m for m in all_allgmodel if check_type(m,"LDXRailBracket")]

if len(all_brackets) == 0:
    forms.alert('Es wurden keine Schienenbügel gefunden.', exitscript=True)

# Famdoc for each bracket
for brack in all_brackets:
    fam_id = (brack.get_Parameter(BuiltInParameter.ELEM_FAMILY_PARAM).AsElementId())
    fam_sym = doc.GetElement(fam_id)
    fam = fam_sym.Family
    famdoc = doc.EditFamily(fam)

    # Get Ref Planes
    all_refplanes = FilteredElementCollector(famdoc).OfCategory(BuiltInCategory.OST_CLines).ToElements()

    #Modify the center elevation
    for rp in all_refplanes:
        if rp.Normal.Z == 1:
            ref_name = rp.LookupParameter('Ist eine Referenz')
            ref_name.Set(int(7))

    opt = FamilyLoadOptions()

    family = famdoc.LoadFamily(doc, opt)

# Z-Referenz der Schienenbügel auslesen

elevations = []
for b in all_brackets:
    refs = b.GetReferences(FamilyInstanceReferenceType.CenterElevation)
    if refs:
        elevations.append(refs[0])

print(elevations)

filter_cats       = ISelectionFilter_Categories([BuiltInCategory.OST_Levels])
Ebene_SG = selection.PickObject(ObjectType.Element, filter_cats, "Wählen sie die Ebene der Schachtgrube!")


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
