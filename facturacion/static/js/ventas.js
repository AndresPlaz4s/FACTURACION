let productosSeleccionados = [];
let listaOriginal = [];

window.onload = function() {
  // Cargar productos desde el select (limpiando texto)
  const opts = document.querySelectorAll("#selectProducto option");
  opts.forEach(op => {
    if (op.value !== "") {
      listaOriginal.push({
        id: op.value.trim(),
        nombre: op.textContent.trim().toLowerCase(),
        nombreMostrar: op.textContent.trim(),
        precio: parseFloat(op.dataset.precio),
        stock: parseInt(op.dataset.stock)
      });
    }
  });
};

function mostrarResultados(filtrados) {
  const listaResultados = document.getElementById('lista-resultados');
  listaResultados.innerHTML = '';

  filtrados.forEach(p => {
    const li = document.createElement('li');
    li.innerHTML = `
      <span class="nombre-producto">${p.nombreMostrar}</span>
      <span class="precio-producto">$${p.precio.toFixed(2)}</span>
      <span class="stock-producto">Stock: ${p.stock}</span>
      <button class="btn-agregar" onclick="agregarProducto('${p.id}')">
        <i class="fa-solid fa-plus"></i>
      </button>
    `;
    listaResultados.appendChild(li);
  });
}

function buscarProducto() {
  const texto = document.getElementById("buscarProducto").value.toLowerCase().trim();
  if (texto === '') {
    document.getElementById('lista-resultados').innerHTML = '';
    return;
  }
  
  const filtrados = listaOriginal.filter(p => p.nombre.includes(texto));
  
  if (filtrados.length === 0) {
    document.getElementById('lista-resultados').innerHTML = 
      '<li>No se encontraron productos que coincidan con "' + texto + '". Verifique el inventario.</li>';
  } else {
    mostrarResultados(filtrados);
  }
}

// Buscar mientras escribe
document.getElementById("buscarProducto").addEventListener("keyup", function() {
  buscarProducto();
});

function agregarProducto(id) {
  const producto = listaOriginal.find(p => p.id === id);
  if (!producto) return;

  const productoExistente = productosSeleccionados.find(p => p.id === id);
  
  if (productoExistente) {
    if (productoExistente.cantidad < producto.stock) {
      productoExistente.cantidad++;
    } else {
      alert('No hay más stock disponible para este producto');
      return;
    }
  } else {
    if (producto.stock > 0) {
      productosSeleccionados.push({
        id: producto.id,
        nombre: producto.nombreMostrar,
        cantidad: 1,
        precio: producto.precio
      });
    } else {
      alert('No hay stock disponible para este producto');
      return;
    }
  }

  actualizarTabla();
}

function actualizarTabla() {
  const tbody = document.getElementById("grupoinputs");
  tbody.innerHTML = "";
  let totalVenta = 0;

  productosSeleccionados.forEach((p, i) => {
    let subtotal = p.cantidad * p.precio;
    totalVenta += subtotal;
    
    // Agregamos data-productoid para mantener el ID del producto
    tbody.innerHTML += `
      <tr data-productoid="${p.id}">
        <td>${p.nombre}</td>
        <td>
          <input type="number" min="1" value="${p.cantidad}" 
                 onchange="cambiar(${i}, this.value)">
        </td>
        <td>$${p.precio.toFixed(2)}</td>
        <td>$${subtotal.toFixed(2)}</td>
        <td>
          <button type="button" onclick="eliminar(${i})" class="btn-eliminar">
            <i class="fa-solid fa-trash"></i>
          </button>
        </td>
      </tr>
    `;
  });
}

  document.getElementById("totalVenta").textContent = totalVenta.toFixed(2);
}

function cambiar(i, value) {
  const producto = listaOriginal.find(p => p.id === productosSeleccionados[i].id);
  const valorNumerico = parseInt(value);
  
  if (isNaN(valorNumerico) || valorNumerico < 1) {
    alert('La cantidad debe ser al menos 1');
    productosSeleccionados[i].cantidad = 1;
  } else if (valorNumerico > producto.stock) {
    alert('No hay suficiente stock disponible para este producto. Stock disponible: ' + producto.stock);
    productosSeleccionados[i].cantidad = producto.stock;
  } else {
    productosSeleccionados[i].cantidad = valorNumerico;
  }
  
  actualizarTabla();
}

function eliminar(i) {
  if (confirm('¿Está seguro de eliminar este producto?')) {
    productosSeleccionados.splice(i, 1);
    actualizarTabla();
  }
}

function eliminarTodos() {
  if (productosSeleccionados.length > 0) {
    if (confirm('¿Está seguro de limpiar toda la venta?')) {
      productosSeleccionados = [];
      actualizarTabla();
      document.getElementById('lista-resultados').innerHTML = '';
      document.getElementById('buscarProducto').value = '';
      document.getElementById('cliente').value = '';
    }
  }
}

// Manejo del envío del formulario
document.getElementById("formVenta").addEventListener("submit", function(e) {
  e.preventDefault();
  
  const cliente = document.getElementById("cliente").value;
  
  // Validaciones
  if (!cliente) {
    alert("Debe seleccionar un cliente");
    return;
  }
  
  if (productosSeleccionados.length === 0) {
    alert("Debe agregar al menos un producto a la venta");
    return;
  }
  
  // Preparar datos para enviar
  const data = {
    cliente: cliente,
    productos: productosSeleccionados.map(p => ({
      id: p.id,
      cantidad: p.cantidad
    }))
  };
  
  // Asignar al input hidden
  document.getElementById("dataVenta").value = JSON.stringify(data);
  
  // Enviar el formulario
  this.submit();
});
