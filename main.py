# -*- coding: utf-8 -*-
"""
Created on Thu Sep 25 11:16:18 2025

@author: backy
"""

from use_cases.clientes import insertar_cliente, listar_clientes

insertar_cliente("Hotel Copilot", "contacto@copilot.ai")

clientes = listar_clientes()
for cliente in clientes:
    print(f"🧾 ID: {cliente.id} | Nombre: {cliente.nombre} | Email: {cliente.email}")
    
from use_cases.propiedades import listar_propiedades_por_cliente

propiedades = listar_propiedades_por_cliente(1)
for p in propiedades:
    print(f"🏠 ID: {p.id} | Nombre: {p.nombre} | Tipo: {p.tipo} | Ubicación: {p.ubicacion}")

from use_cases.tarifas import insertar_tarifa

insertar_tarifa(
    propiedad_id=1,
    categoria_id=101,
    fecha="2025-10-02",
    precio=15000.0,
    disponibilidad=5
)    

from use_cases.tarifas import listar_tarifas_por_propiedad
from use_cases.tarifas import insertar_tarifa_base

tarifas = listar_tarifas_por_propiedad(1, "2025-10-01")
for t in tarifas:
    print(f"💲 ID: {t.id} | Fecha: {t.fecha} | Precio: {t.precio} | Disponibilidad: {t.disponibilidad}")
    insertar_tarifa_base(propiedad_id=1, precio_base=12000.0)
    
from use_cases.tarifas import insertar_tarifas_por_rango

insertar_tarifas_por_rango(
    propiedad_id=1,
    categoria_id=101,
    fecha_inicio="2025-10-03",
    fecha_fin="2025-10-07",
    precio=16000.0,
    disponibilidad=4
)    

from use_cases.tarifas import consultar_disponibilidad

dispo = consultar_disponibilidad(1, 101, "2025-10-04")
print(f"📅 Disponibilidad para 2025-10-04: {dispo['disponibilidad']} | Precio: {dispo['precio']}")  