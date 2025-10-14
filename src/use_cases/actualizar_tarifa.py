# -*- coding: utf-8 -*-
"""
Created on Thu Sep  4 10:27:20 2025

@author: backy
"""

from domain.models import Tarifa
from infrastructure.tarifa_repository import TarifaRepository
from infrastructure.portal_gateway import PortalGateway

class ActualizarTarifaUseCase:
    def __init__(self, repository: TarifaRepository, gateway: PortalGateway):
        self.repository = repository
        self.gateway = gateway

    def ejecutar(self, tarifa: Tarifa):
        self.repository.guardar(tarifa)
        resultado = self.gateway.enviar_tarifa(tarifa)
        return resultado
