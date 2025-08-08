import pandas as pd
import re

# Cargar archivos
def cargar_archivos():
    try:
        base_a = pd.read_csv("SerieA2024.csv", dtype=str)
        base_b = pd.read_excel("Establecimientos DEIS MINSAL 05-08-2025.xlsx", sheet_name=None, dtype=str, engine="openpyxl")
        return base_a, base_b
    except Exception as e:
        print("error al cargar archivos:", e)
        exit()

def normalizar_codigo(codigo):
    if pd.isna(codigo):
        return ""
    codigo = str(codigo).strip()
    codigo = re.sub(r'\.0+$', '', codigo)
    return codigo.zfill(8)

def encontrar_columna(df, nombres_posibles):
    for col in df.columns:
        if isinstance(col, str):
            for nombre in nombres_posibles:
                if nombre.lower() in col.lower():
                    return col
    return None

def buscar_en_establecimientos(codigo, hojas):
    encontrado_antiguo = False
    encontrado_nuevo = False
    for nombre_hoja, hoja in hojas.items():
        col_vigente = encontrar_columna(hoja, ["codigo vigente"])
        col_antiguo = encontrar_columna(hoja, ["codigo antiguo"])
        if col_vigente and any(normalizar_codigo(c) == codigo for c in hoja[col_vigente].dropna()):
            encontrado_nuevo = True
        if col_antiguo and any(normalizar_codigo(c) == codigo for c in hoja[col_antiguo].dropna()):
            encontrado_antiguo = True
    return encontrado_antiguo, encontrado_nuevo

def buscar_en_serie_a(codigo, df):
    # Ajuste aquí: se busca directamente por el nombre exacto "CodigoPrestacion"
    if "CodigoPrestacion" not in df.columns:
        return False
    return any(normalizar_codigo(c) == codigo for c in df["CodigoPrestacion"].dropna())

# Función principal
def main():
    base_a, hojas_b = cargar_archivos()

    while True:
        codigo_input = input("Ingrese el código (o escriba 'salir' para terminar): ").strip()
        if codigo_input.lower() == 'salir':
            break

        codigo = normalizar_codigo(codigo_input)

        if not codigo.isdigit() or len(codigo) != 8:
            print("❌ Código inválido. Debe tener 8 dígitos.")
            continue

        print(f"\nCódigo ingresado: {codigo}")

        # Buscar en SerieA2024
        existe_serie_a = buscar_en_serie_a(codigo, base_a)
        if existe_serie_a:
            print(f"SerieA2024 → El código de la base de datos SerieA2024 es {codigo}")
        else:
            print("SerieA2024 → NO ENCONTRADO")

        # Buscar en Establecimientos DEIS
        existe_antiguo, existe_vigente = buscar_en_establecimientos(codigo, hojas_b)
        if existe_antiguo:
            print(f"DEIS MINSAL (Código Antiguo) → El código en Establecimientos DEIS MINSAL (Código Antiguo) es {codigo}")
        else:
            print("DEIS MINSAL (Código Antiguo) → NO ENCONTRADO")

        if existe_vigente:
            print(f"DEIS MINSAL (Código Nuevo) → El código en Establecimientos DEIS MINSAL (Código Nuevo) es {codigo}")
        else:
            print("DEIS MINSAL (Código Nuevo) → NO ENCONTRADO")

        print("-" * 50)

# Asegura que se ejecute el main
if __name__ == "__main__":
    main()


