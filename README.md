# Incrustar Subtítulos Español v3

¡Bienvenido! Este script te permite **incrustar dos pistas de subtítulos** (por ejemplo, inglés y español) directamente en un video MKV, generando un archivo final con ambos subtítulos visibles y estilizados. ¡Ideal para karaoke, aprendizaje de idiomas o simplemente disfrutar tus películas favoritas con subtítulos duales!

---

## 🚀 ¿Qué hace este script?

- **Carga un video MKV** que contenga al menos dos pistas de subtítulos (usualmente inglés y español).
- **Incrusta** (hardcode) ambos subtítulos en el video:
  - El primer subtítulo (índice 0, normalmente inglés) se muestra tal cual.
  - El segundo subtítulo (índice 1, normalmente español) se muestra con un estilo personalizado (color, tamaño, posición).
- **Genera un nuevo archivo MKV** con los subtítulos ya incrustados en la imagen del video.

---

## 🛠️ Requisitos

- **Python 3.7+**
- **ffmpeg** instalado y agregado al PATH del sistema.
- **Librerías Python**:
  - `tkinter` (incluida en la mayoría de instalaciones de Python)
  - `shutil`, `subprocess`, `os` (incluidas en la biblioteca estándar)

---

## ⚡ Instalación de ffmpeg

- Descarga ffmpeg desde [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
- Asegúrate de agregarlo al PATH de tu sistema para que el script lo encuentre.

---

## 📦 ¿Cómo usarlo?

1. **Guarda el script** [incrustar_subs_español_select_v3.py](incrustar_subs_español_select_v3.py) en la misma carpeta que tus videos.
2. **Ejecuta el script** desde la terminal o haciendo doble clic:
   ```sh
   python incrustar_subs_español_select_v3.py
   ```
3. **Selecciona el archivo de video** (debe ser MKV y tener al menos dos pistas de subtítulos).
4. El script generará un archivo nuevo con el sufijo `_subs-inc.mkv` en el mismo directorio.

---

## 💡 Consideraciones y Consejos

- **El video debe tener dos pistas de subtítulos**: la primera será el subtítulo base (inglés), la segunda será el subtítulo estilizado (español).
- **El orden de los subtítulos importa**: si tus subtítulos no están en el orden esperado, puedes reorganizarlos con herramientas como MKVToolNix.
- **El script detecta si tienes GPU NVIDIA** y usará codificación acelerada si está disponible (¡más rápido!).
- **El estilo del subtítulo español** se puede ajustar modificando la variable `STYLE_ESPANOL` en el script.
- **No modifica el archivo original**: siempre crea un nuevo archivo de salida.

---

## 🧩 Personalización

¿Quieres cambiar el color, tamaño o posición del subtítulo español? Edita la variable `STYLE_ESPANOL` en el script:

```python
STYLE_ESPANOL = f"Fontname=Tahoma,Fontsize=25,Alignment=2,MarginV=60,PrimaryColour=&H00FFFFEE,OutlineColour=&H80000000,BorderStyle=1,Outline=1,Shadow=0.5"
```

Consulta la [documentación de ASS/SSA](https://docs.aegisub.org/3.2/ASS_Tags/) para más opciones de estilo.

---

## 🐞 Problemas comunes

- **ffmpeg no encontrado**: Asegúrate de que ffmpeg esté instalado y en el PATH.
- **El video no tiene dos pistas de subtítulos**: Usa MKVToolNix para añadir o reorganizar subtítulos.
- **Errores de permisos**: Ejecuta la terminal como administrador si tienes problemas de escritura.

---

## 🎉 ¡Listo!

¡Disfruta tus videos con subtítulos duales y personalizados!  
Si tienes dudas o sugerencias, ¡anímate a mejorar el script!

---