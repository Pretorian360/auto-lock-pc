import ctypes
import logging

logger = logging.getLogger(__name__)

def lock_workstation():
    """
    Locks the Windows workstation.
    Equivalent to pressing Win+L.
    """
    logger.info("Locking workstation...")
    try:
        ctypes.windll.user32.LockWorkStation()
        return True
    except Exception as e:
        logger.error(f"Failed to lock: {e}")
        return False

def wake_screen():
    """
    Simulates minimal user activity to wake the screen or prevent sleep.
    Sends an imperceptible mouse move followed by a key press/release.
    """
    logger.debug("Sending wake/keep-awake signal...")
    try:
        # 1. Wake monitor (Imperceptible mouse move)
        ctypes.windll.user32.mouse_event(0x0001, 1, 0, 0, 0)
        
        # 2. Show password field (Press/Release SPACE)
        # 0x20 = VK_SPACE
        ctypes.windll.user32.keybd_event(0x20, 0, 0, 0) # Press Space
        ctypes.windll.user32.keybd_event(0x20, 0, 2, 0) # Release Space
        
        return True
    except Exception as e:
        logger.error(f"Failed to wake screen: {e}")
        return False
