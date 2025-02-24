# -*- coding: utf-8 -*-
__title__   = "Maße Kabine"
__doc__     = """Version = 1.0
Date    = 24.02.25
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

# classes
class FamilyLoadOptions(IFamilyLoadOptions):
    'A Class implementation for loading families'

    def OnFamilyFound(self, familyInUse, overwriteParameterValues):
        'Defines behavior when a family is found in the model.'
        overwriteParameterValues = True
        return True

    def OnSharedFamilyFound(self, sharedFamily, familyInUse, source, overwriteParameterValues):
        'Defines behavior when a shared family is found in the model.'
        source = FamilySource.Project
        # source = FamilySource.Family
        overwriteParameterValues = True
        return True

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
    forms.alert('Es wurde keine Referenzebene für die Mitte des Aufzugs gefunden.', exitscript=True)
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
all_k    = [m for m in all_allgmodel if check_family(m,"LDXCar")]

if len(all_k) == 0:
    forms.alert('Es wurde keine Kabine gefunden.', exitscript=True)
elif len(all_k) > 1:
    dic = {}
    k_names = []
    for el in all_k:
        k_names.append(el.Name)
        dic[el.Name] = el
    k_name = forms.SelectFromList.show(k_names, button_name='Wählen Sie die Kabine aus')
    kabine = dic[k_name]
else:
    kabine = all_k[0]

# Famdoc for Kabinbe
fam_id = (kabine.get_Parameter(BuiltInParameter.ELEM_FAMILY_PARAM).AsElementId())
fam_sym = doc.GetElement(fam_id)
fam = fam_sym.Family
famdoc = doc.EditFamily(fam)

# Get Ref Planes
all_refplanes = FilteredElementCollector(famdoc).OfCategory(BuiltInCategory.OST_CLines).ToElements()

#Modify the center elevation
for rp in all_refplanes:
    if rp.Normal.Z == 1:
        ref_name = rp.LookupParameter('Ist eine Referenz')
        ref_name.Set(int(7))
opt = FamilyLoadOptions()
family = famdoc.LoadFamily(doc, opt)

geom_opt = Options()
geom_opt.ComputeReferences = True
geom_opt.View = view


geom = kabine.get_Geometry(geom_opt)

geom_inst = []

for solid in geom:
    geoms = geom.GetEnumerator()
    while geoms.MoveNext():
        geom_inst.append(geoms.Current)

geom_inst = geom_inst[0].GetInstanceGeometry()
edges_dir = {}

for solid in geom_inst:
    if solid.SurfaceArea > 0:
        edge_a = solid.Edges
        edges = edge_a.GetEnumerator()
        while edges.MoveNext():
            edge = edges.Current
            length = edge.ApproximateLength
            if length > 1:
                curve = edge.AsCurve() #type:Line
                curve_dir = curve.Direction
                if curve_dir.IsAlmostEqualTo(view_dir) or curve_dir.IsAlmostEqualTo(-1 * view_dir):
                    edges_dir[curve.Origin] = edge

faces_dir = {}

for solid in geom_inst:
    if solid.SurfaceArea > 0:
        face_a = solid.Faces
        faces = face_a.GetEnumerator()
        while faces.MoveNext():
            face = faces.Current #type:Face
            normal = face.FaceNormal
            if normal.IsAlmostEqualTo(view_up) or normal.IsAlmostEqualTo(-1 * view_up):
                faces_dir[face] = face.Origin

print(faces_dir)

# Schritt 1: Finde den höchsten Z-Wert
max_z = float('-inf')  # Beginne mit dem kleinstmöglichen Wert

for origin in faces_dir.values():
    if origin.Z > max_z:
        max_z = origin.Z

# Schritt 2: Sammle alle Edges mit diesem maximalen Z-Wert
max_z_faces = []

for face, origin in faces_dir.items():
    if origin.Z == max_z:
        max_z_faces.append(face)

print(max_z_faces)
print(max_z_faces[0].Origin)

"""
highest_z_origin = None
highest_z_face = None

for origin, f in faces_dir.items():
    # Wenn wir noch keinen höchsten Z-Wert haben oder der aktuelle Z-Wert höher ist
    if highest_z_origin is None or origin.Z > highest_z_origin.Z:
        highest_z_origin = origin
        highest_z_face = f #type:Face

print(highest_z_face)
"""

ref_face = max_z_faces[0].Reference

print('Referenz des Face:')
print(ref_face)

Dim_ref = ReferenceArray()
Dim_ref.Append(ref_face)
ref_bottom = kabine.GetReferences(FamilyInstanceReferenceType.CenterElevation)
Dim_ref.Append(ref_bottom[0])

# curve for dimline
pos_k = kabine.get_BoundingBox(view).Max
point_1 = pos_k + 20 * view_dir
point_2 = point_1 + 10 * view_up
dimline = Line.CreateBound(point_1, point_2)

# Transaction
t = Transaction(doc, __title__)
t.Start()
try:
    #Changes
    SG_Dim = doc.Create.NewDimension(view, dimline, Dim_ref, bm_stil) #type: Dimension
    t.Commit()
except Exception as e:
    print(e)
    t.RollBack()

