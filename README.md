<h1>SISTEMA DE FACTURACION
</h1>

![](/assets/images/mi_imagen.png)



###  🎯Objetivo general 
<P>
Este proyecto es un sistema de facturación desarrollado en Django para la Droguería “FARMAVISION ".
Permite registrar productos, clientes, usuarios del sistema y generar facturas de venta de manera rápida.
</P>

## 🎯Objetivos Espesificos
- Diseñar y desarrollar un módulo de registro de productos que permita gestionar nombre, precio, categoría, fecha de vencimiento y cantidad en inventario.

- Implementar un módulo de gestión de clientes para almacenar y consultar información básica como nombre, documento y datos de contacto

- Crear un sistema de facturación automatizado que permita generar facturas, calcular subtotales, y total final de manera precisa.-

- Desarrollar un control de inventario que descuente automáticamente la cantidad vendida al momento de generar una factura.

- Implementar un sistema de autenticación de usuarios que garantice el acceso seguro al sistema según roles (administrador, vendedor, etc.).

- Generar reportes de ventas por fecha, producto o cliente para facilitar la toma de decisiones en la droguería.

- Optimizar la interfaz de usuario para lograr un sistema fácil de usar, rápido y accesible para los empleados de la droguería.

## 👌inicios

Pasos para ejecutar el proyecto.
- 1.Clonar el repositorio
Copiamos la URL del repositorio y lo clonamos con el siguiente comando:
``` bash
 git clone https://github.com/AndresPlaz4s/SISTEMA-DE-FACTURACION.git
 ```

- 2.Ingresarmos  a la carpeta del proyecto
``` bash
 cd FACTURACION
```

- 3.Abrirmos el proyecto en una nueva ventana puede ser  (opcional)
Puedes abrir la carpeta con:
``` Ctrl + clic en tu editor ``` de código para trabajar más cómodamente.
 
- 4.Crear el entorno virtual
``` bash
python -m venv venv
```
(Puedes cambiar “venv” por el nombre del entorno si lo deseas.

- 5.Activar el entorno virtual
o	Windows:
```bash
 .\venv\Scripts\activate
```
o	Linux / macOS:
``` bash
source venv/bin/activate
```

- 6.Instalar los requerimientos del proyecto
``` bash
pip install -r requirements.txt
```

- 7.Crear y aplicar las migraciones
o	 Para crear las migraciones:
``` bash
python manage.py makemigrations
```
o	Para aplicar las migraciones:
``` bash
python manage.py migrate
```

2.	Por ultimo ejecutarmos  el servidor con :
```	 bash
python manage.py runserver
```



## 🏗️ 3. Arquitectura del Proyecto

- La estructura principal del proyecto Django.
proyecto_facturacion/proyecto_facturacion/

```bash 
proyecto_facturacion/
│
├── manage.py
├── proyecto_facturacion/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
└── facturacion/
    ├── migrations/
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── forms.py
    ├── templates/
    │   └── facturacion/
    │       ├── home.html
    │       ├── productos_list.html
    │       ├── clientes_list.html
    │       ├── factura_crear.html
    │       └── factura_detalle.html
    └── static/
```


## 🔧 4. Modelos de la Base de Datos

### **Producto**
- Nombre  
- Precio  
- stock
- descripcion
- tipo
- f _entrada.
- f _vencimiento  

### **Cliente**
- Nombre  
- imail
- n_documento
- 
- Teléfono  

### **Factura**
- Cliente  
- Fecha  
- Total  

### **Detalle de Factura**
- Factura  
- Producto  
- Cantidad  
- Subtotal  

### venta
- producto
- cliente
- cantidad
- p_unitario
- total
### Provedor
- Nit
- N_empresa
- contactio


## 🧩5. Vistas Principales

| Vista | Función |
|-------|---------|
| `home` | Página principal del sistema |
| `listar_productos` | Muestra todos los productos |
| `crear_producto` | Formulario para registrar productos |
| `listar_clientes` | Lista de clientes |
| `crear_factura` | Crear una venta |
| `detalle_factura` | Ver detalles de la factura |
| `usuario` | ver los usuario que estan en el sistema   |
| `crear_usuarios` | crear usuarios para es istema |



---
