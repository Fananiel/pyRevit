from Autodesk.Revit.DB import *


def get_param_value(param):
    """Get a value from a Parameter based on its StorageType"""
    value = None
    if param.StorageType == StorageType.Double:
        value = param.AsDouble()
    if param.StorageType == StorageType.ElementId:
        value = param.AsElementId()
    if param.StorageType == StorageType.Integer:
        value = param.AsInteger()
    if param.StorageType == StorageType.String:
        value = param.AsString()

    return value
