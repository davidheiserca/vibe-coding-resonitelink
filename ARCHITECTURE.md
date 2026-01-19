# ResoniteLink AI World Builder v4.0 - Architecture

**Version:** 4.0  
**Date:** January 17, 2026  
**Status:** In Development

---

## Design Goals

1. **Clean, modular architecture** - Separate concerns into distinct modules
2. **Extensible component system** - Easy to add new component types
3. **Better error handling** - Graceful recovery, informative messages
4. **All v2.1 features** - Config, logging, JSON export, Comment, License
5. **New v3.0 features** - Lights, Enums, more meshes, multi-object scenes

---

## Module Structure

```
v4/
├── resonite_builder.py      # Main entry point
├── config.py                # Configuration loading
├── logging_utils.py         # Logging and JSON export
├── client.py                # ResoniteLink WebSocket client
├── executor.py              # AI command execution
├── components.py            # Component type definitions
├── types.py                 # Resonite type helpers (colorX, float3, etc.)
└── templates.py             # Multi-object scene templates
```

---

## New Features in v4.0

### 1. Light Components
- `[FrooxEngine]FrooxEngine.Light`
- Fields: LightType (enum), Intensity (float), Color (colorX), Range (float)
- LightType values: Point, Spot, Directional

### 2. Enum Support
- Proper `$type: "enum"` format
- BlendMode: Opaque, Cutout, Alpha
- LightType: Point, Spot, Directional

### 3. More Mesh Types
- BevelBoxMesh
- RampMesh
- FrameMesh
- QuadMesh

### 4. More Animation Components
- Wiggler (_speed, _magnitude)
- Wobbler (_speed, _magnitude)

### 5. Multi-Object Scenes
- Scene templates (table with chairs, room, etc.)
- Hierarchical slot creation (parent-child)
- Relative positioning

### 6. System Object Protection
- Prevent accidental deletion of critical world objects

---

## Type System

```python
# types.py

def colorX(r, g, b, a=1.0):
    return {
        "$type": "colorX",
        "value": {"r": r, "g": g, "b": b, "a": a, "profile": "sRGB"}
    }

def float3(x, y, z):
    return {
        "$type": "float3",
        "value": {"x": x, "y": y, "z": z}
    }

def floatQ(x, y, z, w=1.0):
    return {
        "$type": "floatQ",
        "value": {"x": x, "y": y, "z": z, "w": w}
    }

def enum(value, enum_type):
    return {
        "$type": "enum",
        "value": value,
        "enumType": enum_type
    }

def reference(target_id):
    return {
        "$type": "reference",
        "targetId": target_id
    }

def string(value):
    return {
        "$type": "string",
        "value": value
    }

def bool_val(value):
    return {
        "$type": "bool",
        "value": value
    }

def float_val(value):
    return {
        "$type": "float",
        "value": value
    }
```

---

## Component Registry

```python
# components.py

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
    
    # Rendering
    "material": "[FrooxEngine]FrooxEngine.PBS_Metallic",
    "renderer": "[FrooxEngine]FrooxEngine.MeshRenderer",
    
    # Physics
    "box_collider": "[FrooxEngine]FrooxEngine.BoxCollider",
    "sphere_collider": "[FrooxEngine]FrooxEngine.SphereCollider",
    "mesh_collider": "[FrooxEngine]FrooxEngine.MeshCollider",
    
    # Interaction
    "grabbable": "[FrooxEngine]FrooxEngine.Grabbable",
    
    # Animation
    "spinner": "[FrooxEngine]FrooxEngine.Spinner",
    "wiggler": "[FrooxEngine]FrooxEngine.Wiggler",
    "wobbler": "[FrooxEngine]FrooxEngine.Wobbler",
    
    # Lighting
    "light": "[FrooxEngine]FrooxEngine.Light",
    
    # Metadata
    "comment": "[FrooxEngine]FrooxEngine.Comment",
    "license": "[FrooxEngine]FrooxEngine.License",
}

# Enum types
ENUMS = {
    "LightType": ["Point", "Spot", "Directional"],
    "BlendMode": ["Opaque", "Cutout", "Alpha"],
}

# System objects that should not be modified
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
```

---

## Scene Templates

```python
# templates.py

TEMPLATES = {
    "table_with_chairs": {
        "description": "A table with 4 chairs around it",
        "objects": [
            {"name": "Table", "mesh": "box", "position": [0, 0.4, 0], "scale": [1, 0.05, 0.6], "color": [0.4, 0.2, 0.1]},
            {"name": "TableLeg1", "mesh": "box", "position": [-0.4, 0.2, -0.25], "scale": [0.05, 0.4, 0.05], "color": [0.4, 0.2, 0.1]},
            {"name": "TableLeg2", "mesh": "box", "position": [0.4, 0.2, -0.25], "scale": [0.05, 0.4, 0.05], "color": [0.4, 0.2, 0.1]},
            {"name": "TableLeg3", "mesh": "box", "position": [-0.4, 0.2, 0.25], "scale": [0.05, 0.4, 0.05], "color": [0.4, 0.2, 0.1]},
            {"name": "TableLeg4", "mesh": "box", "position": [0.4, 0.2, 0.25], "scale": [0.05, 0.4, 0.05], "color": [0.4, 0.2, 0.1]},
            {"name": "Chair1", "mesh": "box", "position": [0, 0.25, -0.8], "scale": [0.4, 0.05, 0.4], "color": [0.3, 0.15, 0.05]},
            {"name": "Chair2", "mesh": "box", "position": [0, 0.25, 0.8], "scale": [0.4, 0.05, 0.4], "color": [0.3, 0.15, 0.05]},
            {"name": "Chair3", "mesh": "box", "position": [-0.8, 0.25, 0], "scale": [0.4, 0.05, 0.4], "color": [0.3, 0.15, 0.05]},
            {"name": "Chair4", "mesh": "box", "position": [0.8, 0.25, 0], "scale": [0.4, 0.05, 0.4], "color": [0.3, 0.15, 0.05]},
        ]
    },
    "campfire": {
        "description": "A campfire with logs and a light",
        "objects": [
            {"name": "FireLight", "type": "light", "position": [0, 0.3, 0], "light_type": "Point", "color": [1, 0.5, 0.1], "intensity": 3.0, "range": 5.0},
            {"name": "Log1", "mesh": "cylinder", "position": [0.2, 0.1, 0], "rotation": [0, 0, 90], "scale": [0.1, 0.4, 0.1], "color": [0.3, 0.15, 0.05]},
            {"name": "Log2", "mesh": "cylinder", "position": [-0.2, 0.1, 0], "rotation": [0, 0, 90], "scale": [0.1, 0.4, 0.1], "color": [0.3, 0.15, 0.05]},
            {"name": "Log3", "mesh": "cylinder", "position": [0, 0.1, 0.2], "rotation": [90, 0, 0], "scale": [0.1, 0.4, 0.1], "color": [0.3, 0.15, 0.05]},
        ]
    },
}
```

---

## AI System Prompt (v4.0)

The system prompt will be significantly expanded to include:
- All new component types
- Enum format examples
- Light creation examples
- Multi-object scene examples
- Scale/rotation support

---

## Implementation Order

1. ✅ Create architecture document (this file)
2. [ ] Create types.py - Type helper functions
3. [ ] Create components.py - Component registry
4. [ ] Create config.py - Configuration loading
5. [ ] Create logging_utils.py - Logging system
6. [ ] Create client.py - WebSocket client
7. [ ] Create executor.py - Command execution
8. [ ] Create templates.py - Scene templates
9. [ ] Create resonite_builder.py - Main entry point
10. [ ] Test basic object creation
11. [ ] Test lights and enums
12. [ ] Test multi-object scenes
13. [ ] Create documentation

---

## Migration from v2.1

All v2.1 features will be preserved:
- External config file
- Timestamped log files (YYMMDD_HHMM)
- JSON command export
- Comment component with prompt metadata
- License component (CC BY-SA 4.0)
- Materials list 2-step process

---

*Architecture Document - v4.0*
