import pystray
from PIL import Image, ImageDraw
import threading
import sys
import os
import logging

logger = logging.getLogger(__name__)

def create_image(width=64, height=64, color1="blue", color2="white"):
    # Generate an icon with a padlock shape or similar
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    
    # Draw a simple circle/padlock
    dc.ellipse((10, 10, 54, 54), fill=color2)
    dc.rectangle((20, 32, 44, 50), fill=color1)
    
    return image

class SystemTrayApp:
    def __init__(self, stop_callback):
        self.stop_callback = stop_callback
        self.icon = None

    def on_quit(self, icon, item):
        logger.info("Encerrando via System Tray...")
        icon.stop()
        if self.stop_callback:
            self.stop_callback()

    def run(self):
        image = create_image()
        menu = pystray.Menu(
            pystray.MenuItem('Auto Lock PC está rodando', lambda: None, enabled=False),
            pystray.MenuItem('Sair', self.on_quit)
        )

        self.icon = pystray.Icon("AutoLockPC", image, "Auto Lock PC", menu)
        self.icon.run()

    def notify(self, message):
        if self.icon:
            self.icon.notify(message, "Auto Lock PC")
