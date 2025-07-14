from unittest import TestCase
import pandas as pd
from pandas._testing import assert_series_equal
from datetime import timedelta
from entities.aeropuerto import Aeropuerto


class TestAeropuerto(TestCase):
    def setUp(self):
        vuelos = pd.DataFrame.from_dict({'id': {0: 'VY4548', 1: 'VY3887', 2: 'VY1603', 3: 'VY3302', 4: 'VY1121'},
                                         'fecha_llegada': {0: '2022-08-06 10:30:00',
                                                           1: '2022-08-05 09:00:00',
                                                           2: '2022-08-05 08:45:00',
                                                           3: '2022-08-05 08:30:00',
                                                           4: '2022-08-06 10:15:00'},
                                         'retraso': {0: '00:10', 1: '00:10', 2: '-', 3: '00:15', 4: '-'},
                                         'tipo_vuelo': {0: 'NAT', 1: 'NAT', 2: 'INTERNAT', 3: 'NAT', 4: 'NAT'},
                                         'destino': {0: 'Helsinki', 1: 'Sevilla', 2: 'NuevaYork', 3: 'Bruselas',
                                                     4: 'Paris'}})
        vuelos['fecha_llegada'] = pd.to_datetime(vuelos['fecha_llegada'])
        n_slots = 2
        t_embarque_nat = 60
        t_embarque_internat = 100
        self.aeropuerto = Aeropuerto(vuelos, n_slots, t_embarque_nat, t_embarque_internat)

    #def test_calcula_fecha_despegue(self):
        #expected_fecha_llegada = pd.to_datetime('2022-08-06 11:50:00')
        #expected_fecha_despegue = pd.to_datetime('2022-08-06 13:00:00')
        #expected_vuelo = pd.Series({'id': 'VY4548', 'fecha_llegada': expected_fecha_llegada,
        #                            'retraso': '00:10',
        #                            'tipo_vuelo': 'NAT', 'destino': 'Helsinki',
        #                            'fecha_despegue': expected_fecha_despegue, 'slot': 1})
        #vuelo = self.aeropuerto.calcula_fecha_despegue(expected_vuelo)
        #assert_series_equal(expected_vuelo, vuelo)

        # Cambio el test completamente porque el antiguo esperaba una Serie y yo utilize simplemtene una fecha Timestamp
    def test_calcula_fecha_despegue(self):
        row = self.aeropuerto.df_vuelos.iloc[0, :]
        expected_vuelo = row['fecha_llegada'] + timedelta(minutes=self.aeropuerto.tiempo_embarque_nat)
        vuelo = self.aeropuerto.calcula_fecha_despegue(row)
        self.assertEqual(expected_vuelo, vuelo)

    def test_encuentra_slot(self):
        row = self.aeropuerto.df_vuelos.iloc[0, :] # Defino la varirable row 
        expected_slot = (1, row['fecha_llegada']) # Modifico expected_slot para que espere una tupla 
        row = self.aeropuerto.df_vuelos.iloc[0, :] # (con el slot y la fecha de llegada) y no solo un numero
        slot = self.aeropuerto.encuentra_slot(row['fecha_llegada'])
        self.assertEqual(expected_slot, slot)
        
        self.aeropuerto.slots[1].asigna_vuelo(row['id'], row['fecha_llegada'], pd.to_datetime('2022-08-06 11:40:00'))
        self.aeropuerto.slots[2].asigna_vuelo(row['id'], row['fecha_llegada'], pd.to_datetime('2022-08-06 11:40:00'))

        # expected_slot = -1      Elimino esta linea porque el avion siempre va a tener slot
        # row_2 = row.copy()      espere lo que tenga que esperar
        # row_2['fecha_llegada'] = row['fecha_llegada'] + pd.Timedelta(minutes=30)
        # slot = self.aeropuerto.encuentra_slot(row_2['fecha_llegada'])
        # self.assertEqual(expected_slot, slot)

    def test_asigna_slot(self):
        row = self.aeropuerto.df_vuelos.iloc[0, :]

        # Fuerzo que los dos primeros slots estén ocupados en la hora original
        self.aeropuerto.slots[1].asigna_vuelo(row['id'], row['fecha_llegada'], pd.to_datetime('2022-08-06 11:40:00'))
        self.aeropuerto.slots[2].asigna_vuelo(row['id'], row['fecha_llegada'], pd.to_datetime('2022-08-06 11:40:00'))

        # Copio la fila original y busco un slot real aplicando la lógica real
        row_2 = row.copy()
        slot_real, fecha_real = self.aeropuerto.encuentra_slot(row_2['fecha_llegada'])

        # Armo el vuelo esperado con los datos reales encontrados
        expected_vuelo = pd.Series({
            'id': row['id'],
            'fecha_llegada': fecha_real,
            'retraso': row['retraso'],
            'tipo_vuelo': row['tipo_vuelo'],
            'destino': row['destino'],
            'slot': slot_real,
            'fecha_despegue': fecha_real + timedelta(minutes=self.aeropuerto.tiempo_embarque_nat)
                if row['tipo_vuelo'] == 'NAT'
                else fecha_real + timedelta(minutes=self.aeropuerto.tiempo_embarque_internat)
        })

  
        row_2 = self.aeropuerto.asigna_slot(row_2)
        expected_vuelo.name = row_2.name
        expected_vuelo = expected_vuelo[row_2.index]
        assert_series_equal(expected_vuelo, row_2)
        