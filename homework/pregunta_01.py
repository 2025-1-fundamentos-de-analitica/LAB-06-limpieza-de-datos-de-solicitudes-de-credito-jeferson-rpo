"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""



import pandas as pd
import os


def limpiar_texto(df, columna):
    df[columna] = (
        df[columna]
        .str.lower()
        .str.strip()
        .str.replace("_", " ")
        .str.replace("-", " ")
        .str.replace(",", "")
        .str.replace(".00", "")
        .str.replace("$", "")
        .str.strip()
    )
    return df


def cargar_datos(ruta):
    return pd.read_csv(ruta, sep=";", index_col=0)


def procesar_datos(ruta_entrada, ruta_salida):
    df = cargar_datos(ruta_entrada)

    columnas_texto = [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "monto_del_credito",
        "línea_credito",
    ]

    for col in columnas_texto:
        df = limpiar_texto(df, col)

    df["barrio"] = df["barrio"].str.lower().str.replace("_", " ").str.replace("-", " ")

    df["comuna_ciudadano"] = pd.to_numeric(df["comuna_ciudadano"], errors="coerce")
    df["monto_del_credito"] = pd.to_numeric(df["monto_del_credito"], errors="coerce")

    fecha_1 = pd.to_datetime(df["fecha_de_beneficio"], format="%d/%m/%Y", errors="coerce")
    fecha_2 = pd.to_datetime(df["fecha_de_beneficio"], format="%Y/%m/%d", errors="coerce")
    df["fecha_de_beneficio"] = fecha_1.combine_first(fecha_2)

    df = df.drop_duplicates()
    df = df.dropna()

    guardar_salida(df, "solicitudes_de_credito", ruta_salida)


def guardar_salida(df, nombre_archivo, carpeta_salida):
    os.makedirs(carpeta_salida, exist_ok=True)
    df.to_csv(os.path.join(carpeta_salida, f"{nombre_archivo}.csv"), sep=";", index=False)


def pregunta_01():
    """
    Limpieza del archivo 'files/input/solicitudes_de_credito.csv'
    y escritura del resultado limpio en 'files/output/solicitudes_de_credito.csv'
    """
    procesar_datos(
        ruta_entrada="files/input/solicitudes_de_credito.csv",
        ruta_salida="files/output"
    )


if __name__ == "__main__":
    pregunta_01()
