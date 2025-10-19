# -*- coding: utf-8 -*-
"""
Created on Sun Oct 19 14:28:11 2025

@author: backy
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from infrastructure.db import get_db
from domain.models import Cliente

router = APIRouter()

@router.get("/clientes")
def get_clientes(db: Session = Depends(get_db)):
    return db.query(Cliente).all()