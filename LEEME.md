# El regalo de Yonis

La web ya incluye **56 fotos y 2 videos**, una caja de regalo animada y memoria del último recuerdo visto. Se prepararon 41 copias JPG de las fotos HEIC. Los originales de tu carpeta de origen no se modificaron. Los JPG y videos que ya eran compatibles se copiaron sin recomprimir.

## Archivos

```text
yonis-birthday/
├── index.html              ← Toda la web: diseño, animaciones y galería
├── media/                  ← Tus fotos y videos
├── generar.py              ← Actualiza la lista automáticamente
├── LEEME.md
└── .github/workflows/
    └── publicar.yml        ← Publicación automática en GitHub Pages
```

El archivo `index.html` ya está generado. Puedes abrirlo para ver el regalo, pero para comprobar la memoria del navegador de forma fiable usa la vista previa HTTP o el sitio publicado. El comportamiento de almacenamiento bajo `file://` depende del navegador.

## Personalizar

Abre `index.html` en un editor y busca `const CONFIG`. Cambia `name`, `quote` y `apology`. El título de cumpleaños y las fechas están en el HTML y también pueden editarse.

Opcionalmente, agrega anécdotas en `details`, utilizando la ruta real sin codificar:

```javascript
details: {
  'media/Mi viaje.jpg': {
    alt: 'Los dos durante nuestro viaje',
    caption: 'Ese día que siempre vamos a recordar.'
  }
}
```

No tienes que escribir las rutas para que las imágenes aparezcan; esta configuración sirve únicamente para añadir textos opcionales.

## Agregar o eliminar recuerdos

1. Agrega o elimina archivos dentro de `media`. Los nombres pueden llevar espacios y tildes.
2. Con GitHub Pages configurado, envía los cambios al repositorio. La automatización regenerará y publicará la web.
3. Para uso local o S3, abre Terminal en la carpeta del proyecto y ejecuta:

```sh
python3 generar.py
```

Requiere Python 3.9 o posterior. El script no instala dependencias. Ordena por nombre de manera natural (2 antes de 10), incluye subcarpetas e ignora archivos ocultos y enlaces simbólicos. No cambia tus textos ni el diseño. La lista se actualiza al preparar/publicar: el navegador no explora la carpeta remota.

La carpeta de origen `Yonis birthday` no está sincronizada: los cambios futuros deben hacerse en `media` o pedirme que vuelva a importar tus archivos.

Para volver a iniciar la vista previa local desde la carpeta del proyecto:

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

Luego visita `http://127.0.0.1:8765`. Esta dirección solo funciona en este computador; para compartir con tu amigo necesitas publicar el sitio.

## Fotos de iPhone y videos

- Las 41 imágenes HEIC iniciales ya se convirtieron a JPG conservando sus dimensiones; una conversión a JPG no es idéntica al archivo HEIC original.
- Para nuevos HEIC/HEIF, conviértelos a JPG antes de ponerlos en `media`. En Mac puedes abrirlos en Vista Previa y usar Archivo → Exportar → JPEG, guardando una copia. El script los detecta y avisa, pero no los convierte ni los publica.
- Los videos iniciales se conservaron tal cual. Se detectó H.264 en ambos; el MP4 también contiene audio AAC. El MOV se pudo reproducir en el navegador de la vista previa. Aun así, conviene probar en el teléfono de destino.
- La opción más compatible para nuevos videos es MP4 con H.264 y audio AAC. Cambiar `.mov` por `.mp4` no convierte el archivo.
- La descarga entrega el archivo que está en `media`, sin reducir su resolución. Para los HEIC convertidos entrega la copia JPG. Si el navegador no descarga directamente, aparece un enlace para abrir y guardar el archivo.
- Los videos comienzan pausados; al cambiar de recuerdo se detienen y vuelven al inicio.
- La presentación avanza las fotos cada 5 segundos y se detiene al llegar a un video. Si pulsas «Iniciar presentación» mientras estás en un video, continúa hacia el siguiente recuerdo.

## Publicar en GitHub Pages

**Todavía no se ha publicado nada.** Estos pasos activan la publicación cuando tú decidas.

1. Crea un repositorio y coloca el contenido de esta carpeta en su raíz. `index.html`, `generar.py`, `media` y `.github` deben quedar al mismo nivel; no dentro de otra carpeta adicional.
2. Usa GitHub Desktop o Git para enviar los archivos. Uno de tus videos pesa aproximadamente 53 MB: supera el límite de carga por navegador de 25 MiB, aunque está por debajo del límite de 100 MiB de un archivo normal del repositorio. Puede aparecer una advertencia por superar 50 MiB. No necesitas Git LFS para estos archivos. [Límites oficiales](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github).
3. Asegúrate de incluir `.github/workflows/publicar.yml`. En Finder puedes mostrar carpetas ocultas con `⌘ + Shift + .`.
4. La rama principal debe llamarse `main`. Si tiene otro nombre, cambia `branches: [main]` en `publicar.yml`.
5. En GitHub abre **Settings → Pages → Build and deployment → Source → GitHub Actions**.
6. Abre **Actions → Publicar el regalo → Run workflow** para la primera publicación después de configurar Pages. Luego cada actualización de `main` lo ejecutará automáticamente.
7. Espera a que termine y abre el enlace que aparece en **Settings → Pages** o en la ejecución de Actions.
8. Comprueba el enlace desde tu teléfono y comparte esa dirección con tu amigo.

La automatización prepara una carpeta pública que contiene únicamente el HTML y los archivos reconocidos de la galería. No publica esta guía ni el script en el sitio. Si el repositorio es público, sus archivos sí pueden verse en GitHub. GitHub Pages en repositorios privados depende del plan; un repositorio privado no implica que el sitio publicado sea privado. [Configuración oficial de workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

## Alternativa: Amazon S3

1. Ejecuta `python3 generar.py`.
2. Usa un bucket dedicado al regalo y sube `index.html` junto con `media`, manteniendo la estructura.
3. En **Properties → Static website hosting**, activa el alojamiento e indica `index.html` como documento inicial.
4. Para usar directamente el endpoint web público de S3, configura lectura pública de esos objetos según el tutorial oficial. Esto requiere ajustar Block Public Access y una política de lectura. No se ha cambiado ninguna configuración de tu cuenta.
5. Abre el endpoint web que muestra S3 y comprueba la galería.

El endpoint web directo de S3 usa HTTP. Para HTTPS, AWS recomienda CloudFront con acceso al origen (OAC), manteniendo privado el bucket; en esa alternativa configura `index.html` como objeto raíz de CloudFront y usa el origen normal de S3. El sitio puede seguir siendo público a través de CloudFront. [Tutorial oficial de S3 y alternativa con CloudFront](https://docs.aws.amazon.com/AmazonS3/latest/userguide/HostingWebsiteOnS3Setup.html).

## Visibilidad y memoria

Una web pública permite que otros accedan a las fotos y videos mediante su enlace. No incorpora contraseña ni cuentas. Publica solo el material que quieres compartir.

El último recuerdo y la apertura se guardan en el mismo navegador, dispositivo y dirección del sitio. Cambiar de navegador o dominio, usar modo privado o borrar sus datos puede reiniciar esa memoria. Si el navegador bloquea el almacenamiento, la galería funciona, pero no recuerda el progreso.

## Comprobaciones

Se comprobaron la apertura, la navegación y la presentación automática, el regreso al último recuerdo al recargar, la visualización en tamaño móvil y la reproducción de ambos videos con pausa al cambiar. Se revisó también la generación con carpeta vacía, un archivo, nombres con espacios/tildes/caracteres especiales y generación repetida sin modificar la configuración. En el navegador se verificaron también la galería vacía, un único archivo, la navegación tras un archivo ausente y el funcionamiento con almacenamiento bloqueado.

La publicación de GitHub Actions y la configuración de S3 quedan pendientes hasta que decidas usar una cuenta. Las pruebas locales no sustituyen una comprobación final del enlace publicado en el teléfono de tu amigo.
