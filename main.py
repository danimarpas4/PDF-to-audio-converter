import os
import asyncio # Necesario para la nueva librería
import edge_tts # El nuevo motor de voz
from pypdf import PdfReader, PdfWriter

# --- 1. CONFIGURACIÓN ---
nombre_archivo_pdf = "documento.pdf"
carpeta_salida = "material_por_temas"

# Elige tu voz favorita. Opciones en español:
# "es-ES-AlvaroNeural" (Hombre, España - Muy buena)
# "es-ES-ElviraNeural" (Mujer, España - Muy buena)
# "es-MX-DaliaNeural"  (Mujer, México)
VOZ_ELEGIDA = "es-ES-AlvaroNeural"

# TUS TEMAS (He corregido los nombres para evitar errores con barras /)
temas = {
    "01_Reales_:Ordenanzas": (11, 21),    # Lee de la página 1 a la 2
    "02_Seguridad_Fuerzas_Armadas":     (25, 32),    # Lee de la 3 a la 5
    "03_Normas_Mando": (35, 46) ,    # Lee solo la página 6
    "04_Régimen disciplinario de las Fuerzas Armadas":     (49, 62),
    "05_Codigo_Penal_Militar":     (64, 74),
    "06_Instrucción 14-2021 por la que se desarrolla la organización del Ejército de Tierra":     (77, 87),
    "07_Ley 39-2007 de la carrera militar. Situaciones administrativas del personal de las Fuerzas Armadas":     (88, 92),
    "08_LEY ORGÁNICA 9-2011, DE DERECHOS Y DEBERES DE LOS MIEMBROS DE LAS FUERZAS ARMADAS":     (95, 103),
    "11_Instrucción técnica de combate":     (119, 155),
    "12_Instrucción táctica. Escuadra-Equipo":     (156, 160),
    "13_Cartografía":     (163, 172),
    "14_Orientación":     (173, 184),
    "15_Navegación":     (185, 185),
    "16_ARMAMENTO Y TEORÍA DEL TIRO":     (189, 236),
}

# --- FUNCIÓN AUXILIAR PARA GENERAR AUDIO ---
async def crear_audio_microsoft(texto, archivo_salida):
    comunicate = edge_tts.Communicate(texto, VOZ_ELEGIDA)
    await comunicate.save(archivo_salida)

# --- PROGRAMA PRINCIPAL ---
async def main():
    print(f"--- Iniciando proyecto con MOTOR MICROSOFT: {nombre_archivo_pdf} ---")

    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)

    try:
        reader = PdfReader(nombre_archivo_pdf)
        total_paginas_pdf = len(reader.pages)

        # Bucle por temas
        for nombre_tema, (pag_inicio, pag_fin) in temas.items():
            
            nombre_pdf = f"{nombre_tema}.pdf"
            nombre_mp3 = f"{nombre_tema}.mp3"
            ruta_pdf = os.path.join(carpeta_salida, nombre_pdf)
            ruta_mp3 = os.path.join(carpeta_salida, nombre_mp3)

            # 1. VERIFICACIÓN (Si ya existen ambos, saltamos)
            if os.path.exists(ruta_pdf) and os.path.exists(ruta_mp3):
                print(f"⏩ Saltando: {nombre_tema} (Ya completado).")
                continue

            print(f"\nProcesando: {nombre_tema} (Págs {pag_inicio}-{pag_fin})...")
            
            if pag_fin > total_paginas_pdf:
                pag_fin = total_paginas_pdf

            texto_acumulado = ""
            escritor_pdf = PdfWriter()

            # 2. EXTRAER TEXTO Y CREAR PDF
            for i in range(pag_inicio - 1, pag_fin):
                pagina = reader.pages[i]
                escritor_pdf.add_page(pagina)
                
                texto = pagina.extract_text()
                
                if texto:
                    # --- LIMPIEZA DE TEXTO (NUEVO) ---
                    # 1. Cambiamos los saltos de línea (\n) por espacios simples
                    texto_limpio = texto.replace('\n', ' ')
                    
                    # 2. (Opcional) A veces quedan espacios dobles, los quitamos
                    texto_limpio = texto_limpio.replace('  ', ' ')
                    
                    # 3. Añadimos el texto limpio al acumulador
                    texto_acumulado += texto_limpio + " "
            # Guardar PDF pequeño
            with open(ruta_pdf, "wb") as f:
                escritor_pdf.write(f)
            print(f"  [PDF] Generado.")

            # 3. GENERAR AUDIO CON MICROSOFT (EDGE-TTS)
            if texto_acumulado.strip():
                print(f"  [MP3] Generando audio de alta calidad...")
                try:
                    # Llamamos a la función asíncrona
                    await crear_audio_microsoft(texto_acumulado, ruta_mp3)
                    print(f"  ✅ ¡ÉXITO! Audio guardado: {nombre_mp3}")
                except Exception as e:
                    print(f"  ❌ Error al generar audio: {e}")
            else:
                print("  ⚠️ No había texto para leer.")

    except FileNotFoundError:
        print("ERROR: No encuentro el archivo PDF.")
    except Exception as e:
        print(f"Error crítico: {e}")

    print("\n" + "="*30)
    print("¡PROCESO TERMINADO!")

# Ejecutar el programa
if __name__ == "__main__":
    asyncio.run(main())