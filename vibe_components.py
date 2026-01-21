# ResoniteLink AI World Builder v5.0
# components.py - Component registry and definitions

"""
Registry of all supported Resonite components and their metadata.
"""


# ============================================================
# COMPONENT TYPES
# ============================================================

COMPONENTS = {
    # Meshes
    "box": "[FrooxEngine]FrooxEngine.BoxMesh",
    "sphere": "[FrooxEngine]FrooxEngine.SphereMesh",
    "cylinder": "[FrooxEngine]FrooxEngine.CylinderMesh",
    "cone": "[FrooxEngine]FrooxEngine.ConeMesh",
    "capsule": "[FrooxEngine]FrooxEngine.CapsuleMesh",
    "torus": "[FrooxEngine]FrooxEngine.TorusMesh",
    "bevel_box": "[FrooxEngine]FrooxEngine.BevelBoxMesh",
    "quad": "[FrooxEngine]FrooxEngine.QuadMesh",
    "triangle": "[FrooxEngine]FrooxEngine.TriangleMesh",
    
    # Rendering
    "material": "[FrooxEngine]FrooxEngine.PBS_Metallic",
    "material_metallic": "[FrooxEngine]FrooxEngine.PBS_Metallic",
    "material_specular": "[FrooxEngine]FrooxEngine.PBS_Specular",
    "unlit_material": "[FrooxEngine]FrooxEngine.UnlitMaterial",
    "renderer": "[FrooxEngine]FrooxEngine.MeshRenderer",
    "mesh_renderer": "[FrooxEngine]FrooxEngine.MeshRenderer",
    
    # Physics
    "box_collider": "[FrooxEngine]FrooxEngine.BoxCollider",
    "sphere_collider": "[FrooxEngine]FrooxEngine.SphereCollider",
    "mesh_collider": "[FrooxEngine]FrooxEngine.MeshCollider",
    "capsule_collider": "[FrooxEngine]FrooxEngine.CapsuleCollider",
    "cylinder_collider": "[FrooxEngine]FrooxEngine.CylinderCollider",
    
    # Interaction
    "grabbable": "[FrooxEngine]FrooxEngine.Grabbable",
    
    # Animation/Transform
    "spinner": "[FrooxEngine]FrooxEngine.Spinner",
    "wiggler": "[FrooxEngine]FrooxEngine.Wiggler",
    "wobbler": "[FrooxEngine]FrooxEngine.Wobbler",
    "panner1d": "[FrooxEngine]FrooxEngine.Panner1D",
    "panner2d": "[FrooxEngine]FrooxEngine.Panner2D",
    "panner3d": "[FrooxEngine]FrooxEngine.Panner3D",
    
    # Lighting
    "light": "[FrooxEngine]FrooxEngine.Light",
    
    # Metadata
    "comment": "[FrooxEngine]FrooxEngine.Comment",
    "license": "[FrooxEngine]FrooxEngine.License",

    # ProtoFlux (experimental)
    "protoflux_node_visual": "[FrooxEngine]FrooxEngine.ProtoFlux.ProtoFluxNodeVisual",
    "protoflux_node_debug": "[FrooxEngine]FrooxEngine.ProtoFlux.ProtoFluxNodeDebugInfo",
    "protoflux_wire_manager": "[FrooxEngine]FrooxEngine.ProtoFlux.ProtoFluxWireManager",
    "protoflux_arrow_manager": "[FrooxEngine]FrooxEngine.ProtofluxArrowManager",
}


# ============================================================
# ENUM TYPES
# ============================================================

ENUMS = {
    "LightType": ["Directional", "Point", "Spot"],
    "BlendMode": ["Opaque", "Cutout", "Alpha"],
    "ShadowCastMode": ["Off", "On", "TwoSided", "ShadowsOnly"],
    "Sidedness": ["Auto", "Front", "Back", "Double"],
    "WireType": ["Input", "Output", "Reference"],
}


# ============================================================
# COMPONENT FIELD DEFINITIONS
# ============================================================

# Maps component short names to their configurable fields
COMPONENT_FIELDS = {
    "spinner": {
        "speed": "_speed",  # float3 - rotation in degrees/sec
    },
    "wiggler": {
        "speed": "_speed",      # float3
        "magnitude": "_magnitude",  # float3
    },
    "wobbler": {
        "speed": "_speed",      # float
        "magnitude": "_magnitude",  # float
    },
    "light": {
        "type": "LightType",      # enum (Point, Spot, Directional)
        "intensity": "Intensity",  # float
        "color": "Color",          # colorX
        "range": "Range",          # float
        "spot_angle": "SpotAngle", # float (for Spot lights)
    },
    "material": {
        "color": "AlbedoColor",     # colorX
        "albedo": "AlbedoColor",    # alias
        "metallic": "Metallic",     # float (0-1)
        "smoothness": "Smoothness", # float (0-1)
        "blend_mode": "BlendMode",  # enum
        "emission": "EmissiveColor", # colorX
    },
    "renderer": {
        "mesh": "Mesh",         # reference
        "materials": "Materials", # list of references
    },
    "comment": {
        "text": "Text",  # string
    },
    "license": {
        "credit": "CreditString",       # string
        "require_credit": "RequireCredit", # bool
        "can_export": "CanExport",      # bool
    },
    "protoflux_wire_manager": {
        "connect_point": "ConnectPoint",  # reference (slot)
        "type": "Type",                   # enum WireType
        "width": "Width",                 # float
        "start_color": "StartColor",      # colorX
        "end_color": "EndColor",          # colorX
    },
}


# ============================================================
# MESH TO COLLIDER MAPPING
# ============================================================

# Automatically select appropriate collider for mesh type
MESH_TO_COLLIDER = {
    "box": "box_collider",
    "bevel_box": "box_collider",
    "sphere": "sphere_collider",
    "cylinder": "cylinder_collider",
    "capsule": "capsule_collider",
    "cone": "mesh_collider",
    "torus": "mesh_collider",
    "quad": "mesh_collider",
    "triangle": "mesh_collider",
}


# ============================================================
# SYSTEM OBJECTS - DO NOT MODIFY
# ============================================================

SYSTEM_OBJECTS = [
    "Controllers",
    "Roles",
    "SpawnArea",
    "Light",
    "Skybox",
    "__TEMP",
    "Undo Manager",
    "Assets",
    "Clipboard Importer",
]


def is_system_object(name):
    """Check if a slot name is a protected system object.
    
    Args:
        name: Slot name to check
    
    Returns:
        bool: True if this is a system object that should not be modified
    """
    if name in SYSTEM_OBJECTS:
        return True
    if name.startswith("User "):
        return True
    return False


def get_component_type(short_name):
    """Get full component type from short name.
    
    Args:
        short_name: Short name like "box" or "spinner"
    
    Returns:
        str: Full component type or None if not found
    """
    return COMPONENTS.get(short_name.lower())


def get_collider_for_mesh(mesh_name):
    """Get appropriate collider type for a mesh.
    
    Args:
        mesh_name: Short mesh name like "box" or "sphere"
    
    Returns:
        str: Short collider name or "mesh_collider" as default
    """
    return MESH_TO_COLLIDER.get(mesh_name.lower(), "mesh_collider")


def get_field_name(component_name, field_alias):
    """Get actual field name from alias.
    
    Args:
        component_name: Short component name
        field_alias: Field alias used in prompt
    
    Returns:
        str: Actual field name or the alias if not found
    """
    fields = COMPONENT_FIELDS.get(component_name.lower(), {})
    return fields.get(field_alias.lower(), field_alias)
