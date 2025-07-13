import requests
import time

USER_API_URL = "http://localhost:5002"
MODULE_NAME = "Flujo de Usuario"

def run_user_tests(report):
    """Prueba el registro, login y recuperación, registrando y mostrando resultados."""
    print(f"\n--- Ejecutando Pruebas de {MODULE_NAME} ---")
    
    timestamp = int(time.time() * 1000)
    unique_email = f"integration_{timestamp}@test.com"
    test_user = {"name": "UsuarioDeIntegracion", "email": unique_email, "password": "aSafePassword123"}
    access_token = None

    # Prueba de Registro Exitoso
    start_time = time.time()
    try:
        res = requests.post(f"{USER_API_URL}/register", json=test_user, timeout=5)
        res.raise_for_status()
        message = "El usuario se registró correctamente."
        duration = time.time() - start_time
        report.add_test_result(MODULE_NAME, "Registro de Usuario", "PASSED", message, duration)
        print(f"[PASSED] Registro de Usuario: {message} ({duration:.2f}s)")
    except requests.exceptions.ConnectionError as e:
        duration = time.time() - start_time
        message = f"Fallo de conexión a {USER_API_URL}."
        report.add_test_result(MODULE_NAME, "Registro de Usuario", "FATAL", message, duration)
        print(f"[FATAL] Registro de Usuario: {message}")
        raise e
    except Exception as e:
        duration = time.time() - start_time
        message = str(e)
        report.add_test_result(MODULE_NAME, "Registro de Usuario", "FAILED", message, duration)
        print(f"[FAILED] Registro de Usuario: {message}")
        return None, None

    # Prueba de Registro con Email Duplicado
    start_time = time.time()
    try:
        res = requests.post(f"{USER_API_URL}/register", json=test_user, timeout=5)
        if res.status_code == 400 and "Este email ya esta registrado" in res.json().get("mensaje", ""):
            message = "La API rechazó correctamente el registro duplicado."
            duration = time.time() - start_time
            report.add_test_result(MODULE_NAME, "Registro (Error: Email Duplicado)", "PASSED", message, duration)
            print(f"[PASSED] Registro (Error: Email Duplicado): {message} ({duration:.2f}s)")
        else:
            raise Exception(f"La API no respondió con el error esperado. Status: {res.status_code}")
    except Exception as e:
        duration = time.time() - start_time
        message = str(e)
        report.add_test_result(MODULE_NAME, "Registro (Error: Email Duplicado)", "FAILED", message, duration)
        print(f"[FAILED] Registro (Error: Email Duplicado): {message}")

    # Prueba de Login con Contraseña Incorrecta
    start_time = time.time()
    try:
        res = requests.post(f"{USER_API_URL}/login", json={"email": test_user["email"], "password": "wrongpassword"})
        if res.status_code == 400 and "Contraseña incorrecta" in res.json().get("mensaje", ""):
            message = "La API rechazó correctamente el login."
            duration = time.time() - start_time
            report.add_test_result(MODULE_NAME, "Login (Error: Contraseña Incorrecta)", "PASSED", message, duration)
            print(f"[PASSED] Login (Error: Contraseña Incorrecta): {message} ({duration:.2f}s)")
        else:
            raise Exception(f"La API no respondió con el error esperado. Status: {res.status_code}")
    except Exception as e:
        duration = time.time() - start_time
        message = str(e)
        report.add_test_result(MODULE_NAME, "Login (Error: Contraseña Incorrecta)", "FAILED", message, duration)
        print(f"[FAILED] Login (Error: Contraseña Incorrecta): {message}")

    # Prueba de Login Exitoso
    start_time = time.time()
    try:
        login_credentials = {"email": test_user["email"], "password": test_user["password"]}
        res = requests.post(f"{USER_API_URL}/login", json=login_credentials)
        res.raise_for_status()
        access_token = res.json().get("access_token")
        if not access_token: raise Exception("No se recibió access_token.")
        message = "Login correcto y token JWT obtenido."
        duration = time.time() - start_time
        report.add_test_result(MODULE_NAME, "Login", "PASSED", message, duration)
        print(f"[PASSED] Login: {message} ({duration:.2f}s)")
    except Exception as e:
        duration = time.time() - start_time
        message = str(e)
        report.add_test_result(MODULE_NAME, "Login", "FAILED", message, duration)
        print(f"[FAILED] Login: {message}")
        return None, None

    # Prueba de Recuperación de Contraseña
    start_time = time.time()
    try:
        res = requests.post(f"{USER_API_URL}/recover", json={"email": test_user["email"]})
        res.raise_for_status()
        message = "La API procesó la solicitud de recuperación."
        duration = time.time() - start_time
        report.add_test_result(MODULE_NAME, "Recuperación de Contraseña", "PASSED", message, duration)
        print(f"[PASSED] Recuperación de Contraseña: {message} ({duration:.2f}s)")
    except Exception as e:
        duration = time.time() - start_time
        message = str(e)
        report.add_test_result(MODULE_NAME, "Recuperación de Contraseña", "FAILED", message, duration)
        print(f"[FAILED] Recuperación de Contraseña: {message}")

    return access_token, unique_email