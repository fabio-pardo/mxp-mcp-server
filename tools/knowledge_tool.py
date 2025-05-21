"""
Knowledge Base Tool
A more complex tool that demonstrates knowledge retrieval capabilities.
"""

import json
import os
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class KnowledgeBaseTool:
    """
    A tool that simulates knowledge base retrieval and search functionality.
    This demonstrates how to implement a more complex tool with multiple operations.
    """

    def __init__(self, knowledge_base_path: Optional[str] = None):
        self.name = "knowledge_tool"
        self.description = "Access and search knowledge base information"
        
        # If a specific path is provided, use it, otherwise use a default path
        self.knowledge_base_path = knowledge_base_path or os.environ.get(
            "KNOWLEDGE_BASE_PATH", 
            "./knowledge_base.json"
        )
        
        # Initialize with a default knowledge base if file doesn't exist
        self._initialize_knowledge_base()
        
    def _initialize_knowledge_base(self) -> None:
        """Initialize the knowledge base if it doesn't exist."""
        if not os.path.exists(self.knowledge_base_path):
            # Create a default knowledge base with some sample data
            default_kb = {
                "entries": [
                    {
                        "id": "kb001",
                        "title": "What is MCP?",
                        "content": "Model Context Protocol (MCP) is a standard that connects AI systems with external tools and data sources.",
                        "tags": ["mcp", "protocol", "ai"],
                        "created_at": "2025-05-21T13:00:00-04:00"
                    },
                    {
                        "id": "kb002",
                        "title": "Containerizing MCP Servers",
                        "content": "MCP servers can be containerized using Docker for easy deployment and scaling.",
                        "tags": ["docker", "container", "deployment"],
                        "created_at": "2025-05-21T13:10:00-04:00"
                    },
                    {
                        "id": "kb003",
                        "title": "Security Best Practices",
                        "content": "Implement proper authentication and authorization. Use HTTPS. Validate all inputs.",
                        "tags": ["security", "best-practices", "auth"],
                        "created_at": "2025-05-21T13:20:00-04:00"
                    }
                ],
                "metadata": {
                    "last_updated": "2025-05-21T13:49:25-04:00",
                    "total_entries": 3
                }
            }
            
            # Save the default knowledge base
            with open(self.knowledge_base_path, 'w') as f:
                json.dump(default_kb, f, indent=2)
                
            logger.info(f"Created default knowledge base at {self.knowledge_base_path}")
    
    def _load_knowledge_base(self) -> Dict[str, Any]:
        """Load the knowledge base from file."""
        try:
            with open(self.knowledge_base_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading knowledge base: {str(e)}")
            return {"entries": [], "metadata": {"last_updated": "", "total_entries": 0}}
    
    def _save_knowledge_base(self, kb: Dict[str, Any]) -> None:
        """Save the knowledge base to file."""
        try:
            # Update metadata
            kb["metadata"]["last_updated"] = "2025-05-21T13:49:25-04:00"  # Using the provided time
            kb["metadata"]["total_entries"] = len(kb["entries"])
            
            with open(self.knowledge_base_path, 'w') as f:
                json.dump(kb, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving knowledge base: {str(e)}")
    
    def execute(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the knowledge tool with the given parameters.
        
        Args:
            parameters: A dictionary of parameters for the tool
                - operation: The operation to perform (search, get, add, delete)
                - query: Search query (for search operation)
                - id: Entry ID (for get and delete operations)
                - entry: Entry data (for add operation)
                
        Returns:
            A dictionary containing the result
        """
        operation = parameters.get("operation", "search")
        
        try:
            if operation == "search":
                return self._search(parameters.get("query", ""), parameters.get("tags", []))
            elif operation == "get":
                return self._get_entry(parameters.get("id", ""))
            elif operation == "add":
                return self._add_entry(parameters.get("entry", {}))
            elif operation == "delete":
                return self._delete_entry(parameters.get("id", ""))
            else:
                return {
                    "success": False,
                    "error": f"Unknown operation: {operation}",
                    "available_operations": ["search", "get", "add", "delete"]
                }
        except Exception as e:
            logger.error(f"Error executing knowledge tool: {str(e)}")
            return {
                "success": False,
                "error": f"Error executing operation {operation}: {str(e)}"
            }
    
    def _search(self, query: str, tags: List[str] = None) -> Dict[str, Any]:
        """Search for entries in the knowledge base."""
        kb = self._load_knowledge_base()
        results = []
        
        if not tags:
            tags = []
        
        query = query.lower()
        
        for entry in kb["entries"]:
            # Check if the entry matches the query in title or content
            title_match = query in entry["title"].lower()
            content_match = query in entry["content"].lower()
            
            # Check if the entry has any of the specified tags
            tag_match = False
            if tags:
                for tag in tags:
                    if tag in entry["tags"]:
                        tag_match = True
                        break
            else:
                # If no tags specified, consider it a match
                tag_match = True
            
            # Add the entry to results if it matches
            if (title_match or content_match) and tag_match:
                results.append(entry)
        
        return {
            "success": True,
            "query": query,
            "tags": tags,
            "results_count": len(results),
            "results": results
        }
    
    def _get_entry(self, entry_id: str) -> Dict[str, Any]:
        """Get a specific entry by ID."""
        if not entry_id:
            return {"success": False, "error": "No entry ID provided"}
        
        kb = self._load_knowledge_base()
        
        for entry in kb["entries"]:
            if entry["id"] == entry_id:
                return {
                    "success": True,
                    "entry": entry
                }
        
        return {
            "success": False,
            "error": f"No entry found with ID: {entry_id}"
        }
    
    def _add_entry(self, entry_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new entry to the knowledge base."""
        if not entry_data:
            return {"success": False, "error": "No entry data provided"}
        
        required_fields = ["title", "content"]
        for field in required_fields:
            if field not in entry_data:
                return {"success": False, "error": f"Missing required field: {field}"}
        
        kb = self._load_knowledge_base()
        
        # Generate a new ID
        new_id = f"kb{len(kb['entries']) + 1:03d}"
        
        # Create the new entry
        new_entry = {
            "id": new_id,
            "title": entry_data["title"],
            "content": entry_data["content"],
            "tags": entry_data.get("tags", []),
            "created_at": "2025-05-21T13:49:25-04:00"  # Using the provided time
        }
        
        # Add to knowledge base
        kb["entries"].append(new_entry)
        self._save_knowledge_base(kb)
        
        return {
            "success": True,
            "message": "Entry added successfully",
            "entry": new_entry
        }
    
    def _delete_entry(self, entry_id: str) -> Dict[str, Any]:
        """Delete an entry from the knowledge base."""
        if not entry_id:
            return {"success": False, "error": "No entry ID provided"}
        
        kb = self._load_knowledge_base()
        
        # Find the entry to delete
        for i, entry in enumerate(kb["entries"]):
            if entry["id"] == entry_id:
                # Remove the entry
                deleted_entry = kb["entries"].pop(i)
                self._save_knowledge_base(kb)
                
                return {
                    "success": True,
                    "message": f"Entry {entry_id} deleted successfully",
                    "deleted_entry": deleted_entry
                }
        
        return {
            "success": False,
            "error": f"No entry found with ID: {entry_id}"
        }
