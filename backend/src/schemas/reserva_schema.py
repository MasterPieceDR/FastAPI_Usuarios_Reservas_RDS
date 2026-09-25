from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ReservaCreate(BaseModel):

    usuario_id: int
    servicio: str
    fecha_inicio: datetime
    fecha_fin: datetime
    estado: str = "PENDIENTE"


class ReservaUpdate(BaseModel):

    usuario_id: int | None = None
    servicio: str | None = None
    fecha_inicio: datetime | None = None
    fecha_fin: datetime | None = None
    estado: str | None = None


class ReservaResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    usuario_id: int
    servicio: str
    fecha_inicio: datetime
    fecha_fin: datetime
    estado: str