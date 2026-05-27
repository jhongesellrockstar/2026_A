nombre=input("Ingrese su nombre")#cadena

edad=int(input("Ingrese su edad"))#cadena->int
sueldo=float(input("Ingrese su sueldo"))#cadena->float

prestamo=input("Ingrese su prestamo")
prestamo=float(prestamo)

#la funcion input siempre retorna un valor string o cadena

print(f"Mi nombre es{nombre} y tengo {edad}, tengo un sueldo de {sueldo}")

import sys
data=sys.argv #se guarda en una lista 
print(data)
print(data[0])