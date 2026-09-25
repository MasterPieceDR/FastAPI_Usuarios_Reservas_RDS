from sqlmodel import Session, select

from models.reserva_model import Reserva
from models.usuario_model import Usuario

from schemas.reserva_schema import (
    ReservaCreate,
    ReservaUpdate
)


def crear_reserva(
    datos: ReservaCreate,
    session: Session
):

    usuario = session.get(
        Usuario,
        datos.usuario_id
    )

    if not usuario:
        return "USUARIO_NO_EXISTE"

    if datos.fecha_fin <= datos.fecha_inicio:
        return "FECHAS_INVALIDAS"

    reserva = Reserva.model_validate(datos)

    session.add(reserva)
    session.commit()
    session.refresh(reserva)

    return reserva


def obtener_reservas(
    session: Session
):

    return session.exec(
        select(Reserva)
    ).all()


def obtener_reserva(
    reserva_id: int,
    session: Session
):

    return session.get(
        Reserva,
        reserva_id
    )


def actualizar_reserva(
    reserva_id: int,
    datos: ReservaUpdate,
    session: Session
):

    reserva = session.get(
        Reserva,
        reserva_id
    )

    if not reserva:
        return None

    cambios = datos.model_dump(
        exclude_unset=True
    )

    usuario_id = cambios.get(
        "usuario_id",
        reserva.usuario_id
    )

    usuario = session.get(
        Usuario,
        usuario_id
    )

    if not usuario:
        return "USUARIO_NO_EXISTE"

    fecha_inicio = cambios.get(
        "fecha_inicio",
        reserva.fecha_inicio
    )

    fecha_fin = cambios.get(
        "fecha_fin",
        reserva.fecha_fin
    )

    if fecha_fin <= fecha_inicio:
        return "FECHAS_INVALIDAS"

    reserva.sqlmodel_update(cambios)

    session.add(reserva)
    session.commit()
    session.refresh(reserva)

    return reserva


def eliminar_reserva(
    reserva_id: int,
    session: Session
):

    reserva = session.get(
        Reserva,
        reserva_id
    )

    if not reserva:
        return None

    session.delete(reserva)
    session.commit()

    return reserva