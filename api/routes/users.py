from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from shared.database import get_db
from shared.models import Usuario, Equipo, UsuarioEquipo, Amistad, Prediccion
from shared.api_client import football_client

router = APIRouter(prefix="/api/users", tags=["users"])


class EquipoResponse(BaseModel):
    api_id: int
    nombre: str
    logo: Optional[str] = None
    pais: str
    liga: str


@router.get("/{user_id}/equipos")
def get_equipos_usuario(user_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    equipos = []
    for ue in usuario.equipos:
        eq = ue.equipo
        equipos.append({
            "id": eq.id,
            "api_id": eq.api_id,
            "nombre": eq.nombre,
            "logo": eq.logo,
            "pais": eq.pais,
            "liga": eq.liga,
        })
    return {"equipos": equipos}


@router.post("/{user_id}/equipos")
def agregar_equipo(user_id: int, api_id: int, nombre: str, logo: str = None, pais: str = "", liga: str = "", db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    equipo = db.query(Equipo).filter(Equipo.api_id == api_id).first()
    if not equipo:
        equipo = Equipo(api_id=api_id, nombre=nombre, logo=logo, pais=pais, liga=liga)
        db.add(equipo)
        db.commit()
        db.refresh(equipo)

    existente = db.query(UsuarioEquipo).filter(
        UsuarioEquipo.usuario_id == user_id,
        UsuarioEquipo.equipo_id == equipo.id,
    ).first()

    if not existente:
        ue = UsuarioEquipo(usuario_id=user_id, equipo_id=equipo.id)
        db.add(ue)
        db.commit()

    return {"ok": True}


@router.delete("/{user_id}/equipos/{equipo_id}")
def eliminar_equipo(user_id: int, equipo_id: int, db: Session = Depends(get_db)):
    db.query(UsuarioEquipo).filter(
        UsuarioEquipo.usuario_id == user_id,
        UsuarioEquipo.equipo_id == equipo_id,
    ).delete()
    db.commit()
    return {"ok": True}


@router.get("/{user_id}/friends")
def get_amigos(user_id: int, db: Session = Depends(get_db)):
    amistades = db.query(Amistad).filter(
        (Amistad.usuario_id == user_id) | (Amistad.amigo_id == user_id),
        Amistad.estado == "aceptada",
    ).all()

    amigos = []
    for a in amistades:
        amigo_id = a.amigo_id if a.usuario_id == user_id else a.usuario_id
        amigo = db.query(Usuario).filter(Usuario.id == amigo_id).first()
        if amigo:
            amigos.append({
                "id": amigo.id,
                "username": amigo.username,
                "first_name": amigo.first_name,
                "photo_url": amigo.photo_url,
            })
    return {"amigos": amigos}


@router.post("/{user_id}/friends/{amigo_id}")
def agregar_amigo(user_id: int, amigo_id: int, db: Session = Depends(get_db)):
    if user_id == amigo_id:
        raise HTTPException(status_code=400, detail="No podés agregarte a vos mismo")

    existente = db.query(Amistad).filter(
        ((Amistad.usuario_id == user_id) & (Amistad.amigo_id == amigo_id)) |
        ((Amistad.usuario_id == amigo_id) & (Amistad.amigo_id == user_id))
    ).first()

    if existente:
        if existente.estado == "pendiente":
            existente.estado = "aceptada"
            db.commit()
            return {"ok": True, "estado": "aceptada"}
        return {"ok": True, "estado": existente.estado}

    amistad = Amistad(usuario_id=user_id, amigo_id=amigo_id, estado="pendiente")
    db.add(amistad)
    db.commit()
    return {"ok": True, "estado": "pendiente"}


@router.post("/{user_id}/predictions")
def crear_prediccion(user_id: int, fixture_id: int, goles_local: int, goles_visitante: int, db: Session = Depends(get_db)):
    existente = db.query(Prediccion).filter(
        Prediccion.usuario_id == user_id,
        Prediccion.fixture_id == fixture_id,
    ).first()

    if existente:
        existente.goles_local = goles_local
        existente.goles_visitante = goles_visitante
    else:
        pred = Prediccion(
            usuario_id=user_id,
            fixture_id=fixture_id,
            goles_local=goles_local,
            goles_visitante=goles_visitante,
        )
        db.add(pred)

    db.commit()
    return {"ok": True}


@router.get("/{user_id}/predictions/{fixture_id}")
def get_prediccion(user_id: int, fixture_id: int, db: Session = Depends(get_db)):
    pred = db.query(Prediccion).filter(
        Prediccion.usuario_id == user_id,
        Prediccion.fixture_id == fixture_id,
    ).first()

    if not pred:
        return {"prediction": None}

    return {
        "prediction": {
            "goles_local": pred.goles_local,
            "goles_visitante": pred.goles_visitante,
            "puntos": pred.puntos,
        }
    }


@router.get("/{user_id}/stats")
def get_stats(user_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    total_predicciones = db.query(Prediccion).filter(Prediccion.usuario_id == user_id).count()
    total_puntos = db.query(Prediccion).filter(Prediccion.usuario_id == user_id).with_entities(Prediccion.puntos).all()
    puntos_sum = sum(p[0] for p in total_puntos)
    equipos_seguidos = db.query(UsuarioEquipo).filter(UsuarioEquipo.usuario_id == user_id).count()
    amigos_count = db.query(Amistad).filter(
        (Amistad.usuario_id == user_id) | (Amistad.amigo_id == user_id),
        Amistad.estado == "aceptada",
    ).count()

    return {
        "stats": {
            "predicciones": total_predicciones,
            "puntos": puntos_sum,
            "equipos_seguidos": equipos_seguidos,
            "amigos": amigos_count,
        }
    }
