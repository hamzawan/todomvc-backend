from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from rococo.models.versioned_model import VersionedModel

@dataclass
class Task(VersionedModel):
    __tablename__ = "task"
    
    title: str = ""
    description: Optional[str] = None
    status: str = "incomplete"
    priority: str = "medium"
    assigned_to_id: Optional[str] = None
    organization_id: Optional[str] = None
    due_date: Optional[datetime] = None
