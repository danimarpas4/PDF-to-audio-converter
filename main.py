import os
import time
from pypdf import PdfReader
from gtts import gTTS

# --- 1. CONFIGURACIÓN ---
nombre_archivo_pdf = "documento.pdf"  # Cambia "documento.pdf" por el nombre del documento que quieres que lea y guardalo al lado del archivo "main.py"
carpeta_salida = "audios_por_temas"   # Cambia "audios_por_temas" por el nombre de la carpeta donde quieres que guarde el programa los archivos

# AQUÍ ES DONDE DEFINES TUS TEMAS
# Formato: "Nombre del archivo": (pagina_inicio, pagina_fin)
# Nota: Pon los números de página tal cual los ves en el visor de PDF
temas = {
    "01_Reales Ordenanzas para las fuerzas armadas": (11, 21),    # Lee de la página 11 a la 21
    "02_Seguridad en las Fuerzas Armadas":     (25, 32),    # Lee de la 25 a la 32
    "03_Normas sobre mando y regimen interior de las unidades e instalaciones del ejército de tierra": (35, 46) ,    
    "04_Régimen disciplinario de las Fuerzas Armadas":     (48, 62),
    "05_Código Penal Militar":     (64, 74),
    "06_Instrucción 14/2021 por la que se desarrolla la organización del Ejército de Tierra":     (77, 87),
    "07_Ley 39/2007 de la carrera militar. Situaciones administrativas del personal de las Fuerzas Armadas":     (88, 92),
    "08_LEY ORGÁNICA 9/2011, DE DERECHOS Y DEBERES DE LOS MIEMBROS DE LAS FUERZAS ARMADAS":     (95, 102),
    "09_RD 176/2014 Por el que se regula el procedimiento para la tramitación de iniciativas y quejas relativas al régimen personal y a las condiciones de vida que pueda plantear el militar":     (103, 103), # Lee solo la página 103
    "10_Modelo de liderazgo":     (106, 113),
    "11_Instrucción técnica de combate":     (119, 155),
    "12_Instrucción táctica. Escuadra/Equipo ":     (156, 160),
    "13_Cartografía":     (163, 172),
    "14_Orientación":     (173, 184),
    "15_Navegación":     (185, 185),
    "16_ARMAMENTO Y TEORÍA DEL TIRO":     (189, 236),
}

print(f"--- Iniciando conversión por temas de: {nombre_archivo_pdf} ---")

try:
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)

    reader = PdfReader(nombre_archivo_pdf)
    total_paginas_pdf = len(reader.pages)

    # --- 2. BUCLE POR CADA TEMA ---
    # Recorremos el diccionario 'temas' que definimos arriba
    for nombre_tema, (pag_inicio, pag_fin) in temas.items():
        
        print(f"\nProcesando: {nombre_tema} (Págs {pag_inicio}-{pag_fin})...")
        
        texto_acumulado_del_tema = ""

        # Verificación de seguridad (para no pedir páginas que no existen)
        if pag_fin > total_paginas_pdf:
            print(f"  AVISO: El tema termina en la pág {pag_fin}, pero el PDF solo tiene {total_paginas_pdf}.")
            pag_fin = total_paginas_pdf

        # --- 3. RECOLECTAR TEXTO DE LAS PÁGINAS DEL TEMA ---
        # Python range(a, b) llega hasta b-1, así que usamos pag_fin (sin restar) 
        # pero ajustamos el inicio con -1 porque las listas empiezan en 0.
        for i in range(pag_inicio - 1, pag_fin):
            pagina = reader.pages[i]
            texto_pagina = pagina.extract_text()
            
            if texto_pagina:
                texto_acumulado_del_tema += texto_pagina + "\n\n" # Añadimos saltos de línea
        
        # --- 4. CONVERTIR SI HAY TEXTO ---
        if texto_acumulado_del_tema.strip():
            print(f"  Texto extraído ({len(texto_acumulado_del_tema)} caracteres). Generando audio...")
            
            tts = gTTS(text=texto_acumulado_del_tema, lang='es')
            
            ruta_archivo = os.path.join(carpeta_salida, f"{nombre_tema}.mp3")
            tts.save(ruta_archivo)
            
            print(f"  ¡Guardado! -> {ruta_archivo}")
            
            # Pausa de cortesía para Google
            time.sleep(2)
        else:
            print("  No se encontró texto en este rango de páginas.")

    print("\n" + "="*30)
    print("¡PROCESO TERMINADO!")

except FileNotFoundError:
    print("ERROR: No encuentro el archivo PDF.")
except Exception as e:
    print(f"Ocurrió un error: {e}")
