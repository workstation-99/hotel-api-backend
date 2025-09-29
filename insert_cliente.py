# -*- coding: utf-8 -*-
"""
Created on Thu Sep 25 10:09:53 2025

@author: backy
"""

from infrastructure.db import SessionLocal
from domain.models import Cliente

session = SessionLocal()

nuevo_cliente = Cliente(nombre="Hotel Copilot", email="contacto@copilot.ai")
session.add(nuevo_cliente)
session.commit()

print("✅ Cliente insertado.")