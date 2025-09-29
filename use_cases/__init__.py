# -*- coding: utf-8 -*-
"""
Created on Thu Sep  4 11:17:58 2025

@author: backy
"""
from infrastructure.db import engine
from domain.models import Base


Base.metadata.create_all(bind=engine)
print("✅ Tablas creadas correctamente en tarifas.db")
