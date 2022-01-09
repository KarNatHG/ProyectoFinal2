import csv

#Se crean los sets y diccionarios que serán utilizados. Se usan conjuntos para los 
transportation=set()    #En este set se guardarán los medios de transporte
income_exp_transp=dict()#En general los diccionarios tendran como clave lo que corresponde a la terminación de su nombre y como valor el ingreso total para tal clave. En este caso específico, este diccionario tendrá los ingresos totales obtenidos por los diferentes medios de transporte en operaciones de exportación
income_imp_transp=dict()#

exp_origin=set()
income_exp_origin=dict()

imp_origin=set()
income_imp_origin=dict()

exp_routes=set()
imp_routes=set()
income_exp_routes=dict()
income_imp_routes=dict()

#El archivo se abrirá dos veces, la primera para llenar los sets y la segunda para obtener los ingresos totales para cada categoría
#Se abre el archivo con la información y se crea el lector para archivos tipo csv
Archivo=open("synergy_logistics_database.csv","r")
lector = csv.reader(Archivo)
i=1 #variable auxiliar para leer y deshechar la primera linea del archivo
for linea in lector:
  if i==1:
    i=0
    continue
  transportation.add(linea[7])#llenar set con los diferentes medios de transporte, al ser un set, no se añadirán entradas repetidas
  if linea[1]=='Exports':     #Se tienen sets separados para importaciones e importaciones
    exp_origin.add(linea[2])
    exp_routes.add(linea[2]+'->'+linea[3])
  if linea[1]=='Imports':
    imp_origin.add(linea[2])
    imp_routes.add(linea[2]+'->'+linea[3])
Archivo.close()

#print(transportation)

#Se inicializan los diccionarios con todas sus claves correspondientes en 0 
for medio in transportation:
  income_exp_transp[medio]=0
  income_imp_transp[medio]=0
for pais in exp_origin:
  income_exp_origin[pais]=0
for pais in imp_origin:
  income_imp_origin[pais]=0
for ruta in exp_routes:
  income_exp_routes[ruta]=0
for ruta in imp_routes:
  income_imp_routes[ruta]=0

#print("income_exp_origin",len(income_exp_origin))
#print("income_imp_origin",len(income_imp_origin))

#Se abre el archivo para ahora obtener los ingresos totales y asignarlos en las diferentes claves de los diferentes diccionarios
Archivo=open("synergy_logistics_database.csv","r")
lector = csv.reader(Archivo)
i=1
for linea in lector:
  #print(linea)
  if i==1:
    i=0
    continue
  #se define una variable para generar las diferentes rutas
  ruta=linea[2]+'->'+linea[3]
  #Se determina si la operación es una exportación o importación para determinar qué diccionarios llenar.
  if linea[1]=="Exports":
    income_exp_transp[linea[7]]+=int(linea[9]) #Las claves y valores se obtienen directamente del archivo de texto y se suman directamete los ingresos a cada valor de la clave correspondiente
    income_exp_origin[linea[2]]+=int(linea[9])
    income_exp_routes[ruta]+=int(linea[9])

  if linea[1]=='Imports':
    income_imp_transp[linea[7]]+=int(linea[9])
    income_imp_origin[linea[2]]+=int(linea[9])
    income_imp_routes[ruta]+=int(linea[9])
Archivo.close()  

#Se define una función que obtiene los valores de un diccionario, los convierte en una lista, la ordena de mayor a menor y devuelve el resultado
def ordena_income(dictionary):
  lista=list(dictionary.values())
  lista.sort(reverse=True)
  return lista

#se obtienen las listas ordenadas de correspondientes a cada diccionario
list_income_exp_transp=ordena_income(income_exp_transp)
list_income_exp_origin=ordena_income(income_exp_origin)
list_income_exp_routes=ordena_income(income_exp_routes)

list_income_imp_transp=ordena_income(income_imp_transp)
list_income_imp_origin=ordena_income(income_imp_origin)
list_income_imp_routes=ordena_income(income_imp_routes)

#se obtiene el valor total de los ingresos para los medios de transporte y rutas por tipo de operación
total_exp_transp=sum(list_income_exp_transp)
total_exp_routes=sum(list_income_exp_routes)
total_imp_transp=sum(list_income_imp_transp)
total_imp_routes=sum(list_income_imp_routes)

#Se imprime la lista de los medios-rutas con mayores ingresos. Como el número está definido, no es necesario procesamiento extra.
print("Top 3 medios de transporte para exportacion")
print("Lugar,Medio,Ingresos totales,Porcentaje del total")
for top3 in range(0,3):
  for medio in transportation: #Para imprimir de manera ordenada debido a los ingresos (para cualquiera de las categorias) es duficiente con comparar el valor de la lista ordenada con todos los del diccionario, cuando se encuentre que coincide, se ha encontrado la clave (medio de transporte, ruta o pais de origen) correspondiente a la posición en la lista. Se imprime también el porcentaje que representa cada clave para hacer más fácil el análisis de cada opción.
    if list_income_exp_transp[top3]==income_exp_transp[medio]:
      print(f"{top3+1},{medio},{list_income_exp_transp[top3]},","{:.2f}".format(list_income_exp_transp[top3]*100/total_exp_transp),"%")

print("\nTop 3 medios de transporte para importacion")
print("Lugar,Medio,Ingresos totales,Porcentaje del total")
for top3 in range(0,3):
  for medio in transportation:
    if list_income_imp_transp[top3]==income_imp_transp[medio]:
      print(f"{top3+1},{medio},{list_income_imp_transp[top3]},","{:.2f}".format(list_income_imp_transp[top3]*100/total_imp_transp),"%")

print("\nTop 10 rutas para exportacion")
print("Lugar,Origen->Destino,Ingresos totales,Porcentaje del total")
for top10 in range(0,10):
  for ruta in exp_routes:
    if list_income_exp_routes[top10]==income_exp_routes[ruta]:
      print(f"{top10+1},{ruta},{list_income_exp_routes[top10]},","{:.2f}".format(list_income_exp_routes[top10]*100/total_exp_routes),"%")

print("\nTop 10 rutas para importacion")
print("Lugar,Origen->Destino,Ingresos totales,Porcentaje del total")
for top10 in range(0,10):
  for ruta in imp_routes:
    if list_income_imp_routes[top10]==income_imp_routes[ruta]:
      print(f"{top10+1},{ruta},{list_income_imp_routes[top10]},","{:.2f}".format(list_income_imp_routes[top10]*100/total_imp_routes),"%")

#La única diferencia para imprimir el top de paises de origen es que debemos enontrar cuántos países son necesarios para obtener al menos el 80% de los ingresos. Para esto se suman los ingresos de cada entrada de la lista ordenada hasta que la suma entre el total de la lista sea mayor a 0.8.
total_exp_origin=sum(list_income_exp_origin)
total_imp_origin=sum(list_income_imp_origin)
suma=0
top_exp_origin=0
for elemento in list_income_exp_origin:
  suma+=elemento
  top_exp_origin+=1
  #print(suma/total_exp_origin)
  if suma/total_exp_origin>0.8:
    break

#Para imprimir se sigue el mismo procedimiento que en las impresiones anteriores ya que se encontró el número de países que deben tomarse
print(f"\nTop {top_exp_origin} paises que aportan el 80% de ingresos de exportacion")
print("Lugar,Pais,Ingresos totales,Porcentaje del total")
for top in range(0,top_exp_origin):
  for pais in exp_origin:
    if list_income_exp_origin[top]==income_exp_origin[pais]:
      print(f"{top+1},{pais},{list_income_exp_origin[top]},","{:.2f}".format(list_income_exp_origin[top]*100/total_exp_origin),"%")

#Se repite el mismo proceso anterior pero para las importaciones
suma=0
top_imp_origin=0
for elemento in list_income_imp_origin:
  suma+=elemento
  top_imp_origin+=1
  #print(suma/total_imp_origin)
  if suma/total_imp_origin>0.8:
    break

print(f"\nTop {top_imp_origin} paises que aportan el 80% de ingresos de importacion")
print("Lugar,Pais,Ingresos totales,Porcentaje del total")
for top in range(0,top_imp_origin):
  for pais in imp_origin:
    if list_income_imp_origin[top]==income_imp_origin[pais]:
      print(f"{top+1},{pais},{list_income_imp_origin[top]},","{:.2f}".format(list_income_imp_origin[top]*100/total_imp_origin),"%")
"""
print('income_exp_transp ',income_exp_transp)
print('income_imp_transp ',income_imp_transp)
print('income_exp_origin ',income_exp_origin)
print('income_imp_origin ',income_imp_origin)
print('income_exp_routes ',income_exp_routes)
print('income_imp_routes ',income_imp_routes)
"""
