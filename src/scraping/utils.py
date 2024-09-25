import pandas as pd

def process_table_data(data):
    # Transformando os dados em um DataFrame do Pandas
    df = pd.DataFrame(data, columns=['Coluna1', 'Coluna2', 'Coluna3'])

    # Exemplo de manipulação: Filtrar dados, calcular médias, etc.
    df_filtered = df[df['Coluna1'] > 100]

    # Salvar em CSV se necessário
    df_filtered.to_csv('data/extracted_data.csv', index=False)

    return df_filtered