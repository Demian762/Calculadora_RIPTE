import tkinter as tk
from tkinter import *
import numpy as np
import pandas as pd

"""
Cargando archivos de uso general

Preparación del dataframe general de ripte
"""

ripte = pd.read_csv('https://infra.datos.gob.ar/catalog/sspm/dataset/158/distribution/158.1/download/remuneracion-imponible-promedio-trabajadores-estables-ripte-total-pais-pesos-serie-mensual.csv')

ripte['variacion'] = ripte['ripte'].pct_change(periods=1)*100

ripte['indice'] = 100.0

for i in ripte.index:
    if i == 0:
        continue
    ripte.at[i, 'indice'] = ripte.at[i-1,'indice'] * (1+(ripte.at[i,'variacion']/100))

ripte['final'] = 100.0
alto = 100.0
for i in ripte['final'].index:
    if ripte.at[i,'indice'] > alto:
        alto = ripte.at[i,'indice']
    ripte.at[i,'final'] = alto

ripte = ripte.fillna(0)
ripte = ripte.round(2)

ripte['indice_tiempo'] = ripte['indice_tiempo'].astype('datetime64')
ripte = ripte.rename(columns={'indice_tiempo':'fechas'})
ripte['fechas'] = ripte['fechas'].dt.to_period('M')


"""
Cargando las tasas de una pagina random porque al BNA le chupa un huevo
"""

link = 'http://www.abogadosrafaela.com.ar/serviciosaprof/tasas-activas-banco-nacion/'

tasas1 = pd.read_html(link, index_col=0, header=0, decimal=','
    )[0].astype(float)

tasas1 = tasas1.drop(columns='Unnamed: 5')

tasas1['2019']['Enero'] = tasas1['2019']['Enero'] * 10000

tasas1 = tasas1.apply(lambda x: x/10000)

link = 'http://www.abogadosrafaela.com.ar/serviciosaprof/tasas-activas-banco-nacion/'

tasas2 = pd.read_html(link, index_col=0, header=0, decimal=','
    )[1].astype(float)

tasas2['2015']['Noviembre'] = tasas2['2015']['Noviembre'] * 10000
tasas2['2016']['Marzo'] = tasas2['2016']['Marzo'] * 10000
tasas2['2016']['Septiembre'] = tasas2['2016']['Septiembre'] * 10000
tasas2['2018']['Octubre'] = tasas2['2018']['Octubre'] * 10000
tasas2['2018']['Noviembre'] = tasas2['2018']['Noviembre'] * 10000

tasas2 = tasas2.apply(lambda x: x/10000)

tasas = pd.concat([tasas2,tasas1], axis=1)

tasas = tasas.drop(columns=['2014','2015','2016'])

ultimo = int(tasas.columns.max())+1

tasas3 = pd.DataFrame(pd.date_range(start='2017-01',end=str(ultimo),freq='M'))
tasas3[0] = tasas3[0].dt.to_period('M')

tasas3 = tasas3.rename(columns={0:'fechas'})

df = pd.DataFrame()
for i in tasas.columns:
    dfn = tasas[i]
    df = pd.concat([df,dfn])

df = df.reset_index()

tasas = pd.concat([tasas3,df[0]],axis=1)
tasas = tasas.rename(columns={0:'tasas'})

"""
Hardcodeados los ultimos meses
"""
tasas.at[66,'tasas'] = 4.75   # Este hay que borrarlo eventualmente
tasas.at[67,'tasas'] = 5.017


"""
Creando la App
"""
root=Tk()

miFrame=Frame(root,width=1200,height=600)
miFrame.pack()


"""
Funciones de los botones
"""

def limpiar():
    """
    Vacía todos los valores de la interfaz para empezar de nuevo
    """
    fecha_accidente_ano.set('')
    fecha_accidente_mes.set('')
    fecha_accidente_dia.set('')
    edad_app.set('')
    inca.set('')
    sueldo1.set('')
    sueldo2.set('')
    sueldo3.set('')
    sueldo4.set('')
    sueldo5.set('')
    sueldo6.set('')
    sueldo7.set('')
    sueldo8.set('')
    sueldo9.set('')
    sueldo10.set('')
    sueldo11.set('')
    sueldo12.set('')
    resultado_parcial.set('')
    resultado_total.set('')
    
def llenar():
    """
    llena todos los valores de la interfaz para realizar pruebas
    """
    fecha_accidente_ano.set('2020')
    fecha_accidente_mes.set('10')
    fecha_accidente_dia.set('12')
    edad_app.set(32)
    inca.set(7.9)
    sueldo1.set(58000)
    sueldo2.set(65000)
    sueldo3.set(60000)
    sueldo4.set(60000)
    sueldo5.set(63000)
    sueldo6.set(63000)
    sueldo7.set(63000)
    sueldo8.set(72000)
    sueldo9.set(65000)
    sueldo10.set(65000)
    sueldo11.set(65000)
    sueldo12.set(65000)


def calcular():
    """
    Inputs
    """
    fecha_accidente = str(fecha_accidente_ano.get()+'-'+fecha_accidente_mes.get()) # ejemplo de formato: "2020-10"
    sueldos = [
                float(sueldo1.get()),
                float(sueldo2.get()),
                float(sueldo3.get()),
                float(sueldo4.get()),
                float(sueldo5.get()),
                float(sueldo6.get()),
                float(sueldo7.get()),
                float(sueldo8.get()),
                float(sueldo9.get()),
                float(sueldo10.get()),
                float(sueldo11.get()),
                float(sueldo12.get())
    ]
    edad = int(edad_app.get())
    incapacidad_actual = float(inca.get())
    tipo_accidente = int(en_ocasion.get()) # 'in_itinere'=0,'en_ocasion'=1


    """
    Creacion y merge del dataframe particular del cliente
    """

    cliente = pd.DataFrame(sueldos)
    cliente = cliente.rename(columns={0:'sueldos'})

    cliente['fechas'] = pd.date_range(end=fecha_accidente,freq='M',periods=len(sueldos))
    cliente['fechas'] = cliente['fechas'].dt.to_period('M')

    cliente = pd.merge(cliente, ripte, on='fechas', how='left')

    indice = ripte[ripte['fechas']==fecha_accidente].final
    indice = float(indice)

    cliente['coeficiente'] = 0.0

    cliente = cliente.assign(coeficiente = lambda x: (indice/x['final']))
    cliente = cliente.assign(actualizados = lambda x: (x['sueldos']*x['coeficiente']))
    cliente = cliente.round(2)

    """
    Resultados
    """

    resultado = cliente['actualizados'].mean().round(2)

    """
    Calculo final con intereses
    """

    fecha_calculo_final = cliente['fechas'].max()

    interes = tasas[tasas['fechas'] > fecha_calculo_final]['tasas'].sum()/100 + 1

    resultado = (resultado * interes).round(2)

    resultado_ci = 53 * resultado *  (65/edad) * incapacidad_actual/(100)
    resultado_ci = round(resultado_ci,2)

    if tipo_accidente == 1:
        resultado_ci_final = round(resultado_ci*1.2,2)
    else:
        resultado_ci_final = resultado_ci


    resultado_parcial.set(resultado)
    resultado_total.set(resultado_ci_final)


"""
Título
"""

titulo = Label(miFrame,text="Super Calculadora RIPTE")
titulo.grid(row=0,column=1,sticky=W,pady=15,padx=10)


"""
Fecha del accidente
"""
meses = ['01','02','03','04','05','06','07','08','09','10','11','12']

fechaLabel_ano = Label(miFrame,text="Año: ")
fechaLabel_ano.grid(row=1,column=1,sticky=W,pady=0,padx=10)
fechaLabel_mes = Label(miFrame,text="Mes: ")
fechaLabel_mes.grid(row=1,column=2,sticky=W,pady=0,padx=10)
fechaLabel_dia = Label(miFrame,text="Día: ")
fechaLabel_dia.grid(row=1,column=3,sticky=W,pady=0,padx=10)

fechaLabel = Label(miFrame,text="Fecha del accidente: ")
fechaLabel.grid(row=2,column=0,sticky=W,pady=10,padx=10)

fecha_accidente_ano = StringVar()
fecha_accidente_ano.set('')
cuadroFecha=Entry(miFrame, textvariable=fecha_accidente_ano)
cuadroFecha.grid(row=2,column=1,pady=10,padx=10)
cuadroFecha.config(fg='black', justify='center')

fecha_accidente_mes = tk.StringVar(root)
fecha_accidente_mes.set('')
cuadroFecha = tk.OptionMenu(miFrame, fecha_accidente_mes, *meses)
cuadroFecha.grid(row=2,column=2,pady=10,padx=10)
cuadroFecha.config(fg='black', justify='center')

fecha_accidente_dia = StringVar()
fecha_accidente_dia.set('')
cuadroFecha=Entry(miFrame, textvariable=fecha_accidente_dia)
cuadroFecha.grid(row=2,column=3,pady=10,padx=10)
cuadroFecha.config(fg='black', justify='center')

"""
Edad e incapacidad
"""
edadLabel = Label(miFrame,text="Edad: ")
edadLabel.grid(row=3,column=0,sticky=W,pady=10,padx=10)

edad_app = StringVar()
cuadroEdad=Entry(miFrame, textvariable=edad_app)
cuadroEdad.grid(row=3,column=1,pady=10,padx=10)
cuadroEdad.config(fg='black', justify='center')

incaLabel = Label(miFrame,text="Porcentaje de incapacidad: ")
incaLabel.grid(row=3,column=2,sticky=W,pady=10,padx=10)

inca = StringVar()
cuadroInca=Entry(miFrame, textvariable=inca)
cuadroInca.grid(row=3,column=3,pady=10,padx=10)
cuadroInca.config(fg='black', justify='center')

"""
Sueldos
"""
sueldoLabel = Label(miFrame,text="Sueldos: ")
sueldoLabel.grid(row=4,column=0,sticky=W,pady=10,padx=10)

sueldo1 = StringVar()
cuadroSueldo1=Entry(miFrame, textvariable=sueldo1)
cuadroSueldo1.grid(row=4,column=1,pady=10,padx=10)
cuadroSueldo1.config(fg='black', justify='center')

sueldo2 = StringVar()
cuadroSueldo2=Entry(miFrame, textvariable=sueldo2)
cuadroSueldo2.grid(row=4,column=2,pady=10,padx=10)
cuadroSueldo2.config(fg='black', justify='center')

sueldo3 = StringVar()
cuadroSueldo3=Entry(miFrame, textvariable=sueldo3)
cuadroSueldo3.grid(row=4,column=3,pady=10,padx=10)
cuadroSueldo3.config(fg='black', justify='center')

sueldo4 = StringVar()
cuadroSueldo4=Entry(miFrame, textvariable=sueldo4)
cuadroSueldo4.grid(row=5,column=1,pady=10,padx=10)
cuadroSueldo4.config(fg='black', justify='center')

sueldo5 = StringVar()
cuadroSueldo5=Entry(miFrame, textvariable=sueldo5)
cuadroSueldo5.grid(row=5,column=2,pady=10,padx=10)
cuadroSueldo5.config(fg='black', justify='center')

sueldo6 = StringVar()
cuadroSueldo6=Entry(miFrame, textvariable=sueldo6)
cuadroSueldo6.grid(row=5,column=3,pady=10,padx=10)
cuadroSueldo6.config(fg='black', justify='center')

sueldo7 = StringVar()
cuadroSueldo7=Entry(miFrame, textvariable=sueldo7)
cuadroSueldo7.grid(row=6,column=1,pady=10,padx=10)
cuadroSueldo7.config(fg='black', justify='center')

sueldo8 = StringVar()
cuadroSueldo8=Entry(miFrame, textvariable=sueldo8)
cuadroSueldo8.grid(row=6,column=2,pady=10,padx=10)
cuadroSueldo8.config(fg='black', justify='center')

sueldo9 = StringVar()
cuadroSueldo9=Entry(miFrame, textvariable=sueldo9)
cuadroSueldo9.grid(row=6,column=3,pady=10,padx=10)
cuadroSueldo9.config(fg='black', justify='center')

sueldo10 = StringVar()
cuadroSueldo10=Entry(miFrame, textvariable=sueldo10)
cuadroSueldo10.grid(row=7,column=1,pady=10,padx=10)
cuadroSueldo10.config(fg='black', justify='center')

sueldo11 = StringVar()
cuadroSueldo11=Entry(miFrame, textvariable=sueldo11)
cuadroSueldo11.grid(row=7,column=2,pady=10,padx=10)
cuadroSueldo11.config(fg='black', justify='center')

sueldo12 = StringVar()
cuadroSueldo12=Entry(miFrame, textvariable=sueldo12)
cuadroSueldo12.grid(row=7,column=3,pady=10,padx=10)
cuadroSueldo12.config(fg='black', justify='center')

"""
Checkboxs varios

in itinere * 1
en ocasion * 1.2

"""

en_ocasion = IntVar()
# De haber más opciones mas adelante, se agregan acá

def opciones():
    opcionEscogida=""

    if(en_ocasion.get()==1):
        opcionEscogida+=' En ocasión'
    
    # De haber más opciones mas adelante, se agregan acá

check_enocasion = Checkbutton(miFrame, text="En ocasión",variable=en_ocasion,onvalue=1,offvalue=0,command=opciones)
check_enocasion.grid(row=8, column=0, pady=10, padx=10)

"""
Botón Calcular y limpiar todo
"""

botonCalcular = Button(miFrame, text = 'Calcular', command = calcular)
botonCalcular.grid(row=9, column=1, pady=10, padx=10)

botonLimpiar = Button(miFrame, text = 'Limpiar todo', command = limpiar)
botonLimpiar.grid(row=9, column=2, pady=10, padx=10)

botonPrueba = Button(miFrame, text = 'llenar', command = llenar)
botonPrueba.grid(row=9, column=3, pady=10, padx=10)

"""
Resultados
"""

resultLabel = Label(miFrame,text="Resultado: ")
resultLabel.grid(row=10,column=0,sticky=W,pady=10,padx=10)

resultado_parcial = StringVar()
cuadroResult=Entry(miFrame, textvariable=resultado_parcial)
cuadroResult.grid(row=10,column=1,pady=10,padx=10)
cuadroResult.config(fg='black', justify='center')

resultotLabel = Label(miFrame,text="Resultado total: ")
resultotLabel.grid(row=10,column=2,sticky=W,pady=10,padx=10)

resultado_total = StringVar()
cuadroResultot=Entry(miFrame, textvariable=resultado_total)
cuadroResultot.grid(row=10,column=3,pady=10,padx=10)
cuadroResultot.config(fg='black', justify='center')


root.mainloop()