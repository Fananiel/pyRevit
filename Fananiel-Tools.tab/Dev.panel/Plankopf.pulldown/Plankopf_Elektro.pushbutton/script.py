# -*- coding: utf-8 -*-
__title__ = "Plankopf_Elektro"
__doc__ = """Version = 1.0
Date    = 28.10.2024
________________________________________________________________
Author: Daniel Förster"""

#⬇ Imports
from Autodesk.Revit.DB import *
from pyrevit import forms
from pyrevit.interop.xl import load
from Autodesk.Revit.UI.Selection import *

# 📦 Variables
app = __revit__.Application
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
selection = uidoc.Selection                     #type: Selection


# FUNCTIONS
def get_loaded_parameters_as_def():
    """Get Loaded Parameters in the project as Definitions"""
    definitions = []

    binding_map = doc.ParameterBindings
    it = binding_map.ForwardIterator()
    for i in it:
        definition = it.Key
        definitions.append(definition)
    return definitions


def check_missing_params(list_param_names):
    """Function to check Loaded Shared Parameters.
    :param list_param_names: List of Parameter names
    :return:                 List of Missing Parameter Names"""
    #1️⃣ Read Loaded Parameter Names
    loaded_p_definitions = get_loaded_parameters_as_def()
    loaded_param_names = [d.Name for d in loaded_p_definitions]

    # Check if Parameters Missing
    missing_params = [p_name for p_name in list_param_names if p_name not in loaded_param_names]
    # 👇 It's the same as
    # missing_params = []
    # for p_name in list_param_names:
    #     if p_name not in loaded_param_names:
    #         missing_params.append(p_name)
    return missing_params


def load_params(p_names_to_load,
                bic_cats,
                bind_mode='instance',
                p_group=BuiltInParameterGroup.PG_TITLE):
    #type: (list, list, str, BuiltInParameterGroup) -> None
    """Function to check Loaded Shared Parameters.
    :param p_names_to_load: List of Parameter names
    :param bic_cats:        List of BuiltInCategories for Parameters
    :param bind_mode:       Binding Mode: 'instance' / 'type'
    :param p_group:         BuiltInParameterGroup"""

    # 📁 Ensure SharedParameterFile is available
    sp_file = app.OpenSharedParameterFile()
    if not sp_file:
        forms.alert('Could not find SharedParameter File. '
                    '\nPlease Set the File in Revit and Try Again', title=__title__, exitscript=True)

    #🙋‍ Ask for User Confirmation
    if missing_params:
        confirmed = forms.alert("There are {n_missing} missing parameters for the script."
                                "\n{missing_params}"
                                "\n\nWould you like to try loading them from the following SharedParameterFile:"
                                "\n{p_filepath}".format(n_missing=len(missing_params),
                                                        missing_params='\n'.join(missing_params),
                                                        p_filepath=sp_file.Filename),
                                yes=True, no=True)

        if confirmed:
            # Prepare Categories
            all_cats = doc.Settings.Categories
            cats = [all_cats.get_Item(bic_cat) for bic_cat in bic_cats]

            # Create Category Set
            cat_set = CategorySet()
            for cat in cats:
                cat_set.Insert(cat)

            # Create Binding
            binding = TypeBinding(cat_set) if bind_mode == 'type' \
                else InstanceBinding(cat_set)

            # Add Parameters (if possible)
            for d_group in sp_file.Groups:
                for p_def in d_group.Definitions:
                    if p_def.Name in p_names_to_load:
                        doc.ParameterBindings.Insert(p_def, binding, p_group)
                        p_names_to_load.remove(p_def.Name)

            # SetAllowVaryBetweenGroups (If Possible
            loaded_p_definitions = get_loaded_parameters_as_def()
            for definition in loaded_p_definitions:
                if definition.Name in p_names_to_load:
                    try:
                        definition.SetAllowVaryBetweenGroups(doc, True)
                    except:
                        pass

            #👀 Reported Not Loaded Parameters
            if p_names_to_load:
                msg = "Couldn't Find following Parameters: \n{}".format('\n'.join(p_names_to_load))
                forms.alert(msg, title=__title__)

def transform_elevator_data(input_data):
    """
    Transform elevator data into a dictionary with Aufzugstyp as key.

    Args:
        input_data (dict): Input dictionary containing rows and headers

    Returns:
        dict: Transformed dictionary with Aufzugstyp as key
    """
    # Extract rows and headers
    rows = input_data['Elektroangaben_Plankopf_API']['rows']
    headers = input_data['Elektroangaben_Plankopf_API']['headers']

    # Create result dictionary
    result = {}

    # Transform data
    for row in rows:
        elevator_type = row[0]  # Aufzugstyp is the first column
        # Create dictionary for each row using headers
        row_dict = {headers[i]: value for i, value in enumerate(row)}
        result[elevator_type] = row_dict

    return result


# MAIN
# Falls notwendig: Laden der benötigten Parameter für den Plankopf.pulldown und hinzufügen der Parameter zu der Kategorie: Pläne

req_params = ['Nennspannung', 'Nennfrequenz', 'Absicherung', 'Nennleistung', 'Nennstrom', 'Anlaufstrom', 'Waermeentwicklung', 'Aufzugstyp',
              'Schneelastzone_sk', 'Schneelastzone', 'Windzone', 'Windzone_vb,0', 'Windzone_qb', 'Erdbebenzone', 'HGV-Text',
              'FF1_K', 'FF2_K',	'FF1_GGW', 'FF2_GGW',	'F1_Plan',	'F2_Plan',	'F3_Plan',	'F4_Plan',	'F5_Plan',	'F8_Plan',	'F9_Plan',
              'F10_Plan',	'F14_Plan',	'F15_Plan',	'F16_Plan',	'F17_Plan',	'F18_Plan',
              'TRAGKRAFT', 'Personenzahl', 'FOERDERHOEHE', 'Geschwindigkeit', 'Anzahl Haltestellen', 'Anzahl Schachtzugänge',
              'PLN_Bauherr_Adresse_Zeile1', 'PLN_Bauherr_Adresse_Zeile2','PLN_Bauherr_Adresse_Zeile3',
              'Erdung_Text', 'Notruf_Text', 'Planungsgrundlage Text', 'PLN_Projektbezeichnung_Zeile1', 'PLN_Projektnummer',
              'PLN_Planungsphase', 'Planbezeichnung', 'Planart', 'PLN_Plannummer', 'Strecke_Bezeichnung', 'Strecke_Nr.', 'Stations_km', 'Bahnhofs-Nr.',
              'Planersteller', 'Datum', 'Datum Zeichner', 'CAD_Zeichner', 'CAD_Prüfer', 'CAD_Prüfer_Datum']

missing_params  = check_missing_params(req_params)

if missing_params:
    # 🔓 Transaction Start
    t = Transaction(doc, 'Add SharedParameters')
    t.Start()

    bic_cats = [BuiltInCategory.OST_Sheets]

    load_params(p_names_to_load = missing_params,
                bic_cats        = bic_cats,
                bind_mode       = 'instance',
                p_group         = BuiltInParameterGroup.PG_TEXT)

    t.Commit()


# Importieren der Excel-Datei


filepath = r"N:\F-KA-Plandaten\170-079 Deutsche Bahn Rahmenvertrag\170-079-000 Sonstiges\Revit\Elektroangaben_Plankopf_API.xlsx"
data = load(filepath)

# Umwandeln der Tabelle in ein Dictionary mit key: Aufzugstyp

data = transform_elevator_data(data)

# User muss aus Aufzugstypen wählen

keysList = list(data.keys())
keysList.sort()

selected_option = forms.CommandSwitchWindow.show(
    keysList,
     message='Wählen sie den Aufzugstyp:',
)

aufzugsdaten = data[selected_option]
param_list_exc = list(aufzugsdaten.keys())

param_list = []

# Wählen des Plans

selected_sheets = forms.select_sheets()
for sheet in selected_sheets:
    for param in param_list_exc:
        param_list.append(sheet.LookupParameter(param))

# Setzen der Parameter

t = Transaction(doc, 'Set Parameters')
t.Start()
for param in param_list:
    if param:
        param_Name = param.Definition.Name
        wert = aufzugsdaten[param_Name]

        # Modifizieren der Werte

        if type(wert) == float:
            wert = round(wert, 1)
        if param_Name == 'Personenzahl':
            wert = int(wert)
        else:
            wert = str(wert)
            wert = wert.replace('.', ',')

        # Einheiten
        A_list = ['Absicherung', 'Nennstrom', 'Anlaufstrom']
        if param_Name in A_list:
            wert = wert + ' A'

        elif param_Name == 'Nennleistung':
            wert = wert + ' kVA'

        elif param_Name == 'Waermeentwicklung':
            wert = wert + ' W'

        elif param_Name == 'Tragfähigkeit':
            wert = wert + ' kg'

        elif param_Name == 'Personenzahl' or param_Name == 'Aufzugstyp':
            wert = wert

        else:
            if wert != '-':
                wert = wert + ' kN'

        param.Set(wert)
t.Commit()
