import requests

URL = "http://localhost:5000"

# Función para autenticación
def autenticar():
    usuario = input("Usuario: ")
    password = input("Contraseña: ")

    response = requests.post(f"{URL}/login", json={"usuario": usuario, "password": password})
    
    if response.status_code == 200:
        token = response.json().get("token")
        print("✅ Autenticación exitosa.")
        return token
    else:
        print("❌ Error de autenticación:", response.json().get("error"))
        return None

# Función para agregar un usuario
def agregar_usuario(token):
    if not token:
        print("⚠️ Debe autenticarse primero.")
        return

    id = int(input("Ingrese el ID del usuario: "))
    nombre = input("Ingrese el nombre del usuario: ")
    
    datos = {"id": id, "nombre": nombre}
    response = requests.post(f"{URL}/usuarios", json=datos, headers={"Authorization": f"Bearer {token}"})
    
    if response.status_code == 201:
        print("✅ Usuario agregado:", response.json())
    else:
        print("❌ Error al agregar usuario:", response.json())

# Función para eliminar un usuario por ID
def eliminar_usuario(token):
    if not token:
        print("⚠️ Debe autenticarse primero.")
        return

    id = int(input("Ingrese el ID del usuario a eliminar: "))
    response = requests.delete(f"{URL}/usuarios/{id}", headers={"Authorization": f"Bearer {token}"})
    
    if response.status_code == 200:
        print("✅ Usuario eliminado:", response.json())
    else:
        print("❌ Error al eliminar usuario:", response.json())

# Función para buscar un usuario por ID (no requiere autenticación)
def buscar_usuario():
    id = int(input("Ingrese el ID del usuario a buscar: "))
    response = requests.get(f"{URL}/usuarios/{id}")
    
    if response.status_code == 200:
        print("✅ Usuario encontrado:", response.json())
    else:
        print("❌ Usuario no encontrado.")

# Menú interactivo
def menu():
    token = None  # Variable para almacenar el token de autenticación

    # Forzar autenticación antes de mostrar el menú
    while not token:
        print("\n🔐 Debe iniciar sesión para continuar.")
        token = autenticar()
    
    while True:
        print("\n--- Menú ---")
        print("1. Agregar usuario")
        print("2. Eliminar usuario")
        print("3. Buscar usuario por ID")
        print("4. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            agregar_usuario(token)
        elif opcion == "2":
            eliminar_usuario(token)
        elif opcion == "3":
            buscar_usuario()
        elif opcion == "4":
            print("Saliendo del programa...")
            break
        else:
            print("❌ Opción inválida, intente nuevamente.")

if __name__ == "__main__":
    menu()
