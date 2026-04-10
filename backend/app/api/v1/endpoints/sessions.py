"""
sessions.py — Endpoints de la API para Sessions.

Cambios respecto al mock original:
- create_session ahora es async y llama a SessionService en lugar de retornar mock hardcodeado.
- Se agrega Depends(get_session_service) para inyección de dependencias.
- El contrato de respuesta (SessionCreateResponse) NO cambia — el frontend sigue recibiendo
  exactamente los mismos campos: session_id y message.

Lo que este archivo NO hace:
- No contiene lógica de negocio. Solo recibe, delega al servicio, y mapea la respuesta.
- No maneja el estado de la sesión directamente.
"""

from fastapi import APIRouter, Depends, HTTPException

from app.application.dto.session_dto import SessionCreateResponse
from app.application.services.session_service import SessionService
from app.api.deps import get_session_service

router = APIRouter()


@router.post("", response_model=SessionCreateResponse)
async def create_session(
    service: SessionService = Depends(get_session_service),
) -> SessionCreateResponse:
    """
    Crea una nueva sesión.

    Por ahora no recibe parámetros de entrada (mismo contrato que el mock).
    Cuando el frontend esté listo para enviar un título, se agrega un body:
        body: SessionCreateRequest = Body(...)
    y se pasa body.title al servicio sin cambiar nada más.

    El servicio usará "Nueva sesión" como título por defecto hasta entonces.
    """
    try:
        session = await service.create_session()
    except ValueError as e:
        # En esta operación específica un ValueError sería inesperado,
        # pero lo capturamos por consistencia con el resto de endpoints.
        raise HTTPException(status_code=400, detail=str(e))

    # Mapeamos la entidad Session → SessionCreateResponse.
    # Este es el único lugar donde se toca el DTO.
    # Si el DTO cambia (ej: agregar más campos), solo se modifica aquí.
    return SessionCreateResponse(
        session_id=session.id,
        message="Session created successfully",
    )