import asyncio
from bleak import BleakScanner
import logging

logger = logging.getLogger(__name__)

async def is_device_near(mac_address: str, rssi_threshold: int, service_uuid: str = None) -> bool:
    """
    Verifica se o dispositivo está próximo.
    - Se mac_address for fixo, verifica MAC.
    - Se service_uuid for fornecido, verifica se algum device anuncia esse serviço.
    """
    try:
        # Nota: scan de 3 segundos é um bom equilíbrio
        # Required return_adv=True for Bleak 2.0+
        devices = await BleakScanner.discover(timeout=3.0, return_adv=True)
        
        for d, adv in devices.values():
            found = False
            
            # Checagem por MAC (se não for randomizado ou se coincidir na sorte)
            if mac_address and d.address.upper() == mac_address.upper():
                found = True
            
            # Checagem por UUID de Serviço (Mais robusto para Android/iOS modernos)
            if not found and service_uuid:
                if service_uuid.lower() in [u.lower() for u in adv.service_uuids]:
                    found = True
                    # Atualiza o MAC alvo para logs futuros se necessário? 
                    # Por enquanto apenas detectamos a presença.
            
            if found:
                logger.debug(f"Dispositivo encontrado: {d.address}, RSSI: {adv.rssi}")
                
                if adv.rssi >= rssi_threshold:
                    return True
                else:
                    logger.debug(f"Sinal fraco: {adv.rssi} < {rssi_threshold}")
                    return False
        
        logger.debug(f"Nenhum dispositivo correspondente encontrado no scan.")
        return False
        
    except Exception as e:
        logger.error(f"Erro ao escanear: {e}")
        return False
