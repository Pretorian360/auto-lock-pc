import asyncio
from bleak import BleakScanner

async def scan_details():
    print("Iniciando escaneamento DETALHADO...")
    print("Aproxime o celular do PC agora (RSSI > -50).")
    print("Aguardando 5 segundos...\n")

    # return_adv=True traz os dados de propaganda (AdvertisementData)
    devices = await BleakScanner.discover(timeout=5.0, return_adv=True)

    # Ordena por sinal (mais forte primeiro)
    sorted_devices = sorted(devices.values(), key=lambda x: x[1].rssi, reverse=True)

    count = 0
    for d, adv in sorted_devices:
        # Exibe apenas os top 3 mais fortes para não poluir
        if count >= 3:
            break
        
        print(f"📍 DISPOSITIVO: {d.address}")
        print(f"Nome: {d.name or adv.local_name or 'Desconhecido'}")
        print(f"RSSI: {adv.rssi}")
        print(f"Serviços (UUIDs): {adv.service_uuids}")
        print(f"Manufacturer Data: {adv.manufacturer_data}")
        print("-" * 40)
        count += 1

    if count == 0:
        print("Nenhum dispositivo encontrado.")

if __name__ == "__main__":
    asyncio.run(scan_details())
