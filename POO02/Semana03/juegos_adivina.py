import random

print("Bienvenido al Juego Adivina el numero")
numero_aletorio=random.randint(1,100)
intento_maximo=10
intentos_realizados=0
print(numero_aletorio)

while intentos_realizados<intento_maximo:
    intento=int(input("Ingrese un numero entre  1 y 100:"))
    intentos_realizados+=1
    
    if intento==numero_aletorio:
        print("Felicitaciones acertaste")
        break
    elif intento<numero_aletorio:
        print(f"El numero ingresado es menor.Te quedan {intento_maximo-intentos_realizados} intentos")
    else:
        print(f"El numero ingresado es mayor.Te quedam {intento_maximo-intentos_realizados} intentos")

if intentos_realizados==intento_maximo:
    print("Perdio el juego") 
    