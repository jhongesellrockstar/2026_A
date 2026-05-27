frutas=["manzana","fresa","pera","lucuma"]
print(frutas)
frutas.append("uva")
print(frutas)
vegetales=["poro","apio","papa","nabo"]

frutas.extend(vegetales)
print(frutas)
frutas.insert(1,"melocoton")
print(frutas)
frutas.remove("apio")#este eliminar el elemento que coincida con la palabra de la lista frutas
print(frutas)
frutas.pop()#esto eliminar el ultimo elemento de la lista frutas
print(frutas)
frutas.pop(2)
print(frutas)
print(frutas.count("poro"))
frutas.reverse()
print(frutas)
