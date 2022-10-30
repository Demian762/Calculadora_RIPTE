from tkinter import *
from tkinter import messagebox
import numpy as np
import pandas as pd

"""
Cargando archivos de uso general

Cargando ripte
"""

ripte = pd.read_csv('https://raw.githubusercontent.com/Demian762/Calculadora_RIPTE/main/ripte.csv')
ripte['fechas'] = ripte['fechas'].astype('datetime64')
ripte['fechas'] = ripte['fechas'].dt.to_period('M')

"""
Cargando las tasas
"""

tasas = pd.read_csv('https://raw.githubusercontent.com/Demian762/Calculadora_RIPTE/main/tasas.csv')
tasas['fechas'] = tasas['fechas'].astype('datetime64')
tasas['fechas'] = tasas['fechas'].dt.to_period('M')


"""
Estableciendo colores
"""
fondo = "#9F4D0C"
boton = "#763909"
letras = "#F6E1D1"
casilla = "#F2944A"

"""
Creando la App
"""
root=Tk()
root.title('Calculadora de Indemnización de ART')
root.resizable(0,0)
root.config(bg=fondo)

miTitulo=Frame(root, width=1200, height=50)
miTitulo.pack(side="top")
miTitulo.config(bg=fondo)
miNombre=Frame(root, width=1200, height=50)
miNombre.pack()
miNombre.config(bg=fondo)
miFrame=Frame(root,width=1200,height=600)
miFrame.pack()
miFrame.config(bg=fondo)
miSalida=Frame(root, width=1200, height=100)
miSalida.pack(side="bottom")
miSalida.config(bg=fondo)

"""
Funciones de los botones
"""

def cargar():
    """
    Carga un archivo Excel con el nombre indicado en el campo correspondiente
    """

    nombre_archivo = "indemnizacion " + str(nombre_cliente.get()) + ".xlsx"

    carga = pd.read_excel(nombre_archivo)

    edad_app.set(int(carga["edad"][0]))
    inca.set(carga["incapacidad"][0])
    fecha_accidente_ano.set((carga["fecha"][0]).year)
    fecha_accidente_mes.set((carga["fecha"][0]).month)
    sueldo1.set(carga["sueldos"][0])
    sueldo2.set(carga["sueldos"][1])
    sueldo3.set(carga["sueldos"][2])
    sueldo4.set(carga["sueldos"][3])
    sueldo5.set(carga["sueldos"][4])
    sueldo6.set(carga["sueldos"][5])
    sueldo7.set(carga["sueldos"][6])
    sueldo8.set(carga["sueldos"][7])
    sueldo9.set(carga["sueldos"][8])
    sueldo10.set(carga["sueldos"][9])
    sueldo11.set(carga["sueldos"][10])
    sueldo12.set(carga["sueldos"][11])


def limpiar():
    """
    Vacía todos los valores de la interfaz para empezar de nuevo
    """
    nombre_cliente.set('')
    fecha_accidente_ano.set('')
    fecha_accidente_mes.set('')
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
    resultado_vib_ripte.set('')
    resultado_tasa_interes.set('')
    resultado_vib_ripte_tasa.set('')
    resultado_indemnizacion.set('')


def llenar():
    """
    llena todos los valores de la interfaz para realizar pruebas
    """
    nombre_cliente.set('Juan Prueba')
    fecha_accidente_ano.set('2020')
    fecha_accidente_mes.set('10')
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
    nombres = nombre_cliente.get()
    # ejemplo de formato: "2020-10"
    fecha_accidente = str(fecha_accidente_ano.get()+'-'+fecha_accidente_mes.get())
    sueldos = [
                sueldo1.get(),
                sueldo2.get(),
                sueldo3.get(),
                sueldo4.get(),
                sueldo5.get(),
                sueldo6.get(),
                sueldo7.get(),
                sueldo8.get(),
                sueldo9.get(),
                sueldo10.get(),
                sueldo11.get(),
                sueldo12.get()
    ]
    sueldos = list(filter(None, sueldos))
    sueldos = list(map(float,sueldos))
    edad = int(edad_app.get())
    incapacidad = float(inca.get())
    tipo_accidente = int(en_ocasion.get()) # 'in_itinere'=0,'en_ocasion'=1
    exportar = int(generar_excel.get()) # generar excel = 1 , no hacer nada =0

    """
    Creacion y merge del dataframe particular del cliente
    """

    cliente = pd.DataFrame(sueldos)
    cliente = cliente.rename(columns={0:'sueldos'})

    cliente['fechas'] = pd.date_range(end=fecha_accidente,freq='M',periods=len(sueldos))
    cliente['fechas'] = cliente['fechas'].dt.to_period('M')

    cliente = pd.merge(cliente, ripte, on='fechas', how='left')
    cliente = pd.merge(cliente, tasas, on="fechas", how="left")

    indice = ripte[ripte['fechas']==fecha_accidente].final
    indice = float(indice)

    cliente['coeficiente'] = 0.0

    cliente = cliente.assign(coeficiente = lambda x: (indice/x['final']))
    cliente = cliente.assign(actualizados = lambda x: (x['sueldos']*x['coeficiente']))
    cliente = cliente.round(2)

    cliente.loc[0,"nombres"] = nombres
    cliente.loc[0,"edad"] = edad
    cliente.loc[0,"incapacidad"] = incapacidad
    cliente.loc[0,"fecha"] = pd.to_datetime(fecha_accidente)

    """
    Resultados finales
    """

    vib_ripte = cliente['actualizados'].mean().round(2)

    fecha_calculo_final = cliente['fechas'].max()

    tasa_interes = tasas[tasas['fechas'] > fecha_calculo_final]['tasas'].sum()/100 + 1

    vib_ripte_tasa = (vib_ripte * tasa_interes).round(2)

    tasa_interes = str(((tasa_interes - 1) * 100).round(2)) + " %"

    indemnizacion = 53 * vib_ripte_tasa *  (65/edad) * incapacidad/(100)
    indemnizacion = round(indemnizacion,2)

    if tipo_accidente == 1:
        indemnizacion = round(indemnizacion*1.2,2)
    else:
        indemnizacion = indemnizacion

    resultado_vib_ripte.set(vib_ripte)
    resultado_tasa_interes.set(tasa_interes)
    resultado_vib_ripte_tasa.set(vib_ripte_tasa)
    resultado_indemnizacion.set(indemnizacion)

    if exportar == 1:
        cliente.to_excel(
            excel_writer="Indemnizacion "+nombre_cliente.get()+".xlsx",
            index=False,
            sheet_name="Indemnización "+nombre_cliente.get(),
            engine='openpyxl'
            )

def pormil():
    
    sueldo1.set(int(sueldo1.get()*1000))
    sueldo2.set(int(sueldo2.get()*1000))
    sueldo3.set(int(sueldo3.get()*1000))
    sueldo4.set(int(sueldo4.get()*1000))
    sueldo5.set(int(sueldo5.get()*1000))
    sueldo6.set(int(sueldo6.get()*1000))
    sueldo7.set(int(sueldo7.get()*1000))
    sueldo8.set(int(sueldo8.get()*1000))
    sueldo9.set(int(sueldo9.get()*1000))
    sueldo10.set(int(sueldo10.get()*1000))
    sueldo11.set(int(sueldo11.get()*1000))
    sueldo12.set(int(sueldo12.get()*1000))

def divmil():
    
    sueldo1.set(int(sueldo1.get()/1000))
    sueldo2.set(int(sueldo2.get()/1000))
    sueldo3.set(int(sueldo3.get()/1000))
    sueldo4.set(int(sueldo4.get()/1000))
    sueldo5.set(int(sueldo5.get()/1000))
    sueldo6.set(int(sueldo6.get()/1000))
    sueldo7.set(int(sueldo7.get()/1000))
    sueldo8.set(int(sueldo8.get()/1000))
    sueldo9.set(int(sueldo9.get()/1000))
    sueldo10.set(int(sueldo10.get()/1000))
    sueldo11.set(int(sueldo11.get()/1000))
    sueldo12.set(int(sueldo12.get()/1000))

def licencia():
    messagebox.showinfo(
        "Licencia y versión","Software de código abierto y gratuito,\n\nNO pagues por este programa\n\nVersión 1.2"
        )

def contacto():
    messagebox.showinfo("Contacto:","Por sugerencias:\njoangodoy@hotmail.com")

def donaciones():
    messagebox.showinfo("Donaciones","Alias CVU de mercadopago:\n\njoan.demian.godoy")


"""
Creación de la barra de menú
"""

barraMenu = Menu(root)
root.config(menu=barraMenu)

archivoMenu=Menu(barraMenu, tearoff=0)
archivoMenu.add_command(label="Llenar con ejemplo", command=llenar)
archivoMenu.add_command(label='Salir', command=root.destroy)

acercaMenu=Menu(barraMenu, tearoff=0)
acercaMenu.add_command(label="Donaciones", command=donaciones)
acercaMenu.add_command(label="Licencia", command=licencia)
acercaMenu.add_command(label="Contacto", command=contacto)

barraMenu.add_cascade(label="Archivo", menu=archivoMenu)
barraMenu.add_cascade(label="Acerca", menu=acercaMenu)

"""
Título
"""

titulo = Label(miTitulo,text="CIART 1.2")
titulo.grid(row=0,column=0,sticky=W,pady=15,padx=10)
titulo.config(bg=fondo, fg=letras, font=("Times New Roman",25))

"""
Nombre del Cliente
"""
nombre_cliente = StringVar()
nombre_cliente.set('')
nombreLabel = Label(miNombre, text="Nombre del Cliente:")
nombreLabel.grid(row=1, column=0, sticky=W, pady=10)
nombreLabel.config(bg=fondo, fg=letras, font=("Times New Roman",14))
cuadroNombre = Entry(miNombre, textvariable=nombre_cliente)
cuadroNombre.grid(row=1, column=1, sticky=W, pady=10)
cuadroNombre.config(fg="black", justify='center', bg=casilla, font=("Times New Roman",14))



"""
Fecha del accidente
"""

fechaLabel_ano = Label(miFrame,text="Año: ")
fechaLabel_ano.grid(row=0,column=1,sticky=SW,pady=0,padx=10)
fechaLabel_ano.config(bg=fondo, fg=letras, font=("Times New Roman",14))
fechaLabel_mes = Label(miFrame,text="Mes: ")
fechaLabel_mes.grid(row=0,column=2,sticky=SW,pady=0,padx=10)
fechaLabel_mes.config(bg=fondo, fg=letras, font=("Times New Roman",14))

fechaLabel = Label(miFrame,text="Fecha del accidente: ")
fechaLabel.grid(row=1,column=0,sticky=E,pady=0,padx=10)
fechaLabel.config(bg=fondo, fg=letras, font=("Times New Roman",14))

fecha_accidente_ano = StringVar()
fecha_accidente_ano.set('')
cuadroFecha=Entry(miFrame, textvariable=fecha_accidente_ano)
cuadroFecha.grid(row=1,column=1,pady=0,padx=0)
cuadroFecha.config(fg="black", justify='center', bg=casilla, font=("Times New Roman",14))

fecha_accidente_mes = StringVar()
fecha_accidente_mes.set('')
cuadroFecha = Entry(miFrame, textvariable=fecha_accidente_mes)
cuadroFecha.grid(row=1,column=2,pady=0,padx=10)
cuadroFecha.config(fg='black', justify='center', bg=casilla, font=("Times New Roman",14))


"""
Edad e incapacidad
"""
edadLabel = Label(miFrame,text="Edad: ")
edadLabel.grid(row=2,column=0,sticky=E,pady=10,padx=10)
edadLabel.config(bg=fondo, fg=letras, font=("Times New Roman",14))

edad_app = IntVar()
edad_app.set('')
cuadroEdad=Entry(miFrame, textvariable=edad_app)
cuadroEdad.grid(row=2,column=1,pady=10,padx=10)
cuadroEdad.config(fg='black', justify='center', bg=casilla, font=("Times New Roman",14))


incaLabel = Label(miFrame,text="Porcentaje de incapacidad: ")
incaLabel.grid(row=2,column=2,sticky=E,pady=10,padx=10)
incaLabel.config(bg=fondo, fg=letras, font=("Times New Roman",14))

inca = DoubleVar()
inca.set('')
cuadroInca=Entry(miFrame, textvariable=inca)
cuadroInca.grid(row=2,column=3,pady=10,padx=10)
cuadroInca.config(fg='black', justify='center', bg=casilla, font=("Times New Roman",14))

"""
Margen
"""
margen = Label(miFrame, text="")
margen.grid(row=3, pady=5)
margen.config(bg=fondo)


"""
Sueldos
"""
sueldoLabel = Label(miFrame,text="Sueldos: ")
sueldoLabel.grid(row=4,column=0,sticky=E,pady=10,padx=10)
sueldoLabel.config(bg=fondo, fg=letras, font=("Times New Roman",14))

sueldo1 = DoubleVar()
sueldo1.set('')
cuadroSueldo1=Entry(miFrame, textvariable=sueldo1)
cuadroSueldo1.grid(row=4,column=1,pady=10,padx=10)
cuadroSueldo1.config(fg='black', justify='center', bg=casilla, font=("Times New Roman",14))

sueldo2 = DoubleVar()
sueldo2.set('')
cuadroSueldo2=Entry(miFrame, textvariable=sueldo2)
cuadroSueldo2.grid(row=4,column=2,pady=10,padx=10)
cuadroSueldo2.config(fg='black', justify='center', bg=casilla, font=("Times New Roman",14), )

sueldo3 = DoubleVar()
sueldo3.set('')
cuadroSueldo3=Entry(miFrame, textvariable=sueldo3)
cuadroSueldo3.grid(row=4,column=3,pady=10,padx=10)
cuadroSueldo3.config(fg='black', justify='center', bg=casilla, font=("Times New Roman",14))

sueldo4 = DoubleVar()
sueldo4.set('')
cuadroSueldo4=Entry(miFrame, textvariable=sueldo4)
cuadroSueldo4.grid(row=5,column=1,pady=10,padx=10)
cuadroSueldo4.config(fg='black', justify='center', bg=casilla, font=("Times New Roman",14))

sueldo5 = DoubleVar()
sueldo5.set('')
cuadroSueldo5=Entry(miFrame, textvariable=sueldo5)
cuadroSueldo5.grid(row=5,column=2,pady=10,padx=10)
cuadroSueldo5.config(fg='black', justify='center', bg=casilla, font=("Times New Roman",14))

sueldo6 = DoubleVar()
sueldo6.set('')
cuadroSueldo6=Entry(miFrame, textvariable=sueldo6)
cuadroSueldo6.grid(row=5,column=3,pady=10,padx=10)
cuadroSueldo6.config(fg='black', justify='center', bg=casilla, font=("Times New Roman",14))

sueldo7 = DoubleVar()
sueldo7.set('')
cuadroSueldo7=Entry(miFrame, textvariable=sueldo7)
cuadroSueldo7.grid(row=6,column=1,pady=10,padx=10)
cuadroSueldo7.config(fg='black', justify='center', bg=casilla, font=("Times New Roman",14))

sueldo8 = DoubleVar()
sueldo8.set('')
cuadroSueldo8=Entry(miFrame, textvariable=sueldo8)
cuadroSueldo8.grid(row=6,column=2,pady=10,padx=10)
cuadroSueldo8.config(fg='black', justify='center', bg=casilla, font=("Times New Roman",14))

sueldo9 = DoubleVar()
sueldo9.set('')
cuadroSueldo9=Entry(miFrame, textvariable=sueldo9)
cuadroSueldo9.grid(row=6,column=3,pady=10,padx=10)
cuadroSueldo9.config(fg='black', justify='center', bg=casilla, font=("Times New Roman",14))

sueldo10 = DoubleVar()
sueldo10.set('')
cuadroSueldo10=Entry(miFrame, textvariable=sueldo10)
cuadroSueldo10.grid(row=7,column=1,pady=10,padx=10)
cuadroSueldo10.config(fg='black', justify='center', bg=casilla, font=("Times New Roman",14))

sueldo11 = DoubleVar()
sueldo11.set('')
cuadroSueldo11=Entry(miFrame, textvariable=sueldo11)
cuadroSueldo11.grid(row=7,column=2,pady=10,padx=10)
cuadroSueldo11.config(fg='black', justify='center', bg=casilla, font=("Times New Roman",14))

sueldo12 = IntVar()
sueldo12.set('')
cuadroSueldo12=Entry(miFrame, textvariable=sueldo12)
cuadroSueldo12.grid(row=7,column=3,pady=10,padx=10)
cuadroSueldo12.config(fg='black', justify='center', bg=casilla, font=("Times New Roman",14))

"""
Checkboxs varios

in itinere * 1
en ocasion * 1.2

"""

en_ocasion = IntVar()
generar_excel = IntVar()
# De haber más opciones mas adelante, se agregan acá

def opciones():
    opcionEscogida=""

    if(en_ocasion.get()==1):
        opcionEscogida+=' En ocasión'
    if(generar_excel.get()==1):
        opcionEscogida+=' Generar Excel'
    # De haber más opciones mas adelante, se agregan acá

check_enocasion = Checkbutton(miFrame, text="En ocasión",variable=en_ocasion,onvalue=1,offvalue=0,command=opciones)
check_enocasion.grid(row=8, column=0, pady=10, padx=10)
check_enocasion.config(fg='black', justify='center', bg=fondo, font=("Times New Roman",14))

check_generar_excel = Checkbutton(miFrame, text="Generar Excel",variable=generar_excel,onvalue=1,offvalue=0,command=opciones)
check_generar_excel.grid(row=8, column=1, pady=10, padx=10)
check_generar_excel.config(fg='black', justify='center', bg=fondo, font=("Times New Roman",14))

"""
Botones por y div mil
"""

botonpormil = Button(miFrame, text = '  Sueldos x 1000  ', command = pormil)
botonpormil.grid(row=8, column=2, pady=10, padx=10)
botonpormil.config(fg=letras, bg=boton, font=("Times New Roman",14))

botondivmil = Button(miFrame, text = '  Sueldos ÷ 1000  ', command = divmil)
botondivmil.grid(row=8, column=3, pady=10, padx=10)
botondivmil.config(fg=letras, bg=boton, font=("Times New Roman",14))

"""
Margen
"""
margen = Label(miFrame, text="")
margen.grid(row=9, pady=5)
margen.config(bg=fondo)

"""
Botón Cargar, Calcular y limpiar todo
"""

botonCargar = Button(miSalida, text = '  Cargar Excel  ', command = cargar)
botonCargar.grid(row=0, column=0, pady=10, padx=10)
botonCargar.config(fg=letras, bg=boton, font=("Times New Roman",14))

botonLimpiar = Button(miSalida, text = '  Limpiar todo  ', command = limpiar)
botonLimpiar.grid(row=0, column=1, pady=10, padx=10)
botonLimpiar.config(fg=letras, bg=boton, font=("Times New Roman",14))

botonCalcular = Button(miSalida, text = '   Calcular   ', command = calcular)
botonCalcular.grid(row=0, column=3, pady=10, padx=10)
botonCalcular.config(fg=letras, bg=boton, font=("Times New Roman",14))

"""
Resultados
"""

resultvib = Label(miSalida,text="VIB (RIPTE): ")
resultvib.grid(row=1,column=0,sticky=W,pady=10,padx=10)
resultvib.config(bg=fondo, fg=letras, font=("Times New Roman",14))

resultado_vib_ripte = StringVar()
cuadrovib=Entry(miSalida, textvariable=resultado_vib_ripte)
cuadrovib.grid(row=1,column=1,pady=10,padx=10)
cuadrovib.config(fg='black', justify='center', bg=casilla, font=("Times New Roman",14), state="readonly")

resultasa = Label(miSalida,text="Tasa de interés: ")
resultasa.grid(row=1,column=2,sticky=W,pady=10,padx=10)
resultasa.config(bg=fondo, fg=letras, font=("Times New Roman",14))

resultado_tasa_interes = StringVar()
cuadrotasa=Entry(miSalida, textvariable=resultado_tasa_interes)
cuadrotasa.grid(row=1,column=3,pady=10,padx=10)
cuadrotasa.config(fg='black', justify='center', bg=casilla, font=("Times New Roman",14), state="readonly")

resultvibtasa = Label(miSalida,text="VIB (RIPTE + TASA): ")
resultvibtasa.grid(row=2,column=0,sticky=W,pady=10,padx=10)
resultvibtasa.config(bg=fondo, fg=letras, font=("Times New Roman",14))

resultado_vib_ripte_tasa = StringVar()
cuadrovibtasa=Entry(miSalida, textvariable=resultado_vib_ripte_tasa)
cuadrovibtasa.grid(row=2,column=1,pady=10,padx=10)
cuadrovibtasa.config(fg='black', justify='center', bg=casilla, font=("Times New Roman",14), state="readonly")

resultindemnizacion = Label(miSalida,text="Indemnización: ")
resultindemnizacion.grid(row=2,column=2,sticky=W,pady=10,padx=10)
resultindemnizacion.config(bg=fondo, fg=letras, font=("Times New Roman",14))

resultado_indemnizacion = StringVar()
cuadroindemnizacion=Entry(miSalida, textvariable=resultado_indemnizacion)
cuadroindemnizacion.grid(row=2,column=3,pady=10,padx=10)
cuadroindemnizacion.config(fg='black', justify='center', bg=casilla, font=("Times New Roman",14), state="readonly")

"""
Margen
"""
margen = Label(miSalida, text="")
margen.grid(row=3, pady=5)
margen.config(bg=fondo)

root.mainloop()