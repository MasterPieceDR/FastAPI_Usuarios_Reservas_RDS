from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlmodel import Session

from database.database import get_session

from schemas.reserva_schema import (
    ReservaCreate,
    ReservaResponse,
    ReservaUpdate
)

from crud.reserva_crud import (
    actualizar_reserva,
    crear_reserva,
    eliminar_reserva,
    obtener_reserva,
    obtener_reservas
)


router = APIRouter(
    prefix="/reservas",
    tags=["Reservas"]
)


@router.post(
    "/",
    response_model=ReservaResponse,
    status_code=status.HTTP_201_CREATED
)
def post_reserva(
    datos: ReservaCreate,
    session: Session = Depends(get_session)
):

    resultado = crear_reserva(
        datos,
        session
    )

    if resultado == "USUARIO_NO_EXISTE":
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    if resultado == "FECHAS_INVALIDAS":
        raise HTTPException(
            status_code=400,
            detail=(
                "La fecha final debe ser "
                "posterior a la inicial"
            )
        )

    return resultado


@router.get(
    "/",
    response_model=list[ReservaResponse]
)
def get_reservas(
    session: Session = Depends(get_session)
):

    return obtener_reservas(session)


@router.get(
    "/{reserva_id}",
    response_model=ReservaResponse
)
def get_reserva(
    reserva_id: int,
    session: Session = Depends(get_session)
):

    reserva = obtener_reserva(
        reserva_id,
        session
    )

    if not reserva:
        raise HTTPException(
            status_code=404,
            detail="Reserva no encontrada"
        )

    return reserva


@router.patch(
    "/{reserva_id}",
    response_model=ReservaResponse
)
def patch_reserva(
    reserva_id: int,
    datos: ReservaUpdate,
    session: Session = Depends(get_session)
):

    resultado = actualizar_reserva(
        reserva_id,
        datos,
        session
    )

    if resultado is None:
        raise HTTPException(
            status_code=404,
            detail="Reserva no encontrada"
        )

    if resultado == "USUARIO_NO_EXISTE":
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    if resultado == "FECHAS_INVALIDAS":
        raise HTTPException(
            status_code=400,
            detail="Las fechas de la reserva no son válidas"
        )

    return resultado


@router.delete(
    "/{reserva_id}"
)
def delete_reserva(
    reserva_id: int,
    session: Session = Depends(get_session)
):

    reserva = eliminar_reserva(
        reserva_id,
        session
    )

    if not reserva:
        raise HTTPException(
            status_code=404,
            detail="Reserva no encontrada"
        )

    return {
        "mensaje": "Reserva eliminada correctamente"
    }