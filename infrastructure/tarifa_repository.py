# -*- coding: utf-8 -*-
"""
Created on Thu Sep  4 10:28:46 2025

@author: backy
"""

from datetime import date
from sqlalchemy import func
from domain.models import TarifaDB, TarifaBaseDB
from infrastructure.db import SessionLocal

class TarifaRepository:
    def guardar(self, tarifa):
        db = SessionLocal()

        # Buscar tarifa base
        tarifa_base = db.query(TarifaBaseDB).filter_by(
            propiedad_id=tarifa.propiedad_id
        ).first()

        # Validar existencia y valor de tarifa base
        if not tarifa_base or tarifa_base.precio_base <= 0:
            db.close()
            raise ValueError("Falta tarifa base para esta propiedad")

        # Validar que la tarifa no sea menor que la base
        if tarifa.precio < tarifa_base.precio_base:
            db.close()
            raise ValueError(
                f"La tarifa no puede ser menor que la tarifa base de {tarifa_base.precio_base}"
            )

        # Buscar si ya existe una tarifa para esa propiedad, categoría y fecha
        tarifa_existente = db.query(TarifaDB).filter_by(
            propiedad_id=tarifa.propiedad_id,
            categoria_id=tarifa.categoria_id,
            fecha=tarifa.fecha
        ).first()

        if tarifa_existente:
            # Actualizar la tarifa existente
            tarifa_existente.precio = tarifa.precio
            tarifa_existente.disponibilidad = tarifa.disponibilidad
            db.commit()
            db.refresh(tarifa_existente)
            print("Tarifa actualizada en la base de datos:", tarifa_existente.id)
        else:
            # Crear una nueva tarifa
            tarifa_db = TarifaDB(
                propiedad_id=tarifa.propiedad_id,
                categoria_id=tarifa.categoria_id,
                fecha=tarifa.fecha,
                precio=tarifa.precio,
                disponibilidad=tarifa.disponibilidad
            )
            db.add(tarifa_db)
            db.commit()
            db.refresh(tarifa_db)
            print("Tarifa guardada en la base de datos:", tarifa_db.id)

        db.close()

    def obtener_todas(self):
        db = SessionLocal()
        tarifas = db.query(TarifaDB).all()
        db.close()
        return tarifas

    def resumen_por_categoria(self, propiedad_id: int):
        db = SessionLocal()
        resultados = db.query(
            TarifaDB.categoria_id,
            func.count().label("total_tarifas"),
            func.avg(TarifaDB.precio).label("promedio_precio"),
            func.sum(TarifaDB.disponibilidad).label("disponibilidad_total")
        ).filter(
            TarifaDB.propiedad_id == propiedad_id
        ).group_by(
            TarifaDB.categoria_id
        ).all()
        db.close()

        return [
            {
                "categoria_id": r.categoria_id,
                "total_tarifas": r.total_tarifas,
                "promedio_precio": round(r.promedio_precio, 2),
                "disponibilidad_total": r.disponibilidad_total
            }
            for r in resultados
        ]

    def disponibilidad_por_fecha(self, propiedad_id: int, desde: date, hasta: date):
        db = SessionLocal()
        resultados = db.query(
            TarifaDB.fecha,
            func.sum(TarifaDB.disponibilidad).label("disponibilidad_total")
        ).filter(
            TarifaDB.propiedad_id == propiedad_id,
            TarifaDB.fecha >= desde,
            TarifaDB.fecha <= hasta
        ).group_by(
            TarifaDB.fecha
        ).order_by(
            TarifaDB.fecha
        ).all()
        db.close()

        return [
            {
                "fecha": r.fecha,
                "disponibilidad_total": r.disponibilidad_total
            }
            for r in resultados
        ]
    def exportar_tarifas(self, propiedad_id: int):
        db = SessionLocal()
        tarifas = db.query(TarifaDB).filter_by(propiedad_id=propiedad_id).order_by(TarifaDB.fecha).all()
        db.close()

        return [
            {
                "propiedad_id": t.propiedad_id,
                "categoria_id": t.categoria_id,
                "fecha": t.fecha,
                "precio": t.precio,
                "disponibilidad": t.disponibilidad
            }
            for t in tarifas
        ]