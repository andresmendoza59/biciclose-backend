import csv
import os

# --- Configuración de Archivos ---
# Nombre del archivo CSV de entrada.
# Asegúrate de usar 'r' para rutas de Windows o barras inclinadas '/'.
CSV_FILE = r"C:\Users\pc\Documents\U. de M\2025-1\Proyecto de Ingeniería I\biciclose\stations\data\Estaciones_EnCicla_AMVA_20250525.csv"
# Nombre del archivo SQL de salida
SQL_OUTPUT_FILE = "encicla_stations_data.sql"

# --- Función Principal ---
def generate_sql_inserts_from_csv(csv_file):
    """
    Lee un archivo CSV con datos de estaciones de EnCicla y genera comandos SQL INSERT.
    """
    sql_statements = []

    try:
        with open(csv_file, mode='r', encoding='utf-8') as file:
            # Usamos csv.DictReader porque es más robusto y permite acceder a los datos por el nombre del encabezado.
            reader = csv.DictReader(file)

            # Opcional: Imprimir los encabezados que el DictReader ha detectado
            print(f"Encabezados detectados en el CSV: {reader.fieldnames}")

            for row_num, row_data in enumerate(reader, start=2): # 'row_num' para mensajes de error, 'start=2' para la línea real en el CSV
                # --- Extracción y Limpieza de Datos por Nombre de Encabezado ---
                try:
                    # Acceder a los datos usando los nombres EXACTOS de los encabezados de tu CSV.
                    # .get(key, default_value) es más seguro que row_data[key] por si una columna falta.
                    # .replace("'", "''") es crucial para escapar comillas simples en strings SQL.

                    # ID original de la estación (columna '#')
                    station_id = int(row_data.get('#', 0))

                    # Nombre de la estación
                    name = row_data.get('NOMBRE ESTACION', '').replace("'", "''").strip()

                    # Dirección
                    address = row_data.get('DIRECCION', '').replace("'", "''").strip()

                    # Municipio / Zona (usamos 'MUNICIPIO' para nuestro campo 'zone')
                    zone = row_data.get('MUNICIPIO', '').replace("'", "''").strip()

                    # Total Anclajes (capacidad)
                    capacity = int(row_data.get('TOTAL ANCLAJES', 0))

                    # Tipo / Estado (usamos 'TIPO' para nuestro campo 'status')
                    status = row_data.get('TIPO', '').replace("'", "''").strip()

                    # Coordenadas (Georeferenciación)
                    coords_str = row_data.get('Georeferenciación', '').strip()

                    # --- Parseo de Coordenadas ---
                    if ';' in coords_str:
                        # La primera parte es latitud, la segunda es longitud
                        # Asegúrate de reemplazar ',' por '.' si tu CSV usa comas para decimales
                        latitude_str, longitude_str = coords_str.split(';')
                        latitude = float(latitude_str.replace(',', '.'))
                        longitude = float(longitude_str.replace(',', '.'))
                    else:
                        print(f"Advertencia: Fila {row_num} - Formato de coordenadas inválido para '{name}' ('{coords_str}'), omitiendo estación.")
                        continue # Salta esta fila si las coordenadas no son válidas

                    # Opcional: Imprimir los datos extraídos para depuración
                    print(f"Procesando Fila {row_num}: ID={station_id}, Nombre='{name}', Lat={latitude}, Lon={longitude}")

                    # --- Construcción de la Sentencia SQL INSERT ---
                    # ST_MakePoint(longitude, latitude) espera LONGITUD primero, luego LATITUD.
                    # ST_SetSRID(..., 4326) asigna el Sistema de Referencia Espacial (SRID) WGS84.
                    sql = (
                        f"INSERT INTO encicla_stations (station_id, name, address, capacity, status, zone, geom) "
                        f"VALUES ({station_id}, '{name}', '{address}', {capacity}, '{status}', '{zone}', "
                        f"ST_SetSRID(ST_MakePoint({longitude}, {latitude}), 4326));"
                    )
                    sql_statements.append(sql)

                except ValueError as ve:
                    print(f"Error en la fila {row_num} (ID: {row_data.get('#', 'N/A')}): Error de conversión de tipo - {ve}. Fila: {row_data}")
                except Exception as e:
                    print(f"Error inesperado en la fila {row_num} (ID: {row_data.get('#', 'N/A')}): {e}. Fila: {row_data}")

    except FileNotFoundError:
        print(f"Error: El archivo '{csv_file}' no se encontró. Verifica la ruta.")
    except Exception as e:
        print(f"Error general al leer el CSV: {e}")

    return "\n".join(sql_statements)

# --- Ejecución del Script ---
if __name__ == "__main__":
    print("Iniciando script de generación SQL para estaciones EnCicla...")
    sql_inserts = generate_sql_inserts_from_csv(CSV_FILE)

    if sql_inserts:
        with open(SQL_OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(sql_inserts)

        print(f"\n¡Comandos SQL INSERT generados exitosamente en '{SQL_OUTPUT_FILE}'!")
        print(f"Para poblar tu base de datos, ejecuta en tu terminal (fuera de psql):")
        print(f"  psql -U your_db_user -d your_database_name -f {SQL_OUTPUT_FILE}")
        print("\n**Asegúrate de reemplazar 'your_db_user' y 'your_database_name' con tus credenciales reales.**")
    else:
        print("\nNo se generaron comandos SQL. Revisa los mensajes de error/advertencia anteriores y el contenido del CSV.")