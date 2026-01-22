import asyncio
import json
import logging
import os
import sys
import threading
import time

# Configura logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger("Main")

# Garante que imports funcionem (adiciona diretório atual ao path se necessário)
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    from bluetooth.scanner import is_device_near
    from system.windows import lock_workstation, wake_screen
    from system.tray import SystemTrayApp
    from core.monitor import ProximityMonitor
except ImportError as e:
    logger.critical(f"Erro de importação: {e}. Verifique se está executando o script corretamente.")
    sys.exit(1)

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'settings.json')

# Global flag for stopping the background thread
STOP_EVENT = threading.Event()

def load_config():
    try:
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Arquivo de configuração não encontrado em: {CONFIG_PATH}")
        return None
    except json.JSONDecodeError:
        logger.error("Erro ao decodificar settings.json")
        return None

async def monitor_task(monitor, interval):
    logger.info("Monitoramento iniciado (Background).")
    try:
        while not STOP_EVENT.is_set():
            await monitor.run_check()
            # Wait with check for quick exit
            for _ in range(interval * 2): # Check every 0.5s
                if STOP_EVENT.is_set():
                    break
                await asyncio.sleep(0.5)
    except asyncio.CancelledError:
        logger.info("Monitoramento cancelado.")
    except Exception as e:
        logger.error(f"Erro fatal no loop de monitoramento: {e}")
    finally:
        logger.info("Monitoramento encerrado.")

def run_asyncio_loop(loop, monitor, interval):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(monitor_task(monitor, interval))
    loop.close()

def main():
    logger.info("Iniciando Proximity Lock com System Tray...")
    
    config = load_config()
    if not config:
        logger.error("Falha ao carregar configuração. Encerrando.")
        return

    # Injeção de dependências
    monitor = ProximityMonitor(
        scanner_func=is_device_near,
        locker_func=lock_workstation,
        waker_func=wake_screen,
        config=config
    )
    
    interval = config.get("scan_interval", 5)

    # Prepare background thread for asyncio
    loop = asyncio.new_event_loop()
    monitor_thread = threading.Thread(
        target=run_asyncio_loop, 
        args=(loop, monitor, interval),
        daemon=True
    )
    
    # Callback to stop application from Tray
    def on_stop():
        logger.info("Sinal de parada recebido do Tray.")
        STOP_EVENT.set()
        # Wait a bit for thread logic if needed, but daemon kills fine usually
        # monitor_thread.join(timeout=2) 
        sys.exit(0)

    # Start Monitor
    monitor_thread.start()

    # Start Tray (Main Thread - Blocking)
    app = SystemTrayApp(stop_callback=on_stop)
    app.notify("Auto Lock iniciado e monitorando!") # Notification on start
    app.run()

if __name__ == "__main__":
    main()
