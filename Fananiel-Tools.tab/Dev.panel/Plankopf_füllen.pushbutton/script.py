# -*- coding: utf-8 -*-
__title__ = "Plankopf_befüllen"
__doc__ = """Version = 1.0
Date    = 08.01.2025
________________________________________________________________
Author: Daniel Förster"""

#⬇ Imports
from Autodesk.Revit.DB import *
from pyrevit import forms
from pyrevit.interop.xl import load
from Autodesk.Revit.UI.Selection import *
from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, TextBox, Separator, Button, CheckBox)
from Snippets._convert import convert_internal_units

# 📦 Variables
app = __revit__.Application
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
selection = uidoc.Selection                     #type: Selection


params = ['Schneelastzone_sk', 'Schneelastzone', 'Windzone', 'Windzone_vb,0', 'Windzone_qb', 'Erdbebenzone', 'HGV-Text',
              'Förderhöhe', 'Geschwindigkeit', 'Anzahl Haltestellen', 'Anzahl Schachtzugänge',
              'Bauherr_Name', 'Bauherr_Abteilung', 'Bauherr_Adresse', 'Bauherrenvertreter_Name', 'Bauherrenvertreter_Abteilung', 'Bauherrenvertreter_Adresse',
              'Erdung_Text', 'Notruf_Text', 'Planungsgrundlage Text', 'PLN_Projektbezeichnung_Zeile1', 'PLN_Projektnummer']

param_list = []

# Wählen des Plans

selected_sheets = forms.select_sheets()
for sheet in selected_sheets:
    for param in params:
        param_list.append(sheet.LookupParameter(param))

schneelast = {'1': 0.65, '1a': 0.81, '2': 0.85, '2a': 1.06, '3': 1.06}
windlast = {1: [22.5, 0.32], 2: [25.0, 0.39], 3: [27.5, 0.47], 4: [30.0, 0.56]}

# 📊 Create a list of Components
components = [Label('Wählen sie die Schneelastzone aus:'),
               ComboBox('Schneelastzone', {'1': '1', '1a': '1a', '2': '2', '2a': '2a', '3': '3'}),
                Label('Wählen sie die Windzone aus:'),
               ComboBox('Windzone', {'1': 1, '2': 2, '3': 3, '4': 4}),
              Label('Wählen sie die Erdbebenzone aus:'),
              ComboBox('Erdbebenzone', {'0': 0, '1': 1, '2': 2, '3': 3}),
              Separator(),
              Button('Select')]

# ✅ Create FlexForm
form = FlexForm('Weitere Angaben', components)

form.show()
# 👀 Preview Results


# Abrufen der Werte
s_zone = form.values['Schneelastzone']
s_last = schneelast[s_zone] * 304.762

e_zone = str(form.values['Erdbebenzone'])

w_zone = form.values['Windzone']
w_v = str(windlast[w_zone][0]) + ' m/s'
w_q = windlast[w_zone][1] * 304.762
#w_q = convert_internal_units(w_q, True, 'm2') * 1000


# Setzen der Parameter
t = Transaction(doc, 'Set Parameters')
t.Start()

for sheet in selected_sheets:
    param = sheet.LookupParameter('Schneelastzone')
    param.Set(s_zone)
    param = sheet.LookupParameter('Schneelastzone_sk')
    param.Set(s_last)
    param = sheet.LookupParameter('Windzone')
    param.Set(str(w_zone))
    param = sheet.LookupParameter('Windzone_vb,0')
    param.Set(w_v)
    param = sheet.LookupParameter('Windzone_qb')
    param.Set(w_q)
    param = sheet.LookupParameter('Erdbebenzone')
    param.Set(e_zone)

for param in param_list:
    if param:
        param_Name = param.Definition.Name

        if param_Name == 'Erdung_Text':
            wert = forms.alert("Wählen sie den Text für die Erdung aus:",
                    options=['PAS-FTA im Schacht', 'PAS-FTA in Schachtgrube', 'Erdung über Bahngleis'],

            )
            param.Set(wert)

        if param_Name == 'Notruf_Text':
            wert = forms.alert("Wählen sie den Text für den Notruf aus:",
                              options=['Für die Notrufübertragung ist ein Festnetzanschluss (Prio 1) und ein Mobilfunkanschluss GSM bzw. GSM-R (Prio 2) herzustellen. Es ist das System SL6 der Firma SafeLine in der speziellen DB-Ausführung zu verwenden.',
                                        'Nur Festnetz',
                                       'Nur GSM-R'])
            param.Set(wert)



t.Commit()
