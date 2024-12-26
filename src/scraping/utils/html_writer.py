import os

def write_html(data, filename):
    """
    Write the given data to an HTML file.

    :param data: Dictionary where keys are groups and values are lists of quotas.
    :param filename: The name of the HTML file to be created.
    """
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Tabela de cotas por grupo</title>
        <style>
            table {
                width: 50%;
                border-collapse: collapse;
                margin: auto;
            }
            table, th, td {
                border: 1px solid black;
            }
            th, td {
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
            }
        </style>
    </head>
    <body>
        <h1 style="text-align: center;">Resultados das Cotas</h1>
        <table>
            <tr>
                <th>Grupo</th>
                <th>Cotas</th>
            </tr>
    """

    # Add table rows
    for group, quotas in data.items():
        html_content += "<tr>"
        html_content += f"<td>{group}</td>"
        html_content += f"<td>{', '.join(quotas)}</td>"
        html_content += "</tr>"

    html_content += """
        </table>
    </body>
    </html>
    """

    # Write the HTML content to the file
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(html_content)

# Example usage
data = {
    '003303': ['524', '665', '739', '1265', '1460', '799', '1053', '941', '045', '1352', '974', '555', '1572', '1554', '540'],
    '003317': ['990', '1323', '1016', '1125', '450', '1432', '473', '958', '014', '676', '1275', '220', '125', '365', '328'],
    '003309': ['1381', '906', '655', '381', '975', '1012', '289', '820', '140', '1002', '1019', '998', '220', '1418', '457'],
    '003301': ['200', '798', '044', '040', '260', '591', '627', '811', '960', '801', '848', '121', '178', '797', '058'],
    '003315': ['133', '575', '824', '073', '521', '1253', '1322', '995', '196', '019', '166', '010', '1378', '344', '080'],
    '003312': ['831', '1348', '1187', '1482', '733', '635', '1171', '312', '823', '1430', '1594', '094', '468', '1475', '1527'],
    '003308': ['1553', '273', '1071', '1104', '451', '167', '378', '743', '004', '1332', '1227', '1580', '1092', '1136', '947'],
    '003304': ['443', '573', '545', '379', '448', '473', '467', '947', '1486', '692', '1353', '534', '1538', '1281', '732'],
    '003306': ['756', '1408', '880', '877', '506', '681', '326', '415', '1586', '295', '281', '722', '604', '1314', '1056'],
    '003314': ['1290', '216', '037', '762', '774', '1287', '716', '1059', '1016', '1132', '394', '1242', '1138', '102', '1555'],
    '003310': ['858', '1468', '648', '676', '359', '1548', '1150', '570', '820', '580', '350', '1425', '991', '127', '1460']
}

output_path = os.path.join(os.path.dirname(__file__), '../../../results.html')
# write_html(data, '/Users/wanderson.leite/Desktop/wando/projetos/disal-crawler/results.html')
write_html(data, output_path)