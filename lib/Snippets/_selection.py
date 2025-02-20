# -*- coding: utf-8 -*-

# Imports
# ==================================================
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import ISelectionFilter, Selection

# Variables
# ==================================================
app    = __revit__.Application
uidoc  = __revit__.ActiveUIDocument
doc    = __revit__.ActiveUIDocument.Document #type:Document
selection = uidoc.Selection # type: Selection


# Functions
def get_selected_elements(filter_types=None):
    """Get Selected Elements in Revit UI.
    You can provide a list of types for filter_types parameter (optionally)

    e.g.
    sel_walls = get_selected_elements([Wall])"""
    selected_element_ids = uidoc.Selection.GetElementIds()
    selected_elements = [doc.GetElement(e_id) for e_id in selected_element_ids]

    # Filter Selection (Optionally)
    if filter_types:
        return [el for el in selected_elements if type(el) in filter_types]
    return selected_elements


# ISelectionFilter
class ISelectionFilter_Classes(ISelectionFilter):
    def __init__(self, allowed_types):
        """ ISelectionFilter made to filter with types
        :param allowed_types: list of allowed Types"""
        self.allowed_types = allowed_types

    def AllowElement(self, element):
        if type(element) in self.allowed_types:
            return True

class ISelectionFilter_Categories(ISelectionFilter):
    def __init__(self, allowed_categories):
        """ ISelectionFilter made to filter with categories
        :param allowed_types: list of allowed Categories"""
        self.allowed_categories = allowed_categories

    def AllowElement(self, element):
        # ❌ Category.BuiltInCategory is not available in all Revit Versions
        if element.Category.BuiltInCategory in self.allowed_categories:
            return True

        # ✅ Let's use Category.Id instead
        # self.allowed_categories = [ElementId(bic) for bic in self.allowed_categories]
        # if element.Category.Id in self.allowed_categories:
        #     return True


def check_type(element, keyword):
    el_type = element.get_Parameter(BuiltInParameter.ELEM_TYPE_PARAM).AsValueString()
    if keyword.lower() in el_type.lower():
        return True