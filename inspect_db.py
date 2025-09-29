# -*- coding: utf-8 -*-
"""
Created on Thu Sep 25 09:41:11 2025

@author: backy
"""

from infrastructure.db import engine
from sqlalchemy import inspect

inspector = inspect(engine)
print("Tablas encontradas:", inspector.get_table_names())