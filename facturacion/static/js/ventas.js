let productosSeleccionados = [];
let listaOriginal = [];

window.onload = function () {
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
        <span class="precio-producto">$${p.precio}</span>
        <span class="stock-producto">Stock: ${p.stock}</span>
        <button class="btn-agregar" onclick="agregarProducto('${p.id}')"><i class="fa-solid fa-plus"></i></button>
      `;
    listaResultados.appendChild(li);
  });
}


function buscarProducto() {
  const texto = document.getElementById("buscarProducto").value.toLowerCase();
  if (texto === '') {
    document.getElementById('lista-resultados').innerHTML = '';
    return;
  }
  const filtrados = listaOriginal.filter(p => p.nombre.includes(texto));

  if (filtrados.length === 0) {
    document.getElementById('lista-resultados').innerHTML = '<li>No se encontraron productos que coincidan con "' + texto + '". Verifique el inventario.</li>';
  } else {
    mostrarResultados(filtrados);
  }
}


document.getElementById("buscarProducto").addEventListener("keyup", function () {
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
    tbody.innerHTML += `
        <tr>
          <td>${p.nombre}</td>
          <td><input type="number" min="1" value="${p.cantidad}" onchange="cambiar(${i}, this.value)"></td>
          <td>$${p.precio.toFixed(2)}</td>
          <td>$${subtotal.toFixed(2)}</td>
          <td><button onclick="eliminar(${i})" class="btn-eliminar">
            <i class="fa-solid fa-trash"></i>
          </button></td>
        </tr>
      `;
  }); 
  if (productosSeleccionados.length === 0) {
    tbody.innerHTML = `
      <tr id="noProductosRow">
        <td colspan="5" style="text-align:center;">
          No hay productos agregados
        </td>
      </tr>
    `;
  }

  document.getElementById("totalVenta").textContent = totalVenta.toFixed(2);
}


function cambiar(i, value) {
  const producto = listaOriginal.find(p => p.id === productosSeleccionados[i].id);
  if (parseInt(value) > producto.stock) {
    alert('No hay suficiente stock disponible para este producto');
    productosSeleccionados[i].cantidad = producto.stock;
  } else {
    productosSeleccionados[i].cantidad = parseInt(value);
  }
  actualizarTabla();
}

function eliminar(i) {
  productosSeleccionados.splice(i, 1);
  actualizarTabla();
}

function eliminarTodos() {
  productosSeleccionados = [];
  actualizarTabla();
  document.getElementById('lista-resultados').innerHTML = '';
  document.getElementById('buscarProducto').value = '';
}


document.getElementById("formVenta").addEventListener("submit", function (e) {
  if (productosSeleccionados.length === 0) {
    alert("Debe agregar productos");
    e.preventDefault();
    return;
  }

  const cliente = document.getElementById("cliente").value;
  if (!cliente) {
    alert("Debe seleccionar un cliente");
    e.preventDefault();
    return;
  }

  document.getElementById("dataVenta").value = JSON.stringify({ cliente, productos: productosSeleccionados });
});



