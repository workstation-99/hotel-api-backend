# -*- coding: utf-8 -*-
"""
Created on Mon Oct 20 11:35:25 2025

@author: backy
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from infrastructure.db import get_db
from domain.models import Tarifa, TarifaBase, Propiedad
from domain.schemas import TarifaInput, TarifaBaseInput, TarifaExportada
from typing import List

router = APIRouter()

@router.get("/tarifas-base")
def get_tarifas_base(db: Session = Depends(get_db)):
    return db.query(TarifaBase).all()

@router.post("/tarifas-base")
def crear_tarifa_base(tarifa: TarifaBaseInput, db: Session = Depends(get_db)):
    nueva = TarifaBase(**tarifa.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.get("/tarifas")
def get_tarifas(db: Session = Depends(get_db)):
    return db.query(Tarifa).all()

@router.post("/tarifas")
def crear_tarifa(tarifa: TarifaInput, db: Session = Depends(get_db)):
    nueva = Tarifa(**tarifa.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.get("/tarifas-exportadas", response_model=List[TarifaExportada])
def exportar_tarifas(db: Session = Depends(get_db)):
    tarifas = db.query(Tarifa).join(Propiedad).all()
    resultado = []

    for tarifa in tarifas:
        resultado.append(TarifaExportada(
            propiedad_id=tarifa.propiedad_id,
            categoria_id=tarifa.categoria_id,
            fecha=tarifa.fecha,
            precio=tarifa.precio,
            disponibilidad=tarifa.disponibilidad
        ))

    return resultado