# -*- coding: utf-8 -*-
__title__   = "Mitten AZ"
__doc__     = """Version = 1.0
Date    = 14.02.2025
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

# Active View
active_view  = doc.ActiveView
active_level = active_view.GenLevel

# All view types
view_types = FilteredElementCollector(doc).OfClass(ViewFamilyType).ToElements()

# Filter view types
view_types_sections     =   [vt for vt in view_types if vt.ViewFamily == ViewFamily.Section]
view_types_plan         =   [vt for vt in view_types if vt.ViewFamily == ViewFamily.FloorPlan]

#Ebenen für AZ Mitte wählen
filter_cats       = ISelectionFilter_Categories([BuiltInCategory.OST_CLines])
m_az_bs           = selection.PickObject(ObjectType.Element, filter_cats, "Wählen sie Mitte AZ BS")
m_az_ts           = selection.PickObject(ObjectType.Element, filter_cats, "Wählen sie Mitte AZ TS")

#Mittelpunkt wählen
mid = selection.PickPoint()

m_az_bs = doc.GetElement(m_az_bs)
m_az_ts = doc.GetElement(m_az_ts)

plane = m_az_bs.GetPlane()

normal = plane.Normal
xvec = plane.XVec
yvec = plane.YVec


# Create Transform
trans        = Transform.Identity
trans.Origin = mid

trans.BasisX = xvec
trans.BasisY = yvec
trans.BasisZ = normal

# Create SectionBox
sectionBox           = BoundingBoxXYZ()
sectionBox.Transform = trans

# Offset
bs = 2.2 + 1.5
ts = 2.75 + 1.5
sk = 4
fh = 7
sg = 1.4

ts_feet = convert_internal_units(ts)
sk_feet = convert_internal_units(sk)
sh_feet = convert_internal_units(fh+sg)


sectionBox.Min = XYZ(-(ts_feet/2)  , -sh_feet     , 0)
sectionBox.Max = XYZ(ts_feet/2  , sk_feet     , 5)
                    # Left/Right  Up/Down   Forward/Backwards

# Transaction
t = Transaction(doc, __title__)
t.Start()

# Create Section
view_type_section_id = doc.GetDefaultElementTypeId(ElementTypeGroup.ViewTypeSection)
view_section = ViewSection.CreateSection(doc, view_type_section_id, sectionBox)

t.Commit()