#!/usr/bin/env python3
"""
Script de inicio completo para News Aggregator Pro
Ejecuta todos los servicios necesarios en paralelo
"""

import subprocess
import sys
import os
import time
import signal
import threading
from datetime import datetime

class ServiceManager:
    def __init__(self):
        self.processes = {}
        self.running = True
        
    def start_service(self, name, command, cwd=None):
        """Inicia un servicio en un proceso separado"""
        try:
            print(f"🚀 Iniciando {name}...")
            
            if isinstance(command, str):
                cmd = command.split()
            else:
                cmd = command
                
            process = subprocess.Popen(
                cmd,
                cwd=cwd or os.getcwd(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.processes[name] = process
            print(f"✅ {name} iniciado (PID: {process.pid})")
            return process
            
        except Exception as e:
            print(f"❌ Error iniciando {name}: {e}")
            return None
    
    def monitor_service(self, name, process):
        """Monitorea un servicio y muestra su output"""
        try:
            while self.running and process.poll() is None:
                output = process.stdout.readline()
                if output:
                    print(f"[{name}] {output.strip()}")
                time.sleep(0.1)
        except Exception as e:
            print(f"❌ Error monitoreando {name}: {e}")
    
    def stop_all(self):
        """Detiene todos los servicios"""
        print("\n🛑 Deteniendo todos los servicios...")
        self.running = False
        
        for name, process in self.processes.items():
            try:
                print(f"Deteniendo {name}...")
                process.terminate()
                process.wait(timeout=5)
                print(f"✅ {name} detenido")
            except subprocess.TimeoutExpired:
                print(f"⚠️ {name} no respondió, forzando cierre...")
                process.kill()
            except Exception as e:
                print(f"❌ Error deteniendo {name}: {e}")
    
    def check_dependencies(self):
        """Verifica que las dependencias estén instaladas"""
        print("🔍 Verificando dependencias...")
        
        required_packages = [
            'flask', 'flask-sqlalchemy', 'feedparser', 
            'beautifulsoup4', 'requests', 'dateparser', 'pandas'
        ]
        
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package.replace('-', '_'))
                print(f"✅ {package}")
            except ImportError:
                missing_packages.append(package)
                print(f"❌ {package}")
        
        if missing_packages:
            print(f"\n⚠️ Faltan dependencias: {', '.join(missing_packages)}")
            print("Ejecuta: pip install " + " ".join(missing_packages))
            return False
        
        print("✅ Todas las dependencias están instaladas")
        return True
    
    def start_all_services(self):
        """Inicia todos los servicios"""
        if not self.check_dependencies():
            return False
        
        print("\n🚀 Iniciando News Aggregator Pro...")
        print("=" * 50)
        
        # Servicio principal (Flask app)
        app_process = self.start_service(
            "Flask App", 
            [sys.executable, "app.py"]
        )
        
        if not app_process:
            print("❌ No se pudo iniciar la aplicación principal")
            return False
        
        # Esperar un poco para que la app se inicie
        time.sleep(3)
        
        # Scheduler automático
        scheduler_process = self.start_service(
            "Scheduler",
            [sys.executable, "scheduler.py"]
        )
        
        # Análisis de sentimientos (opcional)
        try:
            sentiment_process = self.start_service(
                "Sentiment Analyzer",
                [sys.executable, "sentiment_analyzer.py"]
            )
        except:
            print("⚠️ Sentiment Analyzer no disponible (dependencias opcionales)")
        
        # Monitor del sistema (opcional)
        try:
            monitor_process = self.start_service(
                "System Monitor",
                [sys.executable, "monitor.py"]
            )
        except:
            print("⚠️ System Monitor no disponible (dependencias opcionales)")
        
        # Monitorear servicios en threads separados
        for name, process in self.processes.items():
            if process:
                thread = threading.Thread(
                    target=self.monitor_service,
                    args=(name, process),
                    daemon=True
                )
                thread.start()
        
        print("\n" + "=" * 50)
        print("🎉 ¡News Aggregator Pro está ejecutándose!")
        print("\n📱 Accesos disponibles:")
        print("   • Aplicación principal: http://127.0.0.1:8000")
        print("   • Búsqueda avanzada: http://127.0.0.1:8000/search")
        print("   • API REST: http://127.0.0.1:8000/api/articles")
        print("   • Vista de DB: http://127.0.0.1:8000/admin/db")
        print("\n⌨️ Presiona Ctrl+C para detener todos los servicios")
        print("=" * 50)
        
        return True
    
    def run(self):
        """Ejecuta el gestor de servicios"""
        try:
            if self.start_all_services():
                # Mantener el programa ejecutándose
                while self.running:
                    time.sleep(1)
                    
                    # Verificar si algún proceso ha terminado
                    for name, process in list(self.processes.items()):
                        if process.poll() is not None:
                            print(f"⚠️ {name} terminó inesperadamente (código: {process.returncode})")
                            del self.processes[name]
                            
                            # Si es la app principal, detener todo
                            if name == "Flask App":
                                print("❌ La aplicación principal terminó, deteniendo todos los servicios...")
                                self.stop_all()
                                break
            else:
                print("❌ No se pudieron iniciar los servicios")
                
        except KeyboardInterrupt:
            print("\n🛑 Interrupción del usuario detectada...")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
        finally:
            self.stop_all()

def signal_handler(signum, frame):
    """Manejador de señales para cierre limpio"""
    print("\n🛑 Señal de cierre recibida...")
    sys.exit(0)

def main():
    """Función principal"""
    print("🚀 News Aggregator Pro - Gestor de Servicios")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Configurar manejador de señales
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Crear y ejecutar gestor de servicios
    manager = ServiceManager()
    manager.run()
    
    print("\n👋 ¡Hasta luego!")

if __name__ == "__main__":
    main()
