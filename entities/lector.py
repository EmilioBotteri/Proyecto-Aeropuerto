
import pandas as pd
import os
import json

class Lector:
    def __init__(self, path: str):
        self.path = path

    def _comprueba_extension(self):  # puede ser .txt , .json , .csv
        extension = os.path.splitext(self.path)[1]
        if extension == ".csv":   # os.path.splitext(self.path)[1] divide nombre y extension
            return LectorCSV(self.path).lee_archivo()         # y se queda solo con la extension
        elif extension == ".json":
            return LectorJSON(self.path).lee_archivo()
        elif extension == ".txt":
            return LectorTXT(self.path).lee_archivo()
        else:
            raise ValueError("La extension del archivo no es compatible")

    def lee_archivo(self):
        return self._comprueba_extension()

    @staticmethod
    def convierte_dict_a_csv(data: dict):
        return pd.DataFrame(data)


class LectorCSV(Lector):
    def __init__(self, path: str):
        super().__init__(path)

    def lee_archivo(self,datetime_columns=[]):
        base = os.getcwd()
        ruta_completa = os.path.join(base, self.path)
        df_lectura = pd.read_csv(ruta_completa)
        for col in datetime_columns:
            df_lectura[col] = pd.to_datetime(df_lectura[col])
        return df_lectura


class LectorJSON(Lector):
    def __init__(self, path: str):
        super().__init__(path)

    def lee_archivo(self):
        base = os.getcwd()
        ruta_completa = os.path.join(base, self.path)
        with open(ruta_completa) as archivo:
            lectura = json.load(archivo)
            df = pd.DataFrame(lectura)
            return df


class LectorTXT(Lector):
    def __init__(self, path: str):
        super().__init__(path)

    def lee_archivo(self):
        base = os.getcwd()
        ruta_completa = os.path.join(base, self.path)
        df = pd.read_csv(ruta_completa, sep=',', encoding='utf-8', skipinitialspace=True)
        return df


# prueba_json = Lector(r"C:\Users\emicl\OneDrive\Desktop\Proyecto Aeropuerto Modulo 6\data\vuelos_3.json")
# print(prueba_json.lee_archivo())
# 
# prueba_csv = Lector(r"C:\Users\emicl\OneDrive\Desktop\Proyecto Aeropuerto Modulo 6\data\vuelos_2.csv")
# print(prueba_csv.lee_archivo())
# 
# prueba_txt = Lector(r"C:\Users\emicl\OneDrive\Desktop\Proyecto Aeropuerto Modulo 6\data\vuelos_1.txt")
# print(prueba_txt.lee_archivo())
