import csv
from typing import List, Dict

class GruposCotasProcessor:
    def __init__(self, grupos_cotas: Dict[str, List[str]]):
        self.grupos_cotas = grupos_cotas

    def _load_csv(self) -> Dict[str, List[int]]:
        with open(self.csv_file, mode="r") as file:
            reader = csv.DictReader(file)
            return {
                row["Grupo"]: list(map(int, row["Cotas"].split(", ")))
                for row in reader
            }

    def find_closest_cotas(self, sorteio: int) -> Dict[str, List[int]]:
        all_cotas = [
            (grupo, int(cota))
            for grupo, cotas in self.grupos_cotas.items()
            for cota in cotas
            if sorteio - 10 < int(cota) < sorteio
        ]

        all_cotas.sort(key=lambda x: abs(sorteio - x[1]))

        result = {}
        for grupo, cota in all_cotas:
            result.setdefault(grupo, []).append(cota)

        return result

    def save_closest_cotas_to_csv(self, sorteio: int, output_csv_file: str):
        closest_cotas = self.find_closest_cotas(sorteio)
        with open(output_csv_file, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Grupo", "Cotas"])
            for grupo, cotas in closest_cotas.items():
                writer.writerow([grupo, ", ".join(map(str, cotas))])
