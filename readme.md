# Proximity Lock PC

Este projeto bloqueia automaticamente o seu PC Windows quando o seu dispositivo Bluetooth (celular) se afasta, e mantém a tela ativa quando você está por perto.
Pode ser usado com outros dispositivos Bluetooth, como pulseiras inteligentes, smartwatches, etc.

## 📋 Estrutura do Projeto

- `config/settings.json`: Configurações de MAC, RSSI e intervalos.
- `scripts/scan_details.py`: Utilitário para descobrir UUIDs de serviços (mais estável que MAC).
- `scripts/install_startup.ps1`: Script para configurar inicialização automática com o Windows.
- `src/`: Código fonte principal.
  - `bluetooth/`: Lógica de scanner BLE.
  - `system/`: Interações com o Windows (Lock, Wake + Space).
  - `system/tray.py`: Ícone de bandeja do sistema.
  - `core/`: Lógica de monitoramento.
  - `main.py`: Ponto de entrada com suporte a Tray e Multithreading.

## 🚀 Como Usar

### 1. Instalação

Crie um ambiente virtual e instale as dependências:

```bash
py -m venv win_lock_env
.\win_lock_env\Scripts\activate
pip install -r requirements.txt

### 2. Configuração (Recomendado: Via UUID)

Devido à privacidade do Bluetooth (MAC Randomization), recomenda-se usar o UUID de Serviço:
Importante: Crie a o arquivo config/settings.json como no exemplo abaixo:

1. Aproxime o celular do PC. Nem sempre o nome do dispositivo aparece, por isso a importancia de colocado o mais próximo do PC.
2. Rode `python scripts/scan_details.py`.
3. Copie o UUID encontrado (ex: `00005246...`) no `config/settings.json`.
4. Quanto mais positivo o RSSI exemplo (-67 > -40) mais próximo está seu dispositivo.

```json
{
    "phone_mac": "",
    "service_uuid": "SEU_UUID_AQUI",
    "scan_interval": 5,
    "max_misses": 2,
    "rssi_threshold": -85
}
```

| Parâmetro | Descrição |
| :--- | :--- |
| `phone_mac` | Endereço MAC do dispositivo. (Opcional se usar UUID, pois muitos celulares mudam o MAC aleatoriamente). |
| `service_uuid` | Identificador único do serviço BLE. Recomendado para Android/iOS modernos. |
| `scan_interval` | Intervalo em segundos entre cada varredura Bluetooth. |
| `max_misses` | Número de falhas consecutivas permitidas antes de bloquear o PC (tolerância contra falhas momentâneas). |
| `rssi_threshold` | Limite de sinal (em dBm). Se o sinal for menor que isso (ex: -95), considera-se que você está longe. Valores mais próximos de 0 indicam maior proximidade. |

### 3. Execução

**Modo Manual:**
```bash
python src/main.py
```

**Modo Background (System Tray):**
O ícone aparecerá na bandeja do sistema (Icone azul).

### 4. Inicialização Automática

Para que o programa inicie junto com o Windows (silenciosamente):

```powershell
.\scripts\install_startup.ps1
```

## 🛠️ Tecnologias

- **Python 3.10+**
- **Bleak**: Scanner Bluetooth Low Energy.
- **Pystray**: Ícone de bandeja do sistema.
- **PyWin32 / Ctypes**: Interação nativa (LockWorkStation, SendInput).

## ⚠️ Limitações Conhecidas

- A precisão do RSSI pode variar conforme o ambiente.
- Interferências Bluetooth podem causar falsos positivos raros.
- Não funciona durante hibernação/sleep profundo.

Diagrama simples do funcionamento:
[ Smartphone ]
      ↓ BLE
[ Scanner ]
      ↓
[ Monitor ]
      ↓
[ Windows Lock / Wake ]
