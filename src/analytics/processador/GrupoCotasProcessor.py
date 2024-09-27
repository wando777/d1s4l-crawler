import csv
from typing import List, Dict

class GruposCotasProcessor:
    def __init__(self, csv_file: str):
        self.csv_file = csv_file
        self.grupos_cotas = self._load_csv()

    def _load_csv(self) -> Dict[str, List[int]]:
        grupos_cotas = {}
        with open(self.csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                grupo = row['Grupo']
                cotas = list(map(int, row['Cotas'].split(', ')))
                grupos_cotas[grupo] = cotas
        return grupos_cotas

    def find_closest_cotas(self, sorteio: int) -> Dict[str, List[int]]:
        all_cotas = []
        for grupo, cotas in self.grupos_cotas.items():
            menores_cotas = [cota for cota in cotas if cota < sorteio]
            all_cotas.extend([(grupo, cota) for cota in menores_cotas])
        
        all_cotas.sort(key=lambda x: x[1], reverse=True)
        closest_cotas = all_cotas[:5]
        
        result = {}
        for grupo, cota in closest_cotas:
            if grupo not in result:
                result[grupo] = []
            result[grupo].append(cota)
        
        return result
    
    def save_closest_cotas_to_csv(self, sorteio: int, output_csv_file: str):
        closest_cotas = self.find_closest_cotas(sorteio)
        with open(output_csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Grupo', 'Cotas'])
            for grupo, cotas in closest_cotas.items():
                writer.writerow([grupo, ', '.join(map(str, cotas))])