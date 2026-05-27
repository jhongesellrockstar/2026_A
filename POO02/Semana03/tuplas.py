tupla_valores=(45,40,1,'fiis',2.5)
print(type(tupla_valores))
print(tupla_valores)
#tupla_valores[0]="Fiis"
#print(tupla_valores[0])

mi_lista=list(tupla_valores)
print(mi_lista)
mi_lista[0]="FIIS UNAC Winner"
tupla_valores=tuple(mi_lista)
print(tupla_valores)
