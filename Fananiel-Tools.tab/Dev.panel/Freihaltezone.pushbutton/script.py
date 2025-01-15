# -*- coding: utf-8 -*-
__title__ = "Freihaltezone"
__doc__ = """Version = 1.0
Date    = 08.01.2025
________________________________________________________________
Author: Daniel Förster"""

from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import *
from pyrevit import forms
import math
from Snippets._convert import *

# Document und Selection Setup
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
selection = uidoc.Selection

try:
    # IFC Element auswählen und Informationen holen
    ref = selection.PickObject(ObjectType.LinkedElement, "Wählen Sie ein Element aus der IFC")

    link_instance = doc.GetElement(ref.ElementId)
    link_doc = link_instance.GetLinkDocument()
    linked_element = link_doc.GetElement(ref.LinkedElementId)

    geom = linked_element.Geometry

    print(linked_element)
    print(geom)

    # Transformation des Links holen
    transform = link_instance.GetTransform()

    # Geometrie-Parameter abrufen
    bbox = linked_element.get_BoundingBox(None)

    # Dimensionen berechnen
    width = bbox.Max.X - bbox.Min.X
    height = bbox.Max.Z - bbox.Min.Z
    depth = bbox.Max.Y - bbox.Min.Y

    # Level (Ebene) des Elements finden
    level_id = linked_element.LevelId
    level = link_doc.GetElement(level_id)
    level_name = level.Name if level is not None else "Keine Ebene zugewiesen"

    print("Element-Informationen:")
    print("Breite: " + str(convert_internal_units(width,False,)))
    print("Hoehe: " + str(convert_internal_units(height, False)))
    print("Tiefe: " + str(convert_internal_units(depth,False)))
    print("Ebene: " + str(level_name))

    # Level vom User auswählen lassen
    host_level = forms.select_levels(title='Wählen Sie ein Level')[0]

    if host_level is None:
        print("Kein Level ausgewählt!")
        raise Exception()

    # Z-Offset in internen Revit-Einheiten (12100)
    z_offset = 12100 / 304.8  # Umrechnung von Millimeter in Fuß

    # Unterer Mittelpunkt im IFC-Koordinatensystem mit Level-Höhe und Offset
    ifc_origin = XYZ(
        (bbox.Min.X + bbox.Max.X) / 2,  # X-Mittelpunkt
        (bbox.Min.Y + bbox.Max.Y) / 2,  # Y-Mittelpunkt
        host_level.Elevation + z_offset  # Z-Wert mit Offset
    )



    # Transformation auf Revit-Koordinaten
    origin = transform.OfPoint(ifc_origin)

    # Dimensionen berechnen
    width = abs(bbox.Max.X - bbox.Min.X)  # Breite in X-Richtung
    height = abs(bbox.Max.Z - bbox.Min.Z)  # Höhe in Z-Richtung
    depth = abs(bbox.Max.Y - bbox.Min.Y)  # Tiefe in Y-Richtung

    print(width)
    print(depth)

    print("\nOriginal Dimensionen:")
    print("Breite (X): " + str(width * 304.8) + " mm")
    print("Tiefe (Y): " + str(depth * 304.8) + " mm")
    print("Höhe (Z): " + str(height * 304.8) + " mm")

    # Familie finden
    collector = FilteredElementCollector(doc).OfClass(FamilySymbol)
    family_symbol = None
    for symbol in collector:
        if symbol.FamilyName == "Freihaltezone_Förderanlagen":
            family_symbol = symbol
            break

    if family_symbol is None:
        print("Familie 'Freihaltezone_Förderanlagen' nicht gefunden!")
        raise Exception()

    # Transaction für das Erstellen der Instanz
    t = Transaction(doc, "Freihaltezone erstellen")
    t.Start()
    try:
        # Familientyp aktivieren
        if not family_symbol.IsActive:
            family_symbol.Activate()

        # Instanz erstellen
        instance = doc.Create.NewFamilyInstance(
            origin,
            family_symbol,
            host_level,
            0)

        # Parameter setzen (Tauschen von Breite und Tiefe)
        instance.LookupParameter("Länge").Set(width)  # X-Dimension als Länge
        instance.LookupParameter("Breite").Set(depth)  # Y-Dimension als Breite
        instance.LookupParameter("Höhe").Set(height)  # Z-Dimension als Höhe

        t.Commit()
        print("Freihaltezone wurde erfolgreich erstellt!")
        print("\nPositionierung:")
        print("X: " + str(origin.X))
        print("Y: " + str(origin.Y))
        print("Z: " + str(origin.Z))

    except Exception as e:
        t.RollBack()
        print("Fehler beim Erstellen der Instanz: " + str(e))

except Exception as e:
    print("Fehler: " + str(e))

