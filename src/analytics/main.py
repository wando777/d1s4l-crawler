from src.analytics.processador.grupo_cotas_processador import GruposCotasProcessor

def main():
    # Iniciar o processador de dados de cotas
    processor = GruposCotasProcessor('/Users/wanderson.leite/Desktop/wando/projetos/disal-crawler/20240929_c3e23383_grupos_cotas.csv')
    sorteio = 1600  # Exemplo de número de sorteio
    # resultado = processor.find_closest_cotas(sorteio)
    processor.save_closest_cotas_to_csv(sorteio, "sorteio.csv")
    print("salvou")

# Exemplo de uso
if __name__ == "__main__":
    main()
    