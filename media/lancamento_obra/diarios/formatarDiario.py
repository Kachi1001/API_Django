from pathlib import Path    
import os

# arquivos = Path(os.path.dirname(os.path.abspath(__file__)))
# for child in arquivos.iterdir():
#     if not (child.suffix in [".jpg",'.py']):
#         try:
#             formatado = child.stem + '.jpg'
#             os.rename(child, os.path.join(arquivos, formatado))
#         except:
#             os.remove(os.path.join(arquivos, formatado))
#             os.rename(child, os.path.join(arquivos, formatado))
# print(input("Finalizados com sucesso")) 
def adicionarZero(valor):
    valor = int(valor)
    if valor <= 9:
        return '0' + str(valor) +'-'
    else:
        return str(valor) + '-'
    
dir = Path(os.path.dirname(os.path.abspath(__file__)))
for child in dir.iterdir():
    if not (child.suffix in ['.py','.db']):
        print(child)

        formatado = child.stem.split('_')
        data = formatado[1].split('-')
        if data[0] != '2024':
            print(data)
            
            newdata =[0,0,0]
            newdata[0] = data[1]
            newdata[1] = data[2][:2]
            newdata[2] = data[2][2:]
            print(newdata)
            data = adicionarZero(newdata[2]) + adicionarZero(newdata[1]) +  newdata[0]
            
            formatado[1] = data
            formatado = formatado[0] + '_' + formatado[1] + '_' + formatado[2]+ '.jpg'

            print (formatado)
            os.rename(child, os.path.join(dir, formatado))
            
print(input("Finalizados com sucesso"))