from processador.GrupoCotasProcessor import GruposCotasProcessor

def main():
    # Iniciar o processador de dados de cotas
    processor = GruposCotasProcessor('/Users/wanderson.leite/Desktop/wando/projetos/disal-crawler/grupos_cotas.csv')
    sorteio = 2416  # Exemplo de número de sorteio
    # resultado = processor.find_closest_cotas(sorteio)
    processor.save_closest_cotas_to_csv(sorteio, "sorteio.csv")
    print("salvou")

# Exemplo de uso
if __name__ == "__main__":
    main()
    