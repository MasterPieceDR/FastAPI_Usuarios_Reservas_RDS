from datetime import datetime

from sqlmodel import Field, SQLModel


class Reserva(SQLModel, table=True):

    __tablename__ = "reservas"

    id: int | None = Field(
        default=None,
        primary_key=True
    )

    usuario_id: int = Field(
        foreign_key="usuarios.id"
    )

    servicio: str

    fecha_inicio: datetime

    fecha_fin: datetime

    estado: str = "PENDIENTE"