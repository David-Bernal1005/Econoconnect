from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ....db.session import get_db
from ....models.user import User
from ....core.security import get_current_user
from ....schemas.chatmiembro import MiembroCreate, MiembroUpdate, MiembroResponse, MiembroInvitation
from ....services.chatmiembro_service import ChatMiembroService

router = APIRouter()

@router.post("/chats/{chat_id}/miembros/", response_model=MiembroResponse)
async def agregar_miembro(
    chat_id: int,
    miembro: MiembroCreate,
    db: Session = Depends(get_db),
    usuario_actual: User = Depends(get_current_user)
):
   
    return ChatMiembroService.agregar_miembro(
        db=db,
        chat_id=chat_id,
        miembro=miembro,
        usuario_actual_id=usuario_actual.id_user
    )

@router.post("/chats/{chat_id}/miembros/invitar/")
async def invitar_miembros(
    chat_id: int,
    invitacion: MiembroInvitation,
    db: Session = Depends(get_db),
    usuario_actual: User = Depends(get_current_user)
):

    resultados = []
    for usuario_id in invitacion.usuarios:
        try:
            miembro = MiembroCreate(id_user=usuario_id)
            resultado = ChatMiembroService.agregar_miembro(
                db=db,
                chat_id=chat_id,
                miembro=miembro,
                usuario_actual_id=usuario_actual.id_user
            )
            resultados.append({"usuario_id": usuario_id, "estado": "agregado"})
        except HTTPException as e:
            resultados.append({"usuario_id": usuario_id, "estado": "error", "mensaje": str(e.detail)})
    return resultados

@router.delete("/chats/{chat_id}/miembros/{usuario_id}")
async def eliminar_miembro(
    chat_id: int,
    usuario_id: int,
    db: Session = Depends(get_db),
    usuario_actual: User = Depends(get_current_user)
):
    """
    Eliminar un miembro del chat.
    Los administradores pueden eliminar a cualquier miembro.
    Los usuarios pueden eliminarse a sí mismos.
    """
    return ChatMiembroService.eliminar_miembro(
        db=db,
        chat_id=chat_id,
        usuario_id=usuario_id,
        usuario_actual_id=usuario_actual.id_user
    )

@router.patch("/chats/{chat_id}/miembros/{usuario_id}/rol")
async def actualizar_rol_miembro(
    chat_id: int,
    usuario_id: int,
    rol_update: MiembroUpdate,
    db: Session = Depends(get_db),
    usuario_actual: User = Depends(get_current_user)
):
    """
    Actualizar el rol de un miembro en el chat.
    Solo administradores pueden cambiar roles.
    """
    return ChatMiembroService.actualizar_rol(
        db=db,
        chat_id=chat_id,
        usuario_id=usuario_id,
        rol_update=rol_update,
        usuario_actual_id=usuario_actual.id_user
    )

@router.get("/chats/{chat_id}/miembros/")
async def obtener_miembros(
    chat_id: int,
    db: Session = Depends(get_db),
    usuario_actual: User = Depends(get_current_user)
):
    """
    Obtener la lista de miembros del chat.
    En chats privados, solo los miembros pueden ver la lista.
    """
    return ChatMiembroService.obtener_miembros(
        db=db,
        chat_id=chat_id,
        usuario_actual_id=usuario_actual.id_user
    )