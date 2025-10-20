# -*- coding: utf-8 -*-
"""
Created on Mon Oct 20 09:28:51 2025

@author: backy
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from infrastructure.db import get_db
from domain.models import Propiedad
from domain.schemas import PropiedadInput, PropiedadOut

router = APIRouter()

@router.get("/propiedades", response_model=List[PropiedadOut])
def get_propiedades(db: Session = Depends(get_db)):
    return db.query(Propiedad).all()

@router.post("/propiedades")
def crear_propiedad(propiedad: PropiedadInput, db: Session = Depends(get_db)):
    nueva = Propiedad(**propiedad.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva