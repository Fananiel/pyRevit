# -*- coding: utf-8 -*-
__title__   = "Maße Fassade"
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


# Türzargen filtern

all_allgmodel   = FilteredElementCollector(doc, view.Id).OfCategory(BuiltInCategory.OST_GenericModel).WhereElementIsNotElementType().ToElements()
all_mh    = [m for m in all_allgmodel if check_family(m,"DB_Mundhaus")]

if len(all_mh) == 0:
    forms.alert('Es wurde kein Mundhaus gefunden.', exitscript=True)


mh = all_mh[0] #type:FamilyInstance

ref_names = ["FP_1", "FP_2", "FP_3", "FP_4", "FP_5", "FP_6", "FP_7", "FP_8", "FP_9", "FP_10"]

# Reference Array
SG_ref = ReferenceArray()
for ref_n in ref_names:
    SG_ref.Append(mh.GetReferenceByName(ref_n))

# curve for dimline
pos_tz = mh.get_BoundingBox(view).Max
point_1 = pos_tz - 10 * view_dir
point_2 = point_1 - 10 * view_up
dimline = Line.CreateBound(point_1, point_2)
# Transaction
t = Transaction(doc, __title__)
t.Start()
try:
    #Changes
    TZ_Dim = doc.Create.NewDimension(view, dimline, SG_ref, bm_stil) #type: Dimension
    t.Commit()
except Exception as e:
    print(e)
    t.RollBack()

"""

ref_v_names = ["FP_v_1", "FP_v_2", "FP_v_3", "FP_v_4", "FP_v_5", "FP_v_6"]

# Reference Array
SG_ref_2 = ReferenceArray()
for ref_n in ref_v_names:
    ref_p = mh.GetReferenceByName(ref_n)
    SG_ref_2.Append(ref_p)

# curve for dimline
pos_mh = mh.get_BoundingBox(view).Max
point_3 = pos_mh + 10 * view_up
point_4 = point_3 + 10 * view_dir
dimline2 = Line.CreateBound(point_3, point_4)

# Transaction
t = Transaction(doc, __title__)
t.Start()
try:
    #Changes
    MH_v_Dim = doc.Create.NewDimension(view, dimline2, SG_ref_2, bm_stil) #type: Dimension
    t.Commit()
except Exception as e:
    print(e)
    t.RollBack()

"""