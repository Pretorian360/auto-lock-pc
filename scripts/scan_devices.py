import asyncio
from bleak import BleakScanner

async def scan():
    """
    Performs a standard BLE scan and lists all found devices.
    Displays MAC Address, RSSI, and Name in a tabular format.
    """
    print("Starting Bluetooth Device Scan...")
    print("Make sure your device is discoverable.")
    print("Scanning for 5 seconds...")
    
    # return_adv=True is required in Bleak 2.0+ to get RSSI
    devices = await BleakScanner.discover(timeout=5.0, return_adv=True)
    
    print("\nDevices Found:")
    print("-" * 50)
    print(f"{'MAC Address':<20} | {'RSSI':<5} | {'Name'}")
    print("-" * 50)
    
    # Sort by RSSI (strongest signal first)
    sorted_devices = sorted(devices.values(), key=lambda x: x[1].rssi, reverse=True)

    found = False
    for d, adv in sorted_devices:
        name = d.name or "Unknown"
        rssi = adv.rssi
        print(f"{d.address:<20} | {rssi:<5} | {name}")
        found = True
        
    if not found:
        print("No devices found.")
    print("-" * 50)

if __name__ == "__main__":
    asyncio.run(scan())
