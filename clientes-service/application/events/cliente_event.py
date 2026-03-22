from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class ClienteEvent:
    event_type: str  # 'CREATED', 'UPDATED', 'DELETED'
    cliente_id: int
    data: dict
    timestamp: datetime
    
    def __post_init__(self):
        self.timestamp = datetime.now()
