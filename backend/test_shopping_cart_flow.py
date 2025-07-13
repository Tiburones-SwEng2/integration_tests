import requests
import time

SHOPPING_CART_API_URL = "http://localhost:5003"
MODULE_NAME = "Flujo de Carrito de Compras"

def run_shopping_cart_tests(access_token, user_email, initial_donation_id, report):
    """Prueba el flujo del carrito, registrando y mostrando resultados."""
    print(f"\n--- Ejecutando Pruebas de {MODULE_NAME} ---")
    if not all([access_token, user_email, initial_donation_id]):
        message = "Faltan datos de entrada (token, email o ID de donación)."
        report.add_test_result(MODULE_NAME, "Pruebas de Carrito", "SKIPPED", message)
        print(f"[SKIPPED] {MODULE_NAME}: {message}")
        return

    headers = {'Authorization': f'Bearer {access_token}'}
    cart_item_id = None

    # --- Flujo de Añadir al Carrito ---
    start_time = time.time()
    try:
        payload = {"user_email": user_email, "donation_id": initial_donation_id}
        res = requests.post(f"{SHOPPING_CART_API_URL}/cart", json=payload, headers=headers)
        res.raise_for_status()
        cart_item_id = res.json().get("_id")
        message = "La donación se añadió al carrito."
        duration = time.time() - start_time
        report.add_test_result(MODULE_NAME, "Añadir al Carrito", "PASSED", message, duration)
        print(f"[PASSED] Añadir al Carrito: {message} ({duration:.2f}s)")
    except Exception as e:
        duration = time.time() - start_time
        message = str(e)
        report.add_test_result(MODULE_NAME, "Añadir al Carrito", "FAILED", message, duration)
        print(f"[FAILED] Añadir al Carrito: {message}")
        return

    start_time = time.time()
    try:
        payload = {"user_email": user_email, "donation_id": "ID_FALSO_123"}
        res = requests.post(f"{SHOPPING_CART_API_URL}/cart", json=payload, headers=headers)
        if res.status_code == 404:
            message = "La API rechazó una donación inexistente."
            duration = time.time() - start_time
            report.add_test_result(MODULE_NAME, "Añadir (Error: Donación No Encontrada)", "PASSED", message, duration)
            print(f"[PASSED] Añadir (Error: Donación No Encontrada): {message} ({duration:.2f}s)")
        else:
            raise Exception(f"La API no respondió con 404. Status: {res.status_code}")
    except Exception as e:
        duration = time.time() - start_time
        message = str(e)
        report.add_test_result(MODULE_NAME, "Añadir (Error: Donación No Encontrada)", "FAILED", message, duration)
        print(f"[FAILED] Añadir (Error: Donación No Encontrada): {message}")

    # --- Flujo de Ver Carrito ---
    start_time = time.time()
    try:
        res = requests.get(f"{SHOPPING_CART_API_URL}/cart/{user_email}", headers=headers)
        res.raise_for_status()
        if any(item.get('_id') == cart_item_id for item in res.json()):
            message = "La donación aparece en el carrito del usuario."
            duration = time.time() - start_time
            report.add_test_result(MODULE_NAME, "Ver Carrito", "PASSED", message, duration)
            print(f"[PASSED] Ver Carrito: {message} ({duration:.2f}s)")
        else:
            raise Exception("No se encontró el ítem recién añadido en el carrito.")
    except Exception as e:
        duration = time.time() - start_time
        message = str(e)
        report.add_test_result(MODULE_NAME, "Ver Carrito", "FAILED", message, duration)
        print(f"[FAILED] Ver Carrito: {message}")

    start_time = time.time()
    try:
        res = requests.get(f"{SHOPPING_CART_API_URL}/cart/{user_email}") # Sin headers
        if res.status_code == 401:
            message = "La API denegó el acceso correctamente."
            duration = time.time() - start_time
            report.add_test_result(MODULE_NAME, "Ver Carrito (Error: Sin Token)", "PASSED", message, duration)
            print(f"[PASSED] Ver Carrito (Error: Sin Token): {message} ({duration:.2f}s)")
        else:
            raise Exception(f"La API no respondió con 401. Status: {res.status_code}")
    except Exception as e:
        duration = time.time() - start_time
        message = str(e)
        report.add_test_result(MODULE_NAME, "Ver Carrito (Error: Sin Token)", "FAILED", message, duration)
        print(f"[FAILED] Ver Carrito (Error: Sin Token): {message}")

    # --- Flujo de Reclamar Donación ---
    start_time = time.time()
    try:
        res_claim = requests.post(f"{SHOPPING_CART_API_URL}/cart/{cart_item_id}/claim", headers=headers)
        res_claim.raise_for_status()
        if res_claim.json().get("status") == "claimed":
            message = "El ítem fue reclamado correctamente."
            duration = time.time() - start_time
            report.add_test_result(MODULE_NAME, "Reclamar Donación", "PASSED", message, duration)
            print(f"[PASSED] Reclamar Donación: {message} ({duration:.2f}s)")
        else:
            raise Exception("El estado del ítem no cambió a 'claimed'.")
    except Exception as e:
        duration = time.time() - start_time
        message = str(e)
        report.add_test_result(MODULE_NAME, "Reclamar Donación", "FAILED", message, duration)
        print(f"[FAILED] Reclamar Donación: {message}")

    start_time = time.time()
    try:
        res = requests.post(f"{SHOPPING_CART_API_URL}/cart/{cart_item_id}/claim", headers=headers)
        if res.status_code == 400:
            message = "La API rechazó reclamar un ítem ya procesado."
            duration = time.time() - start_time
            report.add_test_result(MODULE_NAME, "Reclamar Donación (Error: Ya Reclamado)", "PASSED", message, duration)
            print(f"[PASSED] Reclamar Donación (Error: Ya Reclamado): {message} ({duration:.2f}s)")
        else:
            raise Exception(f"La API no respondió con 400. Status: {res.status_code}")
    except Exception as e:
        duration = time.time() - start_time
        message = str(e)
        report.add_test_result(MODULE_NAME, "Reclamar Donación (Error: Ya Reclamado)", "FAILED", message, duration)
        print(f"[FAILED] Reclamar Donación (Error: Ya Reclamado): {message}")

    # --- Flujo de Eliminar del Carrito ---
    start_time = time.time()
    try:
        res = requests.delete(f"{SHOPPING_CART_API_URL}/cart/{cart_item_id}", headers=headers)
        res.raise_for_status()
        message = "El ítem fue eliminado."
        duration = time.time() - start_time
        report.add_test_result(MODULE_NAME, "Eliminar del Carrito", "PASSED", message, duration)
        print(f"[PASSED] Eliminar del Carrito: {message} ({duration:.2f}s)")
    except Exception as e:
        duration = time.time() - start_time
        message = str(e)
        report.add_test_result(MODULE_NAME, "Eliminar del Carrito", "FAILED", message, duration)
        print(f"[FAILED] Eliminar del Carrito: {message}")

    start_time = time.time()
    try:
        res = requests.delete(f"{SHOPPING_CART_API_URL}/cart/{cart_item_id}", headers=headers)
        if res.status_code == 404:
            message = "La API manejó correctamente un ID ya borrado."
            duration = time.time() - start_time
            report.add_test_result(MODULE_NAME, "Eliminar del Carrito (Error: No Encontrado)", "PASSED", message, duration)
            print(f"[PASSED] Eliminar del Carrito (Error: No Encontrado): {message} ({duration:.2f}s)")
        else:
            raise Exception(f"La API no respondió con 404. Status: {res.status_code}")
    except Exception as e:
        duration = time.time() - start_time
        message = str(e)
        report.add_test_result(MODULE_NAME, "Eliminar del Carrito (Error: No Encontrado)", "FAILED", message, duration)
        print(f"[FAILED] Eliminar del Carrito (Error: No Encontrado): {message}")