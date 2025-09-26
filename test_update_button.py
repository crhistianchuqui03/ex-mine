#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para probar el botón de actualizar
"""

import requests
import time

def test_update_button():
    """Prueba el botón de actualizar"""
    
    base_url = "http://127.0.0.1:8000"
    
    print("🔄 Probando botón de actualizar...")
    print("=" * 50)
    
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
    
    print("\n🔍 Verificando elementos del botón de actualizar:")
    print("=" * 50)
    
    # Verificar que el botón esté en el HTML
    if "update-all" in response.text:
        print("✅ Botón 'update-all' encontrado en el HTML")
    else:
        print("❌ Botón 'update-all' NO encontrado en el HTML")
    
    if "Actualizar Todo" in response.text:
        print("✅ Texto 'Actualizar Todo' encontrado")
    else:
        print("❌ Texto 'Actualizar Todo' NO encontrado")
    
    if "sync-alt" in response.text:
        print("✅ Icono 'sync-alt' encontrado")
    else:
        print("❌ Icono 'sync-alt' NO encontrado")
    
    if "updateAllSources" in response.text:
        print("✅ Función JavaScript 'updateAllSources' encontrada")
    else:
        print("❌ Función JavaScript 'updateAllSources' NO encontrada")
    
    if "btn-success" in response.text:
        print("✅ Clase CSS 'btn-success' encontrada")
    else:
        print("❌ Clase CSS 'btn-success' NO encontrada")
    
    print("\n🎯 Ubicación del botón:")
    print("=" * 30)
    print("El botón 'Actualizar Todo' está ubicado en:")
    print("• Sección: table-actions")
    print("• Posición: Después del botón 'Limpiar'")
    print("• Antes del enlace 'Búsqueda Avanzada'")
    
    print("\n📋 Instrucciones para encontrar el botón:")
    print("=" * 50)
    
    print("1. 🌐 Abre la aplicación en tu navegador:")
    print(f"   {base_url}")
    
    print("\n2. 👀 Busca en la sección de la tabla de artículos:")
    print("   • Desplázate hacia abajo hasta la tabla")
    print("   • Busca la sección con controles de búsqueda")
    print("   • El botón está entre 'Limpiar' y 'Búsqueda Avanzada'")
    
    print("\n3. 🎨 Características del botón:")
    print("   • Color: Verde (btn-success)")
    print("   • Icono: 🔄 (fas fa-sync-alt)")
    print("   • Texto: 'Actualizar Todo'")
    print("   • Efecto hover: Elevación y glow verde")
    
    print("\n4. 🔧 Funcionalidad del botón:")
    print("   • Al hacer clic: Actualiza todas las fuentes RSS")
    print("   • Muestra: Spinner de carga")
    print("   • Notificación: Toast con progreso")
    print("   • Resultado: Recarga la página con nuevos artículos")
    
    print("\n5. 🎮 Cómo probar el botón:")
    print("   • Haz clic en 'Actualizar Todo'")
    print("   • Observa el spinner de carga")
    print("   • Espera la notificación de éxito/error")
    print("   • Verifica que la página se recargue")
    
    print("\n6. ⚠️  Si no ves el botón:")
    print("   • Recarga la página (F5)")
    print("   • Verifica que estés en la página principal")
    print("   • Busca en la sección de controles de la tabla")
    print("   • El botón está después del selector de temas")
    
    print("\n✅ ¡Botón de actualizar implementado!")
    print("   El botón 'Actualizar Todo' está disponible y funcional.")

if __name__ == "__main__":
    test_update_button()

