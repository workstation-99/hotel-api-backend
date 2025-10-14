# -*- coding: utf-8 -*-
"""
Created on Thu Sep 25 11:28:32 2025

@author: backy
"""

from infrastructure.db import SessionLocal
from domain.models import Cliente

def listar_propiedades_por_cliente(cliente_id: int):
    session = SessionLocal()
    cliente = session.query(Cliente).filter(Cliente.id == cliente_id).first()
    propiedades = cliente.propiedades if cliente else []
    session.close()
    return propiedades