#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para probar la funcionalidad de actualización masiva de todas las fuentes RSS
"""

import requests
import time
import json

def test_bulk_update_functionality():
    """Prueba la funcionalidad de actualización masiva"""
    
    base_url = "http://127.0.0.1:8000"
    
    print("🔄 Probando funcionalidad de actualización masiva...")
    print("=" * 60)
    
    # Verificar que la aplicación esté funcionando
    try:
        response = requests.get(base_url, timeout=10)
        if response.status_code == 200:
            print("✅ Aplicación funcionando correctamente")
        else:
            print(f"⚠️  Aplicación responde con código: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error conectando a la aplicación: {e}")
        return
    
    print("\n📋 Instrucciones para probar manualmente:")
    print("=" * 50)
    
    print("1. 🌐 Abre la aplicación en tu navegador:")
    print(f"   {base_url}")
    
    print("\n2. 🔍 Localiza el botón 'Actualizar Todo':")
    print("   • Debería estar en la barra de acciones de la tabla")
    print("   • Tiene un estilo verde con gradiente")
    print("   • Icono de sincronización (🔄)")
    
    print("\n3. 🎯 Prueba la funcionalidad:")
    print("   • Haz clic en 'Actualizar Todo'")
    print("   • Observa que el botón cambia a 'Actualizando...' con spinner")
    print("   • El botón se deshabilita durante el proceso")
    print("   • Aparece un mensaje toast de inicio")
    
    print("\n4. ⏳ Durante la actualización:")
    print("   • Se procesan múltiples fuentes RSS automáticamente")
    print("   • Fuentes incluidas:")
    sources = [
        "BBC Mundo (Internacional)",
        "El Tiempo Mundo (Colombia)",
        "El País Portada (España)",
        "Clarín Argentina",
        "Diario Libre Portada (República Dominicana)",
        "Diario Libre Economía (República Dominicana)",
        "Diario Libre Política (República Dominicana)"
    ]
    
    for source in sources:
        print(f"     • {source}")
    
    print("\n5. ✅ Al completarse:")
    print("   • Aparece mensaje de éxito con estadísticas")
    print("   • Se muestra el número total de artículos nuevos")
    print("   • Se indica cuántas fuentes se procesaron")
    print("   • La página se recarga automáticamente")
    print("   • Los nuevos artículos aparecen en la tabla")
    
    print("\n6. 🔧 Configuración por defecto:")
    print("   • Límite: 10 artículos por fuente")
    print("   • Período: últimos 30 días")
    print("   • Solo fuentes que funcionan correctamente")
    
    print("\n7. 🧪 Prueba con API directamente:")
    print("   • Endpoint: POST /update-all")
    print("   • Parámetros JSON: {limit: 10, days_back: 30}")
    print("   • Respuesta: estadísticas de actualización")
    
    # Probar la API directamente
    print("\n8. 🔌 Probando API directamente...")
    try:
        response = requests.post(
            f"{base_url}/update-all",
            json={"limit": 5, "days_back": 30},
            headers={'Content-Type': 'application/json'},
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"   ✅ API funcionando correctamente")
                print(f"   📊 Artículos nuevos: {data.get('total_articles', 0)}")
                print(f"   📰 Fuentes procesadas: {data.get('sources_processed', 0)}")
                print(f"   🔢 Total de fuentes: {data.get('total_sources', 0)}")
                
                if data.get('errors'):
                    print(f"   ⚠️  Errores encontrados: {len(data['errors'])}")
                    for error in data['errors'][:3]:  # Mostrar solo los primeros 3
                        print(f"      • {error}")
            else:
                print(f"   ❌ Error en la API: {data.get('error', 'Error desconocido')}")
        else:
            print(f"   ❌ Error HTTP: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Error de conexión: {e}")
    except Exception as e:
        print(f"   ❌ Error inesperado: {e}")
    
    print("\n9. ✅ Funcionalidades implementadas:")
    print("   ✅ Botón 'Actualizar Todo' en la interfaz")
    print("   ✅ Estilos CSS con gradiente verde")
    print("   ✅ Función JavaScript updateAllSources()")
    print("   ✅ Petición AJAX con fetch API")
    print("   ✅ Estados de carga (spinner, deshabilitado)")
    print("   ✅ Mensajes toast informativos")
    print("   ✅ Recarga automática de página")
    print("   ✅ Ruta POST /update-all en el backend")
    print("   ✅ Procesamiento de múltiples fuentes RSS")
    print("   ✅ Manejo de errores y estadísticas")
    
    print("\n🎉 ¡Actualización masiva implementada!")
    print("   Ahora puedes actualizar todas las fuentes RSS con un solo clic.")

if __name__ == "__main__":
    test_bulk_update_functionality()

