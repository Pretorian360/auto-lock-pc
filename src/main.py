import asyncio
import json
import logging
import os
import sys
import threading
import time

# Configures basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger("Main")

# Ensure proper path for imports if run directly
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    from bluetooth.scanner import is_device_near
    from system.windows import lock_workstation, wake_screen
    from system.tray import SystemTrayApp
    from core.monitor import ProximityMonitor
except ImportError as e:
    logger.critical(f"Import error: {e}. Ensure you are running from the correct directory.")
    sys.exit(1)

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'settings.json')
STOP_EVENT = threading.Event()

def load_config():
    """Validates and loads the configuration from JSON file."""
    try:
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Config file not found at: {CONFIG_PATH}")
        return None
    except json.JSONDecodeError:
        logger.error("Error decoding settings.json")
        return None

async def monitor_task(monitor, interval):
    """
    Main monitoring loop. 
    Runs the check logic and handles graceful shutdown via STOP_EVENT.
    """
    logger.info("Monitoring started.")
    try:
        while not STOP_EVENT.is_set():
            await monitor.run_check()
            
            # Smart sleep: check STOP_EVENT frequently during the interval
            for _ in range(interval * 2): # Check every 0.5s
                if STOP_EVENT.is_set():
                    break
                await asyncio.sleep(0.5)
                
    except asyncio.CancelledError:
        logger.info("Monitoring cancelled.")
    except Exception as e:
        logger.error(f"Fatal error in monitoring loop: {e}")
    finally:
        logger.info("Monitoring stopped.")

def run_asyncio_loop(loop, monitor, interval):
    """Entry point for the background thread running the asyncio loop."""
    asyncio.set_event_loop(loop)
    loop.run_until_complete(monitor_task(monitor, interval))
    loop.close()

def main():
    """Main application entry point."""
    logger.info("Starting Proximity Lock with System Tray...")
    
    config = load_config()
    if not config:
        logger.error("Failed to load config. Exiting.")
        return

    # Dependency Injection
    monitor = ProximityMonitor(
        scanner_func=is_device_near,
        locker_func=lock_workstation,
        waker_func=wake_screen,
        config=config
    )
    
    interval = config.get("scan_interval", 5)

    # Setup background thread for monitoring
    loop = asyncio.new_event_loop()
    monitor_thread = threading.Thread(
        target=run_asyncio_loop, 
        args=(loop, monitor, interval),
        daemon=True
    )
    
    def on_stop():
        """Callback to stop application from Tray."""
        logger.info("Stop signal received from Tray.")
        STOP_EVENT.set()
        sys.exit(0)

    # Start Monitor
    monitor_thread.start()

    # Start Tray (Main Thread - Blocking)
    app = SystemTrayApp(stop_callback=on_stop)
    app.notify("Auto Lock started and monitoring!")
    app.run()

if __name__ == "__main__":
    main()
