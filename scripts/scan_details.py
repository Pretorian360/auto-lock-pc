import asyncio
from bleak import BleakScanner

async def scan_details():
    """
    Scans for BLE devices and prints detailed information for the top 3 strongest signals.
    Useful for debugging and finding Service UUIDs.
    """
    print("Starting Detailed Scan...")
    print("Bring your device close to the PC.")
    print("Scanning for 5 seconds...\n")

    # return_adv=True retrieves AdvertisementData
    devices = await BleakScanner.discover(timeout=5.0, return_adv=True)

    # Sort by signal strength (strongest first)
    sorted_devices = sorted(devices.values(), key=lambda x: x[1].rssi, reverse=True)

    count = 0
    for d, adv in sorted_devices:
        # Show only top 3 to avoid clutter
        if count >= 3:
            break
        
        print(f"📍 DEVICE: {d.address}")
        print(f"Name: {d.name or adv.local_name or 'Unknown'}")
        print(f"RSSI: {adv.rssi}")
        print(f"Services (UUIDs): {adv.service_uuids}")
        print(f"Manufacturer Data: {adv.manufacturer_data}")
        print("-" * 40)
        count += 1

    if count == 0:
        print("No devices found.")

if __name__ == "__main__":
    asyncio.run(scan_details())
