# -*- coding: utf-8 -*-
"""
Created on Mon Sep  8 11:29:29 2025

@author: backy
"""

from pydantic import BaseModel
from datetime import date

class ResumenCategoria(BaseModel):
    categoria_id: int
    total_tarifas: int
    promedio_precio: float
    disponibilidad_total: int


class DisponibilidadPorFecha(BaseModel):
    fecha: date
    disponibilidad_total: int
    

class TarifaExportada(BaseModel):
    propiedad_id: int
    categoria_id: int
    fecha: date
    precio: float
    disponibilidad: int    
    
class TarifaBaseInput(BaseModel):
    propiedad_id: str
    precio_base: float
    
from pydantic import BaseModel

class ClienteInput(BaseModel):
    nombre: str
    tipo: str
    contacto: str    
    
from pydantic import BaseModel

class PropiedadInput(BaseModel):
    cliente_id: int
    nombre: str
    tipo: str
    ubicacion: str    
    
from sqlalchemy import Column, Integer, Float, Date
from infrastructure.base import Base

class TarifaBaseDB(Base):
    __tablename__ = "tarifa_base"

    id = Column(Integer, primary_key=True, index=True)
    propiedad_id = Column(Integer, index=True)
    categoria_id = Column(Integer, index=True)
    fecha = Column(Date)

class TarifaDB(Base):
    __tablename__ = "tarifa"

    id = Column(Integer, primary_key=True, index=True)
    propiedad_id = Column(Integer, index=True)
    categoria_id = Column(Integer, index=True)
    fecha = Column(Date)
    precio = Column(Float)
    disponibilidad = Column(Integer)    