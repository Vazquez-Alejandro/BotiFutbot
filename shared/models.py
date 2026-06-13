from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from shared.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    photo_url = Column(String, nullable=True)
    creado_en = Column(DateTime, default=datetime.utcnow)
    activo = Column(Boolean, default=True)

    equipos = relationship("UsuarioEquipo", back_populates="usuario")
    amigos = relationship("Amistad", foreign_keys="Amistad.usuario_id", back_populates="usuario")
    predicciones = relationship("Prediccion", back_populates="usuario")


class Equipo(Base):
    __tablename__ = "equipos"

    id = Column(Integer, primary_key=True, index=True)
    api_id = Column(Integer, unique=True, index=True)
    nombre = Column(String)
    logo = Column(String, nullable=True)
    pais = Column(String)
    liga = Column(String)

    usuarios = relationship("UsuarioEquipo", back_populates="equipo")


class UsuarioEquipo(Base):
    __tablename__ = "usuario_equipos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    equipo_id = Column(Integer, ForeignKey("equipos.id"))
    creado_en = Column(DateTime, default=datetime.utcnow)

    usuario = relationship("Usuario", back_populates="equipos")
    equipo = relationship("Equipo", back_populates="usuarios")


class Amistad(Base):
    __tablename__ = "amistades"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    amigo_id = Column(Integer, ForeignKey("usuarios.id"))
    estado = Column(String, default="pendiente")
    creado_en = Column(DateTime, default=datetime.utcnow)

    usuario = relationship("Usuario", foreign_keys=[usuario_id], back_populates="amigos")
    amigo = relationship("Usuario", foreign_keys=[amigo_id])


class Prediccion(Base):
    __tablename__ = "predicciones"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    fixture_id = Column(Integer, index=True)
    goles_local = Column(Integer)
    goles_visitante = Column(Integer)
    puntos = Column(Integer, default=0)
    creada_en = Column(DateTime, default=datetime.utcnow)

    usuario = relationship("Usuario", back_populates="predicciones")


class PartidoGuardado(Base):
    __tablename__ = "partidos_guardados"

    id = Column(Integer, primary_key=True, index=True)
    fixture_id = Column(Integer, unique=True, index=True)
    liga_id = Column(Integer)
    liga_nombre = Column(String)
    fecha_utc = Column(DateTime)
    local_id = Column(Integer)
    local_nombre = Column(String)
    local_logo = Column(String, nullable=True)
    visitante_id = Column(Integer)
    visitante_nombre = Column(String)
    visitante_logo = Column(String, nullable=True)
    goles_local = Column(Integer, nullable=True)
    goles_visitante = Column(Integer, nullable=True)
    estado = Column(String, default="NS")
    ronda = Column(String, nullable=True)
    actualizado_en = Column(DateTime, default=datetime.utcnow)


class BotUsuario(Base):
    __tablename__ = "bot_usuarios"

    chat_id = Column(Integer, primary_key=True)
    username = Column(String, nullable=True)
    equipos = Column(Text, default="[]")
    activo = Column(Boolean, default=True)
    creado_en = Column(DateTime, default=datetime.utcnow)


class EventoEnviado(Base):
    __tablename__ = "eventos_enviados"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, index=True)
    evento_id = Column(String, index=True)
    tipo = Column(String, nullable=True)
    enviado_en = Column(DateTime, default=datetime.utcnow)


class NoticiaEnviada(Base):
    __tablename__ = "noticias_enviadas"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, index=True)
    noticia_url = Column(String, unique=True)
    enviado_en = Column(DateTime, default=datetime.utcnow)


class PartidoProgramado(Base):
    __tablename__ = "partidos_programados"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, index=True)
    equipo_id = Column(Integer)
    equipo_nombre = Column(String)
    fixture_id = Column(String, unique=True, index=True)
    fecha_utc = Column(DateTime)
    local = Column(String)
    visitante = Column(String)
    liga = Column(String)
    notificado_inicio = Column(Boolean, default=False)
    notificado_15min = Column(Boolean, default=False)
    notificado_manana = Column(Boolean, default=False)
    notificado_lineup = Column(Boolean, default=False)
    notificado_ht = Column(Boolean, default=False)
    notificado_2h = Column(Boolean, default=False)
    en_vivo = Column(Boolean, default=False)
    goles_local = Column(Integer, default=0)
    goles_visitante = Column(Integer, default=0)
    estado = Column(String, default="")
    enviado_en = Column(DateTime, default=datetime.utcnow)


class AnalyticsEvent(Base):
    __tablename__ = "analytics"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, index=True)
    accion = Column(String)
    detalle = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class MetricaDiaria(Base):
    __tablename__ = "metricas_diarias"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(String, unique=True, index=True)
    usuarios_nuevos = Column(Integer, default=0)
    usuarios_activos = Column(Integer, default=0)
    clicks_links = Column(Integer, default=0)
    conversiones = Column(Integer, default=0)
    mensajes_enviados = Column(Integer, default=0)
