import csv
from typing import List, Dict


class GruposCotasProcessor:
    def __init__(self, grupos_cotas: Dict[str, List[str]]):
        self.grupos_cotas = grupos_cotas

    def _normalize_grupos_cotas_keys(self):
        """Normaliza as chaves do dicionário para strings de inteiros."""
        self.grupos_cotas = {
            str(int(key)): value for key, value in self.grupos_cotas.items()
        }

    def find_closest_cotas(self, sorteio: int) -> dict[str, dict]:
        """
        Busca as cotas mais próximas em cada grupo com base nas regras definidas.

        Retorna um dicionário onde cada grupo possui:
        - cotas: lista das cotas filtradas
        - referencia: o número usado como referência para o cálculo
        """
        # Normalizar as chaves do dicionário
        self._normalize_grupos_cotas_keys()

        # Regras de negócio
        regras = {
            "990": [3301, 3302],
            "1600": [
                3303,
                3304,
                3305,
                3306,
                3307,
                3308,
                3309,
                3310,
                3311,
                3312,
                3313,
                3314,
                3315,
                3316,
                3317,
                3318,
            ],
            "9999": [3319, 3320, 3321, 3322, 3323, 3324],
        }

        # Extrair os últimos 4 dígitos do sorteio
        ultimos_4_digitos = sorteio % 10000

        # Função auxiliar para calcular a referência
        def calcular_referencia(limite: str) -> int:
            if limite == "990":
                return sorteio % 1000  # Últimos 3 dígitos
            elif limite == "1600":
                referencia = ultimos_4_digitos
                return referencia % 1600
            elif limite == "9999":
                return ultimos_4_digitos
            return 0

        # Inicializar o dicionário de resultados
        result = {}

        # Iterar sobre as regras e aplicar as condições
        for limite, grupos in regras.items():
            referencia = calcular_referencia(limite)
            for grupo in grupos:
                grupo_str = str(grupo)  # Garantir que a chave seja uma string
                if grupo_str in self.grupos_cotas:
                    # Filtrar as cotas que estão dentro do intervalo desejado
                    cotas_filtradas = [
                        cota
                        for cota in self.grupos_cotas[grupo_str]
                        if referencia - 10 <= int(cota) <= referencia
                    ]

                    # Ordenar as cotas pela proximidade ao número de referência
                    cotas_filtradas.sort(key=lambda x: abs(referencia - int(x)))

                    # Adicionar ao resultado apenas se houver cotas filtradas
                    if cotas_filtradas:
                        result[grupo_str] = {
                            "cotas": cotas_filtradas,
                            "referencia": referencia,
                        }
        print(result)
        
        return result

    def _load_csv(self) -> Dict[str, List[int]]:
        with open(self.csv_file, mode="r") as file:
            reader = csv.DictReader(file)
            return {
                row["Grupo"]: list(map(int, row["Cotas"].split(", "))) for row in reader
            }

    def save_closest_cotas_to_csv(self, sorteio: int, output_csv_file: str):
        closest_cotas = self.find_closest_cotas(sorteio)
        with open(output_csv_file, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Grupo", "Cotas"])
            for grupo, cotas in closest_cotas.items():
                writer.writerow([grupo, ", ".join(map(str, cotas))])
