from dataclasses import dataclass

@dataclass
class LoginEvent:
    user_id: str
    timestamp: str
    success: bool

@dataclass
class Incident:
    incident_id: str
    user_id: str
    description: str
    status: str