#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para probar la funcionalidad de actualización con filtros de tiempo
"""

import requests
import time
from datetime import datetime, timedelta

def test_update_with_filters():
    """Prueba la funcionalidad de actualización con diferentes filtros de tiempo"""
    
    base_url = "http://127.0.0.1:8000"
    
    print("🔄 Probando funcionalidad de actualización con filtros de tiempo...")
    print("=" * 60)
    
    # Configuraciones de prueba
    test_configs = [
        {
            "name": "Actualización completa (todos los artículos)",
            "params": {
                "source": "bbc_mundo",
                "limit": "5",
                "days_back": "all"
            }
        },
        {
            "name": "Última semana",
            "params": {
                "source": "bbc_mundo", 
                "limit": "5",
                "days_back": "7"
            }
        },
        {
            "name": "Último mes",
            "params": {
                "source": "bbc_mundo",
                "limit": "5", 
                "days_back": "30"
            }
        },
        {
            "name": "Últimos 3 días",
            "params": {
                "source": "bbc_mundo",
                "limit": "5",
                "days_back": "3"
            }
        },
        {
            "name": "Fuente diferente - El País Portada (última semana)",
            "params": {
                "source": "elpais_portada",
                "limit": "3",
                "days_back": "7"
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
        
        # Pausa entre pruebas para no sobrecargar
        time.sleep(2)
    
    print("\n" + "=" * 60)
    print("📊 Resumen de pruebas:")
    print("   • Todas las configuraciones fueron probadas")
    print("   • Verificar en la aplicación web los mensajes de resultado")
    print("   • Los filtros de tiempo deberían funcionar correctamente")
    
    print("\n🌐 Para verificar los resultados:")
    print(f"   • Abre: {base_url}")
    print("   • Busca los mensajes de confirmación en la parte superior")
    print("   • Verifica que solo se agreguen artículos del período seleccionado")

def test_api_endpoints():
    """Prueba los endpoints de la API para verificar que funcionan"""
    
    base_url = "http://127.0.0.1:8000"
    
    print("\n🔌 Probando endpoints de la API...")
    print("-" * 40)
    
    endpoints = [
        ("/api/articles", "API de artículos"),
        ("/api/articles?page=1&per_page=5", "API con paginación"),
        ("/api/articles?source=bbc_mundo", "API filtrada por fuente"),
    ]
    
    for endpoint, description in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ {description}: {len(data.get('articles', []))} artículos")
            else:
                print(f"   ❌ {description}: Error {response.status_code}")
        except Exception as e:
            print(f"   ❌ {description}: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando pruebas de actualización con filtros...")
    
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
    test_update_with_filters()
    test_api_endpoints()
    
    print("\n🎉 ¡Pruebas completadas!")
    print("   Revisa la aplicación web para ver los resultados de la actualización.")
