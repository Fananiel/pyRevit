# -*- coding: utf-8 -*-
__title__ = "Spot Elevation"
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
from Snippets._selection import ISelectionFilter_Categories
from Snippets._convert import convert_internal_units

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

work_planes = {}

# Get all levels
level_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Levels).WhereElementIsNotElementType()
for level in level_collector:
    name = "Ebene: {0}".format(level.Name)
    work_planes[name] = level

# Let user select the level
selected_plane_name = forms.SelectFromList.show(
    sorted(work_planes.keys()),
    title='Select Reference Plane',
    multiselect=False
)

if not selected_plane_name:
    forms.alert('No reference plane selected.', exitscript=True)

selected_level = work_planes[selected_plane_name]
level_ref = Reference(selected_level)

# Select point where to place spot elevation
point_ref = selection.PickPoint("Select point for spot elevation")

object_ref = selection.PickObject(ObjectType.Edge)

# Get active view
active_view = doc.ActiveView

# Transaction to create spot elevation
t = Transaction(doc, __title__)
t.Start()
try:
    # Create spot elevation
    spot_elevation = doc.Create.NewSpotElevation(
        active_view,  # View to place the spot elevation
        object_ref,  # Reference object
        point_ref,  # Reference point
        point_ref + XYZ(1, 2, 0),  # Bend point (offset from location)
        point_ref + XYZ(2, 0, 0),  # End point (where text will be placed)
        point_ref,  # Reference point
        True  # Whether to use bottom elevation
    )

    t.Commit()
except Exception as e:
    print("Error creating spot elevation:", str(e))
    t.RollBack()

