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
from Snippets._text import *

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

