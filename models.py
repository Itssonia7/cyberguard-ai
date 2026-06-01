from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class PortScanResult(BaseModel):
    """Represents an open port discovered during scanning."""
    port: int
    protocol: str = "tcp"
    state: str
    service: str = "unknown"
    version: Optional[str] = None

class HostScanResult(BaseModel):
    """Aggregates all port discoveries for a specific target host."""
    target: str
    status: str
    open_ports: List[PortScanResult] = Field(default_factory=list)
    scan_time: datetime = Field(default_factory=datetime.utcnow)

class CVEInfo(BaseModel):
    """Structured vulnerability metrics from the NVD database."""
    cve_id: str
    description: str
    cvss_score: Optional[float] = None
    severity: Optional[str] = None

class AgentAction(BaseModel):
    """Tracks a tool execution decision made by the LLM."""
    tool_name: str
    arguments: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    result_summary: str

class SessionState(BaseModel):
    """The master state file mapped to the JSON memory tracking."""
    session_id: str
    target: str
    start_time: datetime = Field(default_factory=datetime.utcnow)
    discovered_host_info: Optional[HostScanResult] = None
    actions_taken: List[AgentAction] = Field(default_factory=list)
    findings_summary: List[str] = Field(default_factory=list)