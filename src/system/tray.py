import pystray
from PIL import Image, ImageDraw
import logging

logger = logging.getLogger(__name__)

def create_image(width=64, height=64, color1="blue", color2="white"):
    """
    Generates a simple icon image for the system tray (a padlock-like shape).
    """
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    
    # Draw simple shapes to resemble a lock
    dc.ellipse((10, 10, 54, 54), fill=color2)
    dc.rectangle((20, 32, 44, 50), fill=color1)
    
    return image

class SystemTrayApp:
    def __init__(self, stop_callback):
        """
        :param stop_callback: Function to call when 'Exit' is clicked.
        """
        self.stop_callback = stop_callback
        self.icon = None

    def on_quit(self, icon, item):
        """Handles the Exit menu action."""
        logger.info("Exiting via System Tray...")
        icon.stop()
        if self.stop_callback:
            self.stop_callback()

    def run(self):
        """Initializes and runs the System Tray icon (Blocking)."""
        image = create_image()
        menu = pystray.Menu(
            pystray.MenuItem('Auto Lock PC is running', lambda: None, enabled=False),
            pystray.MenuItem('Exit', self.on_quit)
        )

        self.icon = pystray.Icon("AutoLockPC", image, "Auto Lock PC", menu)
        self.icon.run()

    def notify(self, message):
        """Sends a system notification."""
        if self.icon:
            self.icon.notify(message, "Auto Lock PC")
