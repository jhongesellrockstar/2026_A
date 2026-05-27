'''
#Palabras palindromas 
palabra=input("Ingrese  una palabra")
palabra=palabra.lower()#para que sea minuscula
#palindromo como es "luz azul" unirlos "luzazul"
#eliminar los espacios
palabra=palabra.replace(" ","")
#invertir la palabra
invertir_palabra=palabra[::-1]#invertir la palabra

if palabra==invertir_palabra:
    print(f"{palabra.capitalize()} es palindromo")
else:
    print("La palabra no es palindromo")
'''
palabra=input("Ingrese  una palabra").lower().replace(" ","")
print(f"{palabra.capitalize()} es palindromo" if palabra==palabra[::-1] else "La palabra no es palindromo")
