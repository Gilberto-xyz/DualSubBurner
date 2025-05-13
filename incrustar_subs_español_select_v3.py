import tkinter as tk
from tkinter import filedialog
import subprocess
import os
import shutil # Para verificar si ffmpeg está instalado

# --- Constantes de estilo para el subtítulo en español ---
FONTSIZE_ESPANOL = "25"  # Tamaño de fuente más grande
ALIGNMENT_ESPANOL = "2"  # 2 = Bottom Center (abajo, centrado)- antes era 10
MARGINV_ESPANOL = "60"   # Puedes ajustar este valor para subir o bajar el texto
# Estilo adicional para mejor legibilidad (texto blanco con borde negro)
STYLE_ESPANOL = f"Fontname=Tahoma,Fontsize={FONTSIZE_ESPANOL},Alignment={ALIGNMENT_ESPANOL},MarginV={MARGINV_ESPANOL},PrimaryColour=&H00FFFFEE,OutlineColour=&H80000000,BorderStyle=1,Outline=1,Shadow=0.5"
#100 lo deja en el centro

def verificar_ffmpeg():
    """Verifica si ffmpeg está instalado y en el PATH."""
    if shutil.which("ffmpeg") is None:
        print("Error: ffmpeg no está instalado o no se encuentra en el PATH del sistema.")
        print("Por favor, instala ffmpeg y asegúrate de que esté en el PATH.")
        print("Puedes descargarlo desde: https://ffmpeg.org/download.html")
        return False
    print("ffmpeg encontrado correctamente.")
    return True

def seleccionar_archivo_video():
    """Abre un diálogo para seleccionar un archivo de video."""
    root = tk.Tk()
    root.withdraw()
    filepath = filedialog.askopenfilename(
        title="Selecciona un archivo de video (MKV con ambos subtítulos)",
        filetypes=(("Archivos MKV", "*.mkv"),
                   ("Archivos de video", "*.mp4 *.avi *.mov"),
                   ("Todos los archivos", "*.*"))
    )
    if filepath:
        return filepath.replace("\\", "/")
    return None

def generar_nombre_salida(filepath_entrada):
    """Genera el nombre del archivo de salida añadiendo '_subs-inc'."""
    if not filepath_entrada:
        return None
    directorio, nombre_completo = os.path.split(filepath_entrada)
    nombre_base, extension = os.path.splitext(nombre_completo)
    # Siempre generamos .mkv para la salida
    nombre_salida = f"{nombre_base}_subs-inc.mkv"
    return os.path.join(directorio, nombre_salida).replace("\\", "/")

def escapar_ruta_ffmpeg(ruta):
    """Escapa caracteres especiales en una ruta para usarla en un filtro de ffmpeg."""
    if not ruta:
        return ""
    escapada = ruta.replace(":", "\\:")
    escapada = escapada.replace("'", "\\'")
    escapada = escapada.replace(",", "\\,")
    return escapada

def incrustar_subtitulos(filepath_entrada, filepath_salida):
    """
    Utiliza ffmpeg para incrustar dos streams de subtítulos (hardcode) desde el mismo video.
    El primer stream de subtítulos (índice 0, asumido inglés) se muestra tal cual.
    El segundo stream de subtítulos (índice 1, asumido español) se estiliza.
    """
    if not filepath_entrada or not filepath_salida:
        print("Error: Rutas de entrada o salida no válidas.")
        return False

    print(f"Procesando: {filepath_entrada}")
    print(f"Archivo de salida: {filepath_salida}")

    video_path_escaped_for_subs = escapar_ruta_ffmpeg(filepath_entrada)

    # Filtro para el primer stream de subtítulos (asumido inglés, índice 0)
    # se muestra con su estilo original (si lo tiene) o el default de ffmpeg.
    # Usamos 'si' como abreviatura de 'stream_index'.
    vf_sub1 = f"subtitles=filename='{video_path_escaped_for_subs}':stream_index=0"
    # Alternativamente, si=0 también funciona:
    # vf_sub1 = f"subtitles=filename='{video_path_escaped_for_subs}':si=0"

    # Filtro para el segundo stream de subtítulos (asumido español, índice 1)
    # con estilo forzado.
    vf_sub2 = f"subtitles=filename='{video_path_escaped_for_subs}':stream_index=1:force_style='{STYLE_ESPANOL}'"
    # Alternativamente, si=1 también funciona:
    # vf_sub2 = f"subtitles=filename='{video_path_escaped_for_subs}':si=1:force_style='{STYLE_ESPANOL}'"


    # Combinar ambos filtros. El orden importa: el último dibujado queda encima.
    # Si quieres que el español quede "encima" del inglés (en caso de solapamiento, poco probable con buena posición)
    # el orden actual es correcto.
    vf_option = f"{vf_sub1},{vf_sub2}"

    # Detectar GPU NVIDIA
    tiene_gpu = shutil.which("nvidia-smi") is not None

    comando_base = [
        'ffmpeg',
        '-i', filepath_entrada,
        '-vf', vf_option
    ]

    if tiene_gpu:
        print("GPU NVIDIA detectada. Usando codificación HEVC (h265_nvenc) con alta calidad.")
        comando_codec = [
            '-c:v', 'hevc_nvenc',
            '-preset', 'p1',    # Cambiado de p6 a p1 (calidad máxima)
            '-rc', 'vbr_hq',    # Cambiado de vbr a vbr_hq (alta calidad)
            '-cq', '18',        # Reducido de 23 a 18 (menor valor = mejor calidad)
            '-qmin', '10',      # Valor mínimo de cuantización
            '-qmax', '22',      # Valor máximo de cuantización 
            '-b:v', '0',
            '-c:a', 'copy',     # Copiar stream de audio
            '-y',
            filepath_salida
        ]
    else:
        print("No se detectó GPU NVIDIA. Usando codificación x264 por CPU.")
        comando_codec = [
            '-c:v', 'libx264',
            '-crf', '20',       # Calidad (0-51, menor es mejor)
            '-preset', 'medium', # Balance velocidad/compresión
            '-c:a', 'copy',    # Copiar stream de audio
            '-y',
            filepath_salida
        ]
    
    comando = comando_base + comando_codec

    print("\nEjecutando comando ffmpeg:")
    print(" ".join(f'"{arg}"' if " " in arg else arg for arg in comando)) # Mejorado para copiar y pegar

    try:
        creationflags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        proceso = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                                   text=True, encoding='utf-8', errors='replace', creationflags=creationflags)
        stdout, stderr = proceso.communicate()

        if proceso.returncode == 0:
            print("\n¡Proceso completado exitosamente!")
            print(f"Video con subtítulos incrustados guardado en: {filepath_salida}")
            return True
        else:
            print("\nError durante el procesamiento con ffmpeg.")
            print("Código de retorno:", proceso.returncode)
            print("Salida estándar (stdout):")
            print(stdout)
            print("Salida de error (stderr):")
            print(stderr)
            return False
    except FileNotFoundError:
        print("Error: El ejecutable de ffmpeg no se encontró. Asegúrate de que esté instalado y en el PATH.")
        return False
    except Exception as e:
        print(f"Ocurrió un error inesperado durante la ejecución de ffmpeg: {e}")
        return False


def main():
    if not verificar_ffmpeg():
        return

    archivo_video_entrada = seleccionar_archivo_video()
    if not archivo_video_entrada:
        print("No se seleccionó ningún archivo de video. Saliendo.")
        return
    print(f"Archivo de video seleccionado: {archivo_video_entrada}")

    archivo_video_salida = generar_nombre_salida(archivo_video_entrada)
    if not archivo_video_salida:
        print("No se pudo generar el nombre del archivo de salida. Saliendo.")
        return

    incrustar_subtitulos(archivo_video_entrada, archivo_video_salida)

if __name__ == "__main__":
    main()