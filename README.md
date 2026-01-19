# ResoniteLink AI World Builder

**Version:** 5.0  
**Date:** January 2026  
**Author:** Dave the Turner  
**AI Assistant:** Claude (Anthropic)

---

## Overview

The ResoniteLink AI World Builder is a natural language interface for creating 3D objects and scenes in Resonite VR. Using the ResoniteLink WebSocket protocol and Claude AI, users can describe what they want to build in plain English, and the system translates those requests into actual 3D objects in their Resonite world.

### What It Does

- **Natural Language Building**: Type "Create a red spinning cube" and watch it appear in VR
- **Multi-Object Scenes**: Build complete scenes like campfires, rooms, and furniture arrangements (not fully tested)
- **Automatic Materials**: Objects appear with proper colors and textures
- **Metadata Tracking**: All created objects include attribution and licensing information
- **Comprehensive Logging**: Full debug logs and JSON export for troubleshooting

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [Architecture](#architecture)
7. [ResoniteLink Protocol](#resonitelink-protocol)
8. [Key Technical Discoveries](#key-technical-discoveries)
9. [Scene Templates](#scene-templates)
10. [Supported Components](#supported-components)
11. [Development History](#development-history)
12. [Future Improvements](#future-improvements)
13. [Resources](#resources)

---

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install anthropic websockets
   ```

2. **Configure the application:**
   - Copy `resonite_builder.conf.example` to `resonite_builder.conf`
   - Add your Anthropic API key
   - Set the WebSocket port (from Resonite)

3. **Enable ResoniteLink in Resonite:**
   - Open Dashboard → Sessions tab
   - Click "Enable ResoniteLink"
   - Note the port number displayed

4. **Run the builder:**
   ```bash
   python resonite_builder.py
   ```

5. **Start building:**
   ```
   You: Create a red sphere
   You: Make a blue spinning cube
   You: Build a campfire
   ```

---

## Requirements

### Software
- **Python 3.10+** (tested with Python 3.13)
- **Resonite VR** with ResoniteLink enabled
- **Anthropic API key** (from https://console.anthropic.com/)

### Python Packages
```bash
pip install anthropic websockets
```

### Resonite Requirements
- You must be the **host** of the session
- You need **Builder-level permissions** or higher
- ResoniteLink must be enabled (Dashboard → Sessions → Enable ResoniteLink)

---

## Installation

1. **Clone or download** the v4.5 folder

2. **Install Python dependencies:**
   ```bash
   pip install anthropic websockets
   ```

3. **Create configuration file:**
   ```bash
   cp resonite_builder.conf.example resonite_builder.conf
   ```

4. **Edit `resonite_builder.conf`:**
   ```ini
   ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
   RESONITE_WS_URL=ws://localhost:19216
   LOG_DIR=.
   ```

---

## Configuration

The application uses `resonite_builder.conf` for all settings:

| Setting | Description | Default |
|---------|-------------|---------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key | (required) |
| `RESONITE_WS_URL` | WebSocket URL from Resonite | `ws://localhost:9000` |
| `LOG_DIR` | Directory for log files | `.` (current directory) |
| `AI_MODEL` | Claude model to use | `claude-sonnet-4-20250514` |
| `COMMAND_TIMEOUT` | Timeout for commands (seconds) | `10` |
| `CONNECTION_TIMEOUT` | Timeout for connection (seconds) | `10` |

### Getting the WebSocket Port

1. In Resonite, open your **Dashboard** (Esc on desktop, menu button in VR)
2. Go to the **Sessions** tab
3. Click **Enable ResoniteLink**
4. Note the port number shown (e.g., "ResoniteLink running on port: 19216")
5. Update your config: `RESONITE_WS_URL=ws://localhost:19216`

**Note:** The port changes each time you enable ResoniteLink!

---

## Usage

### Starting the Application

```bash
python resonite_builder.py
```

You'll see:
```
[HH:MM:SS] Version 4.5
[HH:MM:SS] WebSocket URL: ws://localhost:19216
[HH:MM:SS] AI Model: claude-sonnet-4-20250514
[HH:MM:SS] Connecting to ws://localhost:19216...
[HH:MM:SS] Connected successfully!
[HH:MM:SS] Ready! Type your building requests.
```

### Basic Commands

| Command | Description |
|---------|-------------|
| `quit`, `exit`, `q` | Exit the program |
| `help` | Show available commands and examples |
| `templates` | List available scene templates |

### Building Examples

**Simple Objects:**
```
Create a red box
Make a blue sphere
Create a green cylinder
```

**Positioning:**
```
Create a red box at position 2, 1, 3
Make a sphere 3 meters in front of me
Create a cube at 0, 2, 0
```

**Scaling:**
```
Create a large red cube
Make a tiny blue sphere
Create a box with scale 2, 0.5, 1
```

**Animation:**
```
Create a spinning red cube
Make a wobbling sphere
Create a box that rotates at 90 degrees per second
```

**Lights:**
```
Create a point light
Add a warm orange light
Create a spotlight
```

**Scenes:**
```
Create a table with chairs
Build a campfire
Make a lamp
```

### Applying Colors

After an object is created:
1. Open the **Scene Inspector** in Resonite
2. Find your created object under Root
3. Locate the **PBS_Metallic** component
4. Drag it to the **Materials** list in the **MeshRenderer** component

The object will change from the default checkerboard texture to your specified color.

---

## Architecture

### File Structure

```
v4.5/
├── resonite_builder.py      # Main entry point
├── resonite_builder.conf    # Configuration file
├── vibe_config.py           # Configuration loading
├── vibe_logging.py          # Logging and JSON export
├── vibe_client.py           # ResoniteLink WebSocket client
├── vibe_executor.py         # AI command execution engine
├── vibe_components.py       # Component type definitions
├── vibe_types.py            # Resonite type helpers
├── vibe_templates.py        # Multi-object scene templates
└── ARCHITECTURE.md          # Technical architecture document
```

### Module Responsibilities

| Module | Purpose |
|--------|---------|
| `resonite_builder.py` | Main entry point, user interaction loop |
| `vibe_config.py` | Loads and validates configuration |
| `vibe_logging.py` | Console/file logging, JSON command export |
| `vibe_client.py` | WebSocket connection, ResoniteLink protocol |
| `vibe_executor.py` | AI prompt processing, command execution |
| `vibe_components.py` | Component type registry, field definitions |
| `vibe_types.py` | Type formatters (colorX, float3, etc.) |
| `vibe_templates.py` | Pre-defined multi-object scene templates |

### Data Flow

```
User Prompt
    ↓
vibe_executor.py (sends to Claude AI)
    ↓
AI generates JSON commands
    ↓
vibe_executor.py (parses and executes)
    ↓
vibe_client.py (sends via WebSocket)
    ↓
Resonite (creates objects)
```

---

## ResoniteLink Protocol

ResoniteLink uses a WebSocket-based JSON protocol. Here are the key command types:

### addSlot
Creates a new slot (object container) in the world hierarchy.

```json
{
  "$type": "addSlot",
  "data": {
    "id": "AIBuilder_12345_0",
    "parent": {"$type": "reference", "targetId": "Root"},
    "name": {"$type": "string", "value": "RedBox"},
    "position": {"$type": "float3", "value": {"x": 0, "y": 1.5, "z": 2}}
  },
  "id": 0
}
```

### addComponent
Adds a component to an existing slot.

```json
{
  "$type": "addComponent",
  "containerSlotId": "AIBuilder_12345_0",
  "data": {
    "id": "AIBuilder_12345_1",
    "componentType": "[FrooxEngine]FrooxEngine.BoxMesh"
  },
  "id": 1
}
```

### updateComponent
Modifies properties of an existing component.

```json
{
  "$type": "updateComponent",
  "data": {
    "id": "AIBuilder_12345_2",
    "members": {
      "AlbedoColor": {
        "$type": "colorX",
        "value": {"r": 1.0, "g": 0.0, "b": 0.0, "a": 1.0, "profile": "sRGB"}
      }
    }
  },
  "id": 2
}
```

### getComponent
Retrieves component data (used for getting Materials list element IDs).

```json
{
  "$type": "getComponent",
  "componentId": "AIBuilder_12345_3",
  "id": 3
}
```

---

## Key Technical Discoveries

Throughout development, several important technical constraints were discovered:

### 1. Materials List Cannot Be Auto-Populated

The Materials list in MeshRenderer cannot be directly populated via ResoniteLink. The workaround:
1. Create an empty reference element in the Materials list
2. This displays the object with a default checkerboard texture
3. Users manually drag the material component to apply color

### 2. Color Type is "colorX" (not "color")

```json
// Correct
{"$type": "colorX", "value": {"r": 1, "g": 0, "b": 0, "a": 1, "profile": "sRGB"}}

// Wrong
{"$type": "color", "value": {...}}
```

### 3. Unique IDs Required

Each slot and component needs a unique ID. The system generates IDs like:
```
AIBuilder_12345_0  (session_id + counter)
```

Without unique IDs, Resonite returns "ID already in use" errors.

### 4. Python 3.13 String Literal Handling

Python 3.13 has stricter string literal parsing. Dollar signs (`$`) in f-strings caused issues:
```python
# Problematic in Python 3.13
f"Mapping {placeholder} -> {real_id}"

# Solution: Use chr(36) or string concatenation
DOLLAR = chr(36)
```

### 5. Two-Step Materials Process

To properly link materials to renderers:
1. Create MeshRenderer with Materials list containing empty reference
2. Use getComponent to retrieve the auto-generated element ID
3. Use setMaterialsElement to set the targetId

---

## Scene Templates

Pre-built templates for common multi-object scenes:

| Template | Description |
|----------|-------------|
| `table_with_chairs` | Wooden table with 4 chairs |
| `campfire` | Logs, stones, and warm point light |
| `simple_room` | Floor, ceiling, 4 walls, ceiling light |
| `lamp` | Standing lamp with base, pole, shade, and light |
| `staircase` | 6-step wooden staircase |
| `spotlight_stage` | Stage platform with 3 colored spotlights |

### Using Templates

```
Create a campfire
Build a table with chairs
Make a lamp
```

---

## Supported Components

### Mesh Types
| Name | Component Type |
|------|----------------|
| box | `[FrooxEngine]FrooxEngine.BoxMesh` |
| sphere | `[FrooxEngine]FrooxEngine.SphereMesh` |
| cylinder | `[FrooxEngine]FrooxEngine.CylinderMesh` |
| cone | `[FrooxEngine]FrooxEngine.ConeMesh` |
| capsule | `[FrooxEngine]FrooxEngine.CapsuleMesh` |
| torus | `[FrooxEngine]FrooxEngine.TorusMesh` |
| bevel_box | `[FrooxEngine]FrooxEngine.BevelBoxMesh` |
| quad | `[FrooxEngine]FrooxEngine.QuadMesh` |

### Materials
| Name | Component Type |
|------|----------------|
| material | `[FrooxEngine]FrooxEngine.PBS_Metallic` |
| unlit_material | `[FrooxEngine]FrooxEngine.UnlitMaterial` |

### Animation
| Name | Component Type | Fields |
|------|----------------|--------|
| spinner | `[FrooxEngine]FrooxEngine.Spinner` | `_speed` (float3) |
| wiggler | `[FrooxEngine]FrooxEngine.Wiggler` | `_speed`, `_magnitude` |
| wobbler | `[FrooxEngine]FrooxEngine.Wobbler` | `_speed`, `_magnitude` |

### Lighting
| Name | Component Type | Fields |
|------|----------------|--------|
| light | `[FrooxEngine]FrooxEngine.Light` | `LightType`, `Intensity`, `Color`, `Range` |

Light types: `Point`, `Spot`, `Directional`

### Physics
| Name | Component Type |
|------|----------------|
| box_collider | `[FrooxEngine]FrooxEngine.BoxCollider` |
| sphere_collider | `[FrooxEngine]FrooxEngine.SphereCollider` |
| mesh_collider | `[FrooxEngine]FrooxEngine.MeshCollider` |
| capsule_collider | `[FrooxEngine]FrooxEngine.CapsuleCollider` |

### Interaction
| Name | Component Type |
|------|----------------|
| grabbable | `[FrooxEngine]FrooxEngine.Grabbable` |

### Metadata
| Name | Component Type | Purpose |
|------|----------------|---------|
| comment | `[FrooxEngine]FrooxEngine.Comment` | Stores creation info and prompt |
| license | `[FrooxEngine]FrooxEngine.License` | CC BY-SA 4.0 attribution |

---

## Color Presets

Built-in color names:

| Category | Colors |
|----------|--------|
| Primary | red, green, blue |
| Secondary | yellow, cyan, magenta |
| Neutrals | white, black, gray/grey |
| Extended | orange, purple, pink, brown, tan |
| Light variants | light_red, light_green, light_blue |
| Dark variants | dark_red, dark_green, dark_blue |
| Materials | gold, silver, bronze, copper |
| Wood tones | wood_light, wood_medium, wood_dark |

---

## Development History

### v1.0 (January 10, 2026)
- Initial working prototype
- Basic slot and component creation
- Discovered Materials list limitation
- Implemented checkerboard texture workaround

### v2.0-2.1
- Added external configuration file
- Implemented comprehensive logging
- Added JSON command export
- Added Comment and License metadata components

### v3.0
- Added light components
- Added enum support
- Added more mesh types
- Added animation components (Spinner, Wiggler, Wobbler)

### v4.0-4.5
- Complete modular refactoring
- Separated concerns into distinct modules
- Added scene templates
- Added system object protection
- Improved error handling
- Added collider support

### v5.0 (January 17, 2026)
- **NEW: Hierarchical Building** - Complex scenes are automatically decomposed into manageable sub-structures
- Planning Phase: AI creates high-level structure plan
- Detail Phases: AI generates commands for each sub-structure separately
- Assembly: All pieces automatically assembled under one root slot
- Comprehensive documentation added
- Quick reference guide created
- Codebase stabilized and archived

---

## Hierarchical Building (v5.0)

For complex requests, the system automatically uses a multi-phase approach:

### How It Works

1. **Detection**: The system detects complex requests by keywords (house, building, room, scene, etc.)

2. **Planning Phase**: AI creates a high-level plan breaking the request into sub-structures
   ```
   "Build a small house" →
   - floor
   - walls  
   - roof
   - door
   - windows
   - interior_light
   ```

3. **Detail Phases**: For each sub-structure, AI generates specific build commands

4. **Assembly**: All sub-structures are parented under a single root slot

### Benefits

- **No token limits**: Each sub-structure is built in a separate AI call
- **Better quality**: AI can focus on one part at a time
- **Organized hierarchy**: Clean slot structure in Resonite
- **Scalability**: Can build arbitrarily complex scenes

### Triggering Hierarchical Mode

The system automatically uses hierarchical building for requests containing:
- Building types: house, building, castle, tower, bridge
- Rooms: room, kitchen, bedroom, living room, office
- Environments: scene, environment, world, village, city, forest, garden
- Complex structures: vehicle, ship, playground, stage, arena

### Example Output

```
PHASE 1: PLANNING
==================================================
Plan: A small house with walls, roof, door, and windows
Root: SmallHouse at [0, 0, 2]
Sub-structures: 6
  - floor: A flat box for the floor...
  - walls: Four walls made of boxes...
  - roof: A simple pitched roof...
  - door: A brown door box...
  - windows: Two blue-tinted boxes...
  - interior_light: A warm point light...

CREATING ROOT STRUCTURE
==================================================
OK Created root slot: SmallHouse
OK Added metadata: Comment + License

PHASE 2: BUILDING SUB-STRUCTURES
==================================================
Building sub-structure 1/6: floor
...
```

---

## Future Improvements

### Potential Enhancements

1. **Explore Python ResoniteLink Libraries**
   - [JackTheFoxOtter/ResoniteLink.py](https://github.com/JackTheFoxOtter/ResoniteLink.py)
   - [RobertBaruch/pyresonitelink](https://github.com/RobertBaruch/pyresonitelink)

2. **Automatic Materials Assignment**
   - Research alternative approaches to populate Materials list

3. **Object Modification**
   - "Move that box left"
   - "Make it bigger"
   - "Change color to blue"

4. **Scene Memory**
   - Track created objects
   - Enable undo/redo

5. **Prefab Library**
   - Save and recall complex objects
   - Import external models

6. **Visual Interface**
   - Web-based UI
   - Real-time preview

---

## Resources

### Official Documentation
- [ResoniteLink GitHub](https://github.com/Yellow-Dog-Man/ResoniteLink) - Official protocol implementation
- [Resonite Wiki](https://wiki.resonite.com) - Data model and component documentation
- [Anthropic API](https://console.anthropic.com/) - Claude AI API

### Community Resources
- [JackTheFoxOtter/ResoniteLink.py](https://github.com/JackTheFoxOtter/ResoniteLink.py) - Python wrapper
- [RobertBaruch/pyresonitelink](https://github.com/RobertBaruch/pyresonitelink) - Python bindings

### Key Wiki Pages
- [Data Model](https://wiki.resonite.com/Data_Model)
- [Slots](https://wiki.resonite.com/Slot)
- [Components](https://wiki.resonite.com/Category:Components)

---

## Troubleshooting

### Connection Failed
- Is Resonite running?
- Are you the host of the session?
- Is ResoniteLink enabled? (Dashboard → Sessions)
- Does the port in config match Resonite's displayed port?

### Command Timeout
- Check Resonite is responsive
- Verify WebSocket URL is correct
- Try increasing `COMMAND_TIMEOUT` in config

### Objects Not Visible
- Objects appear with checkerboard texture by default
- Drag the PBS_Metallic component to the Materials list to apply color

### "ID already in use" Error
- This happens when creating multiple objects in quick succession
- The system auto-generates unique IDs to prevent this
- If it persists, restart the builder to get a new session ID

### Python Syntax Errors
- Ensure you're using Python 3.10 or higher
- Python 3.13 has specific string handling requirements

---

## License

This project is provided under **CC BY-SA 4.0**.

All objects created by this tool include a License component with attribution:
> "This asset is licensed under CC BY-SA 4.0 © 2026 Dave the Turner. Please provide attribution when using or redistributing."

---

## Acknowledgments

- **Resonite Team** (Yellow Dog Man Studios) for creating ResoniteLink
- **Anthropic** for Claude AI
- **Community contributors** who created Python ResoniteLink libraries

---

*Documentation generated January 2026*
