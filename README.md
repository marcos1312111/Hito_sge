Este código es una aplicación en Python utilizando Tkinter para crear una interfaz gráfica de usuario (GUI) para gestionar encuestas. La base de datos MySQL almacena los datos de las encuestas, y el código permite insertar, actualizar, eliminar y visualizar encuestas desde una tabla.

Conexión a la base de datos: Utiliza mysql.connector para conectar con una base de datos llamada ENCUESTAS.
Clase EncuestaApp: Hereda de tk.Tk y gestiona la interfaz.
create_widgets: Crea un widget Treeview para mostrar las encuestas en una tabla, con columnas para cada dato de la encuesta (edad, sexo, consumo de alcohol, etc.).
Botones: Crea botones para agregar, actualizar, eliminar, filtrar y mostrar gráficos.
Agregar Encuesta: Muestra una ventana emergente donde puedes ingresar datos de una nueva encuesta, que luego se guarda en la base de datos.
Actualizar Encuesta: Permite seleccionar una encuesta existente y actualizar sus datos.
Eliminar Encuesta: Borra una encuesta seleccionada de la base de datos.
Filtrar Encuestas: Permite filtrar las encuestas por edad, sexo o ID.
view_encuestas: Muestra todas las encuestas en la tabla Treeview cargándolas desde la base de datos.
Exportar a Excel: Exporta los datos de las encuestas a un archivo Excel utilizando pandas.
Mostrar Gráficos: Muestra un gráfico de barras de la cantidad de encuestas por edad.
Interacción con el usuario: A través de simpledialog y tk.Entry, se solicita y procesa la información para agregar o actualizar las encuestas.
El objetivo principal de la aplicación es permitir la gestión de encuestas almacenadas en una base de datos MySQL a través de una GUI interactiva en Tkinter.
