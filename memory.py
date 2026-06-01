import json
from pathlib import Path
from typing import Optional
from config import settings
from models import SessionState

class SessionMemoryManager:
    """
    Manages loading and saving agent state to disk as a JSON file.
    Ensures state synchronization using our Pydantic schema contracts.
    """

    def __init__(self, session_id: str, target: str):
        self.session_id = session_id
        self.target = target
        # e.g., cyberguard-ai/sessions/session_12345.json
        self.filepath: Path = settings.SESSION_MEMORY_DIR / f"session_{session_id}.json"

    def load_session(self) -> SessionState:
        """
        Loads an existing JSON session state file from disk.
        If no file exists, initializes a brand new state tracking instance.
        """
        if self.filepath.exists():
            print(f"[*] Memory found: Resuming tracking state from {self.filepath.name}...")
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    raw_json = f.read()
                    # Convert raw JSON string cleanly into validated Pydantic model
                    return SessionState.model_validate_json(raw_json)
            except Exception as e:
                print(f"[!] Error reading session memory file: {e}. Starting fresh.")
        
        # Fallback: Initialize a brand new session object if none is found or load fails
        print(f"[*] Memory init: Creating brand new tracking session for target: {self.target}")
        return SessionState(session_id=self.session_id, target=self.target)

    def save_session(self, state: SessionState) -> None:
        """
        Serializes the active Pydantic session state into an organized, indented JSON file.
        """
        try:
            # Generate the JSON string formatting timestamps to ISO strings and indenting for legibility
            json_data = state.model_dump_json(indent=4)
            with open(self.filepath, "w", encoding="utf-8") as f:
                f.write(json_data)
        except Exception as e:
            print(f"[!] Critical: Failed to persist agent session memory to disk: {e}")