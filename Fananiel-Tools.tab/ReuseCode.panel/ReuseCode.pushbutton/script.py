# -*- coding: utf-8 -*-
__title__   = "Reuse Code in pyRevit"
__doc__     = """Version = 1.0
Date    = 04.10.2024
________________________________________________________________
Description:

Rename Views in Revit by using Find/Replace Logic.

________________________________________________________________
How-To:
-> Click on the button
-> Select Views
-> Define Renaming Rules
-> Rename Views
________________________________________________________________
TODO:
[FEATURE] - Describe Your ToDo Tasks Here
________________________________________________________________
Last Updates:
- [04.10.2024] v1.0 Release
________________________________________________________________
Author: Daniel Förster"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
#==================================================
from Autodesk.Revit.DB import *

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝
#==================================================
app    = __revit__.Application
uidoc  = __revit__.ActiveUIDocument
doc    = __revit__.ActiveUIDocument.Document #type:Document


# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝
#==================================================

from Snippets._selection import get_selected_elements

sel_el = get_selected_elements()

sel_walls = get_selected_elements([Wall, Floor])

print(sel_el)
print(sel_walls)

