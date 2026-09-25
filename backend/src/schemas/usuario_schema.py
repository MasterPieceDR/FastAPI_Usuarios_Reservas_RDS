from pydantic import BaseModel, ConfigDict


class UsuarioCreate(BaseModel):

    nombre: str
    email: str
    telefono: str | None = None


class UsuarioUpdate(BaseModel):

    nombre: str | None = None
    email: str | None = None
    telefono: str | None = None


class UsuarioResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    nombre: str
    email: str
    telefono: str | None = None