from sqlmodel import Field, SQLModel


class Usuario(SQLModel, table=True):

    __tablename__ = "usuarios"

    id: int | None = Field(
        default=None,
        primary_key=True
    )

    nombre: str

    email: str = Field(
        index=True,
        unique=True
    )
