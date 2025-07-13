# Pruebas de Integración - Proyecto Donatello

Este directorio contiene la suite de pruebas de integración para el proyecto Donatello. El objetivo de estas pruebas es verificar que los diferentes componentes del sistema (APIs, flujos de datos, etc.) funcionan correctamente en conjunto.

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

Las pruebas están organizadas por flujos funcionales para simular interacciones de un usuario real con el sistema.

-   `backend/`: Contiene las pruebas que interactúan directamente con las APIs del backend.
    -   `test_user_flow.py`: Pruebas para registro, login y gestión de perfil.
    -   `test_donation_flow.py`: Pruebas para la creación y consulta de donaciones.
    -   `test_notification_flow.py`: Pruebas para el sistema de notificaciones.
    -   `test_shopping_cart_flow.py`: Pruebas para la gestión del carrito de compras.
-   `reporting/`: Módulos para la generación de reportes.
    -   `pdf_generator.py`: Clase que genera un reporte PDF con los resultados de las pruebas.

## Cómo Ejecutar las Pruebas

Para ejecutar la suite completa de pruebas de integración del backend, utiliza el siguiente comando desde el directorio `integration_tests/backend`:

```bash
python main_backend_tests.py
```

## Generación de Reportes

Al finalizar la ejecución de la suite, se generará automáticamente un reporte en formato PDF en la carpeta `integration_tests/backend/reports/`.

El reporte incluye:
-   Un resumen del estado de las pruebas (Pasadas, Fallidas).
-   Tablas detalladas con los resultados de cada paso por módulo.
-   Gráficos visuales sobre la distribución de resultados y los tiempos de ejecución.