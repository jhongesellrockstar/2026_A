#for valores in range(10):
#    print(valores)
    
##BREAK#####    
#for valores in range(10):
#    if valores==5:
#        break
#    print(valores)

##CONTINUE#####    
for valores in range(10):
    if valores==5:
        continue
    print(valores)

#inicializar las variable
lista_productos=[]#lista vacia
productos=''#variable producto


while productos!='echo':
    productos=input("Ingrese el nombre del producto:(si no deseas ingresar mas registros escribe la palabra 'echo')")
    if productos=='echo':
        break
    #agregar un producto en lista
    lista_productos.append(productos)

for indice,valor in enumerate(lista_productos,start=1):
    print(f"{indice}.{valor}")
