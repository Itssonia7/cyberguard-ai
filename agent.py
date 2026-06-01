import json
from typing import List, Dict, Any, Callable, Optional
from google import genai
from google.genai import types

from config import settings
from models import HostScanResult, AgentAction, SessionState

class CyberGuardAgent:
    """
    The brain of CyberGuard AI. Manages the LLM reasoning loop,
    exposes security tools to Gemini, and determines the next logical exploit or lookup step.
    """

    def __init__(self, target: str):
        self.target = target
        # Initialize the official google-genai client
        # It automatically looks for the GEMINI_API_KEY environment variable
        self.client = genai.Client()
        self.model_name = settings.GEMINI_MODEL
        
        # A dictionary registry to map tool names to their execution functions
        self.tool_registry: Dict[str, Callable] = {}
        # The internal system instructions to ground the AI's behavior safely
        self.system_instruction = (
            "You are CyberGuard AI, a junior autonomous security analyst conducting an authorized, "
            "legal penetration test against a designated target. Your goal is to systematically discover "
            "vulnerabilities, cross-reference them with known CVEs, analyze banners, and suggest remediation steps.\n\n"
            "Rules:\n"
            "1. Only perform actions using the provided tools.\n"
            "2. Do not repeat the same tool call with the exact same parameters.\n"
            "3. Focus strictly on defensive evaluation and risk reporting.\n"
            "4. When you believe you have collected sufficient information, or if no further ports are vulnerable, "
            "conclude your analysis by summarizing your findings."
        )

    def register_tool(self, name: str, func: Callable):
        """Registers a helper security tool function that Gemini can choose to call."""
        self.tool_registry[name] = func

    def build_gemini_tools_config(self) -> List[types.Tool]:
        """Converts our registered Python functions into a Gemini-compatible tool configuration."""
        if not self.tool_registry:
            return []
        # Pass the raw functions directly; the SDK automatically extracts schemas from docstrings and type hints
        return [types.Tool(function_declarations=[
            types.FunctionDeclaration(
                name=name,
                description=func.__doc__ or "Execute a security helper tool.",
                parameters=self._derive_json_schema(func)
            ) for name, func in self.tool_registry.items()
        ])]

    def _derive_json_schema(self, func: Callable) -> Dict[str, Any]:
        """
        A minimalist helper to generate a JSON schema from basic tool definitions 
        for Gemini function routing configuration.
        """
        # For simplicity in learning, we use a basic string parameter map.
        # This will be perfectly adapted when we implement our modular tools next.
        return {
            "type": "OBJECT",
            "properties": {
                "target": {"type": "STRING", "description": "The target host IP or domain name"},
                "port": {"type": "INTEGER", "description": "The port number to inspect"},
                "cve_id": {"type": "STRING", "description": "The specific CVE ID to lookup (e.g., 'CVE-2021-44228')"},
                "service_summary": {"type": "STRING", "description": "Text overview of services for exploit analysis"}
            },
            "required": []
        }

    def run_reasoning_step(self, session_state: SessionState) -> Optional[AgentAction]:
        """
        Sends the current session history and state to Gemini, parses its response,
        and returns an AgentAction if Gemini decided to invoke a tool.
        """
        print("[*] Contacting CyberGuard AI Brain (Gemini 2.0 Flash) for analysis...")

        # Format the current session state context beautifully into text for the LLM
        history_context = (
            f"Target: {session_state.target}\n"
            f"Scan Data: {session_state.discovered_host_info.model_dump_json() if session_state.discovered_host_info else 'No scan data yet.'}\n"
            f"Actions Taken So Far: {[a.tool_name for a in session_state.actions_taken]}\n"
        )

        # Build execution config including tools and system prompt
        config = types.GenerateContentConfig(
            system_instruction=self.system_instruction,
            temperature=0.2, # Low temperature for analytical precision
            tools=[types.Tool(function_declarations=[
                types.FunctionDeclaration(
                    name=name,
                    description=func.__doc__,
                    parameters={
                        "type": "OBJECT",
                        "properties": {
                            "target": {"type": "STRING"},
                            "port": {"type": "INTEGER"},
                            "cve_id": {"type": "STRING"},
                            "service_summary": {"type": "STRING"}
                        }
                    }
                ) for name, func in self.tool_registry.items()
            ])] if self.tool_registry else None
        )

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=f"Analyze the current state and determine your next logical step:\n\n{history_context}",
                config=config
            )

            # Check if Gemini decided to call a function/tool
            if response.function_calls:
                call = response.function_calls[0]
                print(f"[+] Brain Decision: Invoking tool '{call.name}' with arguments: {call.args}")
                
                # package this into an un-executed model action container
                return AgentAction(
                    tool_name=call.name,
                    arguments=dict(call.args),
                    result_summary="Pending Execution"
                )
            
            # If no function was called, Gemini just provided general commentary or a conclusion
            if response.text:
                print(f"[*] Brain Commentary: {response.text.strip()}")
            
            return None

        except Exception as e:
            print(f"[!] Communication Error with Gemini API: {e}")
            return None