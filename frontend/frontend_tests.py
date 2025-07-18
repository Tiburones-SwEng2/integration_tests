import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = "http://localhost:5173/"

def run_tests():
    MODULE_NAME = "Flujo de Registro"
    print(f"\n--- Ejecutando Prueba de {MODULE_NAME} ---")

    options = Options()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")  # Descomenta para ocultar el navegador

    driver = webdriver.Chrome(service=Service(), options=options)

    # Registro exitoso

    start_time = time.time()

    try:
        driver.get(BASE_URL)
        time.sleep(1)

        login_btn = driver.find_element(By.XPATH, "//button[contains(., 'Iniciar sesión')]")
        login_btn.click()
        time.sleep(1)

        create_account_link = driver.find_element(By.LINK_TEXT, "Crear cuenta")
        create_account_link.click()
        time.sleep(1)

        unique_id = int(time.time()) + random.randint(100, 999)
        name = f"Usuario Test {unique_id}"
        email = f"test_{unique_id}@example.com"
        password = "TestPassword123"

        driver.find_element(By.XPATH, "//input[@placeholder='Ingresa tu nombre completo']").send_keys(name)
        driver.find_element(By.XPATH, "//input[@placeholder='Ingresa tu email']").send_keys(email)
        driver.find_element(By.XPATH, "//input[@placeholder='Crea una contraseña']").send_keys(password)
        driver.find_element(By.XPATH, "//input[@placeholder='Repite tu contraseña']").send_keys(password)

        register_btn = driver.find_element(By.XPATH, "//button[contains(., 'Registrarse')]")
        driver.execute_script("arguments[0].scrollIntoView(true);", register_btn)
        time.sleep(0.5)
        register_btn.click()
        time.sleep(3)

        page_source = driver.page_source
        assert "¡Registro exitoso! Por favor inicia sesión." in page_source

        duration = time.time() - start_time
        print(f"[PASSED] Registro de Usuario: El usuario se registró correctamente. ({duration:.2f}s)")

    except NoSuchElementException as e:
        duration = time.time() - start_time
        print(f"[FAILED] Registro de Usuario: Elemento no encontrado - {str(e)} ({duration:.2f}s)")
    except AssertionError as e:
        duration = time.time() - start_time
        print(f"[FAILED] Registro de Usuario: No se encontró mensaje de éxito. ({duration:.2f}s)")
    except Exception as e:
        duration = time.time() - start_time
        print(f"[FAILED] Registro de Usuario: {str(e)} ({duration:.2f}s)")

    #Registro con email duplicado
    start_time = time.time()
    try:
        driver.get(BASE_URL)
        time.sleep(1)

        login_btn = driver.find_element(By.XPATH, "//button[contains(., 'Iniciar sesión')]")
        login_btn.click()
        time.sleep(1)

        create_account_link = driver.find_element(By.LINK_TEXT, "Crear cuenta")
        create_account_link.click()
        time.sleep(1)
        
        driver.find_element(By.XPATH, "//input[@placeholder='Ingresa tu nombre completo']").send_keys(name)
        driver.find_element(By.XPATH, "//input[@placeholder='Ingresa tu email']").send_keys(email)
        driver.find_element(By.XPATH, "//input[@placeholder='Crea una contraseña']").send_keys(password)
        driver.find_element(By.XPATH, "//input[@placeholder='Repite tu contraseña']").send_keys(password)

        register_btn = driver.find_element(By.XPATH, "//button[contains(., 'Registrarse')]")
        driver.execute_script("arguments[0].scrollIntoView(true);", register_btn)
        time.sleep(0.5)
        register_btn.click()
        time.sleep(3)

        page_source = driver.page_source
        assert "Error en el registro" in page_source

        duration = time.time() - start_time
        print(f"[PASSED] Registro con Email Duplicado: Se detectó correctamente el error. ({duration:.2f}s)")

    except NoSuchElementException as e:
        duration = time.time() - start_time
        print(f"[FAILED] Registro con Email Duplicado: Elemento no encontrado - {str(e)} ({duration:.2f}s)")
    except AssertionError as e:
        duration = time.time() - start_time
        print(f"[FAILED] Registro con Email Duplicado: No se mostró mensaje de error esperado. ({duration:.2f}s)")
    except Exception as e:
        duration = time.time() - start_time
        print(f"[FAILED] Registro con Email Duplicado: {str(e)} ({duration:.2f}s)")

    # Login con contraseña incorrecta
    start_time = time.time()
    try:
        driver.get(BASE_URL)
        time.sleep(1)

        password_1 = "IncorrectPassword"

        login_btn = driver.find_element(By.XPATH, "//button[contains(., 'Iniciar sesión')]")
        login_btn.click()
        time.sleep(1)

        wait = WebDriverWait(driver, 10)
        email_input = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='email' or @placeholder='Correo electrónico']")))
        email_input.click()
        email_input.send_keys(email)

        password_input = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='password' or @placeholder='Contraseña']")))
        password_input.click()
        password_input.send_keys(password_1)

        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Ingresar')]")))
        time.sleep(0.5)
        login_button.click()
        time.sleep(3)

        page_source = driver.page_source
        assert "Error en la autenticación" in page_source

        duration = time.time() - start_time
        print(f"[PASSED] Login con contraseña incorrecta: Se detectó correctamente el error. ({duration:.2f}s)")

    except NoSuchElementException as e:
        duration = time.time() - start_time
        print(f"[FAILED] Login con contraseña incorrecta: Elemento no encontrado - {str(e)} ({duration:.2f}s)")
    except AssertionError as e:
        duration = time.time() - start_time
        print(f"[FAILED] Login con contraseña incorrecta: No se mostró mensaje de error esperado. ({duration:.2f}s)")
    except Exception as e:
        duration = time.time() - start_time
        print(f"[FAILED] Login con contraseña incorrecta: {str(e)} ({duration:.2f}s)")

    #Login exitoso
    start_time = time.time()
    try:
        driver.get(BASE_URL)
        time.sleep(1)

        login_btn = driver.find_element(By.XPATH, "//button[contains(., 'Iniciar sesión')]")
        login_btn.click()
        time.sleep(1)

        wait = WebDriverWait(driver, 10)
        email_input = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='email' or @placeholder='Correo electrónico']")))
        email_input.click()
        email_input.send_keys(email)

        password_input = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='password' or @placeholder='Contraseña']")))
        password_input.click()
        password_input.send_keys(password)

        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Ingresar')]")))
        time.sleep(0.5)
        login_button.click()
        time.sleep(3)

        page_source = driver.page_source
        assert name in page_source

        duration = time.time() - start_time
        print(f"[PASSED] Login exitoso. ({duration:.2f}s)")

    except NoSuchElementException as e:
        duration = time.time() - start_time
        print(f"[FAILED] Login: Elemento no encontrado - {str(e)} ({duration:.2f}s)")
    except AssertionError as e:
        duration = time.time() - start_time
        print(f"[FAILED] Login: No se mostró mensaje de error esperado. ({duration:.2f}s)")
    except Exception as e:
        duration = time.time() - start_time
        print(f"[FAILED] Login: {str(e)} ({duration:.2f}s)")

    MODULE_NAME = "Flujo de donación"
    print(f"\n--- Ejecutando Prueba de {MODULE_NAME} ---")

    #Crear donación

    start_time = time.time()
    try:
        driver.get(BASE_URL)
        time.sleep(1)

        unique_id = int(time.time()) + random.randint(100, 999)
        title = f"TestTitle{unique_id}"
        description = f"TestDescription{unique_id}"
        city = f"TestCity{unique_id}"
        address = f"TestAddress{unique_id}"

        create_btn = driver.find_element(By.XPATH, "//button[contains(., 'Realizar donación')]")
        create_btn.click()
        time.sleep(1)

        wait = WebDriverWait(driver, 5)
        donar_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Realizar mi primera donación')]")))
        donar_btn.click()
        time.sleep(1)

        titulo = driver.find_element(By.ID, "title")
        titulo.click()
        titulo.send_keys(title)

        descripcion = driver.find_element(By.ID, "description")
        descripcion.click()
        descripcion.send_keys(description)

        ciudad = driver.find_element(By.ID, "city")
        ciudad.click()
        ciudad.send_keys(city)

        direccion = driver.find_element(By.ID, "address")
        direccion.click()
        direccion.send_keys(address)

        time.sleep(3)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        file_path = os.path.abspath("image.png")
        upload_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
        upload_input.send_keys(file_path)

        publicar_btn = driver.find_element(By.XPATH, "//button[contains(., 'Publicar Donación')]")
        driver.execute_script("arguments[0].scrollIntoView(true);", publicar_btn)
        time.sleep(0.5)
        publicar_btn.click()
        time.sleep(3)

        page_source = driver.page_source
        time.sleep(3)
        assert "¡Donación publicada exitosamente!" in page_source

        duration = time.time() - start_time
        print(f"[PASSED] Donación creada exitosamente. ({duration:.2f}s)")

    except NoSuchElementException as e:
        duration = time.time() - start_time
        print(f"[FAILED] Crear donación: Elemento no encontrado - {str(e)} ({duration:.2f}s)")
    except AssertionError as e:
        duration = time.time() - start_time
        print(f"[FAILED] Crear donación: No se mostró mensaje esperado. ({duration:.2f}s)")
    except Exception as e:
        duration = time.time() - start_time
        print(f"[FAILED] Crear donación: {str(e)} ({duration:.2f}s)")


    #Eliminar donación
    start_time = time.time()
    try:
        driver.get(BASE_URL)
        time.sleep(1)

        unique_id = int(time.time()) + random.randint(100, 999)
        title = f"TestTitle{unique_id}"
        description = f"TestDescription{unique_id}"
        city = f"TestCity{unique_id}"
        address = f"TestAddress{unique_id}"

        create_btn = driver.find_element(By.XPATH, "//button[contains(., 'Realizar donación')]")
        create_btn.click()
        time.sleep(1)

        eliminar_btn = driver.find_element(By.XPATH, "//button[contains(., 'Eliminar')]")
        driver.execute_script("arguments[0].scrollIntoView(true);", eliminar_btn)
        time.sleep(0.5)
        eliminar_btn.click()
        time.sleep(3)

        page_source = driver.page_source
        time.sleep(3)
        assert "Éxito" in page_source

        duration = time.time() - start_time
        print(f"[PASSED] Donación eliminada exitosamente. ({duration:.2f}s)")

    except NoSuchElementException as e:
        duration = time.time() - start_time
        print(f"[FAILED] Eliminar donación: Elemento no encontrado - {str(e)} ({duration:.2f}s)")
    except AssertionError as e:
        duration = time.time() - start_time
        print(f"[FAILED] Eliminar donación: No se mostró mensaje esperado. ({duration:.2f}s)")
    except Exception as e:
        duration = time.time() - start_time
        print(f"[FAILED] Eliminar donación: {str(e)} ({duration:.2f}s)")

    #Crear donación (datos invalidos)

    start_time = time.time()
    try:
        driver.get(BASE_URL)
        time.sleep(1)

        unique_id = int(time.time()) + random.randint(100, 999)
        title = f"TestTitle{unique_id}"
        description = f"TestDescription{unique_id}"
        city = f"TestCity{unique_id}"
        address = f"TestAddress{unique_id}"

        create_btn = driver.find_element(By.XPATH, "//button[contains(., 'Realizar donación')]")
        create_btn.click()
        time.sleep(1)

        wait = WebDriverWait(driver, 5)
        donar_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Realizar mi primera donación')]")))
        donar_btn.click()
        time.sleep(1)

        titulo = driver.find_element(By.ID, "title")
        titulo.click()
        titulo.send_keys(title)

        descripcion = driver.find_element(By.ID, "description")
        descripcion.click()

        ciudad = driver.find_element(By.ID, "city")
        ciudad.click()
        ciudad.send_keys(city)

        direccion = driver.find_element(By.ID, "address")
        direccion.click()
        direccion.send_keys(address)

        time.sleep(3)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        file_path = os.path.abspath("image.png")
        upload_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
        upload_input.send_keys(file_path)

        publicar_btn = driver.find_element(By.XPATH, "//button[contains(., 'Publicar Donación')]")
        driver.execute_script("arguments[0].scrollIntoView(true);", publicar_btn)
        time.sleep(0.5)
        publicar_btn.click()
        time.sleep(3)

        page_source = driver.page_source
        time.sleep(3)
        assert "requerida" in page_source

        duration = time.time() - start_time
        print(f"[PASSED] La donación no fue creada, pues no se suministran todos los datos. ({duration:.2f}s)")

    except NoSuchElementException as e:
        duration = time.time() - start_time
        print(f"[FAILED] Crear donación (datos inválidos): Elemento no encontrado - {str(e)} ({duration:.2f}s)")
    except AssertionError as e:
        duration = time.time() - start_time
        print(f"[FAILED] Crear donación (datos inválidos): No se mostró mensaje de error esperado. ({duration:.2f}s)")
    except Exception as e:
        duration = time.time() - start_time
        print(f"[FAILED] Crear donación (datos inválidos): {str(e)} ({duration:.2f}s)")

    MODULE_NAME = "Flujo de carrito de compras"
    print(f"\n--- Ejecutando Prueba de {MODULE_NAME} ---")

    #Añadir al carrito
    start_time = time.time()
    try:
        driver.get(BASE_URL)
        time.sleep(1)

        donaciones_btn = driver.find_element(By.XPATH, "//button[contains(., 'Ver donaciones disponibles')]")
        time.sleep(0.5)
        donaciones_btn.click()
        time.sleep(3)
        page_source = driver.page_source
        assert "Añadir" in page_source

        añadir_btn = driver.find_element(By.XPATH, "//button[contains(., 'Añadir')]")
        time.sleep(0.5)
        añadir_btn.click()
        time.sleep(3)

        page_source = driver.page_source
        time.sleep(3)
        assert "Añadido" in page_source

        duration = time.time() - start_time
        print(f"[PASSED] El producto fue añadido al carrito. ({duration:.2f}s)")

    except NoSuchElementException as e:
        duration = time.time() - start_time
        print(f"[FAILED] Añadir al carrito: Elemento no encontrado - {str(e)} ({duration:.2f}s)")
    except AssertionError as e:
        duration = time.time() - start_time
        print(f"[FAILED] Añadir al carrito: No se mostró mensaje esperado. ({duration:.2f}s)")
    except Exception as e:
        duration = time.time() - start_time
        print(f"[FAILED] Añadir al carrito: {str(e)} ({duration:.2f}s)")

    #Vaciar carrito
    start_time = time.time()
    try:
        page_source = driver.page_source
        time.sleep(1)

        carrito_btn = driver.find_element(By.XPATH, "//button[contains(., 'Carrito')]")
        time.sleep(0.5)
        carrito_btn.click()
        time.sleep(3)

        vaciar_carrito_btn = driver.find_element(By.XPATH, "//button[contains(., 'Vaciar Carrito')]")
        time.sleep(0.5)
        vaciar_carrito_btn.click()
        time.sleep(3)

        page_source = driver.page_source
        time.sleep(3)
        assert "No hay artículos en tu carrito" in page_source

        duration = time.time() - start_time
        print(f"[PASSED] Se vació el carrito. ({duration:.2f}s)")

    except NoSuchElementException as e:
        duration = time.time() - start_time
        print(f"[FAILED] Vaciar carrito: Elemento no encontrado - {str(e)} ({duration:.2f}s)")
    except AssertionError as e:
        duration = time.time() - start_time
        print(f"[FAILED] Vaciar carrito: No se mostró mensaje esperado. ({duration:.2f}s)")
    except Exception as e:
        duration = time.time() - start_time
        print(f"[FAILED] Vaciar carrito: {str(e)} ({duration:.2f}s)")

    finally:
        driver.quit()


if __name__ == "__main__":
    run_tests()


