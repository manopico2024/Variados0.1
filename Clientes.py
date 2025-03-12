import openpyxl
import pandas
from openpyxl import Workbook

# Criar as tabelas

wb = Workbook()

planilha = wb.worksheets.index(0)

planilha['a1'] = 'nome'
planilha['B2'] = 'endereço:'

wb.save("C:\User\MANO\MYCODES\CLIENTES.xlsx")
