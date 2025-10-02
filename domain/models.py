# -*- coding: utf-8 -*-
"""
Created on Thu Sep  4 10:26:05 2025

@author: backy
"""


from sqlalchemy import Column, Integer, Float, String, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.db import Base

class Cliente(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, nullable=False)
    propiedades = relationship("Propiedad", back_populates="cliente")

class Propiedad(Base):
    __tablename__ = "propiedades"
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    nombre = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    ubicacion = Column(String, nullable=False)
    cliente = relationship("Cliente", back_populates="propiedades")

class Tarifa(Base):
    __tablename__ = "tarifas"
    __table_args__ = (
        UniqueConstraint("propiedad_id", "categoria_id", "fecha", name="uix_tarifa_unica"),
    )
    id = Column(Integer, primary_key=True, index=True)
    propiedad_id = Column(Integer)
    categoria_id = Column(Integer)
    fecha = Column(String)
    precio = Column(Float)
    disponibilidad = Column(Integer)

class TarifaBase(Base):
    __tablename__ = "tarifas_base"
    id = Column(Integer, primary_key=True, index=True)
    propiedad_id = Column(Integer, unique=True)
    precio_base = Column(Float)