#for valores in range(10):
#    print(valores)
    
#for valores in range(10,15):
#    print(valores)

#for valores in range(10,30,2):
#    print(valores)

#lista_frutas=["fresa","manzana","pera","platano"]

#for indice,valor in enumerate(lista_frutas):
#    print(indice,valor)

#inicializar las variable
lista_productos=[]#lista vacia
productos=''#variable producto


while productos!='echo':
    productos=input("Ingrese el nombre del producto:(si no deseas ingresar mas registros escribe la palabra 'echo')")
    #agregar un producto en lista
    lista_productos.append(productos)



 
for indice,valor in enumerate(lista_productos,start=1):
    print(f"{indice}.{valor}")
    