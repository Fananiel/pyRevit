# -*- coding: utf-8 -*-
__title__   = "Schienenbügel Text"
__doc__     = """Version = 1.0
Date    = 14.02.2025
________________________________________________________________
Description:
This is the base for building your WPF forms.
It includes a very simple XAML file and the Python code 
to display your form and react to the submit button.

________________________________________________________________
Last Updates:
- [08.08.2024] v1.0 RELEASE
________________________________________________________________
Author: Erik Frits"""


# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
#====================================================================================================
from Autodesk.Revit.DB import *
from pyrevit import forms   # By importing forms you also get references to WPF package! IT'S Very IMPORTANT !!!
import wpf, os# wpf can be imported only after pyrevit.forms!
import clr
from Snippets._text import *

# .NET Imports
clr.AddReference("System")
from System.Collections.Generic import List
from System.Windows import Window, FontWeights, Thickness, WindowStartupLocation, SizeToContent, ResourceDictionary
from System.Windows.Controls import StackPanel, DockPanel, Button, TextBox, TextBlock, ComboBox, Dock, Separator
from System import Uri

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
#====================================================================================================
PATH_SCRIPT = os.path.dirname(__file__)
doc     = __revit__.ActiveUIDocument.Document #type: Document
uidoc   = __revit__.ActiveUIDocument
app     = __revit__.Application

# classes


class DF_ComboDock():

    def __init__(self, counter, bracket):  # bracket als Parameter hinzugefügt
        self.label = "Bügel {}:".format(counter)
        self.counter = counter
        self.bracket = bracket  # Speichere das zugehörige bracket
        self.combobox = None


    @property
    def control(self):
        dock = DockPanel()
        dock.Margin = Thickness(0, 0, 0, 20)

        text_block = TextBlock()
        text_block.Text = self.label
        text_block.Margin = Thickness(0, 2.5, 5, 0)

        self.combobox = ComboBox()
        items = ["Dübel", "HM", "HTA", "HM (Bestand)", "HTA (Bestand)"]
        for item in items:
            self.combobox.Items.Add(item)
        self.combobox.SelectedIndex = 0

        dock.Children.Add(text_block)
        dock.Children.Add(self.combobox)
        return dock


    @property
    def value(self):
        return self.combobox.SelectedItem

# functions

def check_type(element, keyword):
    el_type = element.get_Parameter(BuiltInParameter.ELEM_TYPE_PARAM).AsValueString()
    if keyword.lower() in el_type.lower():
        return True


# ╔╦╗╔═╗╦╔╗╔  ╔═╗╔═╗╦═╗╔╦╗
# ║║║╠═╣║║║║  ╠╣ ║ ║╠╦╝║║║
# ╩ ╩╩ ╩╩╝╚╝  ╚  ╚═╝╩╚═╩ ╩ MAIN FORM
#====================================================================================================
# Inherit .NET Window for your UI Form Class
class UI_Fenster(Window):
    def __init__(self, brackets):
        path_xaml_file = os.path.join(PATH_SCRIPT, 'script.xaml')
        wpf.LoadComponent(self, path_xaml_file)

        self.stack = StackPanel(Margin=Thickness(10))
        self.brackets = brackets
        self.combo_controls = {}  # Dictionary für die Kontrollelemente

        for i, bracket in enumerate(brackets, 1):
            combo_dock = DF_ComboDock(counter=i, bracket=bracket)
            self.combo_controls[bracket] = combo_dock  # Speichere die Kontrollelemente
            self.stack.Children.Add(combo_dock.control)

        # 🟧 Create Separator
        sep = Separator()
        sep.Margin = Thickness(0, 0, 0, 10)

        # 🟧 Create Button
        button = Button()
        button.Content = 'Submit!'
        button.Click += self.UIe_btn_run

        self.stack.Children.Add(sep)
        self.stack.Children.Add(button)

        self.Content = self.stack
        self.ShowDialog()

    def UIe_btn_run(self, sender, e):
        self.Close()


# ╦ ╦╔═╗╔═╗  ╔═╗╔═╗╦═╗╔╦╗
# ║ ║╚═╗║╣   ╠╣ ║ ║╠╦╝║║║
# ╚═╝╚═╝╚═╝  ╚  ╚═╝╩╚═╩ ╩
#====================================================================================================

plan_texte = {"Dübel": 'Schienenbügel mittels Dübel befestigen \n(AN FA)',
              "HM": 'Schienenbügel mittels HM 40/22/2550 befestigen \n(AN FA)',
              "HTA": 'Schienenbügel mittels HTA 40/22/2550 befestigen \n(AN FA)',
              "HM (Bestand)": 'Schienenbügel an HM Bestand befestigen \n(AN FA)',
              "HTA (Bestand)": 'Schienenbügel an HTA Bestand befestigen \n(AN FA)'}

view = doc.ActiveView

# Schienenbügel filtern

all_allgmodel   = FilteredElementCollector(doc, view.Id).OfCategory(BuiltInCategory.OST_GenericModel).WhereElementIsNotElementType().ToElements()
all_brackets    = [m for m in all_allgmodel if check_type(m,"LDXRailBracket")]

if len(all_brackets) == 0:
    forms.alert('Es wurden keine Schienenbügel gefunden.', exitscript=True)

# Sortieren der Schienenbügel nach Höhe
sorted_brackets = sorted(all_brackets, key=lambda x: x.get_BoundingBox(view).Min.Z)

UI = UI_Fenster(sorted_brackets)

text_type = get_text_type_from_user(doc)

if not text_type:
    forms.alert('No text type selected', exitscript=True)

# Create text note creator instance
creator = TextNoteCreator(doc, view, text_type.Id)

try:
    for bracket in sorted_brackets:
        UI_value = UI.combo_controls[bracket].value
        text = plan_texte[UI_value]
        creator.create_text_note(bracket, text)
except Exception as ex:
    print('Error: {0}'.format(str(ex)))


