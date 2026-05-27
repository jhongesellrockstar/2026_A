
#Ingrese la cantidad de consumo del cliente
total_consumo=float(input("Ingrese la cantidad de consumo en el resturante: "))
#Calculo de los descuento
if total_consumo>50 and total_consumo<=100:
    descuento_porcentaje=0.1
elif total_consumo>100 and total_consumo<=200:
    descuento_porcentaje=0.2
elif total_consumo>200:
    descuento_porcentaje=0.3
else: 
    descuento_porcentaje=0.0

#Calcula el moto final  con descuento

descuento_consumo=total_consumo*descuento_porcentaje
final_consumo=total_consumo-descuento_consumo

#Mostrar la informacion
print("\nResumen de la cuenta: ")
print(f"Monto de consumo S/.{total_consumo:.2f}")
print(f"Descuento aplicado {descuento_porcentaje*100:.0f}%")
print(f"Monto final con descuento {final_consumo:.2f}")

