from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.noticias import Noticia
from app.models.fuentes import Fuente
from app.models.categorias import Categoria
from app.schemas.noticias import NoticiaSchema
from pydantic import BaseModel
from datetime import datetime


# Declaración única del router
router = APIRouter()

# Endpoint para obtener todas las noticias de un usuario (activas e inactivas)
@router.get("/noticias/usuario/{usuario}", response_model=list[NoticiaSchema])
def get_noticias_usuario(usuario: str, db: Session = Depends(get_db)):
    from app.models.user import User
    noticias = db.query(Noticia).filter(Noticia.usuario == usuario).all()
    resultado = []
    for noticia in noticias:
        noticia_dict = noticia.__dict__.copy()
        # El campo profile_image ya está en la noticia
        resultado.append(noticia_dict)
    return resultado


class NoticiaUpdateSchema(BaseModel):
    titulo: str | None = None
    resumen: str | None = None
    enlace: str | None = None
    Id_Categoria: int | None = None
    Id_Fuente: int | None = None
    activa: int | None = None

@router.put("/noticias/{noticia_id}", response_model=NoticiaSchema)
def update_noticia(noticia_id: int, noticia: NoticiaUpdateSchema = Body(...), db: Session = Depends(get_db)):
    print(f"[DEBUG] Editando noticia con ID: {noticia_id}")
    noticia_db = db.query(Noticia).filter(Noticia.Id_Noticia == noticia_id).first()
    print(f"[DEBUG] Resultado de la consulta: {noticia_db}")
    if not noticia_db:
        print(f"[DEBUG] No se encontró la noticia con ID: {noticia_id}")
        raise HTTPException(status_code=404, detail="Noticia no encontrada")
    for field, value in noticia.model_dump(exclude_unset=True).items():
        setattr(noticia_db, field, value)
    db.commit()
    db.refresh(noticia_db)
    print(f"[DEBUG] Noticia actualizada: {noticia_db}")
    return noticia_db

@router.patch("/noticias/{noticia_id}/inactivar", response_model=NoticiaSchema)
def inactivar_noticia(noticia_id: int, db: Session = Depends(get_db)):
    noticia_db = db.query(Noticia).filter(Noticia.Id_Noticia == noticia_id).first()
    if not noticia_db:
        raise HTTPException(status_code=404, detail="Noticia no encontrada")
    noticia_db.activa = 0
    db.commit()
    db.refresh(noticia_db)
    return noticia_db


@router.get("/noticias", response_model=list[NoticiaSchema])
def get_noticias(db: Session = Depends(get_db)):
    # Solo noticias activas
    from app.models.user import User
    noticias = db.query(Noticia).filter(Noticia.activa == 1).all()
    resultado = []
    for noticia in noticias:
        noticia_dict = noticia.__dict__.copy()
        resultado.append(noticia_dict)
    return resultado




class NoticiaCreateSchema(BaseModel):
    titulo: str
    resumen: str
    enlace: str
    fecha_publicacion: str
    categoria: str | None = None
    usuario: str | None = None

@router.post("/noticias", response_model=NoticiaSchema, status_code=201)
def create_noticia(noticia: NoticiaCreateSchema, db: Session = Depends(get_db)):
    # Convierte fecha_publicacion a datetime si es string
    try:
        fecha_pub = noticia.fecha_publicacion
        if isinstance(fecha_pub, str):
            try:
                fecha_pub = datetime.fromisoformat(fecha_pub.replace("Z", ""))
            except Exception:
                fecha_pub = datetime.now()

        # Crear fuente si no existe
        fuente = db.query(Fuente).filter(Fuente.Url_Fuente == noticia.enlace).first()
        if not fuente:
            fuente = Fuente(Nombre_Fuente=noticia.titulo, Url_Fuente=noticia.enlace, Tipo_Fuente="noticia")
            db.add(fuente)
            db.commit()
            db.refresh(fuente)

        # Crear categoría si no existe
        categoria = db.query(Categoria).filter(Categoria.Nombre_Categoria == noticia.categoria).first()
        if not categoria:
            categoria = Categoria(Nombre_Categoria=noticia.categoria, Descripcion=noticia.resumen)
            db.add(categoria)
            db.commit()
            db.refresh(categoria)

        from app.models.user import User
        user = db.query(User).filter((User.username == noticia.usuario) | (User.name == noticia.usuario)).first()
        profile_image = None
        if user and user.profile_image:
            profile_image = user.profile_image
        nueva_noticia = Noticia(
            titulo=noticia.titulo,
            resumen=noticia.resumen,
            enlace=noticia.enlace,
            fecha_publicacion=fecha_pub,
            Id_Categoria=categoria.Id_Categoria,
            Id_Fuente=fuente.Id_Fuente,
            usuario=noticia.usuario,
            profile_image=profile_image
        )
        db.add(nueva_noticia)
        db.commit()
        db.refresh(nueva_noticia)
        noticia_dict = nueva_noticia.__dict__.copy()
        return noticia_dict
    except Exception as e:
        print("Error al crear noticia:", e)
        raise HTTPException(status_code=500, detail=f"Error al crear noticia: {str(e)}")

