#estructura de una cadena
# cadena=|0|1|2|3|4|5|6|7|8|9
#texto=  "H o l a   m u n d o"

texto="python"
print(texto[5])
print(texto[-1])
print(len(texto))#indicar la cantidad de caracteres que tiene la cadena
#    cadena[inicio:final]
#print(texto[0:5])
#print(texto[2:])iniciara desde el indice 0 hasta el ultimo indice de la cadena 
print(texto[:2])#indica que tomara desde el indice cero hasta el 2

#texto[0]="P"
#print(texto[0])

nueva_variable="P"+texto[1:]
print(nueva_variable)
