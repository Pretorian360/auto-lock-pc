import asyncio
from bleak import BleakScanner
import logging

logger = logging.getLogger(__name__)

async def is_device_near(mac_address: str, rssi_threshold: int, service_uuid: str = None) -> bool:
    """
    Checks if the target device is near based on RSSI threshold.
    
    :param mac_address: Target MAC address to check.
    :param rssi_threshold: Minimum RSSI value to consider "near".
    :param service_uuid: Optional Service UUID to check for (useful for modern Android/iOS).
    :return: True if device is found and signal >= threshold, else False.
    """
    try:
        # Scan for 3 seconds to gather advertisements
        devices = await BleakScanner.discover(timeout=3.0, return_adv=True)
        
        for d, adv in devices.values():
            found = False
            
            # Check by MAC address
            if mac_address and d.address.upper() == mac_address.upper():
                found = True
            
            # Check by Service UUID (More robust for randomized MACs)
            if not found and service_uuid:
                # adv.service_uuids uses standard normalization, but safe to lower() just in case
                advertised_uuids = [u.lower() for u in adv.service_uuids]
                if service_uuid.lower() in advertised_uuids:
                    found = True
            
            if found:
                logger.debug(f"Device found: {d.address}, RSSI: {adv.rssi}")
                
                if adv.rssi >= rssi_threshold:
                    return True
                else:
                    logger.debug(f"Signal weak: {adv.rssi} < {rssi_threshold}")
                    return False
        
        logger.debug("No matching device found in scan.")
        return False
        
    except Exception as e:
        logger.error(f"Error checking device proximity: {e}")
        return False
