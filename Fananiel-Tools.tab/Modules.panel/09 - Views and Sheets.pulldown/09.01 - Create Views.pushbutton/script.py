


from Autodesk.Revit.DB import *

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
#==================================================
uidoc  = __revit__.ActiveUIDocument
doc    = __revit__.ActiveUIDocument.Document #type:Document


# Get Active Level
active_view  = doc.ActiveView
active_level = active_view.GenLevel #Only for ViewPlans!

# ALL VIEW TYPES
view_types = FilteredElementCollector(doc).OfClass(ViewFamilyType).ToElements()

# FILTER CERTAIN VIEW TYPES
view_types_plans    = [vt for vt in view_types if vt.ViewFamily == ViewFamily.FloorPlan]
view_types_sections = [vt for vt in view_types if vt.ViewFamily == ViewFamily.Section]
view_types_3D       = [vt for vt in view_types if vt.ViewFamily == ViewFamily.ThreeDimensional]
view_types_legends  = [vt for vt in view_types if vt.ViewFamily == ViewFamily.Legend]
view_types_drafting = [vt for vt in view_types if vt.ViewFamily == ViewFamily.Drafting]
view_types_elev     = [vt for vt in view_types if vt.ViewFamily == ViewFamily.Elevation]
view_types_ceil     = [vt for vt in view_types if vt.ViewFamily == ViewFamily.CeilingPlan]
view_types_stru     = [vt for vt in view_types if vt.ViewFamily == ViewFamily.StructuralPlan]
view_types_area     = [vt for vt in view_types if vt.ViewFamily == ViewFamily.AreaPlan]