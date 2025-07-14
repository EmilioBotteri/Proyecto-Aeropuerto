
import os
import pandas as pd
from entities.lector import Lector
from entities.aeropuerto import Aeropuerto
from entities.slot import Slot

def preprocess_data(df_list):
    
    df_list = [df.rename(columns=lambda col: col.strip()) for df in df_list]
    df = pd.concat(df_list, ignore_index=True)
    df["fecha_llegada"] = df["fecha_llegada"].astype(str).str.replace('T', ' ', regex=False)
    df['fecha_llegada'] = pd.to_datetime(df['fecha_llegada'], errors='coerce', format='%d/%m/%Y %H:%M')
    df = df.sort_values('fecha_llegada').reset_index(drop=True)
    df['slot'] = None
    df['fecha_despegue'] = pd.NaT
    return df


if __name__ == '__main__':
    path_1 = os.path.abspath('./data/vuelos_1.txt')
    path_2 = os.path.abspath('./data/vuelos_2.csv')
    path_3 = os.path.abspath('./data/vuelos_3.json')

    lector1 = Lector(path_1).lee_archivo()
    lector2 = Lector(path_2).lee_archivo()  # Leemos los archivos (clase Lector)
    lector3 = Lector(path_3).lee_archivo()

    df_total = preprocess_data([lector1, lector2, lector3])  # Preparamos los datos y juntamos df (clase preprocess_data)

    aeropuerto = Aeropuerto(df_total, slots=3, t_embarque_nat=30, t_embarque_internat=40) # Creamos la instancia
    resultado = aeropuerto.asigna_slots()  # Asignamos los slots a los vuelos (clase slot y aeropuerto)
    print(resultado)
