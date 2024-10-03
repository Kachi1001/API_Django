from django.utils import timezone

def formatarDecimal(valor):
    if valor >= 10:
        return str(valor)
    else:
        return '0'+str(valor) 

def formatarHTML(valor):
    return str(valor.year)+ '-' + formatarDecimal(valor.month) + '-' + formatarDecimal(valor.day)

def get_hoje():
    return timezone.now().date()
