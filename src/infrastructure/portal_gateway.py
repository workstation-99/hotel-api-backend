# -*- coding: utf-8 -*-
"""
Created on Thu Sep  4 10:28:04 2025

@author: backy
"""

class PortalGateway:
    def enviar_tarifa(self, tarifa):
        print("Enviando tarifa al portal...")
        print(tarifa.dict())
        return {"estado": "ok", "mensaje": "Tarifa enviada correctamente"}
