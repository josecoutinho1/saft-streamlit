import xml.etree.ElementTree as ET

ficheiro_saft = 'saft_vendas.xml'

tree = ET.parse(ficheiro_saft)
root = tree.getroot()

print("Root tag:", root.tag)
print("Nó principal do ficheiro carregado com sucesso.")
import xml.etree.ElementTree as ET

ficheiro_saft = 'saft_vendas.xml'

tree = ET.parse(ficheiro_saft)
root = tree.getroot()

print("Root tag:", root.tag)
print("Nó principal do ficheiro carregado com sucesso.")

import xml.etree.ElementTree as ET

# Caminho para o ficheiro SAFT
ficheiro_saft = 'saft_vendas.xml'

# Carrega o ficheiro XML
tree = ET.parse(ficheiro_saft)
root = tree.getroot()

# Lista todos os elementos <Invoice>
invoices = []
for elem in root.iter():
    if elem.tag.lower().endswith("invoice"):
        invoices.append(elem)

# Soma os valores de GrossTotal
total_faturado = 0.0
faturas_com_valor = 0

for invoice in invoices:
    for elem in invoice.iter():
        if elem.tag.lower().endswith("grosstotal"):
            try:
                total_faturado += float(elem.text)
                faturas_com_valor += 1
            except (TypeError, ValueError):
                continue

# Apresentar resultado
print(f"\n💰 Total faturado com IVA: {total_faturado:.2f} €")
print(f"📄 Número de faturas com valor: {faturas_com_valor}")

