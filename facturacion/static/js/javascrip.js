const buscarBtn = document.getElementById("btnBuscar");
const buscarInput = document.getElementById("buscarProducto");
const listaResultados = document.getElementById("listaResultados");
const tabla = document.querySelector("#tablaProductos tbody");
const cancelarBtn = document.getElementById("btnCancelar");

buscarBtn.addEventListener("click", () => {
    const texto = buscarInput.value.trim();
    listaResultados.innerHTML = "";

    if (texto === "") return;

    const li = document.createElement("li");
    li.textContent = texto;
    li.addEventListener("click", () => agregarProducto(texto));
    listaResultados.appendChild(li);
});

function agregarProducto(nombre) {
    const fila = document.createElement("tr");
    const num = tabla.rows.length + 1;
    fila.innerHTML = `
        <td>${num}</td>
        <td>${nombre}</td>
        <td><input type="number" min="1" value="1" style="width:70px; text-align:center;"></td>
        <td><input type="number" min="0" step="0.01" value="0.00" style="width:90px; text-align:center;"></td>
        <td><button onclick="eliminarFila(this)">Eliminar</button></td>
    `;
    tabla.appendChild(fila);
    listaResultados.innerHTML = "";
    buscarInput.value = "";
}

function eliminarFila(btn) {
    btn.parentElement.parentElement.remove();
}

cancelarBtn.addEventListener("click", () => {
    tabla.innerHTML = "";
    buscarInput.value = "";
    listaResultados.innerHTML = "";
});
