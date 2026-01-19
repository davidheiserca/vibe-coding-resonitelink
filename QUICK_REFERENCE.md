# ResoniteLink AI World Builder - Quick Reference

## Setup Checklist
- [ ] Python 3.10+ installed
- [ ] `pip install anthropic websockets`
- [ ] `resonite_builder.conf` configured with API key
- [ ] Resonite running, you are host with Builder permissions
- [ ] ResoniteLink enabled (Dashboard → Sessions)
- [ ] Port in config matches Resonite's displayed port

## Starting
```bash
python resonite_builder.py
```

## Commands
| Command | Action |
|---------|--------|
| `quit` / `exit` / `q` | Exit program |
| `help` | Show help |
| `templates` | List scene templates |

## Building Objects

### Basic Shapes
```
Create a red box
Make a blue sphere
Create a green cylinder
Create a yellow cone
Make a purple torus
```

### With Position
```
Create a red box at position 2, 1, 3
Create a sphere at 0, 2, 0
```

### With Scale
```
Create a large red cube
Make a tiny blue sphere
Create a box with scale 2, 0.5, 1
```

### With Animation
```
Create a spinning red cube
Make a wobbling sphere
Create a rotating box
```

### Lights
```
Create a point light
Create a warm orange light
Create a spotlight
```

### Scenes
```
Create a campfire
Build a table with chairs
Make a lamp
Create a simple room
Build a staircase
```

## Available Colors
**Primary:** red, green, blue  
**Secondary:** yellow, cyan, magenta  
**Neutrals:** white, black, gray  
**Extended:** orange, purple, pink, brown, tan  
**Materials:** gold, silver, bronze, copper  
**Wood:** wood_light, wood_medium, wood_dark

## Applying Colors (Manual Step)
1. Open Scene Inspector in Resonite
2. Find your object under Root
3. Locate PBS_Metallic component
4. Drag it to Materials list in MeshRenderer

## Hierarchical Building (NEW in v5.0)

Complex requests are automatically broken into sub-structures:

**Triggers automatically for:**
- Buildings: house, castle, tower, bridge
- Rooms: kitchen, bedroom, office
- Environments: scene, world, village, forest
- Complex: vehicle, ship, playground

**Example:**
```
You: Build a small house
→ PHASE 1: Planning (breaks into floor, walls, roof, door, windows, light)
→ PHASE 2: Building each sub-structure
→ Result: Organized hierarchy under one root slot
```

---

## Scene Templates
| Name | Description |
|------|-------------|
| table_with_chairs | Table + 4 chairs |
| campfire | Logs, stones, fire light |
| simple_room | Floor, walls, ceiling, light |
| lamp | Standing lamp with light |
| staircase | 6-step stairs |
| spotlight_stage | Stage + 3 spotlights |

## Troubleshooting
| Problem | Solution |
|---------|----------|
| Connection failed | Check Resonite is running, you're host, ResoniteLink enabled, port matches |
| Objects invisible | Drag material to Materials list |
| Command timeout | Increase COMMAND_TIMEOUT in config |
| ID in use error | Restart builder for new session |

## Config File (resonite_builder.conf)
```ini
ANTHROPIC_API_KEY=sk-ant-api03-...
RESONITE_WS_URL=ws://localhost:PORT
LOG_DIR=.
AI_MODEL=claude-sonnet-4-20250514
COMMAND_TIMEOUT=10
CONNECTION_TIMEOUT=10
```

## Log Files
- `resonite_debug_YYMMDD_HHMM.log` - Debug output
- `resonite_builder_YYMMDD_HHMM.json` - JSON command export

---
*ResoniteLink AI World Builder v5.0 - Quick Reference*
