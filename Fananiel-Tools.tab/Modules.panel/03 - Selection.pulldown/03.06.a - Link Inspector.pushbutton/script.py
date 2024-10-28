# -*- coding: utf-8 -*-
__title__     = "Link Inspector"
__author__    = "Mohamed Bedair"
__doc__       = """Version = 1.0
Date    = 21.12.2023
_____________________________________________________________________
Description:
Select Linked Elements based on selected in UI:
- Revit Linked Project
- Element Categories 
_____________________________________________________________________
How-to:
-> Run the script
-> Select Linked Revit Project
-> Select Revit Categories
-> Pick Linked Elements matching selected criteria
_____________________________________________________________________
Last update:
- [21.12.2023] - 1.0 RELEASE
_____________________________________________________________________
Author: Mohamed Bedair"""
#--------------------------------------------------------------------
#⬇️ IMPORTS
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import *
from pyrevit import forms


#--------------------------------------------------------------------
#📦VARIABLES
doc         = __revit__.ActiveUIDocument.Document   #type: Document
uidoc       = __revit__.ActiveUIDocument
selection   = uidoc.Selection                       #type: Selection


# MAIN
#--------------------------------------------------------------------
#👉 Get All Linked Documents
all_rvt_links  = FilteredElementCollector(doc)\
                    .OfCategory(BuiltInCategory.OST_RvtLinks)\
                    .WhereElementIsNotElementType()\
                    .ToElements()       #type: List[RevitLinkInstance]

# Prepare Dict {doc.Title: RvtLinkInstance}
dict_rvt_links = {lnk.GetLinkDocument().Title : lnk for lnk in all_rvt_links}
link_names     = dict_rvt_links.keys()

#📰 UI - Select Linked Revit Project
selected_lnk_name = forms.ask_for_one_item(link_names,
                                    default=link_names[0],
                                    prompt="Select Link",
                                    title="Link Selection")
selected_lnk = dict_rvt_links[selected_lnk_name]
#--------------------------------------------------------------------
#  UI - Select Categories
all_cats    = sorted([cat.Name for cat in doc.Settings.Categories])
chosen_cats = forms.SelectFromList.show(all_cats, title="Choose Categories",
                                                  width=300,
                                                  button_name="Select Categories",
                                                  multiselect=True)

#--------------------------------------------------------------------
#🔎 Create ISelectionFilter
class LinkedElemSelectionFilter(ISelectionFilter):
    def AllowElement(self, element):
        return True

    def AllowReference(self, reference, position):
        linked_doc          = selected_lnk.GetLinkDocument()
        linked_elem         = linked_doc.GetElement(reference.LinkedElementId)
        if linked_elem.Category.Name in chosen_cats:
            return True


#--------------------------------------------------------------------
#👉 Pick Linked Objects
ref_picked_objects = selection.PickObjects(ObjectType.LinkedElement,LinkedElemSelectionFilter())

for ref in ref_picked_objects:
    linked_doc          = selected_lnk.GetLinkDocument()
    linked_elem         = linked_doc.GetElement(ref.LinkedElementId)
    print(linked_elem)

#--------------------------------------------------------------------
# Keep improving this code!