# -*- coding: utf-8 -*-
"""
Created on Thu Sep  4 11:17:58 2025

@author: backy
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from infrastructure.db import engine
from domain.models import Base


Base.metadata.create_all(bind=engine)
print("✅ Tablas creadas correctamente en tarifas.db")
