numero=int(input("Ingrese un numero"))

if numero>0:
    if numero%2==0:
        print(f"El numero {numero} es par positivo")
    else:
        print(f"El numero {numero} es impar positivo")
elif numero<0:
    if numero%2==0:
        print(f"El numero {numero} es par negativo")
    else:
        print(f"El numero {numero} es impar negativo")
else:
    print(f"El numero ingresado es {numero}")



