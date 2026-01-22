import logging
import time

# Imports relativos podem ser complexos dependendo de como main é executado.
# Assumindo execução como módulo ou ajustando sys.path.
# Interfaces injetadas evitam acoplamento forte aqui.

logger = logging.getLogger(__name__)

class ProximityMonitor:
    def __init__(self, scanner_func, locker_func, waker_func, config):
        """
        :param scanner_func: async function(mac, rssi_limit) -> bool
        :param locker_func: function() -> void
        :param waker_func: function() -> void
        :param config: dict with keys 'phone_mac', 'rssi_threshold', 'max_misses'
        """
        self.scanner = scanner_func
        self.locker = locker_func
        self.waker = waker_func
        self.config = config
        
        self.missed_scans = 0
        self.is_locked = False
        
        # Carrega configs
        self.mac = config.get("phone_mac")
        self.service_uuid = config.get("service_uuid") # Novo campo opcional
        self.threshold = config.get("rssi_threshold", -85)
        self.max_misses = config.get("max_misses", 3)

    async def run_check(self):
        """Executa uma verificação de ciclo único."""
        # Se não tiver nem MAC nem UUID configurado, avisa
        if (not self.mac or self.mac == "AA:BB:CC:DD:EE:FF") and not self.service_uuid:
            logger.warning("Nenhum Alvo configurado (MAC ou UUID). Verifique settings.json")
            return

        is_near = await self.scanner(self.mac, self.threshold, self.service_uuid)

        if is_near:
            self.missed_scans = 0
            if self.is_locked:
                logger.info("Dispositivo detectado. Desbloqueando (lógica de wake)...")
                self.waker()
                self.is_locked = False
            else:
                logger.debug("Dispositivo próximo. Mantendo desbloqueado.")
        else:
            self.missed_scans += 1
            logger.info(f"Dispositivo longe/ausente. Tentativa {self.missed_scans}/{self.max_misses}")

            if self.missed_scans >= self.max_misses and not self.is_locked:
                logger.info("Limite de ausência atingido. Bloqueando PC.")
                self.locker()
                self.is_locked = True
