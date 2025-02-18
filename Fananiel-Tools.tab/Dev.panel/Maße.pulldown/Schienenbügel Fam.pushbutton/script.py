# -*- coding: utf-8 -*-
__title__   = "Schienenbügel Fam"
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

view = doc.ActiveView

# Schienenbügel filtern

all_allgmodel   = FilteredElementCollector(doc, view.Id).OfCategory(BuiltInCategory.OST_SpecialityEquipment).ToElements()
all_brackets    = [m for m in all_allgmodel if check_type(m,"LDXRailBracket")]

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

