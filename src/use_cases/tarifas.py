# -*- coding: utf-8 -*-
"""
Created on Thu Sep 25 11:41:15 2025

@author: backy
"""

from infrastructure.db import SessionLocal
from domain.models import Tarifa

def insertar_tarifa(propiedad_id: int, categoria_id: int, fecha: str, precio: float, disponibilidad: int):
    session = SessionLocal()
    existe = session.query(Tarifa).filter_by(
        propiedad_id=propiedad_id,
        categoria_id=categoria_id,
        fecha=fecha
    ).first()
    if existe:
        print("⚠️ Ya existe una tarifa para esa combinación.")
        session.close()
        return
    nueva = Tarifa(
        propiedad_id=propiedad_id,
        categoria_id=categoria_id,
        fecha=fecha,
        precio=precio,
        disponibilidad=disponibilidad
    )
    session.add(nueva)
    session.commit()
    session.close()
    print("💲 Tarifa insertada desde use_cases.")
    


def listar_tarifas_por_propiedad(propiedad_id: int, fecha: str = None):
    session = SessionLocal()
    query = session.query(Tarifa).filter(Tarifa.propiedad_id == propiedad_id)
    if fecha:
        query = query.filter(Tarifa.fecha == fecha)
    tarifas = query.all()
    session.close()
    return tarifas   

from domain.models import TarifaBase

def insertar_tarifa_base(propiedad_id: int, precio_base: float):
    session = SessionLocal()
    existe = session.query(TarifaBase).filter_by(propiedad_id=propiedad_id).first()
    if existe:
        print("⚠️ Ya existe una tarifa base para esa propiedad.")
        session.close()
        return
    nueva = TarifaBase(propiedad_id=propiedad_id, precio_base=precio_base)
    session.add(nueva)
    session.commit()
    session.close()
    print("📌 Tarifa base insertada desde use_cases.")  
    
    
from datetime import datetime, timedelta

def insertar_tarifas_por_rango(propiedad_id: int, categoria_id: int, fecha_inicio: str, fecha_fin: str, precio: float, disponibilidad: int):
    session = SessionLocal()
    inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
    fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
    dias = (fin - inicio).days + 1

    insertadas = 0
    duplicadas = 0

    for i in range(dias):
        fecha_actual = (inicio + timedelta(days=i)).strftime("%Y-%m-%d")
        existe = session.query(Tarifa).filter_by(
            propiedad_id=propiedad_id,
            categoria_id=categoria_id,
            fecha=fecha_actual
        ).first()
        if existe:
            duplicadas += 1
            continue
        nueva = Tarifa(
            propiedad_id=propiedad_id,
            categoria_id=categoria_id,
            fecha=fecha_actual,
            precio=precio,
            disponibilidad=disponibilidad
        )
        session.add(nueva)
        insertadas += 1

    session.commit()
    session.close()
    print(f"📆 Tarifas insertadas: {insertadas} | Duplicadas: {duplicadas}")
    
def consultar_disponibilidad(propiedad_id: int, categoria_id: int, fecha: str):
    session = SessionLocal()
    tarifa = session.query(Tarifa).filter_by(
        propiedad_id=propiedad_id,
        categoria_id=categoria_id,
        fecha=fecha
    ).first()
    session.close()

    if tarifa:
        return {
            "fecha": tarifa.fecha,
            "precio": tarifa.precio,
            "disponibilidad": tarifa.disponibilidad
        }
    else:
        return {
            "fecha": fecha,
            "precio": None,
            "disponibilidad": None
        }    