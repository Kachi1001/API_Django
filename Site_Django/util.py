class tempo:
    def formatarDecimal(valor):
        if valor >= 10:
            return str(valor)
        else:
            return '0'+str(valor) 
    
    def formatarHTML(valor):
        return str(valor.year)+ '-' + tempo.formatarDecimal(valor.month) + '-' + tempo.formatarDecimal(valor.day)