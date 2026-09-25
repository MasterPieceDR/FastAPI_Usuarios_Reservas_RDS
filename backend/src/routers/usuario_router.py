from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlmodel import Session

from database.database import get_session

from schemas.usuario_schema import (
    UsuarioCreate,
    UsuarioResponse,
    UsuarioUpdate
)

from crud.usuario_crud import (
    actualizar_usuario,
    crear_usuario,
    eliminar_usuario,
    obtener_usuario,
    obtener_usuarios
)


router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)


@router.post(
    "/",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED
)
def post_usuario(
    datos: UsuarioCreate,
    session: Session = Depends(get_session)
):

    resultado = crear_usuario(
        datos,
        session
    )

    if resultado == "EMAIL_EXISTE":
        raise HTTPException(
            status_code=409,
            detail="El correo ya está registrado"
        )

    return resultado


@router.get(
    "/",
    response_model=list[UsuarioResponse]
)
def get_usuarios(
    session: Session = Depends(get_session)
):

    return obtener_usuarios(session)


@router.get(
    "/{usuario_id}",
    response_model=UsuarioResponse
)
def get_usuario(
    usuario_id: int,
    session: Session = Depends(get_session)
):

    usuario = obtener_usuario(
        usuario_id,
        session
    )

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return usuario


@router.patch(
    "/{usuario_id}",
    response_model=UsuarioResponse
)
def patch_usuario(
    usuario_id: int,
    datos: UsuarioUpdate,
    session: Session = Depends(get_session)
):

    resultado = actualizar_usuario(
        usuario_id,
        datos,
        session
    )

    if resultado is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    if resultado == "EMAIL_EXISTE":
        raise HTTPException(
            status_code=409,
            detail="El correo ya está registrado"
        )

    return resultado


@router.delete(
    "/{usuario_id}"
)
def delete_usuario(
    usuario_id: int,
    session: Session = Depends(get_session)
):

    resultado = eliminar_usuario(
        usuario_id,
        session
    )

    if resultado is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    if resultado == "TIENE_RESERVAS":
        raise HTTPException(
            status_code=409,
            detail=(
                "No se puede eliminar el usuario "
                "porque tiene reservas registradas"
            )
        )

    return {
        "mensaje": "Usuario eliminado correctamente"
    }