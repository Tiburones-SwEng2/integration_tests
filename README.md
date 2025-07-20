# Pruebas de Integración - Proyecto Donatello

Este directorio contiene la suite de pruebas de integración para el proyecto Donatello. El objetivo de estas pruebas es verificar que los diferentes componentes del sistema (APIs, interfaz de usuario, flujos de datos, etc.) funcionan correctamente en conjunto.

## Requisitos Previos

Antes de ejecutar las pruebas, asegúrate de tener los servicios del backend y frontend corriendo y accesibles. Además, necesitas instalar las dependencias de Python para esta suite.

1.  **Navega a este directorio:**
    ```bash
    cd integration_tests
    ```

2.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

## Estructura de las Pruebas

Las pruebas están organizadas por componentes y flujos funcionales.

-   `backend/`: Contiene las pruebas que interactúan directamente con las APIs del backend.
    -   `main_backend_tests.py`: Orquestador principal que ejecuta todas las pruebas del backend.
    -   `test_user_flow.py`: Pruebas para registro, login y gestión de perfil.
    -   `test_donation_flow.py`: Pruebas para la creación y consulta de donaciones.
    -   `test_notification_flow.py`: Pruebas para el sistema de notificaciones.
    -   `test_shopping_cart_flow.py`: Pruebas para la gestión del carrito de compras.
-   `frontend/`: Contiene las pruebas de interfaz de usuario que simulan la interacción en el navegador.
    -   `frontend_tests.py`: Script principal que ejecuta todas las pruebas de Selenium para el frontend.
-   `reporting/`: Módulos para la generación de reportes.
    -   `pdf_generator.py`: Clase que genera un reporte PDF con los resultados de las pruebas.

## Cómo Ejecutar las Pruebas

Las pruebas para el backend y el frontend se ejecutan por separado.

### Pruebas del Backend

Para ejecutar la suite completa de pruebas de integración del backend, utiliza el siguiente comando desde el directorio `integration_tests/backend`:

```bash
python main_backend_tests.py
```

### Pruebas del Frontend

**Importante:** Antes de ejecutar, asegúrate de que la aplicación de frontend esté corriendo en `http://localhost:5173`.

Para ejecutar la suite de pruebas de Selenium para el frontend, utiliza el siguiente comando desde el directorio `integration_tests/frontend`:

```bash
python frontend_tests.py
```

## Generación de Reportes

Al finalizar la ejecución de **cada suite**, se generará automáticamente un reporte en formato PDF en la carpeta correspondiente:

-   **Reporte de Backend:** `integration_tests/backend/reports/`
-   **Reporte de Frontend:** `integration_tests/frontend/reports/`

El reporte incluye:
-   Un resumen del estado de las pruebas (Pasadas, Fallidas).
-   Tablas detalladas con los resultados de cada paso por módulo.
-   Gráficos visuales sobre la distribución de resultados y los tiempos de ejecución.