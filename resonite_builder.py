#!/usr/bin/env python3
# ResoniteLink AI World Builder v5.0
# resonite_builder.py - Main entry point
#
# Date: 2026-01-17
# Author: Dave the Turner
# AI Assistant: Claude (Anthropic)
#
# A natural language interface for creating 3D objects in Resonite VR
# using the ResoniteLink WebSocket protocol.
#
# Features:
#   - Natural language object creation
#   - Automatic material/color application
#   - Multiple mesh types (box, sphere, cylinder, cone, capsule, torus, etc.)
#   - Light components (Point, Spot, Directional)
#   - Animation (Spinner, Wiggler, Wobbler)
#   - Physics (Colliders) and Interaction (Grabbable)
#   - Comment and License metadata
#   - Multi-object scene templates
#   - Comprehensive logging and JSON export

import asyncio
import sys

from vibe_config import load_config
from vibe_logging import init_logging, close_logging, log
from vibe_client import ResoniteLinkClient
from vibe_executor import AIBuildExecutor


VERSION = "5.3"


async def main():
    """Main entry point."""
    
    # Load configuration
    config = load_config()
    
    # Initialize logging
    logger = init_logging(config.log_dir)
    
    log(f"Version {VERSION}")
    log(f"WebSocket URL: {config.resonite_ws_url}")
    log(f"AI Model: {config.ai_model}")
    
    # Create client and connect
    client = ResoniteLinkClient(
        url=config.resonite_ws_url,
        command_timeout=config.command_timeout,
        connection_timeout=config.connection_timeout
    )
    
    if not await client.connect():
        log("Failed to connect. Make sure:")
        log("  1. Resonite is running")
        log("  2. You are in a world as host")
        log("  3. ResoniteLink is enabled (Dashboard -> Sessions)")
        log("  4. The port in resonite_builder.conf matches")
        close_logging()
        return
    
    # Create executor
    executor = AIBuildExecutor(
        client=client,
        api_key=config.anthropic_api_key,
        model=config.ai_model
    )
    
    # Print help
    log("")
    log("Ready! Type your building requests.")
    log("Commands:")
    log("  quit, exit, q - Exit the program")
    log("  help - Show available commands")
    log("  templates - List scene templates")
    log("")
    log("Examples:")
    log("  Create a red sphere")
    log("  Make a blue spinning cube at position 2, 1, 3")
    log("  Create a point light with warm orange color")
    log("  Build a table with chairs")
    log("")
    
    # Main loop
    try:
        while True:
            try:
                prompt = input("\nYou: ").strip()
            except EOFError:
                break
            
            # Handle commands
            if prompt.lower() in ["quit", "exit", "q"]:
                break
            
            if prompt.lower() == "help":
                print_help()
                continue
            
            if prompt.lower() == "templates":
                print_templates()
                continue
            
            if not prompt:
                continue
            
            # Process building prompt
            await executor.process_prompt(prompt)
    
    except KeyboardInterrupt:
        log("\nInterrupted by user")
    
    finally:
        await client.disconnect()
        close_logging()


def print_help():
    """Print help information."""
    print("""
ResoniteLink AI World Builder v5.0
==================================

BASIC OBJECTS:
  "Create a red box"
  "Make a blue sphere"
  "Create a green cylinder"

POSITIONING:
  "Create a red box at position 2, 1, 3"
  "Make a sphere 3 meters in front of me"

SCALING:
  "Create a large red cube" (uses larger scale)
  "Make a tiny blue sphere"
  "Create a box with scale 2, 0.5, 1"

COLORS:
  Basic: red, green, blue, yellow, cyan, magenta
  Neutrals: white, black, gray
  Extended: orange, purple, pink, brown, gold, silver
  Custom: "with RGB 0.5, 0.8, 0.2"

ANIMATION:
  "Create a spinning red cube"
  "Make a wobbling sphere"
  "Create a box that rotates at 90 degrees per second"

LIGHTS:
  "Create a point light"
  "Add a warm orange light above the table"
  "Create a spotlight"

INTERACTION:
  "Create a grabbable red box"

SCENES:
  "Create a table with chairs"
  "Build a campfire"
  "Make a lamp"

Type 'templates' to see all available scene templates.
""")


def print_templates():
    """Print available scene templates."""
    from vibe_templates import list_templates
    
    print("\nAvailable Scene Templates:")
    print("=" * 40)
    for name, description in list_templates():
        print(f"  {name}: {description}")
    print("")
    print("Use: 'Create a <template_name>' or 'Build a <template_name>'")
    print("")


if __name__ == "__main__":
    asyncio.run(main())
