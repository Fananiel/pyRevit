# -*- coding: utf-8 -*-
__title__ = "Create Family Instance"
__doc__ = """Version = 1.0
Date    = 28.10.2024
________________________________________________________________
Author: Daniel Förster"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
# ==================================================
from Autodesk.Revit.DB import *
from pyrevit import forms
from Autodesk.Revit.UI.Selection import *

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝
# ==================================================
app = __revit__.Application
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document  # type:Document
selection = uidoc.Selection  # type: Selection

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝
# ==================================================

# Get elements from specified categories
work_planes = {}

# Get all levels
level_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Levels).WhereElementIsNotElementType()
for level in level_collector:
    name = "Ebene: {0}".format(level.Name)
    work_planes[name] = level

# Get all construction lines
cline_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_CLines).WhereElementIsNotElementType()
for cline in cline_collector:
    name = "Referenzebene: {0}".format(cline.Name)
    work_planes[name] = cline

if not work_planes:
    forms.alert('No levels or construction lines found in the document.', exitscript=True)

# Let user select the reference plane
selected_plane_name = forms.SelectFromList.show(
    sorted(work_planes.keys()),
    title='Select Reference Plane',
    multiselect=False
)

if not selected_plane_name:
    forms.alert('No reference plane selected.', exitscript=True)

selected_plane = work_planes[selected_plane_name]

# Get all family symbols in the project
collector = FilteredElementCollector(doc).OfClass(FamilySymbol)
family_symbols = {}

# Create dictionary of family symbols
for fs in collector:
    family_name = fs.FamilyName
    symbol_name = fs.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
    key = "{0} : {1}".format(family_name, symbol_name)
    family_symbols[key] = fs

# Let user select the family symbol
selected_symbol_name = forms.SelectFromList.show(
    sorted(family_symbols.keys()),
    title='Select Family Type',
    multiselect=False
)

if not selected_symbol_name:
    forms.alert('No family type selected.', exitscript=True)

family_symbol = family_symbols[selected_symbol_name]

# Start transaction
t = Transaction(doc, __title__)
t.Start()
try:

    # Create SketchPlane from selected element's ID
    sketch_plane = SketchPlane.Create(doc, selected_plane.Id)

    # Ensure the symbol is active
    if not family_symbol.IsActive:
        family_symbol.Activate()

    # Let user pick insertion point
    try:
        insertion_point = selection.PickPoint("Select insertion point for the family instance")

        # Create the family instance
        level = view.GenLevel
        new_instance = doc.Create.NewFamilyInstance(
            insertion_point,
            family_symbol,
            level,
            StructuralType.NonStructural
        )

    except Exception as pick_error:
        forms.alert('Error picking point: {0}'.format(str(pick_error)))
        t.RollBack()
        raise

    t.Commit()
except Exception as e:
    if t.HasStarted():
        t.RollBack()
    forms.alert('Error creating family instance: {0}'.format(str(e)))