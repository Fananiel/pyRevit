# -*- coding: utf-8 -*-
__title__   = "04.04 - Shared Parameters"
__doc__     = """Version = 1.0
Date    = 10.10.2024
________________________________________________________________
Author: Daniel Förster"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
#==================================================
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import Room
from Autodesk.Revit.UI.Selection import *
from Snippets._parameters import get_param_value
from Snippets._convert import convert_internal_units
from pyrevit import forms

#.NET Imports
import clr
clr.AddReference('System')
from System.Collections.Generic import List


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


def check_loaded_params(list_p_names):
    """Check if any parameters from provided list are missing in the project
    :param list_p_names:
    :return:
    """
    # Get Parameter Bindings Map
    bm = doc.ParameterBindings

    # Create a Forward Iterator
    itor = bm.ForwardIterator()
    itor.Reset()

    # Iterate over the map
    loaded_parameters = []
    while itor.MoveNext():
        try:
            d = itor.Key
            loaded_parameters.append(d.Name)
        except:
            pass

    missing_params = [p_name for p_name in list_p_names if p_name not in loaded_parameters]
    # missing_params = []
    # for p_name in list_p_ames:
    #     if p_name not in loaded_parameters:
    #         missing_params.append(p_name)

    return missing_params


# req_params = ['DF_Text', 'DF_Material', 'B_Param 1', 'A_Param 3']
# missing_params = check_loaded_params(req_params)
#
# # if missing_params:
# #     print('Missing Parameters:')
# #     for p_name in missing_params:
# #         print(p_name)
#
# # Access Shared Parameter File
# sp_file = app.OpenSharedParameterFile()
# #app.SharedParametersFilename = r'N:\F-KA-Temp\Temp Daniel\RevitAPI\Revit-Test\API_test_shared_parameter.txt'
#
# # Find Matching Definition to Missing Parameter Names
# missing_def = []
# if sp_file:
#     for group in sp_file.Groups:
#         #print('\nGroup Name: {}'.format(group.Name))
#         for p_def in group.Definitions:
#             #if p_def.Name in missing_params:
#             if 'A_' in p_def.Name:
#                 missing_def.append(p_def)
#
# # Select Categories
# all_cats = doc.Settings.Categories
# cat_views = all_cats.get_Item(BuiltInCategory.OST_Views)
# cat_sheets = all_cats.get_Item(BuiltInCategory.OST_Sheets)
#
# # Create Category Set
# cat_set = CategorySet()
# cat_set.Insert(cat_views)
# cat_set.Insert(cat_sheets)
#
# # Create Binding
# binding = InstanceBinding(cat_set)
# #binding = TypeBinding(cat_set)
#
# # Select ParameterGroup
# param_group = BuiltInParameterGroup.PG_TEXT
#
# # Add parameters
# t = Transaction(doc, 'AddSharedParameters')
# t.Start()
#
# for p_def in missing_def:
#     if not doc.ParameterBindings.Contains(p_def):
#         doc.ParameterBindings.Insert(p_def, binding, param_group)
#         print('Adding Shared Parameter: {}'.format(p_def.Name))
#
# t.Commit()

#
# t = Transaction(doc, "SetVariesByGroup")
# t.Start()
#
# bindings_map = doc.ParameterBindings
# it = bindings_map.ForwardIterator()
# it.Reset()
#
# while it.MoveNext():
#     try:
#         p_def = it.Key
#         if 'DF_' in p_def.Name:
#             try:
#                 p_def.SetAllowVaryBetweenGroups(doc, True)
#                 print('Set VaryByGroup for: {}'.format(p_def.Name))
#             except:
#                 pass
#     except:
#         pass
# t.Commit()

#
# def load_params(p_names_to_load,
#                 bic_cats,
#                 bind_mode='instance',
#                 p_group=BuiltInParameterGroup.PG_TEXT,
#                 set_vary_by_group=True):
#     #type: (list, list, str, BuiltInParameterGroup, bool) -> None
#     """Function to check Loaded Shared Parameters.
#     :param p_names_to_load:     List of Parameter names
#     :param bic_cats:            List of BuiltInCategories for Parameters
#     :param bind_mode:           Binding Mode: 'instance' / 'type'
#     :param p_group:             BuiltInParameterGroup
#     :param set_vary_by_group:   Bool to set parameters as VaryByGroup if possible"""
#
#     # Ensure SharedParameeterFile is available
#     sp_file = app.OpenSharedParameterFile()
#     if not sp_file:
#         forms.alert("Could not find SharedParameterFile."
#                     "\n Please Set The file in Revit and Try Again", exitscript=True)
#
#     # Ensure SharedParameterFile is available
#     p_def_to_load = []
#     found_params = []
#     for group in sp_file.Groups:
#         for p_def in group.Definitions:
#             if p_def.Name in p_names_to_load:
#                 p_def_to_load.append(p_def)
#                 found_params.append(p_def.Name)
#
#     not_found_params = [p_name for p_name in p_names_to_load if not p_name in found_params]
#
#     if not_found_params:
#         print("Couldn't find following Parameters:\n{}".format('\n'.join(not_found_params)))
#
#     # Prepare Categories
#     all_cats = doc.Settings.Categories
#     cats = [all_cats.get_Item(bic_cat) for bic_cat in bic_cats]
#
#     # Create Category Sets
#     cat_set = CategorySet()
#     for cat in cats:
#         cat_set.Insert(cat)
#
#     # Binding
#     binding = InstanceBinding(cat_set) if bind_mode == 'instance' else TypeBinding(cat_set)
#
#     # Add Parameters
#     for p_def in p_def_to_load:
#         doc.ParameterBindings.Insert(p_def, binding, p_group)
#
#     # SetVaryByGroup
#     if set_vary_by_group:
#         bindings_map = doc.ParameterBindings
#         it = bindings_map.ForwardIterator()
#         it.Reset()
#
#         while it.MoveNext():
#             p_def = it.Key
#             if p_def in p_def_to_load:
#                 try:
#                     p_def.SetAllowVaryBetweenGroups(doc, True)
#                 except:
#                     pass

def get_loaded_parameters_as_def():
    """Get Loaded Parameters in the project as Definitions"""
    definitions = []

    binding_map = doc.ParameterBindings
    it = binding_map.ForwardIterator()
    for i in it:
        definition = it.Key
        definitions.append(definition)
    return definitions


def load_params(p_names_to_load,
                bic_cats,
                bind_mode = 'instance',
                p_group   = BuiltInParameterGroup.PG_TITLE):
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
                                "\n{p_filepath}".format(n_missing      = len(missing_params),
                                                        missing_params = '\n'.join(missing_params),
                                                        p_filepath     = sp_file.Filename),
                                yes=True, no=True)

        if confirmed:
            # Prepare Categories
            all_cats = doc.Settings.Categories
            cats     = [all_cats.get_Item(bic_cat) for bic_cat in bic_cats]

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


req_params = ['DF_Text', 'DF_Material', 'B_Param 1', 'A_Param 3', 'error']
missing_params = check_loaded_params(req_params)


t = Transaction(doc, 'AddSharedParameters')
t.Start()

bic_cats = [BuiltInCategory.OST_Walls, BuiltInCategory.OST_Floors]

load_params(missing_params,
            bic_cats,
            bind_mode=BuiltInParameterGroup.PG_DATA)

t.Commit()
