# ResoniteLink AI World Builder v5.0
# templates.py - Multi-object scene templates

"""
Pre-defined scene templates for multi-object creation.
"""


# ============================================================
# SCENE TEMPLATES
# ============================================================

TEMPLATES = {
    "table_with_chairs": {
        "description": "A wooden table with 4 chairs around it",
        "objects": [
            # Table top
            {
                "name": "TableTop",
                "mesh": "box",
                "position": [0, 0.75, 0],
                "scale": [1.2, 0.05, 0.8],
                "color": [0.54, 0.36, 0.2]  # wood_medium
            },
            # Table legs
            {
                "name": "TableLeg1",
                "mesh": "box",
                "position": [-0.5, 0.375, -0.3],
                "scale": [0.06, 0.75, 0.06],
                "color": [0.54, 0.36, 0.2]
            },
            {
                "name": "TableLeg2",
                "mesh": "box",
                "position": [0.5, 0.375, -0.3],
                "scale": [0.06, 0.75, 0.06],
                "color": [0.54, 0.36, 0.2]
            },
            {
                "name": "TableLeg3",
                "mesh": "box",
                "position": [-0.5, 0.375, 0.3],
                "scale": [0.06, 0.75, 0.06],
                "color": [0.54, 0.36, 0.2]
            },
            {
                "name": "TableLeg4",
                "mesh": "box",
                "position": [0.5, 0.375, 0.3],
                "scale": [0.06, 0.75, 0.06],
                "color": [0.54, 0.36, 0.2]
            },
            # Chairs
            {
                "name": "Chair1_Seat",
                "mesh": "box",
                "position": [0, 0.45, -0.9],
                "scale": [0.4, 0.05, 0.4],
                "color": [0.3, 0.15, 0.05]  # wood_dark
            },
            {
                "name": "Chair2_Seat",
                "mesh": "box",
                "position": [0, 0.45, 0.9],
                "scale": [0.4, 0.05, 0.4],
                "color": [0.3, 0.15, 0.05]
            },
            {
                "name": "Chair3_Seat",
                "mesh": "box",
                "position": [-0.9, 0.45, 0],
                "scale": [0.4, 0.05, 0.4],
                "color": [0.3, 0.15, 0.05]
            },
            {
                "name": "Chair4_Seat",
                "mesh": "box",
                "position": [0.9, 0.45, 0],
                "scale": [0.4, 0.05, 0.4],
                "color": [0.3, 0.15, 0.05]
            },
        ]
    },
    
    "campfire": {
        "description": "A campfire with logs arranged in a circle and a warm light",
        "objects": [
            # Light source
            {
                "name": "FireLight",
                "type": "light",
                "position": [0, 0.4, 0],
                "light_type": "Point",
                "color": [1.0, 0.5, 0.1],  # warm orange
                "intensity": 3.0,
                "range": 8.0
            },
            # Logs arranged in a circle
            {
                "name": "Log1",
                "mesh": "cylinder",
                "position": [0.25, 0.08, 0],
                "scale": [0.08, 0.5, 0.08],
                "rotation_euler": [0, 0, 75],
                "color": [0.3, 0.15, 0.05]
            },
            {
                "name": "Log2",
                "mesh": "cylinder",
                "position": [-0.25, 0.08, 0],
                "scale": [0.08, 0.5, 0.08],
                "rotation_euler": [0, 0, -75],
                "color": [0.3, 0.15, 0.05]
            },
            {
                "name": "Log3",
                "mesh": "cylinder",
                "position": [0, 0.08, 0.25],
                "scale": [0.08, 0.5, 0.08],
                "rotation_euler": [75, 0, 0],
                "color": [0.3, 0.15, 0.05]
            },
            {
                "name": "Log4",
                "mesh": "cylinder",
                "position": [0, 0.08, -0.25],
                "scale": [0.08, 0.5, 0.08],
                "rotation_euler": [-75, 0, 0],
                "color": [0.3, 0.15, 0.05]
            },
            # Stone ring
            {
                "name": "Stone1",
                "mesh": "sphere",
                "position": [0.4, 0.05, 0],
                "scale": [0.12, 0.1, 0.12],
                "color": [0.4, 0.4, 0.4]
            },
            {
                "name": "Stone2",
                "mesh": "sphere",
                "position": [-0.4, 0.05, 0],
                "scale": [0.12, 0.1, 0.12],
                "color": [0.4, 0.4, 0.4]
            },
            {
                "name": "Stone3",
                "mesh": "sphere",
                "position": [0, 0.05, 0.4],
                "scale": [0.12, 0.1, 0.12],
                "color": [0.4, 0.4, 0.4]
            },
            {
                "name": "Stone4",
                "mesh": "sphere",
                "position": [0, 0.05, -0.4],
                "scale": [0.12, 0.1, 0.12],
                "color": [0.4, 0.4, 0.4]
            },
            {
                "name": "Stone5",
                "mesh": "sphere",
                "position": [0.28, 0.05, 0.28],
                "scale": [0.1, 0.08, 0.1],
                "color": [0.35, 0.35, 0.35]
            },
            {
                "name": "Stone6",
                "mesh": "sphere",
                "position": [-0.28, 0.05, 0.28],
                "scale": [0.1, 0.08, 0.1],
                "color": [0.35, 0.35, 0.35]
            },
            {
                "name": "Stone7",
                "mesh": "sphere",
                "position": [0.28, 0.05, -0.28],
                "scale": [0.1, 0.08, 0.1],
                "color": [0.35, 0.35, 0.35]
            },
            {
                "name": "Stone8",
                "mesh": "sphere",
                "position": [-0.28, 0.05, -0.28],
                "scale": [0.1, 0.08, 0.1],
                "color": [0.35, 0.35, 0.35]
            },
        ]
    },
    
    "simple_room": {
        "description": "A simple room with floor, ceiling, and 4 walls",
        "objects": [
            # Floor
            {
                "name": "Floor",
                "mesh": "box",
                "position": [0, 0, 0],
                "scale": [4, 0.1, 4],
                "color": [0.76, 0.6, 0.42]  # wood_light
            },
            # Ceiling
            {
                "name": "Ceiling",
                "mesh": "box",
                "position": [0, 3, 0],
                "scale": [4, 0.1, 4],
                "color": [0.9, 0.9, 0.9]
            },
            # Walls
            {
                "name": "WallNorth",
                "mesh": "box",
                "position": [0, 1.5, -2],
                "scale": [4, 3, 0.1],
                "color": [0.85, 0.85, 0.8]
            },
            {
                "name": "WallSouth",
                "mesh": "box",
                "position": [0, 1.5, 2],
                "scale": [4, 3, 0.1],
                "color": [0.85, 0.85, 0.8]
            },
            {
                "name": "WallEast",
                "mesh": "box",
                "position": [2, 1.5, 0],
                "scale": [0.1, 3, 4],
                "color": [0.85, 0.85, 0.8]
            },
            {
                "name": "WallWest",
                "mesh": "box",
                "position": [-2, 1.5, 0],
                "scale": [0.1, 3, 4],
                "color": [0.85, 0.85, 0.8]
            },
            # Ceiling light
            {
                "name": "CeilingLight",
                "type": "light",
                "position": [0, 2.8, 0],
                "light_type": "Point",
                "color": [1.0, 0.95, 0.9],
                "intensity": 2.0,
                "range": 6.0
            },
        ]
    },
    
    "lamp": {
        "description": "A standing lamp with light",
        "objects": [
            # Base
            {
                "name": "LampBase",
                "mesh": "cylinder",
                "position": [0, 0.02, 0],
                "scale": [0.2, 0.04, 0.2],
                "color": [0.2, 0.2, 0.2]
            },
            # Pole
            {
                "name": "LampPole",
                "mesh": "cylinder",
                "position": [0, 0.7, 0],
                "scale": [0.03, 1.4, 0.03],
                "color": [0.3, 0.3, 0.3]
            },
            # Shade
            {
                "name": "LampShade",
                "mesh": "cone",
                "position": [0, 1.4, 0],
                "scale": [0.25, 0.2, 0.25],
                "color": [0.9, 0.85, 0.7]
            },
            # Light
            {
                "name": "LampLight",
                "type": "light",
                "position": [0, 1.35, 0],
                "light_type": "Point",
                "color": [1.0, 0.95, 0.8],
                "intensity": 1.5,
                "range": 4.0
            },
        ]
    },
    
    "staircase": {
        "description": "A simple staircase with 6 steps",
        "objects": [
            {
                "name": "Step1",
                "mesh": "box",
                "position": [0, 0.1, 0],
                "scale": [1, 0.2, 0.3],
                "color": [0.54, 0.36, 0.2]
            },
            {
                "name": "Step2",
                "mesh": "box",
                "position": [0, 0.3, 0.3],
                "scale": [1, 0.2, 0.3],
                "color": [0.54, 0.36, 0.2]
            },
            {
                "name": "Step3",
                "mesh": "box",
                "position": [0, 0.5, 0.6],
                "scale": [1, 0.2, 0.3],
                "color": [0.54, 0.36, 0.2]
            },
            {
                "name": "Step4",
                "mesh": "box",
                "position": [0, 0.7, 0.9],
                "scale": [1, 0.2, 0.3],
                "color": [0.54, 0.36, 0.2]
            },
            {
                "name": "Step5",
                "mesh": "box",
                "position": [0, 0.9, 1.2],
                "scale": [1, 0.2, 0.3],
                "color": [0.54, 0.36, 0.2]
            },
            {
                "name": "Step6",
                "mesh": "box",
                "position": [0, 1.1, 1.5],
                "scale": [1, 0.2, 0.3],
                "color": [0.54, 0.36, 0.2]
            },
        ]
    },
    
    "spotlight_stage": {
        "description": "A simple stage with 3 spotlights",
        "objects": [
            # Stage platform
            {
                "name": "Stage",
                "mesh": "box",
                "position": [0, 0.15, 0],
                "scale": [4, 0.3, 3],
                "color": [0.2, 0.15, 0.1]
            },
            # Spotlights
            {
                "name": "SpotlightLeft",
                "type": "light",
                "position": [-1.5, 3, -1],
                "light_type": "Spot",
                "color": [1.0, 0.3, 0.3],  # red
                "intensity": 5.0,
                "range": 6.0
            },
            {
                "name": "SpotlightCenter",
                "type": "light",
                "position": [0, 3, -1],
                "light_type": "Spot",
                "color": [1.0, 1.0, 1.0],  # white
                "intensity": 5.0,
                "range": 6.0
            },
            {
                "name": "SpotlightRight",
                "type": "light",
                "position": [1.5, 3, -1],
                "light_type": "Spot",
                "color": [0.3, 0.3, 1.0],  # blue
                "intensity": 5.0,
                "range": 6.0
            },
        ]
    },
}


def get_template(name):
    """Get a scene template by name.
    
    Args:
        name: Template name (case-insensitive, spaces/hyphens converted to underscores)
    
    Returns:
        dict: Template definition or None if not found
    """
    # Normalize name
    normalized = name.lower().replace(" ", "_").replace("-", "_")
    return TEMPLATES.get(normalized)


def list_templates():
    """Get list of available template names and descriptions.
    
    Returns:
        list: List of (name, description) tuples
    """
    return [(name, data["description"]) for name, data in TEMPLATES.items()]
