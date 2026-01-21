# ResoniteLink AI World Builder v5.0
# vibe_executor.py - AI command execution engine with hierarchical building

"""
Executes AI-generated commands to build objects in Resonite.

NEW IN v5.0: Hierarchical Building
- Planning Phase: AI creates high-level structure plan
- Detail Phases: AI generates commands for each sub-structure separately
- Assembly: All pieces go under one root slot

This approach enables building large, complex scenes without hitting
token limits or complexity constraints.
"""

import datetime
import json
from anthropic import Anthropic

from vibe_logging import get_logger
from vibe_components import COMPONENTS, get_component_type, is_system_object
from vibe_types import colorX, float3, enum, reference, string, bool_val, float_val


# ============================================================
# LICENSE AND COMMENT TEXT
# ============================================================

LICENSE_TEXT = "This asset is licensed under CC BY-SA 4.0 © 2026 Dave the Turner. Please provide attribution when using or redistributing __https://creativecommons.org/licenses/by-sa/4.0/__"


# ============================================================
# GLOBAL PROMPT RULES - Always applied to Claude
# ============================================================

BASE_SYSTEM_PROMPT = '''GLOBAL RULES (always follow):
- Avoid floating objects. Everything must rest on the ground, a platform, or a support.
- If something is elevated, add explicit supports (legs, columns, brackets, etc.).
- Expand high-level requests into a complete, well-connected build plan with explicit sizes and positions.
- Use clear, specific sizes and positions for every part (prefer standard modular dimensions).
- Keep scale reasonable unless the user explicitly asks for extreme scale.
- Align parts precisely: no gaps or overlaps at seams; corners and joints meet cleanly.
- Ensure upper floors and roofs are supported by walls or columns underneath; avoid large unsupported spans or overhangs.
- Use consistent human-scale proportions (e.g. doors ~2m tall, ceilings ~3m, railings ~1m).
- Favor modular pieces and reuse them across the scene for consistency and to minimize unique parts.
- For repetition, describe a pattern or grid (specify count and spacing) instead of listing every item.
- Include circulation for multi-level builds (stairs, ramps, ladders) and put guardrails on any open edges.
- Enclose interior spaces with complete floors, walls, and ceilings (no open gaps).
- Openings (doors, windows) must be properly sized and framed, fitting within walls without weakening the structure.
- Add beams, trusses, or thicker supports for large spans (e.g. long bridges or wide roofs) and substantial overhangs.
- Keep a cohesive design style and material palette across the build.
- Use at least two accent colors plus a neutral base (avoid monochrome scenes).
- Optimize the scene by reusing meshes/prefabs and minimizing unique parts to improve performance.
- Use level-of-detail (LOD) principles: simplify small or distant elements to reduce complexity.
- Prefer simple, clean geometry; avoid excessive detail unless explicitly requested.
- For any rotating or oscillating objects (fans, windmills, antennas, spotlights), group moving parts under a single parent slot and attach Spinner/Wiggler to that parent so the whole assembly moves correctly.
'''



# ============================================================
# PLANNING PROMPT - High-level structure decomposition
# ============================================================

PLANNING_PROMPT = BASE_SYSTEM_PROMPT + '''You are a Resonite world builder planning assistant. Your job is to break down complex building requests into manageable sub-structures with PRECISE DIMENSIONS.

CRITICAL: You must specify exact dimensions and coordinates so all parts align perfectly.

Given a user's request, create a hierarchical build plan with:
1. root_name: Name for the entire build
2. root_position: [x, y, z] where to place in world
3. dimensions: Master dimensions that ALL sub-structures must use
4. sub_structures: List of parts with exact specifications

DIMENSION RULES:
- Define master dimensions FIRST (width, depth, height, wall_thickness)
- All sub-structures MUST reference these dimensions
- Calculate exact coordinates so parts meet at edges (no gaps, no overlaps)
- Floor is at Y=0, walls sit ON the floor, roof sits ON the walls

CONSTRUCTION PRINCIPLES:
- Use MINIMUM number of meshes (1 solid wall is better than 4 pieces)
- For walls with openings: describe the opening position/size, builder will handle it
- Parts must SHARE EDGES at joints (wall corners, roof-to-wall, etc.)
- All measurements in meters

OUTPUT FORMAT:
{
  "root_name": "BuildName",
  "root_position": [0, 0, 2],
  "description": "What this is",
  "dimensions": {
    "width": 4.0,
    "depth": 4.0, 
    "height": 3.0,
    "wall_thickness": 0.1,
    "floor_thickness": 0.1
  },
  "sub_structures": [
    {
      "name": "unique_name",
      "description": "Detailed description with EXACT dimensions from master",
      "position": [x, y, z],
      "bounds": {"min": [x1,y1,z1], "max": [x2,y2,z2]}
    }
  ]
}

EXAMPLE - "Build a small house" (4m x 4m x 3m):
{
  "root_name": "SmallHouse",
  "root_position": [0, 0, 2],
  "description": "A small house with walls, flat roof, door, and windows",
  "dimensions": {
    "width": 4.0,
    "depth": 4.0,
    "height": 3.0,
    "wall_thickness": 0.1,
    "floor_thickness": 0.1,
    "roof_thickness": 0.15,
    "door_width": 1.0,
    "door_height": 2.2,
    "window_width": 0.8,
    "window_height": 1.0
  },
  "sub_structures": [
    {
      "name": "floor",
      "description": "Single box: 4m x 0.1m x 4m, wood brown color. Position centered at origin, top surface at Y=0.",
      "position": [0, -0.05, 0],
      "bounds": {"min": [-2, -0.1, -2], "max": [2, 0, 2]}
    },
    {
      "name": "back_wall",
      "description": "Single solid box: 4m wide x 3m tall x 0.1m thick. Cream/white color. Positioned at back (negative Z). No openings.",
      "position": [0, 1.5, -1.95],
      "bounds": {"min": [-2, 0, -2], "max": [2, 3, -1.9]}
    },
    {
      "name": "front_wall",
      "description": "Wall with door opening: 4m wide x 3m tall x 0.1m thick. Door gap: 1m wide x 2.2m tall, centered. Create as 3 boxes: left section, right section, and top section above door. Cream/white color.",
      "position": [0, 1.5, 1.95],
      "bounds": {"min": [-2, 0, 1.9], "max": [2, 3, 2]}
    },
    {
      "name": "left_wall",
      "description": "Wall with window: 3.8m deep (fits between front/back walls) x 3m tall x 0.1m thick. Window: 0.8m wide x 1.0m tall, centered horizontally, bottom at 1.2m height. Create as 4 boxes around window opening. Cream/white color.",
      "position": [-1.95, 1.5, 0],
      "bounds": {"min": [-2, 0, -1.9], "max": [-1.9, 3, 1.9]}
    },
    {
      "name": "right_wall",
      "description": "Wall with window: 3.8m deep x 3m tall x 0.1m thick. Window: 0.8m wide x 1.0m tall, centered horizontally, bottom at 1.2m height. Create as 4 boxes around window opening. Cream/white color.",
      "position": [1.95, 1.5, 0],
      "bounds": {"min": [1.9, 0, -1.9], "max": [2, 3, 1.9]}
    },
    {
      "name": "roof",
      "description": "Single flat box: 4.4m x 0.15m x 4.4m (slight overhang). Dark brown color. Sits directly on top of walls at Y=3.0.",
      "position": [0, 3.075, 0],
      "bounds": {"min": [-2.2, 3.0, -2.2], "max": [2.2, 3.15, 2.2]}
    },
    {
      "name": "door",
      "description": "Single box door: 0.9m wide x 2.1m tall x 0.05m thick. Brown wood color. Fits inside door frame opening.",
      "position": [0, 1.05, 1.95],
      "bounds": {"min": [-0.45, 0, 1.925], "max": [0.45, 2.1, 1.975]}
    },
    {
      "name": "interior_light",
      "description": "Point light: warm white color, intensity 2.0, range 8.0. Centered in room near ceiling.",
      "position": [0, 2.7, 0],
      "bounds": {"min": [0, 2.7, 0], "max": [0, 2.7, 0]}
    }
  ]
}

RULES:
1. Floor top surface MUST be at Y=0
2. Walls MUST sit on floor (bottom at Y=0) and reach the same height
3. Roof MUST sit on walls (bottom at Y=wall_height)
4. Adjacent walls MUST share edges at corners
5. Use SINGLE boxes for solid walls, only split for openings
6. Window/door openings must be FULLY CONTAINED within wall bounds (not at edges)
7. All sub-structures in same build MUST use consistent dimensions
8. Always include a ground/base slab for scenes (thin box at Y=0)
9. No floating parts: if anything is above Y=0.1, it must have explicit supports
10. For repeated elements (trees, lamps, etc.), cap each cluster at 3 items
11. Floor plates must sit flush on their support (no gaps). If on slab at Y=0, floor bottom must be Y=0.
12. Bridges must be clear-span between buildings (no intersections with walls); place bridge decks offset outward from facades.

Respond with ONLY a JSON object. Do NOT wrap in code fences.
'''


# ============================================================
# DETAIL PROMPT - Build commands for a single sub-structure
# ============================================================

DETAIL_PROMPT = BASE_SYSTEM_PROMPT + '''You are a Resonite world builder assistant. Generate ResoniteLink commands for ONE sub-structure.

CONTEXT:
- You are building a part of a larger structure
- The parent slot ID is: $PARENT
- Your sub-structure should be parented to $PARENT
- Position is RELATIVE to the parent
- You will receive EXACT dimensions and bounds - USE THEM PRECISELY

CONSTRUCTION RULES (CRITICAL):
1. Use MINIMUM number of meshes - prefer 1 box over multiple
2. For walls WITH openings (windows/doors): create boxes AROUND the opening, not overlapping
3. Boxes must BUTT at seams (share edges), never overlap
4. Use the EXACT position and scale from the description
5. All parts of a wall with opening must have SAME thickness and material
6. Avoid floating geometry: if a part is elevated, add supports
7. If this is a scene area, add a ground/base slab first and place all parts on it
8. For repeated elements (trees, streetlights, etc.), cap at 3 items per cluster
9. Floors/plates must sit flush on their supports (no air gap). If ground-level, bottom at Y=0.

CREATING A WALL WITH AN OPENING (e.g., window or door):
- For a wall with a centered rectangular opening, create boxes for:
  - Left section (from wall start to opening start)
  - Right section (from opening end to wall end)  
  - Top section (above opening, spanning full width)
  - Bottom section (below opening, if needed - e.g., below a window)
- Each box position is its CENTER, scale is its FULL SIZE

COMMAND TYPES:
1. addSlot - Create a new slot (object container)
2. addComponent - Add a component to a slot  
3. getComponent - Retrieve component data (needed for Materials list)
4. updateComponent - Modify component properties
5. setMaterialsElement - Special command to link material to renderer

MESH COMPONENTS (use full names):
- [FrooxEngine]FrooxEngine.BoxMesh
- [FrooxEngine]FrooxEngine.SphereMesh
- [FrooxEngine]FrooxEngine.IcoSphereMesh
- [FrooxEngine]FrooxEngine.CylinderMesh
- [FrooxEngine]FrooxEngine.ConeMesh
- [FrooxEngine]FrooxEngine.CapsuleMesh
- [FrooxEngine]FrooxEngine.TorusMesh
- [FrooxEngine]FrooxEngine.CrossMesh

RENDERING COMPONENTS:
- [FrooxEngine]FrooxEngine.PBS_Metallic (standard material)
- [FrooxEngine]FrooxEngine.PBS_RimMetallic
- [FrooxEngine]FrooxEngine.FresnelMaterial
- [FrooxEngine]FrooxEngine.OverlayFresnelMaterial
- [FrooxEngine]FrooxEngine.UnlitMaterial
- [FrooxEngine]FrooxEngine.TextUnlitMaterial
- [FrooxEngine]FrooxEngine.UI_UnlitMaterial
- [FrooxEngine]FrooxEngine.UI_TextUnlitMaterial
- [FrooxEngine]FrooxEngine.WireframeMaterial
- [FrooxEngine]FrooxEngine.MeshRenderer

LIGHT COMPONENT:
- [FrooxEngine]FrooxEngine.Light
  Fields: LightType (enum: Point/Spot/Directional), Intensity (float), Color (colorX), Range (float)

ANIMATION COMPONENTS:
- [FrooxEngine]FrooxEngine.Spinner (fields: _speed as float3 - degrees/sec)
- [FrooxEngine]FrooxEngine.Wiggler (fields: _speed, _magnitude as float3)
- [FrooxEngine]FrooxEngine.Wobbler (fields: _speed, _magnitude as float)

PROTOFLUX VISUALS (EXPERIMENTAL):
- Use [FrooxEngine]FrooxEngine.ProtoFlux.ProtoFluxWireManager to draw flow wires.
- For angled/clean paths, add intermediate anchor slots and chain wire segments.
- Set ConnectPoint (reference to target slot), Type (Input/Output/Reference), Width, StartColor, EndColor.

TYPE FORMATS:
- colorX: {"$type": "colorX", "value": {"r": 1.0, "g": 0.0, "b": 0.0, "a": 1.0, "profile": "sRGB"}}
- float3: {"$type": "float3", "value": {"x": 0, "y": 90, "z": 0}}
- float: {"$type": "float", "value": 1.0}
- bool: {"$type": "bool", "value": true}
- string: {"$type": "string", "value": "text"}
- enum: {"$type": "enum", "value": "Point", "enumType": "LightType"}
- reference: {"$type": "reference", "targetId": "$COMP_ID"}

PLACEHOLDER IDS:
- $SUB_SLOT_0 for the sub-structure root slot (parent it to $PARENT)
- $SUB_SLOT_1, $SUB_SLOT_2, etc. for child slots
- $SUB_SLOT_N_MESH, $SUB_SLOT_N_MAT, $SUB_SLOT_N_RENDERER for components

MATERIALS LINKING (required for visible colored objects):
1. Create MeshRenderer
2. Update with Mesh reference
3. Update with Materials list containing empty reference
4. Use getComponent to retrieve auto-generated element ID  
5. Use setMaterialsElement to link material

EXAMPLE - Solid wall (single box):
[
  {"cmd": "addSlot", "id": "$SUB_SLOT_0", "name": "BackWall", "position": [0, 0, 0], "parent": "$PARENT"},
  {"cmd": "addSlot", "id": "$SUB_SLOT_1", "name": "WallBox", "position": [0, 1.5, 0], "scale": [4.0, 3.0, 0.1], "parent": "$SUB_SLOT_0"},
  {"cmd": "addComponent", "slot": "$SUB_SLOT_1", "id": "$SUB_SLOT_1_MESH", "type": "[FrooxEngine]FrooxEngine.BoxMesh"},
  {"cmd": "addComponent", "slot": "$SUB_SLOT_1", "id": "$SUB_SLOT_1_MAT", "type": "[FrooxEngine]FrooxEngine.PBS_Metallic"},
  {"cmd": "addComponent", "slot": "$SUB_SLOT_1", "id": "$SUB_SLOT_1_RENDERER", "type": "[FrooxEngine]FrooxEngine.MeshRenderer"},
  {"cmd": "updateComponent", "id": "$SUB_SLOT_1_RENDERER", "members": {"Mesh": {"$type": "reference", "targetId": "$SUB_SLOT_1_MESH"}}},
  {"cmd": "updateComponent", "id": "$SUB_SLOT_1_RENDERER", "members": {"Materials": {"$type": "list", "elements": [{"$type": "reference"}]}}},
  {"cmd": "getComponent", "id": "$SUB_SLOT_1_RENDERER", "purpose": "get_materials_element_id"},
  {"cmd": "setMaterialsElement", "renderer": "$SUB_SLOT_1_RENDERER", "material": "$SUB_SLOT_1_MAT"},
  {"cmd": "updateComponent", "id": "$SUB_SLOT_1_MAT", "members": {"AlbedoColor": {"$type": "colorX", "value": {"r": 0.95, "g": 0.93, "b": 0.88, "a": 1.0, "profile": "sRGB"}}}}
]

EXAMPLE - Wall with centered door (3 boxes: left, right, top):
Wall: 4m wide, 3m tall, 0.1m thick. Door: 1m wide, 2.2m tall, centered.
- Left section: 1.5m wide (from -2 to -0.5), full height 3m
- Right section: 1.5m wide (from 0.5 to 2), full height 3m  
- Top section: 4m wide, 0.8m tall (from 2.2 to 3.0)
[
  {"cmd": "addSlot", "id": "$SUB_SLOT_0", "name": "FrontWall", "position": [0, 0, 0], "parent": "$PARENT"},
  {"cmd": "addSlot", "id": "$SUB_SLOT_1", "name": "LeftSection", "position": [-1.25, 1.5, 0], "scale": [1.5, 3.0, 0.1], "parent": "$SUB_SLOT_0"},
  ... (mesh, mat, renderer for $SUB_SLOT_1) ...
  {"cmd": "addSlot", "id": "$SUB_SLOT_2", "name": "RightSection", "position": [1.25, 1.5, 0], "scale": [1.5, 3.0, 0.1], "parent": "$SUB_SLOT_0"},
  ... (mesh, mat, renderer for $SUB_SLOT_2) ...
  {"cmd": "addSlot", "id": "$SUB_SLOT_3", "name": "TopSection", "position": [0, 2.6, 0], "scale": [1.0, 0.8, 0.1], "parent": "$SUB_SLOT_0"},
  ... (mesh, mat, renderer for $SUB_SLOT_3) ...
]

Keep the output concise. If the command list would be too long, reduce repetition (fewer trees, fewer repeated elements) to keep the JSON valid and complete.

Avoid floating parts: everything must sit on ground or on a support. If elevated, add supports.

Respond with ONLY a JSON object (no code fences):
{"sub_name": "...", "commands": [...]}
'''


# ============================================================
# SIMPLE BUILD PROMPT - For non-complex single objects
# ============================================================

SIMPLE_PROMPT = BASE_SYSTEM_PROMPT + '''You are a Resonite world builder assistant. You generate ResoniteLink commands to create 3D objects.

COMMAND TYPES:
1. addSlot - Create a new slot (object container)
2. addComponent - Add a component to a slot  
3. getComponent - Retrieve component data (needed for Materials list)
4. updateComponent - Modify component properties
5. setMaterialsElement - Special command to link material to renderer

MESH COMPONENTS (use full names):
- [FrooxEngine]FrooxEngine.BoxMesh
- [FrooxEngine]FrooxEngine.SphereMesh
- [FrooxEngine]FrooxEngine.IcoSphereMesh
- [FrooxEngine]FrooxEngine.CylinderMesh
- [FrooxEngine]FrooxEngine.ConeMesh
- [FrooxEngine]FrooxEngine.CapsuleMesh
- [FrooxEngine]FrooxEngine.TorusMesh
- [FrooxEngine]FrooxEngine.BevelBoxMesh
- [FrooxEngine]FrooxEngine.QuadMesh
- [FrooxEngine]FrooxEngine.CrossMesh

RENDERING COMPONENTS:
- [FrooxEngine]FrooxEngine.PBS_Metallic (standard material)
- [FrooxEngine]FrooxEngine.PBS_RimMetallic
- [FrooxEngine]FrooxEngine.FresnelMaterial
- [FrooxEngine]FrooxEngine.OverlayFresnelMaterial
- [FrooxEngine]FrooxEngine.MeshRenderer
- [FrooxEngine]FrooxEngine.UnlitMaterial
- [FrooxEngine]FrooxEngine.TextUnlitMaterial
- [FrooxEngine]FrooxEngine.UI_UnlitMaterial
- [FrooxEngine]FrooxEngine.UI_TextUnlitMaterial
- [FrooxEngine]FrooxEngine.WireframeMaterial

PHYSICS COMPONENTS:
- [FrooxEngine]FrooxEngine.BoxCollider
- [FrooxEngine]FrooxEngine.SphereCollider
- [FrooxEngine]FrooxEngine.MeshCollider
- [FrooxEngine]FrooxEngine.CapsuleCollider

INTERACTION COMPONENTS:
- [FrooxEngine]FrooxEngine.Grabbable

ANIMATION COMPONENTS:
- [FrooxEngine]FrooxEngine.Spinner (fields: _speed as float3 - degrees/sec)
- [FrooxEngine]FrooxEngine.Wiggler (fields: _speed, _magnitude as float3)
- [FrooxEngine]FrooxEngine.Wobbler (fields: _speed, _magnitude as float)

PROTOFLUX VISUALS (EXPERIMENTAL):
- Use [FrooxEngine]FrooxEngine.ProtoFlux.ProtoFluxWireManager to draw flow wires.
- For angled/clean paths, add intermediate anchor slots and chain wire segments.
- Set ConnectPoint (reference to target slot), Type (Input/Output/Reference), Width, StartColor, EndColor.

LIGHT COMPONENT:
- [FrooxEngine]FrooxEngine.Light
  Fields: LightType (enum: Point/Spot/Directional), Intensity (float), Color (colorX), Range (float)

METADATA COMPONENTS (add to ROOT slot only):
- [FrooxEngine]FrooxEngine.Comment - use "_commentText" for Text field
- [FrooxEngine]FrooxEngine.License - use "_licenseText" for CreditString, set RequireCredit and CanExport to true

TYPE FORMATS:
- colorX: {"$type": "colorX", "value": {"r": 1.0, "g": 0.0, "b": 0.0, "a": 1.0, "profile": "sRGB"}}
- float3: {"$type": "float3", "value": {"x": 0, "y": 90, "z": 0}}
- float: {"$type": "float", "value": 1.0}
- bool: {"$type": "bool", "value": true}
- string: {"$type": "string", "value": "text"}
- enum: {"$type": "enum", "value": "Point", "enumType": "LightType"}
- reference: {"$type": "reference", "targetId": "$COMP_ID"}

PLACEHOLDER IDS:
- $SLOT_0 for root slot, $SLOT_1, $SLOT_2 for child slots
- $COMP_COMMENT, $COMP_LICENSE, $COMP_MESH, $COMP_MAT, $COMP_RENDERER for components

MATERIALS LINKING (required for visible colored objects):
1. Create MeshRenderer
2. Update with Mesh reference
3. Update with Materials list containing empty reference: {"$type": "list", "elements": [{"$type": "reference"}]}
4. Use getComponent to retrieve auto-generated element ID
5. Use setMaterialsElement to link material

EXAMPLE - Red spinning box:
[
  {"cmd": "addSlot", "id": "$SLOT_0", "name": "RedSpinningBox", "position": [0, 1.5, 2]},
  {"cmd": "addComponent", "slot": "$SLOT_0", "id": "$COMP_COMMENT", "type": "[FrooxEngine]FrooxEngine.Comment"},
  {"cmd": "updateComponent", "id": "$COMP_COMMENT", "members": {"Text": {"$type": "string", "value": "_commentText"}}},
  {"cmd": "addComponent", "slot": "$SLOT_0", "id": "$COMP_LICENSE", "type": "[FrooxEngine]FrooxEngine.License"},
  {"cmd": "updateComponent", "id": "$COMP_LICENSE", "members": {"CreditString": {"$type": "string", "value": "_licenseText"}, "RequireCredit": {"$type": "bool", "value": true}, "CanExport": {"$type": "bool", "value": true}}},
  {"cmd": "addComponent", "slot": "$SLOT_0", "id": "$COMP_MESH", "type": "[FrooxEngine]FrooxEngine.BoxMesh"},
  {"cmd": "addComponent", "slot": "$SLOT_0", "id": "$COMP_MAT", "type": "[FrooxEngine]FrooxEngine.PBS_Metallic"},
  {"cmd": "addComponent", "slot": "$SLOT_0", "id": "$COMP_RENDERER", "type": "[FrooxEngine]FrooxEngine.MeshRenderer"},
  {"cmd": "addComponent", "slot": "$SLOT_0", "id": "$COMP_SPINNER", "type": "[FrooxEngine]FrooxEngine.Spinner"},
  {"cmd": "updateComponent", "id": "$COMP_SPINNER", "members": {"_speed": {"$type": "float3", "value": {"x": 0, "y": 45, "z": 0}}}},
  {"cmd": "updateComponent", "id": "$COMP_RENDERER", "members": {"Mesh": {"$type": "reference", "targetId": "$COMP_MESH"}}},
  {"cmd": "updateComponent", "id": "$COMP_RENDERER", "members": {"Materials": {"$type": "list", "elements": [{"$type": "reference"}]}}},
  {"cmd": "getComponent", "id": "$COMP_RENDERER", "purpose": "get_materials_element_id"},
  {"cmd": "setMaterialsElement", "renderer": "$COMP_RENDERER", "material": "$COMP_MAT"},
  {"cmd": "updateComponent", "id": "$COMP_MAT", "members": {"AlbedoColor": {"$type": "colorX", "value": {"r": 1.0, "g": 0.0, "b": 0.0, "a": 1.0, "profile": "sRGB"}}}}
]

Respond with ONLY a JSON object (no code fences):
{"plan": "brief description", "commands": [...]}
'''


class AIBuildExecutor:
    """Executes AI-generated build commands with hierarchical building support."""
    
    def __init__(self, client, api_key, model="claude-sonnet-4-20250514"):
        """Initialize the executor.
        
        Args:
            client: ResoniteLinkClient instance
            api_key: Anthropic API key
            model: AI model to use
        """
        self.client = client
        self.anthropic = Anthropic(api_key=api_key)
        self.model = model
        self.logger = get_logger()
        self.comment_text = ""
        self.spawn_parent = "Root"  # Will be updated to user's parent slot
        
        # Complexity threshold - requests with these keywords use hierarchical building
        self.complex_keywords = [
            'house', 'building', 'room', 'scene', 'environment', 'world',
            'village', 'city', 'forest', 'garden', 'park', 'street',
            'castle', 'tower', 'bridge', 'ship', 'vehicle', 'car',
            'furniture set', 'kitchen', 'bedroom', 'living room', 'office',
            'playground', 'stage', 'arena', 'stadium', 'complex',
            'protoflux', 'flux', 'node graph'
        ]
    
    def _is_complex_request(self, prompt):
        """Determine if a request needs hierarchical building.
        
        Args:
            prompt: User's building request
            
        Returns:
            bool: True if hierarchical building should be used
        """
        prompt_lower = prompt.lower()
        
        # Check for complexity keywords
        for keyword in self.complex_keywords:
            if keyword in prompt_lower:
                return True
        
        # Check for explicit complexity indicators
        if 'with' in prompt_lower and any(word in prompt_lower for word in ['and', 'multiple', 'several']):
            return True
            
        return False
    
    async def process_prompt(self, prompt):
        """Process a natural language building prompt.
        
        Args:
            prompt: User's building request
        
        Returns:
            bool: True if build completed successfully
        """
        self.logger.log_prompt(prompt)
        
        # Get local user info for attribution and parent slot
        self.logger.log("Finding user location...")
        user_info = await self.client.get_local_user_info()
        self.spawn_parent = await self.client.get_user_root()
        self.logger.log(f"Will spawn content under: {self.spawn_parent}")
        
        # Generate comment text with timestamp and local user attribution
        timestamp = datetime.datetime.now().strftime("%y%m%d %H%M")
        host_tag = " (host)" if user_info.get("is_host") else ""
        creator = f"{user_info.get('name', 'Unknown User')}{host_tag}"
        self.comment_text = (
            f"{timestamp} Created by {creator} using Vibe Coded ResoniteLink. "
            f"Prompt: {prompt}"
        )
        
        # Decide which building approach to use
        if self._is_complex_request(prompt):
            self.logger.log("Detected complex request - using hierarchical building")
            return await self._process_hierarchical(prompt)
        else:
            self.logger.log("Using simple building mode")
            return await self._process_simple(prompt)
    
    async def _process_simple(self, prompt):
        """Process a simple building request (single AI call).
        
        Args:
            prompt: User's building request
            
        Returns:
            bool: True if build completed successfully
        """
        try:
            response = self.anthropic.messages.create(
                model=self.model,
                max_tokens=8192,
                system=SIMPLE_PROMPT,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.content[0].text
            self.logger.log(f"AI response length: {len(content)} chars")
            
            # Parse JSON from response
            plan_data = self._parse_json_response(content)
            if not plan_data:
                return False
            
            self.logger.log_plan(plan_data.get("plan", "No plan"))
            
            commands = plan_data.get("commands", [])
            return await self.execute_commands(commands)
        
        except Exception as e:
            self.logger.log_error(f"AI error: {e}")
            return False
    
    async def _process_hierarchical(self, prompt):
        """Process a complex building request using hierarchical approach.
        
        Phase 1: Get high-level plan
        Phase 2: Build each sub-structure
        Phase 3: Assemble under root
        
        Args:
            prompt: User's building request
            
        Returns:
            bool: True if build completed successfully
        """
        # ========================================
        # PHASE 1: PLANNING
        # ========================================
        self.logger.log("=" * 50)
        self.logger.log("PHASE 1: PLANNING")
        self.logger.log("=" * 50)
        
        try:
            plan_response = self.anthropic.messages.create(
                model=self.model,
                max_tokens=4096,
                system=PLANNING_PROMPT,
                messages=[{"role": "user", "content": prompt}]
            )
            
            plan_content = plan_response.content[0].text
            self.logger.log(f"Planning response length: {len(plan_content)} chars")
            
            plan_data = self._parse_json_response(plan_content)
            if not plan_data:
                self.logger.log_error("Failed to parse planning response")
                return False
            
            root_name = plan_data.get("root_name", "AIBuild")
            root_position = plan_data.get("root_position", [0, 0, 2])
            description = plan_data.get("description", "")
            sub_structures = plan_data.get("sub_structures", [])
            dimensions = plan_data.get("dimensions", {})
            
            self.logger.log(f"Plan: {description}")
            self.logger.log(f"Root: {root_name} at {root_position}")
            if dimensions:
                self.logger.log(f"Dimensions: {dimensions}")
            self.logger.log(f"Sub-structures: {len(sub_structures)}")
            for sub in sub_structures:
                self.logger.log(f"  - {sub.get('name')}: {sub.get('description', '')[:50]}...")
        
        except Exception as e:
            self.logger.log_error(f"Planning error: {e}")
            return False
        
        # ========================================
        # CREATE ROOT SLOT
        # ========================================
        self.logger.log("=" * 50)
        self.logger.log("CREATING ROOT STRUCTURE")
        self.logger.log("=" * 50)
        
        self.client.reset_session()
        
        # Create the root slot
        root_id = self.client.generate_id()
        self.client.map_id("$ROOT", root_id)
        
        response = await self.client.add_slot(
            slot_id=root_id,
            name=root_name,
            position=root_position,
            parent=self.spawn_parent
        )
        
        if not response.get("success", False):
            self.logger.log_error(f"Failed to create root slot: {response.get('errorInfo')}")
            return False
        
        self.logger.log_ok("Created root slot", root_name)
        
        # Add metadata to root
        await self._add_metadata_to_slot(root_id)
        
        # ========================================
        # PHASE 2: BUILD SUB-STRUCTURES
        # ========================================
        self.logger.log("=" * 50)
        self.logger.log("PHASE 2: BUILDING SUB-STRUCTURES")
        self.logger.log("=" * 50)
        
        for i, sub in enumerate(sub_structures):
            sub_name = sub.get("name", f"part_{i}")
            sub_desc = sub.get("description", "")
            sub_pos = sub.get("position", [0, 0, 0])
            sub_bounds = sub.get("bounds", {})
            
            self.logger.log("-" * 40)
            self.logger.log(f"Building sub-structure {i+1}/{len(sub_structures)}: {sub_name}")
            self.logger.log(f"Description: {sub_desc}")
            if sub_bounds:
                self.logger.log(f"Bounds: {sub_bounds}")
            
            # Create a container slot for this sub-structure
            sub_container_id = self.client.generate_id()
            
            response = await self.client.add_slot(
                slot_id=sub_container_id,
                name=sub_name,
                position=sub_pos,
                parent=root_id
            )
            
            if not response.get("success", False):
                self.logger.log_error(f"Failed to create sub-structure container: {response.get('errorInfo')}")
                continue
            
            self.logger.log_ok("Created sub-structure container", sub_name)
            
            # Build detail prompt with all context
            dimensions_str = ""
            if dimensions:
                dimensions_str = f"\nMASTER DIMENSIONS: {json.dumps(dimensions)}"
            
            bounds_str = ""
            if sub_bounds:
                bounds_str = f"\nBOUNDS: min={sub_bounds.get('min', [])}, max={sub_bounds.get('max', [])}"
            
            # Get detailed build commands for this sub-structure
            detail_prompt = f"""Build this sub-structure:
Name: {sub_name}
Description: {sub_desc}
Position: Container already at {sub_pos} relative to root (your objects should be at [0,0,0] relative to container, or offset as needed)
{dimensions_str}
{bounds_str}

IMPORTANT: 
- Use EXACT dimensions from the description
- Position [0,0,0] means center of your container slot
- Scale values are the FULL SIZE of the box (not half-size)
- For a box at position [0, 1.5, 0] with scale [4, 3, 0.1], the box is centered at Y=1.5 and extends from Y=0 to Y=3

Generate the commands to build this. The parent slot ID is $PARENT (already created as the container).
"""
            
            try:
                detail_response = self.anthropic.messages.create(
                    model=self.model,
                    max_tokens=8192,
                    system=DETAIL_PROMPT,
                    messages=[{"role": "user", "content": detail_prompt}]
                )
                
                detail_content = detail_response.content[0].text
                detail_data = self._parse_json_response(detail_content)
                
                if not detail_data:
                    self.logger.log_warning(f"Retrying detail prompt for {sub_name} with strict JSON")
                    retry_prompt = detail_prompt + "\nReturn ONLY valid JSON. Do not use code fences. If too long, reduce repetition."
                    detail_response = self.anthropic.messages.create(
                        model=self.model,
                        max_tokens=8192,
                        system=DETAIL_PROMPT,
                        messages=[{"role": "user", "content": retry_prompt}]
                    )
                    detail_content = detail_response.content[0].text
                    detail_data = self._parse_json_response(detail_content)
                
                if detail_data:
                    commands = detail_data.get("commands", [])
                    self.logger.log(f"Executing {len(commands)} commands for {sub_name}")
                    
                    # Map $PARENT to this sub-structure's container
                    self.client.map_id("$PARENT", sub_container_id)
                    
                    # Execute the commands
                    await self._execute_sub_commands(commands, sub_container_id)
                else:
                    self.logger.log_warning(f"No commands generated for {sub_name}")
            
            except Exception as e:
                self.logger.log_error(f"Error building {sub_name}: {e}")
                continue
        
        # ========================================
        # COMPLETE
        # ========================================
        self.logger.log("=" * 50)
        self.logger.log("BUILD COMPLETE")
        self.logger.log("=" * 50)
        self.logger.log(f"Created: {root_name}")
        self.logger.log(f"Sub-structures: {len(sub_structures)}")
        
        return True
    
    async def _add_metadata_to_slot(self, slot_id):
        """Add Comment and License components to a slot.
        
        Args:
            slot_id: The slot to add metadata to
        """
        # Add Comment component
        comment_id = self.client.generate_id()
        await self.client.add_component(slot_id, "[FrooxEngine]FrooxEngine.Comment", comment_id)
        await self.client.update_component(comment_id, {
            "Text": {"$type": "string", "value": self.comment_text}
        })
        
        # Add License component
        license_id = self.client.generate_id()
        await self.client.add_component(slot_id, "[FrooxEngine]FrooxEngine.License", license_id)
        await self.client.update_component(license_id, {
            "CreditString": {"$type": "string", "value": LICENSE_TEXT},
            "RequireCredit": {"$type": "bool", "value": True},
            "CanExport": {"$type": "bool", "value": True}
        })
        
        self.logger.log_ok("Added metadata", "Comment + License")
    
    async def _execute_sub_commands(self, commands, parent_id):
        """Execute commands for a sub-structure.
        
        Args:
            commands: List of command dictionaries
            parent_id: ID of the parent slot for this sub-structure
        """
        # Reset the sub-structure ID mappings (keep $PARENT)
        parent_mapping = self.client.ref_id_map.get("$PARENT")
        
        for cmd in commands:
            cmd_type = cmd.get("cmd")
            
            try:
                if cmd_type == "addSlot":
                    await self._execute_add_slot(cmd, default_parent=parent_id)
                elif cmd_type == "addComponent":
                    await self._execute_add_component(cmd)
                elif cmd_type == "updateComponent":
                    await self._execute_update_component(cmd)
                elif cmd_type == "getComponent":
                    await self._execute_get_component(cmd)
                elif cmd_type == "setMaterialsElement":
                    await self._execute_set_materials_element(cmd)
                else:
                    self.logger.log_warning(f"Unknown command type: {cmd_type}")
            
            except Exception as e:
                self.logger.log_error(f"Command execution error: {e}")
    
    def _parse_json_response(self, content):
        """Parse JSON from AI response.
        
        Args:
            content: Raw AI response text
            
        Returns:
            dict: Parsed JSON or None if parsing failed
        """
        parsed = self._try_parse_json(content)
        if parsed is not None:
            return parsed
        
        self.logger.log_error("Failed to parse JSON in AI response")
        self.logger.log(f"Raw AI response:\n{content}")
        self._save_debug_json(content)
        return None
    
    def _try_parse_json(self, content):
        """Best-effort JSON parsing with code-fence stripping and recovery."""
        cleaned = self._strip_code_fences(content)
        start = cleaned.find("{")
        if start < 0:
            return None
        
        decoder = json.JSONDecoder()
        try:
            obj, _ = decoder.raw_decode(cleaned[start:])
            return obj
        except json.JSONDecodeError:
            trimmed = self._trim_to_balanced_json(cleaned[start:])
            if not trimmed:
                return None
            try:
                return json.loads(trimmed)
            except json.JSONDecodeError:
                return None
    
    def _strip_code_fences(self, content):
        """Remove markdown code fences if present."""
        text = content.strip()
        fence_start = text.find("```")
        if fence_start == -1:
            return text
        
        fence_end = text.find("```", fence_start + 3)
        if fence_end == -1:
            return text
        
        fenced = text[fence_start + 3:fence_end].strip()
        if fenced.startswith("json"):
            fenced = fenced[4:].strip()
        return fenced
    
    def _trim_to_balanced_json(self, text):
        """Trim to the first fully balanced JSON object."""
        depth = 0
        in_string = False
        escape = False
        for i, ch in enumerate(text):
            if in_string:
                if escape:
                    escape = False
                elif ch == "\\":
                    escape = True
                elif ch == "\"":
                    in_string = False
                continue
            
            if ch == "\"":
                in_string = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return text[:i + 1]
        
        return None
    
    async def execute_commands(self, commands):
        """Execute a list of commands.
        
        Args:
            commands: List of command dictionaries
        
        Returns:
            bool: True if all commands succeeded
        """
        self.client.reset_session()
        
        for cmd in commands:
            cmd_type = cmd.get("cmd")
            
            try:
                if cmd_type == "addSlot":
                    await self._execute_add_slot(cmd)
                elif cmd_type == "addComponent":
                    await self._execute_add_component(cmd)
                elif cmd_type == "updateComponent":
                    await self._execute_update_component(cmd)
                elif cmd_type == "getComponent":
                    await self._execute_get_component(cmd)
                elif cmd_type == "setMaterialsElement":
                    await self._execute_set_materials_element(cmd)
                else:
                    self.logger.log_warning(f"Unknown command type: {cmd_type}")
            
            except Exception as e:
                self.logger.log_error(f"Command execution error: {e}")
        
        self.logger.log("Build complete!")
        return True
    
    def _save_debug_json(self, content):
        """Save malformed JSON for debugging."""
        import os
        debug_file = os.path.join(self.logger.log_dir, "debug_ai_response.txt")
        try:
            with open(debug_file, "w", encoding="utf-8") as f:
                f.write(content)
            self.logger.log(f"Saved raw AI response to: {debug_file}")
        except Exception as e:
            self.logger.log_warning(f"Could not save debug file: {e}")
    
    def _resolve_id(self, placeholder):
        """Resolve placeholder to real ID."""
        return self.client.resolve_id(placeholder)

    def _snap_position_for_grounding(self, name, position, scale):
        """Snap floor/slab positions to avoid floating gaps when near ground."""
        if not scale or not isinstance(scale, (list, tuple)) or len(scale) < 2:
            return position
        if not name:
            return position
        try:
            y = position[1]
            thickness = float(scale[1])
        except Exception:
            return position
        
        lower = name.lower()
        is_roof = "roof" in lower
        is_base = any(token in lower for token in ["base", "foundation", "ground"])
        is_slab = "slab" in lower
        is_floor = "floor" in lower or "floorplate" in lower or "floor_plate" in lower
        is_deck = "deck" in lower or "platform" in lower
        
        # Only snap if already near ground level
        if abs(y) > max(thickness, 0.5):
            return position
        
        # Base slabs: top surface at Y=0
        if is_slab and is_base and not is_roof:
            return [position[0], -thickness / 2.0, position[2]]
        
        # Floor plates/decks at ground level: bottom at Y=0
        if (is_floor or is_deck) and not is_roof:
            return [position[0], thickness / 2.0, position[2]]
        
        return position
    
    def _resolve_refs_in_obj(self, obj):
        """Recursively resolve references in an object."""
        if isinstance(obj, dict):
            result = {}
            for key, value in obj.items():
                if key == "$type":
                    result[key] = value
                elif key == "targetId" and isinstance(value, str) and value.startswith("$"):
                    result[key] = self._resolve_id(value)
                else:
                    result[key] = self._resolve_refs_in_obj(value)
            return result
        elif isinstance(obj, list):
            return [self._resolve_refs_in_obj(item) for item in obj]
        else:
            return obj
    
    def _replace_placeholders(self, obj):
        """Replace _commentText and _licenseText placeholders."""
        if isinstance(obj, dict):
            result = {}
            for key, value in obj.items():
                if isinstance(value, str):
                    if value == "_commentText":
                        result[key] = self.comment_text
                    elif value == "_licenseText":
                        result[key] = LICENSE_TEXT
                    else:
                        result[key] = value
                else:
                    result[key] = self._replace_placeholders(value)
            return result
        elif isinstance(obj, list):
            return [self._replace_placeholders(item) for item in obj]
        else:
            return obj
    
    async def _execute_add_slot(self, cmd, default_parent=None):
        """Execute addSlot command."""
        placeholder_id = cmd.get("id")
        real_id = self.client.generate_id()
        
        if placeholder_id:
            self.client.map_id(placeholder_id, real_id)
        
        position = cmd.get("position", [0, 1.5, 2])
        scale = cmd.get("scale")
        rotation = cmd.get("rotation")
        name = cmd.get("name", "AIObject")
        
        # Hard rule: snap grounded slabs/floors to avoid tiny gaps
        position = self._snap_position_for_grounding(name, position, scale)
        
        # Handle parent - use default_parent if provided and no explicit parent
        # Fall back to spawn_parent (user's location) instead of Root
        parent = cmd.get("parent")
        if parent is None and default_parent:
            parent = default_parent
        elif parent is None:
            parent = self.spawn_parent  # Use user's parent slot
        elif isinstance(parent, str) and parent.startswith("$"):
            parent = self._resolve_id(parent)
        
        response = await self.client.add_slot(
            slot_id=real_id,
            name=name,
            position=position,
            parent=parent,
            scale=scale,
            rotation=rotation
        )
        
        if response.get("success", False):
            self.logger.log_ok("addSlot", name)
        else:
            self.logger.log_fail("addSlot", response.get("errorInfo", "Unknown error"))
    
    async def _execute_add_component(self, cmd):
        """Execute addComponent command."""
        placeholder_id = cmd.get("id")
        real_id = self.client.generate_id()
        
        if placeholder_id:
            self.client.map_id(placeholder_id, real_id)
        
        slot_id = self._resolve_id(cmd.get("slot"))
        component_type = cmd.get("type")
        
        response = await self.client.add_component(
            slot_id=slot_id,
            component_type=component_type,
            component_id=real_id
        )
        
        if response.get("success", False):
            short_name = component_type.split(".")[-1] if component_type else "Unknown"
            self.logger.log_ok("addComponent", short_name)
        else:
            self.logger.log_fail("addComponent", response.get("errorInfo", "Unknown error"))
    
    async def _execute_update_component(self, cmd):
        """Execute updateComponent command."""
        component_id = self._resolve_id(cmd.get("id"))
        members = cmd.get("members", {})
        
        # Resolve references and replace placeholders
        resolved_members = self._resolve_refs_in_obj(members)
        resolved_members = self._replace_placeholders(resolved_members)
        
        response = await self.client.update_component(component_id, resolved_members)
        
        if response.get("success", False):
            self.logger.log_ok("updateComponent")
        else:
            self.logger.log_fail("updateComponent", response.get("errorInfo", "Unknown error"))
    
    async def _execute_get_component(self, cmd):
        """Execute getComponent command."""
        component_id = self._resolve_id(cmd.get("id"))
        purpose = cmd.get("purpose", "")
        
        response = await self.client.get_component(component_id)
        
        if response.get("success", False):
            self.logger.log_ok("getComponent")
            
            # Extract materials element ID if needed
            if purpose == "get_materials_element_id":
                try:
                    data = response.get("data", {})
                    members = data.get("members", {})
                    materials = members.get("Materials", {})
                    elements = materials.get("elements", [])
                    if elements:
                        element_id = elements[0].get("id")
                        if element_id:
                            self.client.map_id("$MATERIALS_ELEM_0", element_id)
                            self.logger.log(f"Got Materials element ID: {element_id}")
                except Exception as e:
                    self.logger.log_warning(f"Error extracting Materials element ID: {e}")
        else:
            self.logger.log_fail("getComponent", response.get("errorInfo", "Unknown error"))
    
    async def _execute_set_materials_element(self, cmd):
        """Execute setMaterialsElement command."""
        renderer_id = self._resolve_id(cmd.get("renderer"))
        material_id = self._resolve_id(cmd.get("material"))
        
        element_id = self.client.ref_id_map.get("$MATERIALS_ELEM_0")
        
        if not element_id:
            self.logger.log_warning("No Materials element ID found - skipping")
            return
        
        members = {
            "Materials": {
                "$type": "list",
                "elements": [{
                    "$type": "reference",
                    "id": element_id,
                    "targetId": material_id
                }]
            }
        }
        
        response = await self.client.update_component(renderer_id, members)
        
        if response.get("success", False):
            self.logger.log_ok("setMaterialsElement", "Material applied!")
        else:
            self.logger.log_fail("setMaterialsElement", response.get("errorInfo", "Unknown error"))
