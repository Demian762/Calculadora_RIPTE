# CIART (Calculadora de Indemnización de ART)

Es una aplicación creada para calcular la indemnización que por Ley de Riesgos del Trabajo corresponde en caso de accidente laboral "in itinere" o "en ocasión". Podrás obtener el Valor Ingreso Base (VIB) con RIPTE más Tasa.

Se puede descargar lista para usar en "Releases" a la derecha de este texto --->

nota: probablemente haga falta desactivar windows defender u otro antivirus y agregarlo como excepción para que no sea borrado de inmediato.

LA IDEA DE ESTA APP ES APROXIMAR UNA IDEA DE LA INDEMNIZACIÓN AL USUARIO, NO SE DEBE TOMAR ESTA INFORMACIÓN COMO BASE PARA NADA MÁS.
ESTE PROYECTO ES GRATUITO Y ABIERTO.

Para crear la aplicación con el código fuente utilizando pyinstaller:
pyinstaller --onefile --windowed app.py

Version 1.2:
El programa ahora carga mucho mas rápido, tomando los datos (ripte y tasas) desde los archivos .csv de este mismo repositorio que mantendré actualizado periodicamente.
Cambiada la forma de insertar el mes.
Agregados los botones para multiplicar y dividir por mil todos los sueldos.
Cambiado el nombre de prueba de Juan Pérez a Juan Prueba.
Agregada la función de cargar un excel ( y su correspondiente guarda de datos ).
Ahora están mejor descriptos y especificados los valores de salida.

Version 1.1:
Se aceptan menos de 12 meses.
Se pueden exportar los datos utilizados en un Excel (tasa incluída).
Cambios estéticos.

Version 1.0:
De momento hay que agregar 12 sueldos, no acepta menos.
Si bien está la casilla de días, solo toma para el cálculo, el año y mes.

Por sugerencias: joangodoy@hotmail.com
