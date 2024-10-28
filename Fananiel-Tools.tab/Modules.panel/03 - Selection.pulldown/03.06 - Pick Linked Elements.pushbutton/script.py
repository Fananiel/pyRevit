# -*- coding: utf-8 -*-
__title__   = "03.06 - Pick Linked Elements"
__doc__     = """Version = 1.0
Date    = 08.10.2024
________________________________________________________________
Author: Daniel Förster"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
#==================================================
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import Room
from Autodesk.Revit.UI.Selection import ObjectType, Selection, ISelectionFilter

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝
#==================================================
uidoc  = __revit__.ActiveUIDocument
doc    = __revit__.ActiveUIDocument.Document    #type:Document
selection = uidoc.Selection                     #type: Selection

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝
#==================================================

# Pick Linked Objects - simple

# ref_picked_objects  = selection.PickObjects(ObjectType.LinkedElement)
# picked_objects      = [doc.GetElement(ref) for ref in ref_picked_objects]
#
# for el in picked_objects:
#     print(el)

# Read Linked Element

# ref_picked_objects  = selection.PickObjects(ObjectType.LinkedElement)
#
# for ref in ref_picked_objects:
#     revit_link_instance = doc.GetElement(ref)
#     linked_doc          = revit_link_instance.GetLinkDocument()
#     linked_el           = linked_doc.GetElement(ref.LinkedElementId)
#     print(linked_el)

# Limit Linked Selection (ISelectionFilter for Linked Models)

class LinkedRoomSelectionFilter(ISelectionFilter):
    def AllowElement(self, elem):
        return True

    def AllowReference(self, ref, position):
        revit_link_instance = doc.GetElement(ref)
        linked_doc          = revit_link_instance.GetLinkDocument()
        linked_el           = linked_doc.GetElement(ref.LinkedElementId)

        if type(linked_el) == Room:
            return True


# Pick and Read Linked Elements with ISelectionFilter
ref_picked_objects = selection.PickObjects(ObjectType.LinkedElement, LinkedRoomSelectionFilter()) #type: List[Reference]


for ref in ref_picked_objects:
    revit_link_instance = doc.GetElement(ref)
    linked_doc          = revit_link_instance.GetLinkDocument()
    linked_el           = linked_doc.GetElement(ref.LinkedElementId)
    print(linked_el)