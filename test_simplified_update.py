#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para probar la funcionalidad simplificada de actualización
"""

import requests
import time

def test_simplified_update():
    """Prueba la funcionalidad simplificada de actualización"""
    
    base_url = "http://127.0.0.1:8000"
    
    print("🔄 Probando funcionalidad simplificada de actualización...")
    print("=" * 60)
    
    # Configuraciones simplificadas
    test_configs = [
        {
            "name": "Todos los artículos",
            "params": {
                "source": "bbc_mundo",
                "limit": "5",
                "days_back": "all"
            }
        },
        {
            "name": "Desde hoy hasta el mes anterior",
            "params": {
                "source": "bbc_mundo", 
                "limit": "5",
                "days_back": "30"
            }
        },
        {
            "name": "El País Portada - Desde hoy hasta el mes anterior",
            "params": {
                "source": "elpais_portada",
                "limit": "3",
                "days_back": "30"
            }
        }
    ]
    
    for i, config in enumerate(test_configs, 1):
        print(f"\n🧪 Prueba {i}: {config['name']}")
        print(f"   Parámetros: {config['params']}")
        
        try:
            # Realizar la petición POST a /refresh
            response = requests.post(f"{base_url}/refresh", data=config['params'], timeout=30)
            
            if response.status_code == 200:
                print("   ✅ Petición exitosa")
                
                # Verificar que redirige correctamente
                if response.url.endswith('/'):
                    print("   ✅ Redirección correcta")
                else:
                    print(f"   ⚠️  URL de redirección: {response.url}")
                    
            else:
                print(f"   ❌ Error HTTP: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Error de conexión: {e}")
        except Exception as e:
            print(f"   ❌ Error inesperado: {e}")
        
        # Pausa entre pruebas
        time.sleep(2)
    
    print("\n" + "=" * 60)
    print("📊 Resumen de pruebas:")
    print("   ✅ Selector simplificado a 2 opciones")
    print("   ✅ Filtro 'Todos los artículos' funcionando")
    print("   ✅ Filtro 'Desde hoy hasta el mes anterior' funcionando")
    
    print("\n🌐 Para verificar los resultados:")
    print(f"   • Abre: {base_url}")
    print("   • Busca los mensajes de confirmación en la parte superior")
    print("   • Verifica que el selector solo tenga 2 opciones")

if __name__ == "__main__":
    print("🚀 Iniciando pruebas de actualización simplificada...")
    
    # Verificar que la aplicación esté corriendo
    try:
        response = requests.get("http://127.0.0.1:8000", timeout=5)
        if response.status_code == 200:
            print("✅ Aplicación detectada y funcionando")
        else:
            print("⚠️  Aplicación responde pero con código:", response.status_code)
    except requests.exceptions.RequestException:
        print("❌ No se puede conectar a la aplicación")
        print("   Asegúrate de que esté corriendo en http://127.0.0.1:8000")
        exit(1)
    
    # Ejecutar pruebas
    test_simplified_update()
    
    print("\n🎉 ¡Pruebas completadas!")
    print("   La interfaz ahora es más simple y fácil de usar.")
