# ResoniteLink AI World Builder v5.0
# client.py - ResoniteLink WebSocket client

"""
WebSocket client for communicating with ResoniteLink.
"""

import asyncio
import json
import random
from vibe_logging import get_logger


class ResoniteLinkClient:
    """WebSocket client for ResoniteLink protocol."""
    
    def __init__(self, url, command_timeout=10, connection_timeout=10):
        """Initialize the client.
        
        Args:
            url: WebSocket URL (e.g., ws://localhost:19216)
            command_timeout: Timeout for commands in seconds
            connection_timeout: Timeout for connection in seconds
        """
        self.url = url
        self.command_timeout = command_timeout
        self.connection_timeout = connection_timeout
        self.ws = None
        self.message_id = 0
        self.session_id = random.randint(10000, 99999)
        self.id_counter = 0
        self.ref_id_map = {}
        self.logger = get_logger()
    
    async def connect(self):
        """Connect to ResoniteLink WebSocket server.
        
        Returns:
            bool: True if connection successful
        """
        import websockets
        
        self.logger.log(f"Connecting to {self.url}...")
        
        try:
            self.ws = await asyncio.wait_for(
                websockets.connect(self.url, ping_interval=None),
                timeout=self.connection_timeout
            )
            self.logger.log("Connected successfully!")
            return True
        
        except asyncio.TimeoutError:
            self.logger.log_error(f"Connection timed out after {self.connection_timeout} seconds")
            return False
        
        except Exception as e:
            self.logger.log_error(f"Connection failed: {e}")
            return False
    
    async def disconnect(self):
        """Disconnect from WebSocket server."""
        if self.ws:
            await self.ws.close()
            self.ws = None
            self.logger.log("Disconnected")
    
    def generate_id(self):
        """Generate a unique ID for slots/components.
        
        Returns:
            str: Unique ID in format AIBuilder_XXXXX_N
        """
        new_id = f"AIBuilder_{self.session_id}_{self.id_counter}"
        self.id_counter += 1
        return new_id
    
    def reset_session(self):
        """Reset session state for a new build."""
        self.ref_id_map = {}
        self.id_counter = 0
        self.session_id = random.randint(10000, 99999)
    
    def map_id(self, placeholder, real_id):
        """Map a placeholder ID to a real ID.
        
        Args:
            placeholder: Placeholder like $SLOT_0
            real_id: Real generated ID
        """
        self.ref_id_map[placeholder] = real_id
        self.logger.log_mapping(placeholder, real_id)
    
    def resolve_id(self, placeholder):
        """Resolve a placeholder ID to its real ID.
        
        Args:
            placeholder: Placeholder or real ID
        
        Returns:
            str: Resolved ID
        """
        if placeholder is None:
            return None
        if isinstance(placeholder, str) and placeholder.startswith("$"):
            resolved = self.ref_id_map.get(placeholder)
            if resolved:
                return resolved
            else:
                self.logger.log_warning(f"Placeholder {placeholder} not found in map!")
                return placeholder
        return placeholder
    
    async def send_command(self, command, timeout=None):
        """Send a command and wait for response.
        
        Args:
            command: Command dictionary
            timeout: Optional timeout override in seconds
        
        Returns:
            dict: Response from server
        """
        command["id"] = self.message_id
        self.message_id += 1
        
        self.logger.log_json("SENDING:", command)
        self.logger.write_json(command)
        
        await self.ws.send(json.dumps(command))
        
        try:
            wait_timeout = self.command_timeout if timeout is None else timeout
            response_text = await asyncio.wait_for(self.ws.recv(), timeout=wait_timeout)
            response = json.loads(response_text)
            self.logger.log_json("RECEIVED:", response)
            return response
        
        except asyncio.TimeoutError:
            wait_timeout = self.command_timeout if timeout is None else timeout
            self.logger.log_error(f"Command timed out after {wait_timeout} seconds")
            return {"success": False, "errorInfo": "Timeout"}
        
        except Exception as e:
            self.logger.log_error(f"Error receiving response: {e}")
            return {"success": False, "errorInfo": str(e)}
    
    # ========================================================
    # HIGH-LEVEL COMMANDS
    # ========================================================
    
    async def add_slot(self, slot_id, name, position, parent="Root", scale=None, rotation=None):
        """Create a new slot.
        
        Args:
            slot_id: ID for the new slot
            name: Display name
            position: [x, y, z] position
            parent: Parent slot ID (default "Root")
            scale: Optional [x, y, z] scale
            rotation: Optional [x, y, z, w] quaternion rotation
        
        Returns:
            dict: Response from server
        """
        data = {
            "id": slot_id,
            "parent": {"$type": "reference", "targetId": parent},
            "name": {"$type": "string", "value": name},
            "position": {
                "$type": "float3",
                "value": {"x": position[0], "y": position[1], "z": position[2]}
            }
        }
        
        if scale:
            data["scale"] = {
                "$type": "float3",
                "value": {"x": scale[0], "y": scale[1], "z": scale[2]}
            }
        
        if rotation:
            data["rotation"] = {
                "$type": "floatQ",
                "value": {"x": rotation[0], "y": rotation[1], "z": rotation[2], "w": rotation[3] if len(rotation) > 3 else 1.0}
            }
        
        command = {
            "$type": "addSlot",
            "data": data
        }
        
        return await self.send_command(command)

    async def update_slot(self, slot_id, parent=None, position=None, rotation=None, scale=None, name=None):
        """Update an existing slot (e.g., reparent or move).
        
        Args:
            slot_id: ID of the slot to update
            parent: Optional new parent slot ID
            position: Optional [x, y, z] position
            rotation: Optional [x, y, z, w] quaternion rotation
            scale: Optional [x, y, z] scale
            name: Optional new name
        
        Returns:
            dict: Response from server
        """
        data = {"id": slot_id}
        
        if parent is not None:
            data["parent"] = {"$type": "reference", "targetId": parent}
        if name is not None:
            data["name"] = {"$type": "string", "value": name}
        if position is not None:
            data["position"] = {
                "$type": "float3",
                "value": {"x": position[0], "y": position[1], "z": position[2]}
            }
        if scale is not None:
            data["scale"] = {
                "$type": "float3",
                "value": {"x": scale[0], "y": scale[1], "z": scale[2]}
            }
        if rotation is not None:
            data["rotation"] = {
                "$type": "floatQ",
                "value": {"x": rotation[0], "y": rotation[1], "z": rotation[2], "w": rotation[3] if len(rotation) > 3 else 1.0}
            }
        
        command = {
            "$type": "updateSlot",
            "data": data
        }
        
        return await self.send_command(command)
    
    async def add_component(self, slot_id, component_type, component_id=None, members=None):
        """Add a component to a slot.
        
        Args:
            slot_id: Slot to add component to
            component_type: Full component type string
            component_id: Optional ID for the component
            members: Optional initial member values
        
        Returns:
            dict: Response from server
        """
        data = {
            "componentType": component_type
        }
        
        if component_id:
            data["id"] = component_id
        
        if members:
            data["members"] = members
        
        command = {
            "$type": "addComponent",
            "containerSlotId": slot_id,
            "data": data
        }
        
        return await self.send_command(command)
    
    async def get_component(self, component_id):
        """Get component data.
        
        Args:
            component_id: Component ID to retrieve
        
        Returns:
            dict: Response with component data
        """
        command = {
            "$type": "getComponent",
            "componentId": component_id
        }
        
        return await self.send_command(command)
    
    async def update_component(self, component_id, members):
        """Update component members.
        
        Args:
            component_id: Component to update
            members: Dictionary of member updates
        
        Returns:
            dict: Response from server
        """
        command = {
            "$type": "updateComponent",
            "data": {
                "id": component_id,
                "members": members
            }
        }
        
        return await self.send_command(command)
    
    async def get_slot(self, slot_id, depth=0, include_components=False):
        """Get slot data.
        
        Args:
            slot_id: Slot ID to retrieve
            depth: How many child levels to include
            include_components: Whether to include component data
        
        Returns:
            dict: Response with slot data
        """
        command = {
            "$type": "getSlot",
            "slotId": slot_id,
            "depth": depth,
            "includeComponentData": include_components
        }
        
        return await self.send_command(command)
    
    async def delete_slot(self, slot_id):
        """Delete a slot.
        
        Args:
            slot_id: Slot to delete
        
        Returns:
            dict: Response from server
        """
        command = {
            "$type": "deleteSlot",
            "slotId": slot_id
        }
        
        return await self.send_command(command)
    
    async def find_slot(self, name, parent_id="Root"):
        """Find a slot by name under a parent.
        
        Args:
            name: Name of the slot to find
            parent_id: Parent slot to search under (default "Root")
        
        Returns:
            dict: Response with slot data or None if not found
        """
        command = {
            "$type": "findSlot",
            "parentSlotId": parent_id,
            "name": name
        }
        
        return await self.send_command(command)
    
    async def get_user_root(self):
        """Get the slot that is the parent of the current user.
        
        This finds the user's slot and returns its parent, which is where
        we want to place generated content (near the user).
        
        Returns:
            str: Slot ID of user's parent, or "Root" if not found
        """
        # First, try to get the local user info
        command = {
            "$type": "getUsers"
        }
        
        response = await self.send_command(command, timeout=30)
        
        if response.get("success", False):
            users = response.get("users", [])
            # Find the local user (the one running the session)
            for user in users:
                if user.get("isLocal", False):
                    user_slot_id = user.get("userRootSlotId")
                    if user_slot_id:
                        self.logger.log(f"Found local user slot: {user_slot_id}")
                        
                        # Get the user slot to find its parent
                        slot_response = await self.get_slot(user_slot_id)
                        if slot_response.get("success", False):
                            slot_data = slot_response.get("data", {})
                            parent_id = slot_data.get("parentId")
                            if parent_id:
                                self.logger.log(f"User's parent slot: {parent_id}")
                                return parent_id
                        
                        # If we can't get parent, return the user slot itself
                        return user_slot_id
        
        self.logger.log_warning("Could not find user slot, using Root")
        return "Root"

    async def get_local_user_info(self):
        """Get the local user's name and host status if available."""
        command = {
            "$type": "getUsers"
        }
        response = await self.send_command(command, timeout=30)
        if response.get("success", False):
            users = response.get("users", [])
            for user in users:
                if user.get("isLocal", False):
                    name = (
                        user.get("username")
                        or user.get("userName")
                        or user.get("displayName")
                        or user.get("name")
                        or user.get("userId")
                        or "Unknown User"
                    )
                    is_host = bool(
                        user.get("isHost")
                        or user.get("isWorldHost")
                        or user.get("host")
                    )
                    return {"name": name, "is_host": is_host}
        return {"name": "Unknown User", "is_host": False}
