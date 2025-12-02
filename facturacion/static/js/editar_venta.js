console.log("JS CARGADO CORRECTAMENTE");

document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM LISTO");

    const lista = document.getElementById("lista");
    const addProd = document.getElementById("addProd");
    const btnAdd = document.getElementById("btnAdd");
    const form = document.getElementById("form");
    const dataInput = document.getElementById("data");
    const cliente = document.getElementById("cliente");

    console.log({ lista, addProd, btnAdd, form, dataInput, cliente });
});


// ELEMENTOS DEL DOM
document.addEventListener("DOMContentLoaded", () => {
    const lista = document.getElementById("lista");
    const addProd = document.getElementById("addProd");
    const btnAdd = document.getElementById("btnAdd");
    const form = document.getElementById("form");
    const dataInput = document.getElementById("data");
    const cliente = document.getElementById("cliente");

    if (!lista || !addProd || !btnAdd || !form || !dataInput || !cliente) {
        console.error("ERROR: Algún elemento del DOM no existe.");
        return;
    }

    // AGREGAR UN PRODUCTO A LA TABLA
    btnAdd.onclick = () => {
        if (!addProd.value) return;

        let id = addProd.value;
        let nombre = addProd.selectedOptions[0].text;

        let tr = document.createElement("tr");
        tr.setAttribute("data-id", id);

        tr.innerHTML = `
            <td>${nombre}</td>
            <td><input type="number" class="cant" value="1" min="1"></td>
            <td><button type="button" class="del">X</button></td>
        `;

        lista.appendChild(tr);
    };

    // ELIMINAR FILA
    lista.addEventListener("click", (e) => {
        if (e.target.classList.contains("del")) {
            e.target.closest("tr").remove();
        }
    });

    // ANTES DE ENVIAR EL FORMULARIO
    form.onsubmit = () => {
        let items = [];

        lista.querySelectorAll("tr").forEach((tr) => {
            items.push({
                id: tr.dataset.id,
                cantidad: tr.querySelector(".cant").value
            });
        });

        dataInput.value = JSON.stringify({
            cliente: cliente.value,
            items: items
        });

        return true;
    };
});
