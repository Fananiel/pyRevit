# -*- coding: utf-8 -*-
__title__   = "IFC drehen"
__doc__     = """Version = 1.0
Date    = 09.04.2025

! Platzieren sie vor Klicken des Buttons eine Detaillinie auf der Wand des Aufzugsschachts !

Beschreibung:
Dieses Skript dreht eine IFC und den Geographischen Norden um den Ursprung (0,0,0)

Vorgehen:
- Wählen sie die Detaillinie
- Wählen sie die senkrechte Referenzebene
- Wählen sie die IFC
- Wählen sie den Winkel 

________________________________________________________________
Author: Daniel Förster"""


# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
#==================================================
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import *
from Snippets._selection import *
import math
from pyrevit import forms


# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝
#==================================================
app    = __revit__.Application
uidoc  = __revit__.ActiveUIDocument
doc    = __revit__.ActiveUIDocument.Document    #type:Document
selection = uidoc.Selection                     #type: Selection

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝
#==================================================

filter_cats       = ISelectionFilter_Categories([BuiltInCategory.OST_Lines])
d_line = selection.PickObject(ObjectType.Element, filter_cats, "Wählen sie eine Linie")
d_line = doc.GetElement(d_line)

filter_cats       = ISelectionFilter_Categories([BuiltInCategory.OST_CLines, BuiltInCategory.OST_Grids])
r_line = selection.PickObject(ObjectType.Element, filter_cats, "Wählen sie die Referenzebene")
r_line = doc.GetElement(r_line)

filter_cats       = ISelectionFilter_Categories([BuiltInCategory.OST_RvtLinks])
ifc = selection.PickObject(ObjectType.Element, filter_cats)
ifc = doc.GetElement(ifc)

#el = selection.PickObject(ObjectType.Element)
#el = doc.GetElement(el)

d_line_dir_vec = d_line.Location.Curve.Direction #type:XYZ
r_line_dir_vec = r_line.Direction #type:XYZ

winkel = r_line_dir_vec.AngleTo(d_line_dir_vec)

winkel_g = winkel * 180 / math.pi

winkel_2 = winkel_g - 180
winkel_3 = 180 - winkel_g
winkel_4 = 360 - winkel_g



res = forms.alert("Um welchen Winkel möchten sie im Uhrzeigersinn drehen?",
                  options=["{}".format(winkel_g),"{}".format(winkel_2), "{}".format(winkel_3), "{}".format(winkel_4)])
if res:
    winkel_dreh = float(res)


res_2 = forms.alert('Möchten sie die IFC und den Projektnorden um den Winkel: {}° im Uhrzeigersinn drehen?'.format(winkel_dreh), ok=False, yes=True, no=True)

if res_2:
    t = Transaction(doc, __title__)
    t.Start()
    winkel_r = winkel_dreh * math.pi / 180
    pl_current = doc.ActiveProjectLocation

    newPosition = app.Create.NewProjectPosition(0, 0, 0, winkel_r)

    pl_current.SetProjectPosition(XYZ(0,0,0), newPosition)

    point1 = XYZ(0,0,0)
    point2 = XYZ(0,0,10)

    axis = Line.CreateBound(point1, point2)

    ifc.Location.Rotate(axis, -winkel_r)

    t.Commit()

    res_3 = forms.alert('Soll die Detaillinie gelöscht werden?', ok=False, yes=True, no=True)

    if res_3:
        t = Transaction(doc, 'Detaillinie löschen')
        t.Start()
        doc.Delete(d_line.Id)
        t.Commit()