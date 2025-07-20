import requests
import time

NOTIFICATION_API_URL = "http://localhost:5001"
MODULE_NAME = "Flujo de Notificación"

def run_notification_tests(access_token, donation_id, report):
    """Prueba el flujo de notificaciones, registrando y mostrando resultados."""
    print(f"\n--- Ejecutando Pruebas de {MODULE_NAME} ---")
    if not all([access_token, donation_id]):
        message = "Faltan datos (token o donation_id)."
        report.add_test_result(MODULE_NAME, "Prueba de Notificaciones", "SKIPPED", message)
        print(f"[SKIPPED] {MODULE_NAME}: {message}")
        return

    headers = {'Authorization': f'Bearer {access_token}'}

    # Prueba de filtrado de donaciones
    start_time = time.time()
    try:
        res = requests.get(f"{NOTIFICATION_API_URL}/filteredDonations?city=Bogotá", headers=headers)
        res.raise_for_status()
        donations = res.json()
        if any(d.get("id") == donation_id for d in donations):
            message = "La donación es visible."
            duration = time.time() - start_time
            report.add_test_result(MODULE_NAME, "Filtrar Donaciones", "PASSED", message, duration)
            print(f"[PASSED] Filtrar Donaciones: {message} ({duration:.2f}s)")
        else:
            raise Exception("La donación creada no fue encontrada.")
    except Exception as e:
        duration = time.time() - start_time
        message = str(e)
        report.add_test_result(MODULE_NAME, "Filtrar Donaciones", "FAILED", message, duration)
        print(f"[FAILED] Filtrar Donaciones: {message}")

    # Prueba de filtrado de donaciones sin token
    start_time = time.time()
    try:
        res = requests.get(f"{NOTIFICATION_API_URL}/filteredDonations?city=Bogotá") # Sin headers
        if res.status_code == 401:
            message = "La API denegó el acceso correctamente."
            duration = time.time() - start_time
            report.add_test_result(MODULE_NAME, "Filtrar (Error: Sin Token)", "PASSED", message, duration)
            print(f"[PASSED] Filtrar (Error: Sin Token): {message} ({duration:.2f}s)")
        else:
            raise Exception(f"La API no respondió con 401. Status: {res.status_code}")
    except Exception as e:
        duration = time.time() - start_time
        message = str(e)
        report.add_test_result(MODULE_NAME, "Filtrar (Error: Sin Token)", "FAILED", message, duration)
        print(f"[FAILED] Filtrar (Error: Sin Token): {message}")

    # Prueba de envío de notificación
    start_time = time.time()
    try:
        payload = {"email": "beneficiary@test.com", "id": donation_id, "description": "Laptop Antigua"}
        res = requests.post(f"{NOTIFICATION_API_URL}/sendNotification", json=payload, headers=headers)
        res.raise_for_status()
        message = "La API procesó el envío."
        duration = time.time() - start_time
        report.add_test_result(MODULE_NAME, "Envío Notificación", "PASSED", message, duration)
        print(f"[PASSED] Envío Notificación: {message} ({duration:.2f}s)")
    except Exception as e:
        duration = time.time() - start_time
        message = str(e)
        report.add_test_result(MODULE_NAME, "Envío Notificación", "FAILED", message, duration)
        print(f"[FAILED] Envío Notificación: {message}")