from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlmodel import Session

from database.database import get_session


router = APIRouter(
    prefix="/database",
    tags=["Database"]
)


@router.get("/status")
def verificar_base_datos(
    session: Session = Depends(get_session)
):
    try:
        info = session.execute(
            text("""
                SELECT
                    current_database() AS database_name,
                    current_user AS database_user,
                    version() AS postgres_version
            """)
        ).mappings().one()

        tablas = session.execute(
            text("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name
            """)
        ).scalars().all()

        total_usuarios = 0

        if "usuarios" in tablas:
            total_usuarios = session.execute(
                text("SELECT COUNT(*) FROM usuarios")
            ).scalar_one()

        total_reservas = 0

        if "reservas" in tablas:
            total_reservas = session.execute(
                text("SELECT COUNT(*) FROM reservas")
            ).scalar_one()

        ssl_activo = session.execute(
            text("""
                SELECT ssl
                FROM pg_stat_ssl
                WHERE pid = pg_backend_pid()
            """)
        ).scalar_one_or_none()

        return {
            "conexion": "OK",
            "motor": "PostgreSQL",
            "proveedor": "Amazon RDS",
            "base_datos": info["database_name"],
            "usuario_bd": info["database_user"],
            "ssl": bool(ssl_activo),
            "tablas": tablas,
            "registros": {
                "usuarios": total_usuarios,
                "reservas": total_reservas
            },
            "mensaje": "FastAPI esta conectado correctamente a Amazon RDS"
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="No se pudo conectar con la base de datos"
        )
