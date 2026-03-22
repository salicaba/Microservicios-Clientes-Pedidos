from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Cliente:
    id: Optional[int]
    nombre: str
    email: str
    telefono: str
    fecha_registro: datetime
    
    def __post_init__(self):
        if not self.id:
            self.fecha_registro = datetime.now()
