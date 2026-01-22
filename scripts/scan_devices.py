import asyncio
from bleak import BleakScanner

async def scan():
    print("Iniciando escaneamento de dispositivos Bluetooth")
    print("Aproxime o celular do PC agora")
    print("Aguarde 5 segundos...")
    
    # return_adv=True is required in Bleak 2.0+ to get RSSI
    start_time = asyncio.get_running_loop().time()
    devices = await BleakScanner.discover(timeout=5.0, return_adv=True)
    
    print("\nDispositivos encontrados:")
    print("-" * 50)
    print(f"{'MAC Address':<20} | {'RSSI':<5} | {'Nome'}")
    print("-" * 50)
    
    # Sort by RSSI (strongest signal first, i.e., larger values closer to 0)
    # devices.values() returns (device, advertisement_data) tuples
    sorted_devices = sorted(devices.values(), key=lambda x: x[1].rssi, reverse=True)

    found = False
    for d, adv in sorted_devices:
        name = d.name or "Desconhecido"
        rssi = adv.rssi
        print(f"{d.address:<20} | {rssi:<5} | {name}")
        found = True
        
    if not found:
        print("Nenhum dispositivo encontrado.")
    print("-" * 50)

if __name__ == "__main__":
    asyncio.run(scan())
