import ctypes
import logging

logger = logging.getLogger(__name__)

def lock_workstation():
    """Bloqueia a estação de trabalho Windows."""
    logger.info("Bloqueando a estação de trabalho...")
    try:
        ctypes.windll.user32.LockWorkStation()
        return True
    except Exception as e:
        logger.error(f"Falha ao bloquear: {e}")
        return False

def wake_screen():
    """
    Simula uma pequena atividade para acordar a tela ou impedir hibernação.
    Envia um input de 'mouse move' imperceptível.
    """
    logger.debug("Enviando sinal de wake/keep-awake...")
    try:
        # 1. Acorda o monitor (Mouse move imperceptível)
        ctypes.windll.user32.mouse_event(0x0001, 1, 0, 0, 0)
        
        # 2. Mostra o campo de senha (Pressiona ESPAÇO)
        # 0x20 = VK_SPACE
        # 0 = Press
        # 2 = Release
        ctypes.windll.user32.keybd_event(0x20, 0, 0, 0) # Press Space
        ctypes.windll.user32.keybd_event(0x20, 0, 2, 0) # Release Space
        
        return True
    except Exception as e:
        logger.error(f"Falha ao acordar tela: {e}")
        return False
