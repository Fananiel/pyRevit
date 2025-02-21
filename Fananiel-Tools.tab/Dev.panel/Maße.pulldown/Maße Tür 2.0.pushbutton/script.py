# -*- coding: utf-8 -*-
__title__   = "Maße Tür"
__doc__     = """Version = 1.0
Date    = 28.10.2024
________________________________________________________________
Author: Daniel Förster"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
#==================================================
from Autodesk.Revit.DB import *
from pyrevit import forms
from Autodesk.Revit.UI.Selection import *
from Snippets._selection import check_family
from Snippets._convert import convert_internal_units

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝
#==================================================
app    = __revit__.Application
uidoc  = __revit__.ActiveUIDocument
doc    = __revit__.ActiveUIDocument.Document    #type:Document
selection = uidoc.Selection                     #type: Selection


# Functions


def check_side(direction_vector, bb1, bb2):
    """
    Returns the coordinate of position_vector that corresponds to direction_vector

    Args:
        direction_vector: XYZ vector that is either (1,0,0), (0,1,0) or (0,0,1)
       bb1: Bounding Box 1
       bb2: Bounding Box 2

    Returns:
        True for left, false for right
    """
    if direction_vector.X == 1 or direction_vector.X == -1:
        v = bb1.X - bb2.X
        return v > 0
    elif direction_vector.Y == 1 or direction_vector.Y == -1:
        v = bb1.Y - bb2.Y
        return v > 0
    elif direction_vector.Z == 1 or direction_vector.Z == -1:
        v = bb1.Z - bb2.Z
        return v > 0
    else:
        raise ValueError("Direction vector must be (1,0,0), (0,1,0) or (0,0,1)")


# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝
#==================================================

# Anicht
view = doc.ActiveView
view_dir = view.RightDirection
view_up = view.UpDirection
view_type = view.ViewType

# Bemaßungsstil
dim_type_group = ElementTypeGroup.SpotElevationType
p = BuiltInParameter.ALL_MODEL_TYPE_NAME
alle_stile = FilteredElementCollector(doc).WhereElementIsElementType().ToElements()
bm_stil = [dt for dt in FilteredElementCollector(doc).OfClass(DimensionType) if dt.get_Parameter(p).AsString() == 'Standard 3mm'][0]

# Ref Ebene
ref_planes = FilteredElementCollector(doc, view.Id) \
    .OfCategory(BuiltInCategory.OST_CLines) \
    .WhereElementIsNotElementType() \
    .ToElements()

if len(ref_planes) == 0:
    forms.alert('Es wurde keine Referenzebene fpr die Mitte des Aufzugs gefunden.', exitscript=True)
elif len(ref_planes) > 1:
    dic = {}
    ref_pl_names = []
    for el in ref_planes:
        ref_pl_names.append(el.Name)
        dic[el.Name] = el
    ref_plane_name = forms.SelectFromList.show(ref_pl_names, button_name='Wählen Sie die Referenzebene Mitte aus')
    ref_plane = dic[ref_plane_name]
else:
    ref_plane = ref_planes[0]

ref_bb = ref_plane.get_BoundingBox(view).Max

# Türzargen filtern

all_allgmodel   = FilteredElementCollector(doc, view.Id).OfCategory(BuiltInCategory.OST_GenericModel).WhereElementIsNotElementType().ToElements()
all_tz    = [m for m in all_allgmodel if check_family(m,"DB_Türzarge")]

if len(all_tz) == 0:
    forms.alert('Es wurde keine Türzarge gefunden.', exitscript=True)


for tz in all_tz:
    if view_type == ViewType.FloorPlan:
        ref_u = tz.GetReferences(FamilyInstanceReferenceType.Left)
        ref_o = tz.GetReferences(FamilyInstanceReferenceType.Right)
        prefix = 'BT'
    else:
        ref_u = tz.GetReferences(FamilyInstanceReferenceType.Bottom)
        ref_o = tz.GetReferences(FamilyInstanceReferenceType.Top)
        prefix = 'HT'

    # Reference Array
    SG_ref = ReferenceArray()
    SG_ref.Append(ref_u[0])
    SG_ref.Append(ref_o[0])

    # curve for dimline
    pos_tz = tz.get_BoundingBox(view).Max
    side = check_side(view_dir, pos_tz, ref_bb)
    if side == False:
        point_1 = pos_tz + 20 * view_dir
        point_2 = point_1 + 10 * view_up
    else:
        point_1 = pos_tz - 20 * view_dir
        point_2 = point_1 - 10 * view_up

    dimline = Line.CreateBound(point_1, point_2)

    # Transaction
    t = Transaction(doc, __title__)
    t.Start()
    try:
        #Changes
        TZ_Dim = doc.Create.NewDimension(view, dimline, SG_ref, bm_stil) #type: Dimension
        TZ_Dim.Prefix = prefix
        t.Commit()
    except Exception as e:
        print(e)
        t.RollBack()

