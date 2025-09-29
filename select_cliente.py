# -*- coding: utf-8 -*-
"""
Created on Thu Sep 25 11:10:32 2025

@author: backy
"""

from infrastructure.db import SessionLocal
from domain.models import Cliente

session = SessionLocal()

clientes = session.query(Cliente).all()

for cliente in clientes:
    print(f"🧾 ID: {cliente.id} | Nombre: {cliente.nombre} | Email: {cliente.email}")