# -*- coding: utf-8 -*-
__title__   = "Projektparameter löschen"
__doc__     = """Version = 1.0
Date    = 19.03.2025

Beschreibung: Bei Klick des Buttons öffnet sich ein Fenster mit allen im Projekt vorhandenen Projektparametern. 
Wählen sie aus dieser Liste alle Parameter aus, die sie löschen möchten.

________________________________________________________________
Author: Daniel Förster"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
#==================================================
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import *
from Snippets._parameters import get_param_value
from Snippets._convert import convert_internal_units
from pyrevit import forms

#.NET Imports
import clr
clr.AddReference('System')



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


def get_loaded_params():
    """Get all parameters loaded in the project
    :return: dictionary of parameters {parameter.name: parameter}
    """
    # Get Parameter Bindings Map
    bm = doc.ParameterBindings

    # Create a Forward Iterator
    itor = bm.ForwardIterator()
    itor.Reset()

    # Iterate over the map
    loaded_parameters = {}
    while itor.MoveNext():
        try:
            d = itor.Key
            loaded_parameters[d.Name] = d
        except:
            pass

    return loaded_parameters


l_params = get_loaded_params()
l_params_names = sorted(l_params.keys())
del_params_names = forms.SelectFromList.show(l_params_names, multiselect=True, button_name='Wählen sie die zu löschenden Projektparameter')

res = forms.alert("Wollen sie folgende Projektparameter löschen? \n"
                  "{}".format(del_params_names),
                  ok=False, yes=True, no=True)
if res:
    for name in del_params_names:
        t = Transaction(doc, '{} löschen'.format(name))
        t.Start()
        param = l_params[name]
        doc.Delete(param.Id)
        t.Commit()

