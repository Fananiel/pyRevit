# -*- coding: utf-8 -*-
__title__ = "Plankopf_Elektro"
__doc__ = """Version = 1.0
Date    = 28.10.2024
________________________________________________________________
Author: Daniel Förster"""

#⬇ Imports
from Autodesk.Revit.DB import *
from pyrevit import forms
from pyrevit import script
import os

# 📦 Variables
app = __revit__.Application
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document


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
    :param bic_cats:        List of BuiltInCategories for Parametetrs
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


# MAIN

# req_params = ['Nennspannung', 'Nennfrequenz', 'Absicherung', 'Nennleistung', 'Nennstrom', 'Anlaufstrom', 'Waermeentwicklung', 'Aufzugstyp' ]
# missing_params  = check_missing_params(req_params)
#
# if missing_params:
#     # 🔓 Transaction Start
#     t = Transaction(doc, 'Add SharedParameters')
#     t.Start()
#
#     bic_cats = [BuiltInCategory.OST_Sheets]
#
#     load_params(p_names_to_load = missing_params,
#                 bic_cats        = bic_cats,
#                 bind_mode       = 'instance',
#                 p_group         = BuiltInParameterGroup.PG_TITLE)
#
#     t.Commit()
#

# Get the directory where the script is located
#script_dir = os.path.dirname(__file__)

# Build the path to your CSV file
#csv_path = os.path.join(script_dir, "my_file.csv")
# csv_path = "C:\Users\d.foerster\AppData\Roaming\Github pyRevit\Fananiel-Tools.extension\Fananiel-Tools.tab\Dev.panel\Plankopf_Elektro.pushbutton\Elektroangaben_Plankopf_API.csv"
#
# # Read the CSV file
# data = script.load_csv(csv_path)
#
# print(data)

# # First let's print what we're getting for a row to understand the structure
# print("First data row raw:", data[1])
# print("First data row split:", data[1][0].split(';'))
#
# # Split the header by semicolon
# headers = data[0][0].split(';')
# print("Headers:", headers)
#
# # Convert to dictionary with first column as key
# data_dict = {}
# for row in data[1:]:  # Skip header row
#     # Each row seems to be a list with multiple elements that need to be joined
#     full_row = ';'.join(row)
#     values = full_row.split(';')
#     print("Processing values:", values)
#
#     if len(values) >= len(headers):
#         key = values[0]
#         row_dict = {}
#         for i, header in enumerate(headers[1:], 1):
#             if i < len(values):
#                 row_dict[header] = values[i]
#         data_dict[key] = row_dict
#
# # Print first entry as example
# if data_dict:
#     first_key = list(data_dict.keys())[0]
#     print("\nFirst entry data:")
#     print("Key:", first_key)
#     print("Values:", data_dict[first_key])
#
#     # Print structure of first entry
#     print("\nDetailed structure of first entry:")
#     print("Available headers:", headers[1:])
#     print("Available values:", data_dict[first_key].values())
#     for header in headers[1:]:
#         value = data_dict[first_key].get(header, 'Not found')
#         print("{0}: {1}".format(header, value))
#
# # Print all entries (optional)
# print("\nAll entries:")
# for key, values in data_dict.items():
#     print("\nKey:", key)
#     for header, value in values.items():
#         print("{0}: {1}".format(header, value))

from pyrevit.interop.xl import load, _read_xlsheet

#columns = ['Nennspannung', 'Nennfrequenz', 'Absicherung', 'Nennleistung', 'Nennstrom', 'Anlaufstrom', 'Waermeentwicklung', 'Aufzugstyp' ]

filepath = "C:\Users\d.foerster\AppData\Roaming\Github pyRevit\Fananiel-Tools.extension\Fananiel-Tools.tab\Dev.panel\Plankopf_Elektro.pushbutton\Elektroangaben_Plankopf_API.xlsx"
data = load(filepath)

print(data)


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


# Example usage:
# input_data = {
#     'Elektroangaben_Plankopf_API': {
#         'rows': [row_data],
#         'headers': ['Aufzugstyp', 'Nennleistung', 'Nennstrom', 'Anlaufstrom',
#                     'Absicherung', 'Waermeentwicklung', 'Nennfrequenz', 'Nennspannung']
#     }
# }

transformed_data = transform_elevator_data(data)

print('#'*100)

print(transformed_data)

print('#'*100)

print(transformed_data['1000-MDL-BT10-ZS'])
print(transformed_data['1400-MDL-BT11-ZS'])

