from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List
from ..models.chat import Chat
from ..models.chatmiembro import ChatMiembro
from ..models.user import User
from ..schemas.chatmiembro import MiembroCreate, MiembroUpdate

class ChatMiembroService:
    @staticmethod
    def verificar_permisos_admin(db: Session, chat_id: int, usuario_id: int) -> bool:
        """Verifica si el usuario es administrador del chat"""
        miembro = db.query(ChatMiembro).filter(
            ChatMiembro.id_chat == chat_id,
            ChatMiembro.id_user == usuario_id,
            ChatMiembro.rol_chat == "admin"
        ).first()
        return miembro is not None

    @staticmethod
    def agregar_miembro(db: Session, chat_id: int, miembro: MiembroCreate, usuario_actual_id: int):
        chat = db.query(Chat).filter(Chat.id_chat == chat_id).first()
        if not chat:
            raise HTTPException(status_code=404, detail="Chat no encontrado")

        # Verificar si el usuario actual tiene permisos para agregar miembros
        if not ChatMiembroService.verificar_permisos_admin(db, chat_id, usuario_actual_id):
            if chat.visibilidad == "privado":
                raise HTTPException(
                    status_code=403,
                    detail="No tienes permisos para agregar miembros a este chat"
                )

        # Verificar si el usuario a agregar existe
        usuario = db.query(User).filter(User.id_user == miembro.id_user).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # Verificar si el usuario ya es miembro
        miembro_existente = db.query(ChatMiembro).filter(
            ChatMiembro.id_chat == chat_id,
            ChatMiembro.id_user == miembro.id_user
        ).first()
        if miembro_existente:
            raise HTTPException(status_code=400, detail="El usuario ya es miembro del chat")

        # Crear nuevo miembro
        nuevo_miembro = ChatMiembro(
            id_chat=chat_id,
            id_user=miembro.id_user,
            rol_chat=miembro.rol_chat
        )
        db.add(nuevo_miembro)
        db.commit()
        db.refresh(nuevo_miembro)
        return nuevo_miembro

    @staticmethod
    def eliminar_miembro(db: Session, chat_id: int, usuario_id: int, usuario_actual_id: int):
        """Elimina un miembro del chat"""
        # Verificar permisos
        if not ChatMiembroService.verificar_permisos_admin(db, chat_id, usuario_actual_id) and usuario_actual_id != usuario_id:
            raise HTTPException(
                status_code=403,
                detail="No tienes permisos para eliminar este miembro"
            )

        # Buscar y eliminar el miembro
        miembro = db.query(ChatMiembro).filter(
            ChatMiembro.id_chat == chat_id,
            ChatMiembro.id_user == usuario_id
        ).first()
        if not miembro:
            raise HTTPException(status_code=404, detail="Miembro no encontrado")

        # No permitir eliminar al último administrador
        if miembro.rol_chat == "admin":
            admins_count = db.query(ChatMiembro).filter(
                ChatMiembro.id_chat == chat_id,
                ChatMiembro.rol_chat == "admin"
            ).count()
            if admins_count <= 1:
                raise HTTPException(
                    status_code=400,
                    detail="No se puede eliminar al último administrador del chat"
                )

        db.delete(miembro)
        db.commit()
        return {"message": "Miembro eliminado exitosamente"}

    @staticmethod
    def actualizar_rol(db: Session, chat_id: int, usuario_id: int, rol_update: MiembroUpdate, usuario_actual_id: int):
        """Actualiza el rol de un miembro"""
        # Verificar permisos de administrador
        if not ChatMiembroService.verificar_permisos_admin(db, chat_id, usuario_actual_id):
            raise HTTPException(
                status_code=403,
                detail="Solo los administradores pueden cambiar roles"
            )

        # Buscar el miembro
        miembro = db.query(ChatMiembro).filter(
            ChatMiembro.id_chat == chat_id,
            ChatMiembro.id_user == usuario_id
        ).first()
        if not miembro:
            raise HTTPException(status_code=404, detail="Miembro no encontrado")

        # No permitir degradar al último administrador
        if miembro.rol_chat == "admin" and rol_update.rol_chat != "admin":
            admins_count = db.query(ChatMiembro).filter(
                ChatMiembro.id_chat == chat_id,
                ChatMiembro.rol_chat == "admin"
            ).count()
            if admins_count <= 1:
                raise HTTPException(
                    status_code=400,
                    detail="No se puede degradar al último administrador del chat"
                )

        miembro.rol_chat = rol_update.rol_chat
        db.commit()
        db.refresh(miembro)
        return miembro

    @staticmethod
    def obtener_miembros(db: Session, chat_id: int, usuario_actual_id: int):
        """Obtiene la lista de miembros de un chat"""
        # Verificar si el usuario actual es miembro del chat
        es_miembro = db.query(ChatMiembro).filter(
            ChatMiembro.id_chat == chat_id,
            ChatMiembro.id_user == usuario_actual_id
        ).first()
        
        chat = db.query(Chat).filter(Chat.id_chat == chat_id).first()
        if not chat:
            raise HTTPException(status_code=404, detail="Chat no encontrado")

        if not es_miembro and chat.visibilidad == "privado":
            raise HTTPException(
                status_code=403,
                detail="No tienes acceso a este chat"
            )

        # Obtener todos los miembros con información básica del usuario
        miembros = db.query(ChatMiembro, User).join(
            User, ChatMiembro.id_user == User.id_user
        ).filter(ChatMiembro.id_chat == chat_id).all()

        return [
            {
                "id_user": user.id_user,
                "nombre": user.name,
                "email": user.email,
                "rol_chat": miembro.rol_chat,
                "fecha_ingreso": miembro.fecha_ingreso
            }
            for miembro, user in miembros
        ]