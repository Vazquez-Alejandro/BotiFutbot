from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from shared.database import Base


class Click(Base):
    __tablename__ = "clicks_afiliados"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    afiliado = Column(String)
    origen = Column(String)
    ip = Column(String, default="")
    user_agent = Column(String, default="")
    creado_en = Column(DateTime, default=datetime.utcnow)

    conversion = relationship("Conversion", uselist=False, back_populates="click")


class Conversion(Base):
    __tablename__ = "conversiones"

    id = Column(Integer, primary_key=True, index=True)
    click_id = Column(Integer, ForeignKey("clicks_afiliados.id"), unique=True)
    valor = Column(Float, default=0)
    confirmado = Column(Boolean, default=False)
    creado_en = Column(DateTime, default=datetime.utcnow)

    click = relationship("Click", back_populates="conversion")


class Suscripcion(Base):
    __tablename__ = "suscripciones"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), unique=True)
    plan = Column(String, default="free")
    fecha_inicio = Column(DateTime, default=datetime.utcnow)
    fecha_fin = Column(DateTime, nullable=True)
    activa = Column(Boolean, default=True)
    pago_id = Column(String, nullable=True)
    monto = Column(Float, default=0)
    metodo_pago = Column(String, nullable=True)


class NotificacionWeb(Base):
    __tablename__ = "notificaciones_web"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    endpoint = Column(String)
    p256dh = Column(String)
    auth = Column(String)
    creado_en = Column(DateTime, default=datetime.utcnow)


class EventoAnalytics(Base):
    __tablename__ = "eventos_analytics"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    tipo = Column(String)
    pagina = Column(String)
    metadata = Column(String, nullable=True)
    creado_en = Column(DateTime, default=datetime.utcnow)
