#!/usr/bin/env python3
"""
Script de prueba rápida para verificar que la aplicación funciona correctamente
"""

import requests
import time
import sys

def test_app():
    """Prueba las funcionalidades principales de la aplicación"""
    base_url = "http://127.0.0.1:8000"
    
    print("🧪 Probando News Aggregator Pro...")
    print("=" * 50)
    
    # Esperar un poco para que la app se inicie
    print("⏳ Esperando que la aplicación se inicie...")
    time.sleep(3)
    
    try:
        # Probar página principal
        print("📄 Probando página principal...")
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            print("✅ Página principal: OK")
        else:
            print(f"❌ Página principal: Error {response.status_code}")
            return False
        
        # Probar búsqueda avanzada
        print("🔍 Probando búsqueda avanzada...")
        response = requests.get(f"{base_url}/search", timeout=10)
        if response.status_code == 200:
            print("✅ Búsqueda avanzada: OK")
        else:
            print(f"❌ Búsqueda avanzada: Error {response.status_code}")
        
        # Probar API REST
        print("🔌 Probando API REST...")
        response = requests.get(f"{base_url}/api/articles", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API REST: OK ({len(data.get('articles', []))} artículos)")
        else:
            print(f"❌ API REST: Error {response.status_code}")
        
        # Probar vista de base de datos
        print("🗄️ Probando vista de base de datos...")
        response = requests.get(f"{base_url}/admin/db", timeout=10)
        if response.status_code == 200:
            print("✅ Vista de DB: OK")
        else:
            print(f"❌ Vista de DB: Error {response.status_code}")
        
        print("\n" + "=" * 50)
        print("🎉 ¡Todas las pruebas completadas!")
        print("\n📱 Accesos disponibles:")
        print(f"   • Aplicación principal: {base_url}")
        print(f"   • Búsqueda avanzada: {base_url}/search")
        print(f"   • API REST: {base_url}/api/articles")
        print(f"   • Vista de DB: {base_url}/admin/db")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar a la aplicación")
        print("   Asegúrate de que la aplicación esté ejecutándose en http://127.0.0.1:8000")
        return False
    except Exception as e:
        print(f"❌ Error durante las pruebas: {e}")
        return False

if __name__ == "__main__":
    success = test_app()
    sys.exit(0 if success else 1)
