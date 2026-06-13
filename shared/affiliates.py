from sqlalchemy.orm import Session
from shared.models_monetization import Click, Conversion
from shared.models import Usuario
from datetime import datetime

AFILIADOS = {
    "bet365": {
        "nombre": "Bet365",
        "url": "https://www.bet365.com/?affiliate={ref}",
        "comision": "20%",
        "descripcion": "La mejor casa de apuestas del mundo",
    },
    "betano": {
        "nombre": "Betano",
        "url": "https://www.betano.com/?ref={ref}",
        "comision": "25%",
        "descripcion": "Apuestas deportivas con los mejores bonus",
    },
    "sportingbet": {
        "nombre": "Sportingbet",
        "url": "https://sportingbet.com/?aff={ref}",
        "comision": "15%",
        "descripcion": "Tradición en apuestas latinas",
    },
}


def registrar_click(db: Session, usuario_id: int, afiliado: str, origen: str):
    click = Click(
        usuario_id=usuario_id,
        afiliado=afiliado,
        origen=origen,
        ip="",
        user_agent="",
    )
    db.add(click)
    db.commit()
    return click.id


def registrar_conversion(db: Session, click_id: int, valor: float = 0):
    conv = Conversion(
        click_id=click_id,
        valor=valor,
        confirmado=False,
    )
    db.add(conv)
    db.commit()


def get_estadisticas_afiliados(db: Session, usuario_id: int = None):
    from sqlalchemy import func
    query = db.query(
        Click.afiliado,
        func.count(Click.id).label("clicks"),
        func.coalesce(func.sum(Conversion.valor), 0).label("ingresos"),
    ).outerjoin(Conversion, Conversion.click_id == Click.id)

    if usuario_id:
        query = query.filter(Click.usuario_id == usuario_id)

    return query.group_by(Click.afiliado).all()


def get_enlace_afiliado(afiliado: str, ref: str) -> str:
    template = AFILIADOS.get(afiliado, {}).get("url", "")
    return template.replace("{ref}", ref)
