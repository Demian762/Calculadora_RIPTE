# Calculadora_RIPTE
Es una aplicación creada para calcular la indemnización que por Ley de Riesgos del Trabajo corresponde en caso de accidente laboral "in itinere" o "en ocasión". Podrás obtener el Valor Ingreso Base (VIB) con RIPTE más Tasa.

Se puede descargar lista para usar desde acá:
https://drive.google.com/file/d/1x_VnT-57ZE7ywJ_FOEBMlf8zTIq35eLp/view?usp=sharing

nota: probablemente haga falta desactivar windows defender u otro antivirus y agregarlo como excepción para que no sea borrado de inmediato.

Las tasas son tomadas de páginas web oficiales y no oficiales cada vez que se abre la app.
Es necesario mantenerla actualizada por este medio para que la precisión del resultado sea mayor.

LA IDEA DE ESTA APP ES APROXIMAR UNA IDEA DE LA INDEMNIZACIÓN AL USUARIO, NO SE DEBE TOMAR ESTA INFORMACIÓN COMO BASE PARA NADA MÁS.
ESTE PROYECTO ES GRATUITO Y ABIERTO.

Para crear la aplicación con el código fuente utilizando pyinstaller:
pyinstaller --onefile --windowed app.py

version 1.1:
Se aceptan menos de 12 meses.
Se puede exportar a excel toda la información procesada (incluídas las tasas).
cambios estéticos.

version 1.0:
De momento hay que agregar 12 sueldos, no acepta menos.
Si bien está la casilla de días, solo toma para el cálculo, el año y mes.

Por sugerencias: joangodoy@hotmail.com
