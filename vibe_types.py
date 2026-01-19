# ResoniteLink AI World Builder v5.0
# types.py - Resonite type helper functions

"""
Helper functions to create properly formatted Resonite type values.
All functions return dictionaries ready to be serialized to JSON.
"""


def colorX(r, g, b, a=1.0, profile="sRGB"):
    """Create a colorX value.
    
    Args:
        r: Red component (0.0-1.0)
        g: Green component (0.0-1.0)
        b: Blue component (0.0-1.0)
        a: Alpha component (0.0-1.0), default 1.0
        profile: Color profile, default "sRGB"
    
    Returns:
        dict: Properly formatted colorX type
    """
    return {
        "$type": "colorX",
        "value": {"r": r, "g": g, "b": b, "a": a, "profile": profile}
    }


def float3(x, y, z):
    """Create a float3 value (3D vector).
    
    Args:
        x: X component
        y: Y component
        z: Z component
    
    Returns:
        dict: Properly formatted float3 type
    """
    return {
        "$type": "float3",
        "value": {"x": x, "y": y, "z": z}
    }


def float2(x, y):
    """Create a float2 value (2D vector).
    
    Args:
        x: X component
        y: Y component
    
    Returns:
        dict: Properly formatted float2 type
    """
    return {
        "$type": "float2",
        "value": {"x": x, "y": y}
    }


def floatQ(x, y, z, w=1.0):
    """Create a floatQ value (quaternion for rotation).
    
    Args:
        x: X component
        y: Y component
        z: Z component
        w: W component, default 1.0
    
    Returns:
        dict: Properly formatted floatQ type
    """
    return {
        "$type": "floatQ",
        "value": {"x": x, "y": y, "z": z, "w": w}
    }


def enum(value, enum_type):
    """Create an enum value.
    
    Args:
        value: Enum value as string (e.g., "Point", "Alpha")
        enum_type: Enum type name (e.g., "LightType", "BlendMode")
    
    Returns:
        dict: Properly formatted enum type
    """
    return {
        "$type": "enum",
        "value": value,
        "enumType": enum_type
    }


def reference(target_id=None):
    """Create a reference value.
    
    Args:
        target_id: ID of the target object, or None for empty reference
    
    Returns:
        dict: Properly formatted reference type
    """
    if target_id is None:
        return {"$type": "reference"}
    return {
        "$type": "reference",
        "targetId": target_id
    }


def string(value):
    """Create a string value.
    
    Args:
        value: String content
    
    Returns:
        dict: Properly formatted string type
    """
    return {
        "$type": "string",
        "value": value
    }


def bool_val(value):
    """Create a bool value.
    
    Args:
        value: Boolean value (True/False)
    
    Returns:
        dict: Properly formatted bool type
    """
    return {
        "$type": "bool",
        "value": value
    }


def float_val(value):
    """Create a float value.
    
    Args:
        value: Float number
    
    Returns:
        dict: Properly formatted float type
    """
    return {
        "$type": "float",
        "value": value
    }


def int_val(value):
    """Create an int value.
    
    Args:
        value: Integer number
    
    Returns:
        dict: Properly formatted int type
    """
    return {
        "$type": "int",
        "value": value
    }


def list_val(elements):
    """Create a list value.
    
    Args:
        elements: List of elements
    
    Returns:
        dict: Properly formatted list type
    """
    return {
        "$type": "list",
        "elements": elements
    }


# ============================================================
# COLOR PRESETS
# ============================================================

COLORS = {
    # Primary
    "red": colorX(1.0, 0.0, 0.0),
    "green": colorX(0.0, 1.0, 0.0),
    "blue": colorX(0.0, 0.0, 1.0),
    
    # Secondary
    "yellow": colorX(1.0, 1.0, 0.0),
    "cyan": colorX(0.0, 1.0, 1.0),
    "magenta": colorX(1.0, 0.0, 1.0),
    
    # Neutrals
    "white": colorX(1.0, 1.0, 1.0),
    "black": colorX(0.0, 0.0, 0.0),
    "gray": colorX(0.5, 0.5, 0.5),
    "grey": colorX(0.5, 0.5, 0.5),
    
    # Extended
    "orange": colorX(1.0, 0.5, 0.0),
    "purple": colorX(0.5, 0.0, 1.0),
    "pink": colorX(1.0, 0.4, 0.7),
    "brown": colorX(0.4, 0.2, 0.1),
    "tan": colorX(0.82, 0.71, 0.55),
    
    # Light variants
    "light_red": colorX(1.0, 0.5, 0.5),
    "light_green": colorX(0.5, 1.0, 0.5),
    "light_blue": colorX(0.5, 0.5, 1.0),
    
    # Dark variants
    "dark_red": colorX(0.5, 0.0, 0.0),
    "dark_green": colorX(0.0, 0.5, 0.0),
    "dark_blue": colorX(0.0, 0.0, 0.5),
    
    # Materials
    "gold": colorX(1.0, 0.84, 0.0),
    "silver": colorX(0.75, 0.75, 0.75),
    "bronze": colorX(0.8, 0.5, 0.2),
    "copper": colorX(0.72, 0.45, 0.2),
    
    # Wood tones
    "wood_light": colorX(0.76, 0.6, 0.42),
    "wood_medium": colorX(0.54, 0.36, 0.2),
    "wood_dark": colorX(0.3, 0.15, 0.05),
}


def get_color(name):
    """Get a color by name, or parse RGB values.
    
    Args:
        name: Color name (e.g., "red") or RGB tuple (r, g, b)
    
    Returns:
        dict: colorX formatted value
    """
    if isinstance(name, str):
        name_lower = name.lower().replace(" ", "_").replace("-", "_")
        if name_lower in COLORS:
            return COLORS[name_lower]
        # Unknown color, default to gray
        return COLORS["gray"]
    elif isinstance(name, (list, tuple)) and len(name) >= 3:
        r, g, b = name[0], name[1], name[2]
        a = name[3] if len(name) > 3 else 1.0
        return colorX(r, g, b, a)
    else:
        return COLORS["gray"]
