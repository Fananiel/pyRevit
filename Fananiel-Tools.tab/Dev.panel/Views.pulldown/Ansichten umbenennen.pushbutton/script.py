# -*- coding: utf-8 -*-
__title__ = "Views umbenennen"
__doc__ = """Version = 1.0
Date    = 18.03.2025
________________________________________________________________
Description:
Ändert die Namen aller Views auf einem ausgewählten Plan,
indem 'Kopie 1' durch 'SG' ersetzt wird.
________________________________________________________________
Author: Claude"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
# ==================================================
from Autodesk.Revit.DB import *
from pyrevit import forms

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

# Funktion zum Ändern des View-Namens
def rename_view(view, old_text, new_text):
    """Ändert den Namen eines Views, indem ein bestimmter Text ersetzt wird"""
    old_name = view.Name
    if old_text in old_name:
        new_name = old_name.replace(old_text, new_text)
        return new_name
    return None


# Wähle einen Plan aus
sheets = forms.select_sheets(title='Wählen sie den Plan aus')

if not sheets:
    forms.alert('Kein Plan ausgewählt. Skript wird beendet.', exitscript=True)

# Sammle alle umzubenennenden Views
views_to_rename = []
sheet = sheets[0]  # Nur der erste ausgewählte Plan wird verwendet

# Hole alle platzierten Views vom Plan
view_ids = sheet.GetAllPlacedViews()
for view_id in view_ids:
    view = doc.GetElement(view_id)
    new_name = rename_view(view, "Kopie 1", "SG")
    if new_name:
        views_to_rename.append((view, new_name))

# Überprüfe, ob Views zum Umbenennen gefunden wurden
if not views_to_rename:
    forms.alert('Keine Views mit "Kopie 1" im Namen gefunden.', exitscript=True)

# Zeige dem Benutzer eine Vorschau der Änderungen
preview_text = "Folgende Views werden umbenannt:\n\n"
for view, new_name in views_to_rename:
    preview_text += "• {} -> {}\n".format(view.Name, new_name)

proceed = forms.alert(preview_text, yes=True, no=True)
if not proceed:
    forms.alert('Vorgang abgebrochen.', exitscript=True)

# Führe die Umbenennung durch
t = Transaction(doc, __title__)
t.Start()

renamed_count = 0
not_renamed = []

try:
    for view, new_name in views_to_rename:
        try:
            view.Name = new_name
            renamed_count += 1
        except Exception as e:
            not_renamed.append((view.Name, str(e)))

    t.Commit()

    # Zeige Ergebnis an
    result_msg = "{} Views wurden erfolgreich umbenannt.".format(renamed_count)
    if not_renamed:
        result_msg += "\n\nFolgende Views konnten nicht umbenannt werden:\n"
        for name, error in not_renamed:
            result_msg += "• {}: {}\n".format(name, error)

    forms.alert(result_msg)

except Exception as e:
    t.RollBack()
    forms.alert('Fehler: {}'.format(str(e)))