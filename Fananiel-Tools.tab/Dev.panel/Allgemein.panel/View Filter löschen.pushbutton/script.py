# -*- coding: utf-8 -*-
__title__ = "View Filter löschen"
__doc__ = """Version = 1.0
Datum   = 07.04.2025
________________________________________________________________
Beschreibung:
View Filter löschen
________________________________________________________________
Autor: Daniel Förster"""
# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
# ==================================================
from Autodesk.Revit.DB import *
from pyrevit import forms
import sys


# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝
# ==================================================
app = __revit__.Application
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document  # type: Document

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝
# ==================================================

all_filters     = FilteredElementCollector(doc).OfClass(FilterElement).ToElements() # Params + Selection Filter
all_par_filters = FilteredElementCollector(doc).OfClass(ParameterFilterElement).ToElements()
all_sel_filters = FilteredElementCollector(doc).OfClass(SelectionFilterElement).ToElements()

filter_dic = {}

# Print Filter Names
for filter in all_filters:
    filter_dic[filter.Name] = filter


filter_names = sorted(filter_dic.keys())
del_filter_names = forms.SelectFromList.show(filter_names, multiselect=True, button_name='Wählen sie die zu löschenden View Filter')

if not del_filter_names:
    forms.alert("Es wurden keine Filter ausgewählt", exitscript=True)

res = forms.alert("Wollen sie folgende {} View Filter löschen? \n"
                  "{}".format(len(del_filter_names), del_filter_names),
                  ok=False, yes=True, no=True)
if res:
    for name in del_filter_names:
        t = Transaction(doc, '{} löschen'.format(name))
        t.Start()
        del_filter = filter_dic[name]
        print(del_filter)
        print(del_filter.Name)
        print(del_filter.Id)
        doc.Delete(del_filter.Id)
        t.Commit()

