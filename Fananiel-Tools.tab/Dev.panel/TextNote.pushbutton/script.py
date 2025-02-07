# -*- coding: utf-8 -*-
__title__   = "Text Note"
__doc__     = """Version = 1.0
Date    = 04.02.2025
________________________________________________________________
Description:

Place a Text Note

________________________________________________________________
How-To:
-> Click on the button

________________________________________________________________
TODO:
[FEATURE] - Describe Your ToDo Tasks Here
________________________________________________________________
Last Updates:
- [04.02.2025] v1.0 Release
________________________________________________________________
Author: Daniel Förster"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
#==================================================
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import *

# pyRevit
from pyrevit import revit, forms

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝
#==================================================
app    = __revit__.Application
uidoc  = __revit__.ActiveUIDocument
doc    = __revit__.ActiveUIDocument.Document #type:Document
selection = uidoc.Selection                     #type: Selection


# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝
#==================================================

active_view  = doc.ActiveView

# Get all text types in document
text_types = FilteredElementCollector(doc).OfClass(TextNoteType).ToElements()
tt_names = {}
names = []

for type in text_types:
    name = Element.Name.__get__(type)
    names.append(name)
    tt_names[name] = type

# Let user select one text type
ops = names
res = forms.SelectFromList.show(ops,
                                multiselect=False,
                                button_name='Select Text type')
text_type = tt_names[res]
text_type_id = text_type.Id

# Let user select an object
ref_picked_object = selection.PickObject(ObjectType.Element)
picked_object = doc.GetElement(ref_picked_object)

# Get Text from Parameter Plantext
text = picked_object.LookupParameter('Beschriftungstext').AsValueString()

# Get Point of Element
bb = picked_object.get_BoundingBox(active_view)
bb_min = bb.Min
bb_max = bb.Max

print(bb_min)
print(bb_max)

text_pos = bb_max + XYZ(10,0,0)

# Start transaction
t = Transaction(doc, __title__)
t.Start()

# CREATE TEXT NOTE
TextNote.Create(doc, active_view.Id, text_pos, text, text_type_id)
#note = TextNote.AddLeader()

t.Commit()
