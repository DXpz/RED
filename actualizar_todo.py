#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script maestro que actualiza todo el sitio web automáticamente
1. Archiva noticias antiguas
2. Genera páginas HTML de noticias nuevas
3. Actualiza el index.html
Autor: Trickzz.sh
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime


def ejecutar_script(script_name, descripcion):
    """Ejecuta un script Python y muestra su salida"""
    print(f"\n{'='*60}")
    print(f"  {descripcion}")
    print(f"{'='*60}\n")
    
    try:
        # Ejecutar el script
        resultado = subprocess.run(
            [sys.executable, script_name],
            capture_output=False,
            text=True,
            check=True
        )
        print(f"\n✅ {descripcion} completado exitosamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error en {descripcion}")
        print(f"Código de salida: {e.returncode}")
        return False
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        return False


def main():
    """Función principal que coordina la actualización completa"""
    print("🚀 ACTUALIZACIÓN COMPLETA DEL SITIO WEB")
    print("=" * 60)
    print("RED - Sistema de actualización automática")
    print("=" * 60)
    
    # Verificar que estamos en el directorio correcto
    if not Path('noticias.json').exists():
        print("\n❌ Error: No se encuentra noticias.json")
        print("Asegúrate de ejecutar este script desde la carpeta del proyecto")
        return False
    
    print("\n📋 Se ejecutarán los siguientes pasos:")
    print("  1. Archivar noticias antiguas → noticias_ant/")
    print("  2. Generar páginas HTML de noticias nuevas")
    print("  3. Actualizar index.html automáticamente")
    print("\n⏳ Iniciando proceso...\n")
    
    # Paso 1 y 2: Generar páginas (incluye archivo automático)
    if not ejecutar_script('generar_paginas.py', 'PASO 1 & 2: Archivo y Generación de Páginas'):
        print("\n⚠️  Proceso detenido debido a un error")
        return False
    
    # Paso 3: Actualizar index.html
    if not ejecutar_script('actualizar_index.py', 'PASO 3: Actualización de Index.html'):
        print("\n⚠️  Proceso detenido debido a un error")
        return False
    
    # Resumen final
    print("\n" + "=" * 60)
    print("🎉 ¡ACTUALIZACIÓN COMPLETA EXITOSA!")
    print("=" * 60)
    print("\n📊 Resumen:")
    print("  ✅ Noticias antiguas archivadas")
    print("  ✅ Páginas HTML generadas")
    print("  ✅ Index.html actualizado")

    # Intentar hacer push automático a GitHub
    proyecto_dir = Path(__file__).resolve().parent
    print("\n🚀 Enviando cambios a GitHub (push automático)...")
    try:
        # Asegurarse de que estamos en la carpeta del repo
        if not (proyecto_dir / ".git").exists():
            print("ℹ️  No se encontró un repositorio Git en esta carpeta. Omitiendo push automático.")
        else:
            # git add
            subprocess.run(
                ["git", "add", "-A"],
                cwd=str(proyecto_dir),
                check=True,
            )

            # git commit (solo si hay cambios)
            resultado_status = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=str(proyecto_dir),
                capture_output=True,
                text=True,
                check=True,
            )

            if resultado_status.stdout.strip():
                mensaje = f"Actualización automática de noticias ({datetime.now().strftime('%Y-%m-%d %H:%M')})"
                subprocess.run(
                    ["git", "commit", "-m", mensaje],
                    cwd=str(proyecto_dir),
                    check=True,
                )

                # git push
                subprocess.run(
                    ["git", "push", "origin", "RED"],
                    cwd=str(proyecto_dir),
                    check=True,
                )
                print("✅ Push a GitHub completado correctamente.")
            else:
                print("ℹ️  No hay cambios nuevos que enviar. Repositorio ya actualizado.")

    except subprocess.CalledProcessError as e:
        print(f"⚠️  Error al ejecutar comandos Git (código {e.returncode}).")
        print("    Revisa el mensaje de error anterior y, si es necesario, haz el push manualmente.")
    except Exception as e:
        print(f"⚠️  Error inesperado durante el push automático: {e}")

    print("\n💡 Recomendado:")
    print("  1. Revisar los cambios: abre index.html en tu navegador")
    print("  2. Verificar en GitHub que el push se haya aplicado correctamente")
    print("\n✨ ¡Listo para publicar!\n")

    return True


if __name__ == "__main__":
    exito = main()
    sys.exit(0 if exito else 1)

