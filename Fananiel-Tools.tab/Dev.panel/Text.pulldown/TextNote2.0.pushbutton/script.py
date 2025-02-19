# -*- coding: utf-8 -*-
__title__   = "Kommentare"
__doc__     = """Version = 2.0
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
from Snippets._convert import *

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


# View orientation constants
class ViewOrientation(object):
    """Constants to handle different view orientations"""
    ELEVATION = "ELEVATION"
    SECTION = "SECTION"
    FLOOR_PLAN = "FLOOR_PLAN"


class TextNoteCreator(object):
    """Handles the creation and positioning of text notes in Revit"""

    OFFSET_DISTANCE = 25
    TEXT_WIDTH = 0.25

    def __init__(self, doc, active_view, text_type_id):
        self.doc = doc
        self.active_view = active_view
        self.text_type_id = text_type_id
        self.view_orientation = self._get_view_orientation()
        self.reference_plane = self._find_reference_plane()

    def _get_view_orientation(self):
        """Determines the view orientation based on active view type"""
        if self.active_view.ViewType == ViewType.Elevation:
            return ViewOrientation.ELEVATION
        elif self.active_view.ViewType == ViewType.Section:
            return ViewOrientation.SECTION
        elif self.active_view.ViewType == ViewType.FloorPlan:
            return ViewOrientation.FLOOR_PLAN
        return None

    def _find_reference_plane(self):
        """Finds the appropriate reference plane based on view orientation"""
        ref_plane_name = "Mitte AZ BS"
        if self.view_orientation == ViewOrientation.SECTION:
            ref_plane_name = "Mitte AZ TS"

        ref_planes = FilteredElementCollector(self.doc) \
            .OfCategory(BuiltInCategory.OST_CLines) \
            .WhereElementIsNotElementType() \
            .ToElements()

        for plane in ref_planes:
            if plane.Name == ref_plane_name:
                return plane

        print('Reference plane {0} not found!'.format(ref_plane_name))
        return None

    def _get_text_from_parameters(self, element):
        """Extracts and combines text from element parameters"""
        text = element.LookupParameter('Beschriftungstext').AsString()

        # Handle special case for DB_Ankerschiene family
        if element.LookupParameter('Familie').AsValueString() == 'DB_Ankerschiene':
            length = element.LookupParameter('l').AsDouble()
            length = str(int(convert_internal_units(length, False, 'm') * 1000))
            text += length

        # Add secondary text if available
        text2_param = element.LookupParameter('Beschriftungstext_2')
        if text2_param:
            text += "\v" + text2_param.AsString()

        return text

    def _get_position_data(self, is_left_side, bbox, offset_vector):
        """Helper method to create position data dictionary"""
        # For section view, we use opposite bbox points
        if self.view_orientation == ViewOrientation.SECTION:
            if is_left_side:
                return {
                    'position': bbox.Max + offset_vector,
                    'alignment': HorizontalTextAlignment.Left,
                    'leader_end': bbox.Max
                }
            return {
                'position': bbox.Min + offset_vector,
                'alignment': HorizontalTextAlignment.Right,
                'leader_end': bbox.Min
            }
        # For other views (elevation, floor plan)
        else:
            if is_left_side:
                return {
                    'position': bbox.Min + offset_vector,
                    'alignment': HorizontalTextAlignment.Left,
                    'leader_end': bbox.Min
                }
            return {
                'position': bbox.Max + offset_vector,
                'alignment': HorizontalTextAlignment.Right,
                'leader_end': bbox.Max
            }

    def _get_elevation_position(self, bbox, ref_plane_bbox):
        """Calculates text position for elevation view"""
        is_left_side = not ref_plane_bbox or ref_plane_bbox.Min.X - bbox.Max.X > 0
        offset_vector = XYZ(-self.OFFSET_DISTANCE if is_left_side else self.OFFSET_DISTANCE, 0, 4)
        return self._get_position_data(is_left_side, bbox, offset_vector)

    def _get_section_position(self, bbox, ref_plane_bbox):
        """Calculates text position for section view"""
        is_left_side = not ref_plane_bbox or ref_plane_bbox.Min.Y - bbox.Max.Y > 0
        offset_vector = XYZ(0, -self.OFFSET_DISTANCE if is_left_side else self.OFFSET_DISTANCE, 4)
        # For sections, we need to flip the alignment compared to the side
        return self._get_position_data(not is_left_side, bbox, offset_vector)

    def _get_floor_plan_position(self, bbox, ref_plane_bbox):
        """Calculates text position for floor plan view"""
        is_left_side = not ref_plane_bbox or ref_plane_bbox.Min.X - bbox.Max.X > 0
        offset_vector = XYZ(-self.OFFSET_DISTANCE if is_left_side else self.OFFSET_DISTANCE, 4, 0)
        return self._get_position_data(is_left_side, bbox, offset_vector)

    def _calculate_text_position(self, bbox, ref_plane_bbox=None):
        """Calculates text position and alignment based on view orientation and reference plane"""
        if self.view_orientation == ViewOrientation.ELEVATION:
            return self._get_elevation_position(bbox, ref_plane_bbox)
        elif self.view_orientation == ViewOrientation.SECTION:
            return self._get_section_position(bbox, ref_plane_bbox)
        elif self.view_orientation == ViewOrientation.FLOOR_PLAN:
            return self._get_floor_plan_position(bbox, ref_plane_bbox)
        return None

    def create_text_note(self, element):
        """Creates a text note with leader for the given element"""
        text = self._get_text_from_parameters(element)
        bbox = element.get_BoundingBox(self.active_view)
        ref_plane_bbox = self.reference_plane.get_BoundingBox(self.active_view) if self.reference_plane else None

        position_data = self._calculate_text_position(bbox, ref_plane_bbox)
        if not position_data:
            print('Could not calculate text position for current view type')
            return

        text_options = TextNoteOptions(self.text_type_id)
        text_options.HorizontalAlignment = position_data['alignment']

        t = Transaction(self.doc, "Create Text Note")
        try:
            t.Start()

            note = TextNote.Create(
                self.doc,
                self.active_view.Id,
                position_data['position'],
                self.TEXT_WIDTH,
                text,
                text_options
            )

            note.LeaderLeftAttachment = LeaderAtachement.TopLine
            note.LeaderRightAttachment = LeaderAtachement.TopLine

            leader = note.AddLeader(leaderType=0)
            leader.End = position_data['leader_end']

            t.Commit()
        except Exception as ex:
            if t.HasStarted():
                t.RollBack()
            print('Error creating text note: {0}'.format(str(ex)))


def get_text_type_from_user(doc):
    """Gets text type selection from user"""
    text_types = FilteredElementCollector(doc).OfClass(TextNoteType).ToElements()
    type_dict = {}
    names = []

    for text_type in text_types:
        name = Element.Name.__get__(text_type)
        names.append(name)
        type_dict[name] = text_type

    selected = forms.SelectFromList.show(
        sorted(names),
        multiselect=False,
        button_name='Select Text type'
    )

    if not selected:
        return None
    return type_dict[selected]


def main():
    # Get active view and text type from user
    active_view = doc.ActiveView
    text_type = get_text_type_from_user(doc)

    if not text_type:
        print('No text type selected')
        return

    # Create text note creator instance
    creator = TextNoteCreator(doc, active_view, text_type.Id)

    try:
        # Let user select objects and create text notes
        selected_refs = selection.PickObjects(ObjectType.Element)
        for ref in selected_refs:
            element = doc.GetElement(ref)
            creator.create_text_note(element)
    except Exception as ex:
        print('Error: {0}'.format(str(ex)))


if __name__ == "__main__":
    main()