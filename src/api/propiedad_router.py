# -*- coding: utf-8 -*-
"""
Created on Mon Oct 20 09:28:51 2025

@author: backy
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from infrastructure.db import get_db
from domain.models import Propiedad

router = APIRouter()

@router.get("/propiedades")
def get_propiedades(db: Session = Depends(get_db)):
    return db.query(Propiedad).all()