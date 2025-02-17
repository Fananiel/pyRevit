# -*- coding: utf-8 -*-
__title__   = "Kommentare ausrichten"
__doc__     = """Version = 1.0
Date    = 10.02.2025
________________________________________________________________
Description:

Align Text Notes

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
from Snippets._selection import ISelectionFilter_Categories

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


# Functions

def move_textnote(elem):
    x2 = elem.Coord.X

    x_vector = x1 - x2

    trans_vector = XYZ(x_vector, 0, 0)

    leaders = elem.GetLeaders()
    leader_ends = []
    for leader in leaders:
        leader_ends.append(leader.End)

    # Start transaction
    t = Transaction(doc, __title__)
    t.Start()

    elem.Location.Move(trans_vector)
    leaders = elem.GetLeaders()
    count = 0
    for leader in leaders:
        try:
            leader.End = leader_ends[count]
        except Exception as e:
            print(e)
        count += 1

    t.Commit()


# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝
#==================================================

# Get Active View and View Type
active_view  = doc.ActiveView

filter_cats_ref = ISelectionFilter_Categories([BuiltInCategory.OST_TextNotes])
Text_ref = selection.PickObject(ObjectType.Element, filter_cats_ref, "Wählen sie einen Kommentar als Referenz!")
Text1 = doc.GetElement(Text_ref)

x1 = Text1.Coord.X

filter_cats_ref = ISelectionFilter_Categories([BuiltInCategory.OST_TextNotes])
Text_ref_2 = selection.PickObjects(ObjectType.Element, filter_cats_ref, "Wählen sie die zu verschiebenden Kommentare!")

for ref in Text_ref_2:
    elem = doc.GetElement(ref)
    move_textnote(elem)

