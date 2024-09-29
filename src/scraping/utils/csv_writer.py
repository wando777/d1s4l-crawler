# src/scraping/utils/csv_writer.py
import csv
from datetime import datetime
import uuid


class CSVWriter:
    @staticmethod
    def gerar_csv(grupos_cotas, nome_arquivo="grupos_cotas.csv"):
        data_atual = datetime.now().strftime("%Y%m%d")
        identificador_unico = uuid.uuid4().hex[:8]
        nome_arquivo = f"{data_atual}_{identificador_unico}_{nome_arquivo}"
        with open(nome_arquivo, mode="w", newline="", encoding="utf-8") as arquivo_csv:
            escritor_csv = csv.writer(arquivo_csv)
            escritor_csv.writerow(["Grupo", "Cotas"])
            for grupo, cotas in grupos_cotas.items():
                escritor_csv.writerow([grupo, ", ".join(cotas)])
        print(f"Arquivo CSV '{nome_arquivo}' gerado com sucesso!")
