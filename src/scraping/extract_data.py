from bs4 import BeautifulSoup

def extract_table_data():
    # Pegando o conteúdo HTML da página atual
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    # Encontrando a tabela específica
    table = soup.find('table', {'id': 'data_table'})

    # Extraindo as linhas da tabela
    rows = table.find_all('tr')

    data = []
    for row in rows:
        cells = row.find_all('td')
        data.append([cell.get_text(strip=True) for cell in cells])

    return data