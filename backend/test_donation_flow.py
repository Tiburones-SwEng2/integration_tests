import requests
import uuid
import time

DONATION_API_URL = "http://localhost:5000"
MODULE_NAME = "Flujo de Donación"

def create_test_donation_form():
    """Crea datos de formulario y un archivo de imagen simulado para las pruebas."""
    unique_id = uuid.uuid4()
    form_data = {
        'title': f'Laptop Antigua {unique_id}',
        'name': f'Laptop Antigua {unique_id}',
        'description': 'Una laptop funcional pero antigua.',
        'city': 'Bogotá',
        'address': 'Calle Falsa 123',
        'category': 'Tecnología',
        'condition': 'Usado'
    }
    image_file = ('image.jpg', b'fake-image-data', 'image/jpeg')
    return form_data, image_file

def run_donation_tests(access_token, report):
    """Prueba el flujo de donaciones, registrando y mostrando resultados."""
    print(f"\n--- Ejecutando Pruebas de {MODULE_NAME} ---")
    if not access_token:
        message = "Falta el token de acceso."
        report.add_test_result(MODULE_NAME, "Pruebas de Donación", "SKIPPED", message)
        print(f"[SKIPPED] {MODULE_NAME}: {message}")
        return

    headers = {'Authorization': f'Bearer {access_token}'}
    donation_id = None

    # Prueba de creación sin token
    start_time = time.time()
    try:
        form_data, image_file = create_test_donation_form()
        res = requests.post(f"{DONATION_API_URL}/api/donations", data=form_data, files={'image': image_file})
        if res.status_code == 401:
            message = "API denegó el acceso correctamente."
            duration = time.time() - start_time
            report.add_test_result(MODULE_NAME, "Creación (Error: Sin Token)", "PASSED", message, duration)
            print(f"[PASSED] Creación (Error: Sin Token): {message} ({duration:.2f}s)")
        else:
            raise Exception(f"La API no respondió con 401. Status: {res.status_code}")
    except Exception as e:
        duration = time.time() - start_time
        message = str(e)
        report.add_test_result(MODULE_NAME, "Creación (Error: Sin Token)", "FAILED", message, duration)
        print(f"[FAILED] Creación (Error: Sin Token): {message}")

    # Prueba de creación con datos inválidos
    start_time = time.time()
    try:
        invalid_data = {'title': 'Solo un título'}
        res = requests.post(f"{DONATION_API_URL}/api/donations", data=invalid_data, headers=headers)
        if res.status_code == 400:
            message = "La API rechazó correctamente los datos incompletos."
            duration = time.time() - start_time
            report.add_test_result(MODULE_NAME, "Creación (Error: Datos Inválidos)", "PASSED", message, duration)
            print(f"[PASSED] Creación (Error: Datos Inválidos): {message} ({duration:.2f}s)")
        else:
            raise Exception(f"La API no respondió con 400. Status: {res.status_code}")
    except Exception as e:
        duration = time.time() - start_time
        message = str(e)
        report.add_test_result(MODULE_NAME, "Creación (Error: Datos Inválidos)", "FAILED", message, duration)
        print(f"[FAILED] Creación (Error: Datos Inválidos): {message}")

    # Prueba de creación exitosa
    start_time = time.time()
    try:
        form_data, image_file = create_test_donation_form()
        res = requests.post(f"{DONATION_API_URL}/api/donations", data=form_data, files={'image': image_file}, headers=headers)
        res.raise_for_status()
        donation_id = res.json().get("_id")
        if not donation_id: raise Exception("La respuesta no incluyó un _id de donación.")
        message = f"Donación creada con ID: {donation_id}"
        duration = time.time() - start_time
        report.add_test_result(MODULE_NAME, "Creación", "PASSED", message, duration)
        print(f"[PASSED] Creación: {message} ({duration:.2f}s)")
    except Exception as e:
        duration = time.time() - start_time
        message = str(e)
        report.add_test_result(MODULE_NAME, "Creación", "FAILED", message, duration)
        print(f"[FAILED] Creación: {message}")
        return

    # Prueba de listado de donaciones
    start_time = time.time()
    try:
        res = requests.get(f"{DONATION_API_URL}/api/donations", headers=headers)
        res.raise_for_status()
        if any(d.get('id') == donation_id for d in res.json()):
            message = "La donación creada aparece en la lista."
            duration = time.time() - start_time
            report.add_test_result(MODULE_NAME, "Listar Donaciones", "PASSED", message, duration)
            print(f"[PASSED] Listar Donaciones: {message} ({duration:.2f}s)")
        else:
            raise Exception("La donación recién creada no se encontró en la lista.")
    except Exception as e:
        duration = time.time() - start_time
        message = str(e)
        report.add_test_result(MODULE_NAME, "Listar Donaciones", "FAILED", message, duration)
        print(f"[FAILED] Listar Donaciones: {message}")
    
    # Prueba de eliminación exitosa
    start_time = time.time()
    try:
        res = requests.delete(f"{DONATION_API_URL}/api/donations/{donation_id}", headers=headers)
        res.raise_for_status()
        message = f"Donación {donation_id} eliminada."
        duration = time.time() - start_time
        report.add_test_result(MODULE_NAME, "Eliminar Donación", "PASSED", message, duration)
        print(f"[PASSED] Eliminar Donación: {message} ({duration:.2f}s)")
    except Exception as e:
        duration = time.time() - start_time
        message = str(e)
        report.add_test_result(MODULE_NAME, "Eliminar Donación", "FAILED", message, duration)
        print(f"[FAILED] Eliminar Donación: {message}")

    # Prueba de eliminación de una donación inexistente
    start_time = time.time()
    try:
        res = requests.delete(f"{DONATION_API_URL}/api/donations/{donation_id}", headers=headers)
        if res.status_code == 404:
            message = "La API manejó correctamente el borrado de un ID inexistente."
            duration = time.time() - start_time
            report.add_test_result(MODULE_NAME, "Eliminar (Error: No Encontrado)", "PASSED", message, duration)
            print(f"[PASSED] Eliminar (Error: No Encontrado): {message} ({duration:.2f}s)")
        else:
            raise Exception(f"La API no respondió con 404. Status: {res.status_code}")
    except Exception as e:
        duration = time.time() - start_time
        message = str(e)
        report.add_test_result(MODULE_NAME, "Eliminar (Error: No Encontrado)", "FAILED", message, duration)
        print(f"[FAILED] Eliminar (Error: No Encontrado): {message}")