# -*- coding: utf-8 -*-
__title__   = "Kommentare"
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

def text_note_from_param(picked_object):

    # Get Text from Parameter
    param_text1 = picked_object.LookupParameter('Beschriftungstext')
    text = param_text1.AsString()

    fam = picked_object.LookupParameter('Familie').AsValueString()
    if fam == 'DB_Ankerschiene':
        length = picked_object.LookupParameter('l').AsDouble()
        length = str(int(convert_internal_units(length, False, 'm')*1000))
        text = text + length

    param_text2 = picked_object.LookupParameter('Beschriftungstext_2')
    if param_text2:
        text_2 = param_text2.AsString()
        text = text + "\v" + text_2

    # Get Point of Element
    bb = picked_object.get_BoundingBox(active_view)
    bb_min = bb.Min
    bb_max = bb.Max
    lo_ecke = XYZ(bb_min.X, bb_max.Y, bb_max.Z)

    # Get Middle Ref Plane
    ref_planes = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_CLines).WhereElementIsNotElementType().ToElements()
    ref_plane = None
    for rp in ref_planes:
        if rp.Name == 'Mitte AZ BS':
            ref_plane = rp

    # Text Options
    text_opt = TextNoteOptions(text_type_id)


    # Text Position
    if view_type == ViewType.Elevation:
        if ref_plane:
            mid_plane = ref_plane.get_BoundingBox(active_view)
            side_check = mid_plane.Min.X - bb_max.X
            # Left Side
            if side_check > 0:
                text_pos = lo_ecke + XYZ(-25, 0, 4)
                text_opt.HorizontalAlignment = HorizontalTextAlignment.Left
                leader_end = lo_ecke
            #Right Side
            else:
                text_pos = bb_max + XYZ(25, 0, 4)
                text_opt.HorizontalAlignment = HorizontalTextAlignment.Right
                leader_end = bb_max
        else:
            text_pos = bb_max + XYZ(25, 0, 4)
            print('Referenzebene Mitte AZ BS nicht gefunden!')

    if view_type == ViewType.FloorPlan:
        if ref_plane:
            mid_plane = ref_plane.get_BoundingBox(active_view)
            side_check = mid_plane.Min.X - bb_max.X
            # Left Side
            if side_check > 0:
                text_pos = lo_ecke + XYZ(-25, 4, 0)
                text_opt.HorizontalAlignment = HorizontalTextAlignment.Left
                leader_end = lo_ecke
            # Right Side
            else:
                text_pos = bb_max + XYZ(25, 4, 0)
                text_opt.HorizontalAlignment = HorizontalTextAlignment.Right
                leader_end = bb_max
        else:
            text_pos = bb_max + XYZ(25, 4, 0)
            print('Referenzebene Mitte AZ BS nicht gefunden!')

    # Start transaction
    t = Transaction(doc, __title__)
    t.Start()

    # CREATE TEXT NOTE
    width = 0.25
    note = TextNote.Create(doc, active_view.Id, text_pos, width, text, text_opt)
    note.LeaderLeftAttachment = LeaderAtachement.TopLine
    note.LeaderRightAttachment = LeaderAtachement.TopLine

    leader = note.AddLeader(leaderType=0)
    leader.End = leader_end
    #leader.Elbow = leader.Anchor + XYZ(-5,0,0)

    t.Commit()


# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝
#==================================================

# Get Active View and View Type
active_view  = doc.ActiveView
view_type = active_view.ViewType

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

# Let user select objects
ref_picked_objects = selection.PickObjects(ObjectType.Element)
for ref in ref_picked_objects:
    picked_object = doc.GetElement(ref)
    text_note_from_param(picked_object)

