**gglp_reviewscraper**

Herramienta pequeña para extraer reseñas desde Google Play Store y guardar las reseñas de 1, 2 y 3 estrellas.

**Requisitos**:

- Python 3.14+
- Dependencias gestionadas con `poetry` (ver `pyproject.toml`).

**Instalación**:

```bash
poetry install
```

**Uso**:

Ejecuta el script principal:

```bash
python src/gglp_reviewscraper/main.py
```

Opcional (con `poetry`):

```bash
poetry run python src/gglp_reviewscraper/main.py
```

**Configuración**:

- Cambia los valores en `src/gglp_reviewscraper/main.py` dentro del diccionario `CONFIG`:
  - `APP_ID`: package name de la app, seleccionado desde el diccionario `APPS` (ej. `APPS["banco_bienestar"]` o `APPS["imss_publico"]`). Para agregar una app nueva, añade su package name a `APPS`.
  - `TARGET_RATINGS`: lista de puntajes a extraer (por defecto `[1,2,3]`).
  - `CUT_OFF_DATE`: fecha mínima; se corta la paginación al llegar a una reseña anterior a esta fecha.
  - `SCRAPE_COUNT`: número de reseñas por llamada (máx. 200 recomendado).
  - `SCRAPE_LANG` / `SCRAPE_COUNTRY`: idioma y país usados en la consulta a Google Play (por defecto `es` / `mx`).
  - `IP_CHECK_URL` / `IP_CHECK_TIMEOUT`: servicio y timeout usados para el chequeo informativo de origen de IP (ver Notas).

El nombre del CSV de salida se calcula en runtime a partir de `APP_ID` (ver `build_output_filename` en el código), por lo que siempre coincide con la app configurada.

Ver el diccionario `CONFIG` en [src/gglp_reviewscraper/main.py](src/gglp_reviewscraper/main.py#L16-L26).

**Salida**:

- Genera un CSV por ejecución con las reseñas filtradas, en la raíz del proyecto, con nombre `reviews_<app_id>_<fecha>_<hora>.csv`.

**Notas**:

- El scraper consulta la IP pública y muestra un warning con el país de origen detectado, recomendando usar VPN y respetar las buenas prácticas de scraping de Google. No hay forma confiable de verificar si la conexión ya usa VPN, así que este chequeo es solo informativo y nunca bloquea la ejecución (ni por país, ni si el servicio de IP falla).
- Para grandes volúmenes (decenas de miles) se usa paginación y se corta por fecha para evitar descargar todo el histórico.

---
Pequeño, directo y configurable.
