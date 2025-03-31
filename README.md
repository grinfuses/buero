# BUERO Cryptocurrency

BUERO es una criptomoneda educativa implementada en Python que demuestra los conceptos básicos de blockchain y criptomonedas.

## Características

- ✨ Interfaz web moderna y fácil de usar
- 💰 Creación y gestión de múltiples carteras
- 💸 Envío de transacciones entre carteras
- ⛏️ Minado de bloques con recompensas
- 📊 Historial completo de transacciones
- 🔒 Criptografía segura para carteras
- 🌐 Interfaz web accesible desde cualquier navegador

## Requisitos

- Python 3.10 o superior
- pip (gestor de paquetes de Python)

## Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/grinfuses/buero.git
cd buero
```

2. Instala el paquete en modo desarrollo:
```bash
pip3 install -e .
```

## Uso

1. Inicia la aplicación:
```bash
PYTHONPATH=src python3 -m buero.wallet.web_interface
```

2. Abre tu navegador y visita:
```
http://127.0.0.1:1988
```

## Funcionalidades

### Gestión de Carteras

- **Crear Nueva Cartera**: Haz clic en el botón "Nueva Cartera" para crear una cartera adicional.
- **Seleccionar Cartera**: Usa el selector de carteras para cambiar entre tus diferentes carteras.
- **Ver Balance**: El balance de la cartera seleccionada se muestra en tiempo real.

### Transacciones

- **Enviar BUERO**: 
  1. Ingresa la dirección de la cartera destinataria
  2. Especifica la cantidad de BUERO a enviar
  3. Haz clic en "Enviar"

### Minado

- **Minar Bloques**: 
  1. Haz clic en el botón "Minar Bloque"
  2. Recibirás 10 BUERO como recompensa por cada bloque minado
  3. Las recompensas se añaden automáticamente a tu cartera actual

### Historial de Transacciones

- Visualiza todas las transacciones en la cadena
- Las transacciones se organizan por bloques
- Muestra:
  - Número de bloque
  - Monto de la transacción
  - Dirección de origen y destino
  - Recompensas de minado

## Estructura del Proyecto

```
src/buero/
├── blockchain/          # Implementación del blockchain
│   ├── blockchain.py   # Lógica principal del blockchain
│   └── __init__.py
├── wallet/             # Gestión de carteras
│   ├── wallet.py       # Implementación de carteras
│   ├── wallet_manager.py # Gestión de múltiples carteras
│   ├── web_interface.py # Interfaz web Flask
│   └── templates/      # Plantillas HTML
│       └── index.html  # Interfaz de usuario
├── utils/             # Utilidades
│   └── crypto.py      # Funciones criptográficas
└── __init__.py
```

## Aspectos Técnicos

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Almacenamiento**: Sistema de archivos local para carteras
- **Criptografía**: ECDSA para firmas digitales
- **Consenso**: Proof of Work (PoW)
- **Dificultad de Minado**: 4 ceros iniciales

## Seguridad

- Las claves privadas se almacenan localmente
- Cada cartera tiene su propia dirección única
- Las transacciones son verificadas antes de ser añadidas al blockchain
- Sistema de sesiones para gestionar múltiples carteras

## Limitaciones

- Proyecto educativo, no usar en producción
- No implementa red P2P
- Almacenamiento local de carteras
- Sin persistencia del blockchain entre reinicios

## Contribuir

Las contribuciones son bienvenidas. Por favor, abre un issue para discutir los cambios propuestos.

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.
