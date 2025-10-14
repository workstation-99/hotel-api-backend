# -*- coding: utf-8 -*-
"""
Created on Thu Sep 25 11:14:38 2025

@author: backy
"""

from infrastructure.db import SessionLocal
from domain.models import Cliente

def insertar_cliente(nombre: str, email: str):
    session = SessionLocal()
    nuevo = Cliente(nombre=nombre, email=email)
    session.add(nuevo)
    session.commit()
    session.close()
    print("✅ Cliente insertado desde use_cases.")

def listar_clientes():
    session = SessionLocal()
    clientes = session.query(Cliente).all()
    session.close()
    return clientes