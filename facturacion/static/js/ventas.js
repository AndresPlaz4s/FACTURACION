let productos = [];
const selCliente = document.getElementById("cliente");
const selPago = document.getElementById("formaPago");
const selectProd = document.getElementById("selectProducto");
const buscar = document.getElementById("buscarProducto");
const resultados = document.getElementById("lista-resultados");
const tabla = document.getElementById("grupoinputs");
const totalVenta = document.getElementById("totalVenta");
const dataHidden = document.getElementById("dataVenta");

/* --------------------------- BUSCADOR --------------------------- */
function buscarProducto() {
    const q = buscar.value.toLowerCase();
    resultados.innerHTML = "";

    if (!q) return;

    [...selectProd.options]
        .filter(o => o.text.toLowerCase().includes(q))
        .slice(0, 7)
        .forEach(o => {
            const li = document.createElement("li");
            li.textContent = `${o.text} ($${o.dataset.precio})`;
            li.onclick = () => seleccionarProducto(o);
            resultados.appendChild(li);
        });
}

/* --------------------- SELECCIONAR Y AGREGAR -------------------- */
function seleccionarProducto(opt) {
    const id = opt.value;
    const nombre = opt.text;
    const precio = parseFloat(opt.dataset.precio);
    const stock = parseInt(opt.dataset.stock);

    let cantidad = 1;
    if (stock <= 0) return alert("Sin stock disponible");

    // Si ya está en la lista, solo aumentar cantidad
    let p = productos.find(x => x.id == id);
    if (p) {
        if (p.cantidad + 1 > stock) return alert("Stock insuficiente");
        p.cantidad++;
        p.total = p.cantidad * p.precio;
    } else {
        productos.push({
            id, nombre, precio,
            cantidad: 1,
            total: precio
        });
    }

    buscar.value = "";
    resultados.innerHTML = "";
    renderTabla();
}

/* -------------------------- TABLA -------------------------- */
function renderTabla() {
    tabla.innerHTML = "";
    let total = 0;

    productos.forEach((p, i) => {
        total += p.total;

        tabla.innerHTML += `
            <tr>
                <td>${p.nombre}</td>
                <td>$${p.precio.toFixed(2)}</td>
                <td>
                    <input type="number" min="1" value="${p.cantidad}"
                        onchange="cambiarCantidad(${i}, this.value)">
                </td>
                <td>$${p.total.toFixed(2)}</td>
                <td><button onclick="eliminar(${i})">X</button></td>
            </tr>
        `;
    });

    totalVenta.textContent = total.toFixed(2);

    dataHidden.value = JSON.stringify({
        cliente: selCliente.value,
        forma_pago: selPago.value,
        productos
    });
}

/* ----------------------- ACCIONES FILA ----------------------- */
function cambiarCantidad(i, nueva) {
    nueva = parseInt(nueva);

    const opt = selectProd.querySelector(`option[value="${productos[i].id}"]`);
    const stock = parseInt(opt.dataset.stock);

    if (nueva > stock) {
        alert("Stock insuficiente");
        return renderTabla();
    }

    productos[i].cantidad = nueva;
    productos[i].total = nueva * productos[i].precio;
    renderTabla();
}

function eliminar(i) {
    productos.splice(i, 1);
    renderTabla();
}

function eliminarTodos() {
    productos = [];
    renderTabla();
}
