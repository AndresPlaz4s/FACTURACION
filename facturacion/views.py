from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate

from .models import Producto, Cliente, Usuario

from .forms import ProductoForm, ClienteForm, UsuarioForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages

@login_required
def home(request):
    return render(request, 'facturacion/home.html')

@login_required
def ventas(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'facturacion/partials/ventas.html')
    return render(request, 'facturacion/ventas.html')

#productos (CRUD)

@login_required
def inventario(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'facturacion/partials/inventario.html')
    producto = Producto.objects.all().order_by("nombre")
    return render(request, 'facturacion/inventario.html', {"producto": producto})


@login_required
def crear_producto(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'facturacion/partials/inventario.html')
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("facturacion:inventario")
    else:
        form = ProductoForm()
    return render(request, 'facturacion/crear_producto.html', {"form": form})


@login_required
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == "POST":
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect("facturacion:inventario")
    else:
        form = ProductoForm(instance=producto)

    return render(request, "facturacion/editar_producto.html", 
                    {"form": form, 
                    "producto": producto
                        })


@login_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        producto.delete()
        return redirect("facturacion:inventario")
    return render(
        request,
        "facturacion/eliminar_producto.html",
        {
            "producto": producto
        }
    )



@login_required
def facturas(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'facturacion/partials/facturas.html')
    return render(request, 'facturacion/facturas.html')
#USUARIOS BRAYAN
@login_required
def usuarios(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'facturacion/partials/usuarios.html')
    usuarios = Usuario.objects.all().order_by('nombre')
    return render(request, 'facturacion/usuarios.html', {'usuarios': usuarios})


def usuario_login(request):
    
    if request.user.is_authenticated:
        return redirect('facturacion:usuarios')

    next_url = request.GET.get('next') or request.POST.get('next')
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(next_url or 'facturacion:usuarios')
        else:
            error = 'Credenciales inválidas. Verifica usuario y contraseña.'
    return render(request, 'registration/login.html', {'error': error, 'next': next_url})



@login_required
def crear_usuario(request):
   
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'facturacion/partials/usuarios.html')
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            
            usuario_obj = form.save(commit=False)
            
            username = usuario_obj.email if usuario_obj.email else usuario_obj.nombre
            password = form.cleaned_data.get('password')

            if User.objects.filter(username=username).exists():
                form.add_error('email', 'Ya existe un usuario con ese email/usuario en el sistema.')
            else:
                
                user = User.objects.create_user(username=username, email=usuario_obj.email or '', password=password)
                
                usuario_obj.user = user
                usuario_obj.save()
                
                login(request, user)
                messages.success(request, 'Usuario creado y sesión iniciada correctamente.')
                
                return redirect('facturacion:usuarios')
    else:
        form = UsuarioForm()  
    return render(request, 'facturacion/crear_usuario.html', {"form": form})

@login_required
def editar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)

    if request.method == "POST":
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            
            user = None
            if usuario.user:
                user = usuario.user
            else:
                if usuario.email:
                    try:
                        user = User.objects.filter(email=usuario.email).first()
                        if user:
                            usuario.user = user
                            usuario.save()
                    except User.DoesNotExist:
                        user = None

            nuevo_password = form.cleaned_data.get('password')

            # guardar cambios en Usuario local
            usuario = form.save()

            # si se proporcionó nueva contraseña y existe User, actualizarla
            if nuevo_password and user:
                user.set_password(nuevo_password)
                user.save()

            return redirect("facturacion:usuarios")

    else:
        form = UsuarioForm(instance=usuario)

    return render(
        request,
        "facturacion/editar_usuario.html",
        {
            "form": form,
            "usuario": usuario
        }
    )



@login_required
def eliminar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == "POST":
        usuario.delete()
        return redirect("facturacion:usuarios")
    return render(
        request,
        "facturacion/eliminar_usuario.html",
        {"usuario": usuario}
    )

#cliente. smith

@login_required
def cliente (request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'facturacion/partials/usuarios.html')
    cliente = Cliente.objects.all().order_by("nombre")
    return render(request, 'facturacion/cliente.html', {"cliente": cliente})

@login_required
def crear_cliente(request):
    # Si es AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'facturacion/partials/cliente.html')
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("facturacion:cliente")
    else:
        form = ClienteForm()
    return render(request, 'facturacion/crear_cliente.html', {"form": form})

@login_required
def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == "POST":
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect("facturacion:cliente")

    else:
        form = ClienteForm(instance=cliente)

    return render(
        request,
        "facturacion/editar_cliente.html",
        {
            "form": form,
            "cliente": cliente
        }
    )



@login_required
def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == "POST":
        cliente.delete()
        return redirect("facturacion:cliente")
    return render(
        request,
        "facturacion/eliminar_cliente.html",
        {"cliente": cliente}
    )