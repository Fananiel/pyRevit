# -*- coding: utf-8 -*-
__title__   = "Piktogramme"
__doc__     = """Version = 1.0
Date    = 20.02.25
________________________________________________________________
Author: Daniel Förster"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
#==================================================
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import *
from Snippets._selection import check_type

#.NET Imports
import clr
from clr import StrongBox

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

view = doc.ActiveView

# Pick object

# Rollstuhl filtern

all_allgmodel   = FilteredElementCollector(doc, view.Id).OfCategory(BuiltInCategory.OST_GenericModel).WhereElementIsNotElementType().ToElements()
ph_rollstuhl    = [m for m in all_allgmodel if check_type(m,"Rollstuhl")]
ph_aufzug       = [m for m in all_allgmodel if check_type(m,"Aufzug")]

phs = ph_rollstuhl + ph_aufzug

for el in phs:

    loc_point = el.Location.Point

    width = el.LookupParameter('B').AsDouble()

    # Import Options
    import_options = ImagePlacementOptions(loc_point, BoxPlacement.Center)
    if check_type(el,"Rollstuhl"):
        new_img_path = r"N:\F-KA-Plandaten\000- Revit Familien FC\02 Aufzüge\Deutsche Bahn Sonderteile\Piktogramme\Piktogramme_einzeln\Material\Rollstuhl.jpg"
    else:
        new_img_path = r"N:\F-KA-Plandaten\000- Revit Familien FC\02 Aufzüge\Deutsche Bahn Sonderteile\Piktogramme\Piktogramme_einzeln\Material\Aufzug.jpg"
    im_type_opt = ImageTypeOptions(new_img_path, True, ImageTypeSource.Import)

    # Create New Image in Revit
    t = Transaction(doc, 'Import Image')
    t.Start()

    image_type = ImageType.Create(doc, im_type_opt)
    image = ImageInstance.Create(doc, view, image_type.Id, import_options)
    image.Width = width
    image.DrawLayer = DrawLayer.Foreground

    t.Commit()

