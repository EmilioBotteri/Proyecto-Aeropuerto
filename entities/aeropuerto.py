import pandas as pd
from datetime import timedelta
from entities.slot import Slot
class Aeropuerto:

    def __init__(self, vuelos: pd.DataFrame, slots: int, t_embarque_nat: int, t_embarque_internat: int):
        self.df_vuelos = vuelos
        self.n_slots = slots
        self.slots = {}
        self.tiempo_embarque_nat = t_embarque_nat
        self.tiempo_embarque_internat = t_embarque_internat

        for i in range(1, self.n_slots + 1):    #  {1: <Slot instancia con id=None, fechas=None>,
            self.slots[i] = Slot()              #  2: <Slot instancia con id=None, fechas=None>}
 
        self.df_vuelos['fecha_despegue'] = pd.NaT   
        self.df_vuelos['slot'] = 0

    def calcula_fecha_despegue(self, row) -> pd.Timestamp:
        time_nac = timedelta(minutes = self.tiempo_embarque_nat)
        time_int = timedelta(minutes = self.tiempo_embarque_internat)
        if row["tipo_vuelo"] == "NAT":
            fecha_despegue = row["fecha_llegada"] + time_nac
        else:
            fecha_despegue = row["fecha_llegada"] + time_int
        return fecha_despegue
    
    def encuentra_slot(self, fecha_vuelo, minutos_aplazo=30):
        fecha_busqueda = fecha_vuelo

        while True:
            for i in self.slots:
                if self.slots[i].slot_esta_libre_fecha_determinada(fecha_busqueda):
                    return i, fecha_busqueda  
            fecha_busqueda += timedelta(minutes=minutos_aplazo)


    def asigna_slot(self, vuelo) -> pd.Series:
        slot_encontrado, fecha_aterrizaje_real = self.encuentra_slot(vuelo["fecha_llegada"])
        vuelo["fecha_llegada"] = fecha_aterrizaje_real
        vuelo["slot"] = slot_encontrado
        vuelo["fecha_despegue"] = self.calcula_fecha_despegue(vuelo)
        
        self.slots[slot_encontrado].asigna_vuelo(vuelo["id"], vuelo["fecha_llegada"], vuelo["fecha_despegue"])

        return vuelo

    def asigna_slots(self):
        self.df_vuelos = self.df_vuelos.apply(self.asigna_slot, axis=1)
        return self.df_vuelos
    
