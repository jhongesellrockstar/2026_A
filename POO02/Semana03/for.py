"""
lista_valores=["Alex",20,4545,45.5]

for elemento_lista in lista_valores:
    print(elemento_lista)

cadena="UNAC-FIIS"
for caracter in cadena:
    print(caracter)
"""

#inicializar las variable
lista_productos=[]#lista vacia
productos=''#variable producto


while productos!='echo':
    productos=input("Ingrese el nombre del producto:(si no deseas ingresar mas registros escribe la palabra 'echo')")
    #agregar un producto en lista
    lista_productos.append(productos)

contador=1

 
for valores_producto in lista_productos:
    print(f"{contador}.{valores_producto}")
    contador+=1
    
