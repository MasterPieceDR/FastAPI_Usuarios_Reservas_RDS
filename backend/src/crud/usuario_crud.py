from sqlmodel import Session, select

from models.usuario_model import Usuario
from models.reserva_model import Reserva

from schemas.usuario_schema import (
    UsuarioCreate,
    UsuarioUpdate
)


def crear_usuario(
    datos: UsuarioCreate,
    session: Session
):

    usuario_existente = session.exec(
        select(Usuario).where(
            Usuario.email == datos.email
        )
    ).first()

    if usuario_existente:
        return "EMAIL_EXISTE"

    usuario = Usuario.model_validate(datos)

    session.add(usuario)
    session.commit()
    session.refresh(usuario)

    return usuario


def obtener_usuarios(
    session: Session
):

    return session.exec(
        select(Usuario)
    ).all()


def obtener_usuario(
    usuario_id: int,
    session: Session
):

    return session.get(
        Usuario,
        usuario_id
    )


def actualizar_usuario(
    usuario_id: int,
    datos: UsuarioUpdate,
    session: Session
):

    usuario = session.get(
        Usuario,
        usuario_id
    )

    if not usuario:
        return None

    cambios = datos.model_dump(
        exclude_unset=True
    )

    if "email" in cambios:

        email_existente = session.exec(
            select(Usuario).where(
                Usuario.email == cambios["email"],
                Usuario.id != usuario_id
            )
        ).first()

        if email_existente:
            return "EMAIL_EXISTE"

    usuario.sqlmodel_update(cambios)

    session.add(usuario)
    session.commit()
    session.refresh(usuario)

    return usuario


def eliminar_usuario(
    usuario_id: int,
    session: Session
):

    usuario = session.get(
        Usuario,
        usuario_id
    )

    if not usuario:
        return None

    reserva = session.exec(
        select(Reserva).where(
            Reserva.usuario_id == usuario_id
        )
    ).first()

    if reserva:
        return "TIENE_RESERVAS"

    session.delete(usuario)
    session.commit()

    return usuario