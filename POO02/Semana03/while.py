"""
while True:#representa un bucle infino
    #codigo
    pass #no genere ningun error en el bucle

contador=1
while contador<=10:
    print(contador)
    contador+=1
    
"""

#inicializar las variable
lista_productos=[]#lista vacia
productos=''#variable producto


while productos!='echo':
    productos=input("Ingrese el nombre del producto:(si no deseas ingresar mas registros escribe la palabra 'echo')")
    #agregar un producto en lista
    lista_productos.append(productos)

contador=1
indice=0
 
while indice<len(lista_productos):
    print(f"{contador}.{lista_productos[indice]}")
    contador+=1
    indice+=1






