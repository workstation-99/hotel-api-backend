# -*- coding: utf-8 -*-
"""
Created on Thu Sep  4 10:29:18 2025

@author: backy
"""
from typing import List
from fastapi import FastAPI, Path, Body, Query
from domain.models import Tarifa, TarifaBaseDB, TarifaDB
from use_cases.actualizar_tarifa import ActualizarTarifaUseCase
from infrastructure.tarifa_repository import TarifaRepository
from infrastructure.portal_gateway import PortalGateway
from infrastructure.db import SessionLocal
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from domain.schemas import ResumenCategoria


app = FastAPI()

@app.get("/")
def root():
    return {"status": "Backend activo"}


class TarifaBaseInput(BaseModel):
    propiedad_id: int
    precio_base: float = Field(gt=0, description="La tarifa base debe ser mayor a cero")

@app.post("/api/tarifa_base")
def cargar_tarifa_base(tarifa_base: TarifaBaseInput):
    db = SessionLocal()
    existente = db.query(TarifaBaseDB).filter_by(propiedad_id=tarifa_base.propiedad_id).first()

    if existente:
        existente.precio_base = tarifa_base.precio_base
        db.commit()
        db.refresh(existente)
        db.close()
        return {"estado": "ok", "mensaje": "Tarifa base actualizada"}
    else:
        nueva_base = TarifaBaseDB(
            propiedad_id=tarifa_base.propiedad_id,
            precio_base=tarifa_base.precio_base
        )
        db.add(nueva_base)
        db.commit()
        db.refresh(nueva_base)
        db.close()
        return {"estado": "ok", "mensaje": "Tarifa base creada"}

@app.post("/actualizar_tarifa")
def actualizar_tarifa(tarifa: Tarifa):
    db = SessionLocal()

    # Validación de duplicados por propiedad, categoría y fecha
    existente = db.query(TarifaDB).filter_by(
        propiedad_id=tarifa.propiedad_id,
        categoria_id=tarifa.categoria_id,
        fecha=tarifa.fecha
    ).first()

    if existente:
        db.close()
        return JSONResponse(status_code=400, content={
            "estado": "error",
            "mensaje": "Ya existe una tarifa para esta propiedad, categoría y fecha"
        })

    db.close()

    use_case = ActualizarTarifaUseCase(
        repository=TarifaRepository(),
        gateway=PortalGateway()
    )
    try:
        resultado = use_case.ejecutar(tarifa)
        return resultado
    except ValueError as e:
        return JSONResponse(status_code=400, content={"estado": "error", "mensaje": str(e)})

@app.get("/tarifas")
def obtener_tarifas(
    propiedad_id: int = Query(default=None),
    categoria_id: int = Query(default=None),
    fecha: str = Query(default=None)
):
    db = SessionLocal()
    query = db.query(TarifaDB)

    if propiedad_id is not None:
        query = query.filter(TarifaDB.propiedad_id == propiedad_id)
    if categoria_id is not None:
        query = query.filter(TarifaDB.categoria_id == categoria_id)
    if fecha is not None:
        query = query.filter(TarifaDB.fecha == fecha)

    tarifas = query.all()
    db.close()

    resultado = [t.__dict__ for t in tarifas]
    for r in resultado:
        r.pop("_sa_instance_state", None)

    return JSONResponse(content=resultado)

@app.get("/tarifa_base/{propiedad_id}")
def obtener_tarifa_base(propiedad_id: int):
    db = SessionLocal()
    tarifa_base = db.query(TarifaBaseDB).filter_by(propiedad_id=propiedad_id).first()
    db.close()

    if tarifa_base:
        return {
            "estado": "ok",
            "propiedad_id": tarifa_base.propiedad_id,
            "precio_base": tarifa_base.precio_base
        }
    else:
        return JSONResponse(status_code=404, content={
            "estado": "error",
            "mensaje": "No se encontró tarifa base para esta propiedad"
        })

@app.delete("/tarifa/{id}")
def eliminar_tarifa(id: int):
    db = SessionLocal()
    tarifa = db.query(TarifaDB).filter_by(id=id).first()

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
def editar_tarifa(
    id: int = Path(..., description="ID de la tarifa a modificar"),
    tarifa_actualizada: Tarifa = Body(...)
):
    db = SessionLocal()
    tarifa = db.query(TarifaDB).filter_by(id=id).first()

    if not tarifa:
        db.close()
        return JSONResponse(status_code=404, content={
            "estado": "error",
            "mensaje": f"No se encontró tarifa con ID {id}"
        })

    tarifa_base = db.query(TarifaBaseDB).filter_by(propiedad_id=tarifa_actualizada.propiedad_id).first()
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

    tarifa.propiedad_id = tarifa_actualizada.propiedad_id
    tarifa.categoria_id = tarifa_actualizada.categoria_id
    tarifa.fecha = tarifa_actualizada.fecha
    tarifa.precio = tarifa_actualizada.precio
    tarifa.disponibilidad = tarifa_actualizada.disponibilidad

    db.commit()
    db.refresh(tarifa)
    db.close()

    return {"estado": "ok", "mensaje": f"Tarifa con ID {id} actualizada correctamente"}

@app.get("/resumen_tarifas/{propiedad_id}")
def resumen_tarifas(propiedad_id: int):
    db = SessionLocal()
    tarifas = db.query(TarifaDB).filter_by(propiedad_id=propiedad_id).all()
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

@app.get("/resumen_por_categoria/{propiedad_id}", response_model=list[ResumenCategoria])
def resumen_por_categoria(propiedad_id: int):
    repo = TarifaRepository()
    resumen = repo.resumen_por_categoria(propiedad_id)

    if not resumen:
        return JSONResponse(
            status_code=404,
            content={"estado": "error", "mensaje": "No se encontraron tarifas para esta propiedad"}
        )

    return resumen


from domain.schemas import DisponibilidadPorFecha
from datetime import date
from fastapi import Query

@app.get("/disponibilidad_por_fecha/{propiedad_id}", response_model=list[DisponibilidadPorFecha])
def disponibilidad_por_fecha(
    propiedad_id: int,
    desde: date = Query(..., description="Fecha de inicio"),
    hasta: date = Query(..., description="Fecha de fin")
):
    repo = TarifaRepository()
    resultado = repo.disponibilidad_por_fecha(propiedad_id, desde, hasta)

    if not resultado:
        return JSONResponse(
            status_code=404,
            content={"estado": "error", "mensaje": "No se encontraron tarifas en ese rango"}
        )

    return resultado



from domain.schemas import TarifaExportada
@app.get("/tarifas_export/{propiedad_id}", response_model=List[TarifaExportada])
def tarifas_export(propiedad_id: int):
    repo = TarifaRepository()
    tarifas = repo.exportar_tarifas(propiedad_id)

    if not tarifas:
        return JSONResponse(
            status_code=404,
            content={"estado": "error", "mensaje": "No se encontraron tarifas para esta propiedad"}
        )

    return [TarifaExportada(
    propiedad_id=t.propiedad_id,
    categoria_id=t.categoria_id,
    fecha=t.fecha,
    precio=t.precio,
    disponibilidad=t.disponibilidad
) for t in tarifas]

from domain.schemas import ClienteInput
from domain.models import ClienteDB


@app.post("/api/clientes")
def crear_cliente(cliente: ClienteInput):
    try:
        db = SessionLocal()
        nuevo_cliente = ClienteDB(
            nombre=cliente.nombre,
            tipo=cliente.tipo,
            contacto=cliente.contacto
        )
        db.add(nuevo_cliente)
        db.commit()
        db.refresh(nuevo_cliente)
        db.close()
        return {"estado": "ok", "cliente_id": nuevo_cliente.id}
    except Exception as e:
        return JSONResponse(status_code=500, content={"estado": "error", "mensaje": str(e)})

from domain.schemas import PropiedadInput
from domain.models import PropiedadDB

@app.post("/api/propiedades")
def crear_propiedad(propiedad: PropiedadInput):
    db = SessionLocal()

    nueva_propiedad = PropiedadDB(
        cliente_id=propiedad.cliente_id,
        nombre=propiedad.nombre,
        tipo=propiedad.tipo,
        ubicacion=propiedad.ubicacion
    )

    db.add(nueva_propiedad)
    db.commit()
    db.refresh(nueva_propiedad)
    db.close()

    return {"estado": "ok", "propiedad_id": nueva_propiedad.id}

@app.get("/")
def root():
    return {"status": "Backend activo"}


@app.get("/healthcheck")
def healthcheck():
    db = SessionLocal()
    try:
        count = db.query(TarifaBaseDB).count()
        return JSONResponse(content={"tarifa_base_count": count})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
from domain.models import Tarifa

@app.get("/healthcheck/tarifas")
def healthcheck_tarifas():
    db = SessionLocal()
    try:
        count = db.query(Tarifa).count()
        return JSONResponse(content={"tarifas_count": count})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)    