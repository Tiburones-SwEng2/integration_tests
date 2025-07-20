import sys
import os
import requests

# Añadir rutas para importar módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importar los módulos de prueba y el generador de reportes
from test_user_flow import run_user_tests
from test_donation_flow import run_donation_tests, create_test_donation_form, DONATION_API_URL
from test_shopping_cart_flow import run_shopping_cart_tests
from test_notification_flow import run_notification_tests
from reporting.pdf_generator import PDFReportGenerator

def create_new_donation(access_token, purpose, report):
    """Función helper para crear una nueva donación para una prueba."""
    if not access_token:
        message = "No se puede crear donación: Falta token."
        report.add_test_result(f"Crear Donación para '{purpose}'", "FATAL", message)
        print(f"[FATAL] Crear Donación para '{purpose}': {message}")
        return None
    
    headers = {'Authorization': f'Bearer {access_token}'}
    try:
        form_data, image_file = create_test_donation_form()
        res = requests.post(f"{DONATION_API_URL}/api/donations", data=form_data, files={'image': image_file}, headers=headers)
        res.raise_for_status()
        donation_id = res.json().get("_id")
        message = f"Donación creada con ID: {donation_id}"
        print(f"\n[SETUP] {message}")
        return donation_id
    except Exception as e:
        message = f"No se pudo crear la donación: {e}"
        print(f"[FATAL] Crear Donación para '{purpose}': {message}")
        return None

def main():
    """Ejecuta la suite completa de pruebas de integración del back-end y genera un reporte."""
    print("🚀 Iniciando Suite de Pruebas de Integración del Back-End 🚀")
    
    report = PDFReportGenerator(
        "Reporte de Pruebas de Integración - Backend",
        report_type="backend"
    )

    access_token = None
    user_email = None

    try:
        # --- Flujo de Usuario ---
        access_token, user_email = run_user_tests(report)
        
        # --- Flujo de Donación ---
        run_donation_tests(access_token, report)

        # --- Flujo de Notificación ---
        donation_id_for_notification = create_new_donation(access_token, "Notificaciones", report)
        run_notification_tests(access_token, donation_id_for_notification, report)

        # --- Flujo de Carrito de Compras ---
        donation_id_for_cart = create_new_donation(access_token, "Carrito", report)
        run_shopping_cart_tests(access_token, user_email, donation_id_for_cart, report)

    except Exception as e:
        error_message = f"Error no controlado detuvo la suite: {e}"
        report.add_test_result("Ejecución General", "FATAL", error_message)
        print(f"\n[FATAL] {error_message}")
    finally:
        print("\n--- Generando Reporte PDF ---")
        report.generate("d:/01_Actuales/unal/Donnatello/integration_tests/backend/reports")
        print("\n✅ Suite de pruebas de Back-End finalizada.")

if __name__ == "__main__":
    main()