# -*- coding: utf-8 -*-
"""
Created on Thu Sep  4 10:29:18 2025

@author: backy
"""

from fastapi import Depends
from sqlalchemy.orm import Session
from .database import get_db
from .models import Cliente
from fastapi import FastAPI, Path, Body, Query
from fastapi.responses import JSONResponse
from typing import List
from datetime import date

from domain.models import Tarifa, TarifaBase, Cliente, Propiedad  
from domain.schemas import (
    TarifaInput, TarifaOut, TarifaBaseInput, TarifaBaseOut,
    ClienteInput, PropiedadInput,
    ResumenCategoria, DisponibilidadPorFecha, TarifaExportada
)
from use_cases.actualizar_tarifa import ActualizarTarifaUseCase
from infrastructure.db import SessionLocal
from infrastructure.tarifa_repository import TarifaRepository
from infrastructure.portal_gateway import PortalGateway

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Backend activo"}

@app.get("/healthcheck")
def healthcheck():
    db = SessionLocal()
    try:
        count = db.query(TarifaBase).count()
        return {"tarifa_base_count": count}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/healthcheck/tarifas")
def healthcheck_tarifas():
    db = SessionLocal()
    try:
        count = db.query(Tarifa).count()
        return {"tarifas_count": count}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/healthcheck/clientes")
def healthcheck_clientes():
    db = SessionLocal()
    try:
        count = db.query(Cliente).count()
        return {"clientes_count": count}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/healthcheck/propiedades")
def healthcheck_propiedades():
    db = SessionLocal()
    try:
        count = db.query(Propiedad).count()
        return {"propiedades_count": count}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/api/clientes")
def crear_cliente(cliente: ClienteInput):
    db = SessionLocal()
    nuevo_cliente = Cliente(**cliente.dict())
    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)
    db.close()
    return {"estado": "ok", "cliente_id": nuevo_cliente.id}

@app.post("/api/propiedades")
def crear_propiedad(propiedad: PropiedadInput):
    db = SessionLocal()
    nueva_propiedad = Propiedad(**propiedad.dict())
    db.add(nueva_propiedad)
    db.commit()
    db.refresh(nueva_propiedad)
    db.close()
    return {"estado": "ok", "propiedad_id": nueva_propiedad.id}

@app.post("/api/tarifa_base")
def cargar_tarifa_base(tarifa_base: TarifaBaseInput):
    db = SessionLocal()
    existente = db.query(TarifaBase).filter_by(propiedad_id=tarifa_base.propiedad_id).first()
    if existente:
        existente.precio_base = tarifa_base.precio_base
        db.commit()
        db.refresh(existente)
        db.close()
        return {"estado": "ok", "mensaje": "Tarifa base actualizada"}
    else:
        nueva_base = TarifaBase(**tarifa_base.dict())
        db.add(nueva_base)
        db.commit()
        db.refresh(nueva_base)
        db.close()
        return {"estado": "ok", "mensaje": "Tarifa base creada"}

@app.post("/actualizar_tarifa")
def actualizar_tarifa(tarifa: TarifaInput):
    db = SessionLocal()
    existente = db.query(Tarifa).filter_by(
        propiedad_id=tarifa.propiedad_id,
        categoria_id=tarifa.categoria_id,
        fecha=tarifa.fecha
    ).first()
    db.close()
    if existente:
        return JSONResponse(status_code=400, content={
            "estado": "error",
            "mensaje": "Ya existe una tarifa para esta propiedad, categoría y fecha"
        })
    use_case = ActualizarTarifaUseCase(
        repository=TarifaRepository(),
        gateway=PortalGateway()
    )
    try:
        resultado = use_case.ejecutar(tarifa)
        return resultado
    except ValueError as e:
        return JSONResponse(status_code=400, content={"estado": "error", "mensaje": str(e)})

@app.get("/tarifas", response_model=List[TarifaOut])
def obtener_tarifas(
    propiedad_id: int = Query(default=None),
    categoria_id: int = Query(default=None),
    fecha: str = Query(default=None)
):
    db = SessionLocal()
    query = db.query(Tarifa)
    if propiedad_id is not None:
        query = query.filter(Tarifa.propiedad_id == propiedad_id)
    if categoria_id is not None:
        query = query.filter(Tarifa.categoria_id == categoria_id)
    if fecha is not None:
        query = query.filter(Tarifa.fecha == fecha)
    tarifas = query.all()
    db.close()
    return tarifas

@app.get("/tarifa_base/{propiedad_id}", response_model=TarifaBaseOut)
def obtener_tarifa_base(propiedad_id: int):
    db = SessionLocal()
    tarifa_base = db.query(TarifaBase).filter_by(propiedad_id=propiedad_id).first()
    db.close()
    if tarifa_base:
        return tarifa_base
    else:
        return JSONResponse(status_code=404, content={
            "estado": "error",
            "mensaje": "No se encontró tarifa base para esta propiedad"
        })

@app.delete("/tarifa/{id}")
def eliminar_tarifa(id: int):
    db = SessionLocal()
    tarifa = db.query(Tarifa).filter_by(id=id).first()
    if not tarifa:
        db.close()
        return JSONResponse(status_code=404, content={
            "estado": "error",
            "mensaje": f"No se encontró tarifa con ID {id}"
        })
    db.delete(tarifa)
    db.commit()
    db.close()
    return {"estado": "ok", "mensaje": f"Tarifa con ID {id} eliminada correctamente"}

@app.put("/tarifa/{id}")
def editar_tarifa(id: int, tarifa_actualizada: TarifaInput):
    db = SessionLocal()
    tarifa = db.query(Tarifa).filter_by(id=id).first()
    if not tarifa:
        db.close()
        return JSONResponse(status_code=404, content={
            "estado": "error",
            "mensaje": f"No se encontró tarifa con ID {id}"
        })
    tarifa_base = db.query(TarifaBase).filter_by(propiedad_id=tarifa_actualizada.propiedad_id).first()
    if not tarifa_base or tarifa_base.precio_base <= 0:
        db.close()
        return JSONResponse(status_code=400, content={
            "estado": "error",
            "mensaje": "Falta tarifa base para esta propiedad"
        })
    if tarifa_actualizada.precio < tarifa_base.precio_base:
        db.close()
        return JSONResponse(status_code=400, content={
            "estado": "error",
            "mensaje": f"La tarifa no puede ser menor que la tarifa base de {tarifa_base.precio_base}"
        })
    for field, value in tarifa_actualizada.dict().items():
        setattr(tarifa, field, value)
    db.commit()
    db.refresh(tarifa)
    db.close()
    return {"estado": "ok", "mensaje": f"Tarifa con ID {id} actualizada correctamente"}

@app.get("/resumen_tarifas/{propiedad_id}")
def resumen_tarifas(propiedad_id: int):
    db = SessionLocal()
    tarifas = db.query(Tarifa).filter_by(propiedad_id=propiedad_id).all()
    db.close()
    if not tarifas:
        return JSONResponse(status_code=404, content={
            "estado": "error",
            "mensaje": f"No se encontraron tarifas para la propiedad {propiedad_id}"
        })
    total_tarifas = len(tarifas)
    promedio_precio = sum(t.precio for t in tarifas) / total_tarifas
    disponibilidad_total = sum(t.disponibilidad for t in tarifas)
    return {
        "estado": "ok",
        "propiedad_id": propiedad_id,
        "total_tarifas": total_tarifas,
        "promedio_precio": round(promedio_precio, 2),
        "disponibilidad_total": disponibilidad_total
    }

@app.get("/resumen_por_categoria/{propiedad_id}", response_model=List[ResumenCategoria])
def resumen_por_categoria(propiedad_id: int):
    repo = TarifaRepository()
    resumen = repo.resumen_por_categoria(propiedad_id)

    if not resumen:
        return JSONResponse(
            status_code=404,
            content={"estado": "error", "mensaje": "No se encontraron tarifas para esta propiedad"}
        )

    return resumen

ClienteDB = Cliente
PropiedadDB = Propiedad

@app.get("/api/clientes")
def listar_clientes(db: Session = Depends(get_db)):
    return db.query(Cliente).all()