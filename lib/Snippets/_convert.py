# -*- coding: utf-8 -*-

# Imports
# ==================================================
from Autodesk.Revit.DB import *

# Variables
# ==================================================
app    = __revit__.Application
uidoc  = __revit__.ActiveUIDocument
doc    = __revit__.ActiveUIDocument.Document #type:Document

rvt_year = int(app.VersionNumber)

# Functions

def convert_internal_units(length, get_internal=True, unit='m'):
    # type: (float,bool) -> float
    """Function to convert Internal units to meters or vice versa
    :param length:          Value to Convert
    :param get_internal:    True to get internal units, False to get Meters
    :param unit:            Select desired Units: ['m', 'm2']
    :return:                Length in Internal units or Meters."""

    if rvt_year >= 2021:
        # New Method
        from Autodesk.Revit.DB import UnitTypeId
        if unit == 'm': units = UnitTypeId.Meters
        elif unit == 'm2':  units = UnitTypeId.SquareMeters

    else:
        from Autodesk.Revit.DB import DisplayUnitType
        if unit == 'm':
            units = DisplayUnitType.DUT_METERS
        elif unit == 'm2':
            units = DisplayUnitType.DUT_SQUARE_METERS

        # Old Method

    if get_internal:
        return UnitUtils.ConvertToInternalUnits(length, units)

    return UnitUtils.ConvertFromInternalUnits(length, units)