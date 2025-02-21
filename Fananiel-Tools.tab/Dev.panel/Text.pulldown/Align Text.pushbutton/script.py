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

def get_tvector_from_direction(direction_vector, x1, x2):
    """
    Returns the coordinate of position_vector that corresponds to direction_vector

    Args:
        direction_vector: XYZ vector that is either (1,0,0), (0,1,0) or (0,0,1)
        position_vector: XYZ vector with coordinates (x,y,z)

    Returns:
        float: The x, y or z coordinate depending on direction_vector
    """
    if direction_vector.X == 1 or direction_vector.X == -1:
        v = XYZ(x1.X - x2.X, 0, 0)
        return v
    elif direction_vector.Y == 1 or direction_vector.Y == -1:
        v = XYZ(0, x1.Y - x2.Y, 0)
        return v
    elif direction_vector.Z == 1 or direction_vector.Z == -1:
        v = XYZ(0, 0, x1.Z - x2.Z)
        return v
    else:
        raise ValueError("Direction vector must be (1,0,0), (0,1,0) or (0,0,1)")

def move_textnote(elem, Text1, view_direction):

    x2 = elem.Coord
    x1 = Text1.Coord
    trans_vector = get_tvector_from_direction(view_direction, x1, x2)

    leaders = elem.GetLeaders()
    leader_ends = []
    for leader in leaders:
        leader_ends.append(leader.End)

    # Start transaction
    t = Transaction(doc, __title__)
    t.Start()

    try:
        elem.Location.Move(trans_vector)
        leaders = elem.GetLeaders()
        count = 0
        for leader in leaders:
            try:
                leader.End = leader_ends[count]
            except Exception as e:
                print(e)
            count += 1
    except Exception as e:
        print(e)

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

view_direction = active_view.RightDirection

filter_cats_ref = ISelectionFilter_Categories([BuiltInCategory.OST_TextNotes])
Text_ref_2 = selection.PickObjects(ObjectType.Element, filter_cats_ref, "Wählen sie die zu verschiebenden Kommentare!")

for ref in Text_ref_2:
    elem = doc.GetElement(ref)
    move_textnote(elem, Text1, view_direction)

