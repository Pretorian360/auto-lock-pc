import logging
import time

logger = logging.getLogger(__name__)

class ProximityMonitor:
    """
    Manages the logic for locking/unlocking based on proximity.
    Orchestrates the scanner and system actions (lock/wake).
    """

    def __init__(self, scanner_func, locker_func, waker_func, config):
        """
        Initialize the monitor with dependencies and configuration.

        :param scanner_func: Async function to detect device presence.
        :param locker_func: Function to lock the workstation.
        :param waker_func: Function to wake the screen.
        :param config: Dictionary containing 'phone_mac', 'rssi_threshold', etc.
        """
        self.scanner = scanner_func
        self.locker = locker_func
        self.waker = waker_func
        self.config = config
        
        self.missed_scans = 0
        self.is_locked = False
        
        # Load configuration values
        self.mac = config.get("phone_mac")
        self.service_uuid = config.get("service_uuid")
        self.threshold = config.get("rssi_threshold", -80)
        self.max_misses = config.get("max_misses", 2)

    async def run_check(self):
        """
        Executes a single check cycle.
        Scans for the device and locks/unlocks the PC based on presence and state.
        """
        # Validate configuration
        if (not self.mac or self.mac == "AA:BB:CC:DD:EE:FF") and not self.service_uuid:
            logger.warning("No target configured (MAC or UUID). Check settings.json")
            return

        # Perform scan
        is_near = await self.scanner(self.mac, self.threshold, self.service_uuid)

        if is_near:
            self.missed_scans = 0
            if self.is_locked:
                logger.info("Device detected. Unlocking/Waking...")
                self.waker()
                self.is_locked = False
            else:
                logger.debug("Device near. Keeping unlocked.")
        else:
            self.missed_scans += 1
            logger.info(f"Device absent. Attempt {self.missed_scans}/{self.max_misses}")

            # Lock if max misses reached and not already locked
            if self.missed_scans >= self.max_misses and not self.is_locked:
                logger.info("Absence limit reached. Locking PC.")
                self.locker()
                self.is_locked = True
