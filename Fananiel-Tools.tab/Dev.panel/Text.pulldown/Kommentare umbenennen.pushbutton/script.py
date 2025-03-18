# -*- coding: utf-8 -*-
__title__ = "Kommentartext suchen und ersetzen"
__doc__ = """Version = 1.0
Date    = 18.03.2025
________________________________________________________________
Beschreibung:

Dieses Skript sucht Kommentare, die einen bestimmten Text enthalten,
und ersetzt deren kompletten Inhalt mit einem neuen Text.

________________________________________________________________
How-To:
-> Klicken Sie auf das Button
-> Geben Sie den zu suchenden Text ein
-> Geben Sie den neuen Text ein (mit Zeilenumbrüchen)
-> Das Skript aktualisiert alle Kommentare, die den Suchtext enthalten

________________________________________________________________
Author: Daniel Förster"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
# ==================================================
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import *

# pyRevit
from pyrevit import revit, forms
from System.Windows.Forms import Form, TextBox as WinFormsTextBox, Button as WinFormsButton, Label as WinFormsLabel
from System.Windows.Forms import DialogResult, ScrollBars, FormBorderStyle, FormStartPosition
from System.Drawing import Point, Size

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝
# ==================================================
app = __revit__.Application
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document  # type:Document
selection = uidoc.Selection  # type: Selection


# Functions
def create_search_replace_form():
    """
    Erstellt ein Windows Form mit mehrzeiligen TextBox-Eingabefeldern für Such- und Ersetzungstext

    Returns:
        tuple: (search_text, replace_text) wenn OK geklickt wurde, sonst (None, None)
    """
    # Form erstellen
    form = Form()
    form.Text = "Kommentartext suchen und ersetzen"
    form.Width = 500
    form.Height = 400
    form.FormBorderStyle = FormBorderStyle.FixedDialog
    form.StartPosition = FormStartPosition.CenterScreen
    form.MaximizeBox = False
    form.MinimizeBox = False

    # Label 1
    label1 = WinFormsLabel()
    label1.Text = "Text zum Suchen (Kommentare mit diesem Text werden aktualisiert):"
    label1.Location = Point(20, 20)
    label1.Size = Size(450, 20)
    form.Controls.Add(label1)

    # TextBox 1 - Mehrzeilig
    textbox1 = WinFormsTextBox()
    textbox1.Multiline = True
    textbox1.ScrollBars = ScrollBars.Vertical
    textbox1.Location = Point(20, 45)
    textbox1.Size = Size(440, 100)
    form.Controls.Add(textbox1)

    # Label 2
    label2 = WinFormsLabel()
    label2.Text = "Neuer Text für die gefundenen Kommentare:"
    label2.Location = Point(20, 160)
    label2.Size = Size(450, 20)
    form.Controls.Add(label2)

    # TextBox 2 - Mehrzeilig
    textbox2 = WinFormsTextBox()
    textbox2.Multiline = True
    textbox2.ScrollBars = ScrollBars.Vertical
    textbox2.Location = Point(20, 185)
    textbox2.Size = Size(440, 100)
    form.Controls.Add(textbox2)

    # OK Button
    button_ok = WinFormsButton()
    button_ok.Text = "OK"
    button_ok.DialogResult = DialogResult.OK
    button_ok.Location = Point(280, 310)
    button_ok.Size = Size(80, 30)
    form.Controls.Add(button_ok)
    form.AcceptButton = button_ok

    # Abbrechen Button
    button_cancel = WinFormsButton()
    button_cancel.Text = "Abbrechen"
    button_cancel.DialogResult = DialogResult.Cancel
    button_cancel.Location = Point(380, 310)
    button_cancel.Size = Size(80, 30)
    form.Controls.Add(button_cancel)
    form.CancelButton = button_cancel

    # Form anzeigen und Ergebnis zurückgeben
    result = form.ShowDialog()
    if result == DialogResult.OK:
        return textbox1.Text, textbox2.Text
    else:
        return None, None


def find_and_replace_comments(search_text, new_text):
    """
    Findet alle TextNotes mit dem gesuchten Text und ersetzt ihren kompletten Inhalt.

    Args:
        search_text (str): Text zum Suchen in Kommentaren
        new_text (str): Neuer Text für gefundene Kommentare

    Returns:
        int: Anzahl der geänderten Kommentare
    """
    # Aktuelle Ansicht abrufen
    active_view = doc.ActiveView

    # Alle TextNotes in der aktuellen Ansicht abrufen
    text_notes = FilteredElementCollector(doc, active_view.Id) \
        .OfCategory(BuiltInCategory.OST_TextNotes) \
        .WhereElementIsNotElementType() \
        .ToElements()

    # Zähler für geänderte Kommentare
    modified_count = 0
    found_notes = []

    # Kommentare mit dem gesuchten Text finden
    for note in text_notes:
        if search_text in note.Text:
            found_notes.append(note)

    # Wenn keine passenden Kommentare gefunden wurden
    if not found_notes:
        return 0

    # Transaction starten
    t = Transaction(doc, __title__)
    t.Start()

    try:
        # Für jede gefundene TextNote den Text komplett ersetzen
        for note in found_notes:
            note.Text = new_text
            modified_count += 1

        t.Commit()
    except Exception as e:
        if t.HasStarted():
            t.RollBack()
        forms.alert("Fehler beim Aktualisieren der Kommentare: {}".format(str(e)), exitscript=True)

    return modified_count


# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝
# ==================================================

def main():
    # Benutzereingabe für Such- und Ersetzungstext
    search_text, new_text = create_search_replace_form()

    # Überprüfen, ob Benutzereingabe vorhanden ist
    if search_text is None:
        return  # Benutzer hat abgebrochen

    # Überprüfen, ob Such-Text eingegeben wurde
    if not search_text:
        forms.alert("Kein Suchtext eingegeben. Das Skript wird beendet.", exitscript=True)
        return

    # Bestätigung anfordern
    confirmed = forms.alert(
        "Sie sind dabei, alle Kommentare zu suchen, die den Text enthalten:\n\n'{}'\n\n"
        "und deren kompletten Inhalt zu ersetzen. Fortfahren?".format(search_text),
        yes=True,
        no=True
    )

    if not confirmed:
        forms.alert("Vorgang abgebrochen.", exitscript=True)
        return

    # Kommentare suchen und ersetzen
    modified_count = find_and_replace_comments(search_text, new_text)

    # Ergebnis anzeigen
    if modified_count > 0:
        forms.alert("Vorgang abgeschlossen!\n{} Kommentar(e) wurden aktualisiert.".format(modified_count))
    else:
        forms.alert("Es wurden keine Kommentare gefunden, die den gesuchten Text enthalten.")


if __name__ == "__main__":
    main()