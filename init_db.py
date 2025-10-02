# -*- coding: utf-8 -*-
"""
Created on Fri Sep 12 18:21:21 2025

@author: backy
"""

from infrastructure.db import engine, Base
from domain.models import Cliente, Propiedad, Tarifa, TarifaBase

Base.metadata.create_all(engine)
print("✅ Base de datos creada.")
