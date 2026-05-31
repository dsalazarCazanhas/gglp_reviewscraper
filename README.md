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
	- `APP_ID`: package name de la app.
	- `TARGET_RATINGS`: lista de puntajes a extraer (por defecto `[1,2,3]`).
	- `CUT_OFF_DATE`: fecha mínima (ej. `datetime(2021,1,1)`).
	- `SCRAPE_COUNT`: número de reseñas por llamada (máx. 200 recomendado).

Ver la configuración en [src/gglp_reviewscraper/main.py](src/gglp_reviewscraper/main.py#L1-L200).

**Salida**:
- Genera un CSV con las reseñas filtradas (nombre por defecto en la raíz del proyecto).

**Notas**:
- El scraper verifica la IP pública y aborta si detecta una IP desde México por la configuración actual.
- Para grandes volúmenes (decenas de miles) se usa paginación y se corta por fecha para evitar descargar todo el histórico.

---
Pequeño, directo y configurable. ¿Quieres que añada ejemplos de configuración o badges de estado?
