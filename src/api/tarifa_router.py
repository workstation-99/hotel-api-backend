# -*- coding: utf-8 -*-
"""
Created on Mon Oct 20 11:35:25 2025

@author: backy
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from infrastructure.db import get_db
from domain.models import TarifaBase, Tarifa
from domain.schemas import TarifaBaseInput, TarifaInput

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