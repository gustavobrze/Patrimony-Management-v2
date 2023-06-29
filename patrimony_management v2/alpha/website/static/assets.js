const container3 = document.getElementById("inputs-container-3");
const btn3 = document.getElementById("add-inputs-btn-3");
let blockCount3 = 0;

btn3.addEventListener("click", () => {
blockCount3++;
const block = document.createElement("div");
block.classList.add("input-block-3");
block.innerHTML = `
<form id="assetsForm" method="POST">
    <div class="form-row">
        <div class="form-group col-md-6">
        <label for="asset-${blockCount3}">Ativo:</label>
        <input id="asset-${blockCount3}" type="text" class="form-control" name="asset-${blockCount3}">
        </div>
        <div class="form-group col-md-6">
            <label for="assetType-${blockCount3}">Classe do ativo:</label>
            <select id="assetType-${blockCount3}" class="form-control" name="assetType-${blockCount3}">
                <option selected>Conta Corrente</option>
                <option>CDI POS</option>
                <option>CDI PRE</option>
                <option>Inflação</option>
                <option>COE</option>
                <option>Multimercado</option>
                <option>Fundo imobiliário</option>
                <option>Ação</option>
                <option>Hedge</option>
                <option>Internacional</option>
                <option>PGBL</option>
                <option>VGBL</option>
                <option>Outro</option>
            </select>
        </div>
        <div class="form-group col-md-6">
            <label for="assetValue-${blockCount3}">Valor atual (R$):</label>
            <input for="assetValue-${blockCount3}" type=text class="form-control campo_editavel" name="assetValue-${blockCount3}" id="assetValue-${blockCount3}" placeholder="Valor atual (R$)" onkeyup="updatePatrimonio(); formatValue()">
        </div>
        <div class="form-group col-md-6">
            <label for="bank-${blockCount3}">Instituição:</label>
            <select for="bank-${blockCount3}" type=text class="form-control" name="bank-${blockCount3}" id="bank-${blockCount3}">
                <option selected>Guide</option>
                <option>XP</option>
                <option>BTG</option>
                <option>Rico</option>
                <option>Itaú</option>
                <option>Bradesco</option>
                <option>Santander</option>
                <option>BB</option>
                <option>Safra</option>
                <option>Outros</option>
            </select>
        </div>
    </div>
</form>
<button class="btn btn-danger delete-btn">Deletar bloco</button>
`;
container3.appendChild(block);

const deleteBtn = block.querySelector(".delete-btn");
deleteBtn.addEventListener("click", () => {
    const blocks = document.querySelectorAll(".input-block-3");
    const index = Array.from(blocks).indexOf(block);
    if (index > -1) {
        block.remove();
        --blockCount3;
        for (let i = index; i < blocks.length; i++) {
            const inputs = blocks[i].querySelectorAll("input, select");
            for (let j = 0; j < inputs.length; j++) {
            const oldName = inputs[j].getAttribute("name");
            const newName = oldName.replace(`-${i + 1}`, `-${i}`);
            inputs[j].setAttribute("name", newName);
            const newLabel = inputs[j].parentNode.querySelector("label").setAttribute("for", newName);
            const oldId = inputs[j].getAttribute("id");
            const newId = oldId.replace(`-${i + 1}`, `-${i}`);
            inputs[j].setAttribute("id", newId)
            }
        }
    }
});

});

const assetsForm = document.getElementById("assetsForm");
const patrFin = document.getElementById("patrFin");

function updatePatrimonio() {
  const fields = document.querySelectorAll(".campo_editavel");
  let sum = 0;
  fields.forEach(field => {
    const value = Number(field.value.replace(",", "."));
    if (!isNaN(value)) {
      sum += value;
    }
  });
  sum2 = sum.toLocaleString()
  document.getElementById("patrFin").value = sum2;
}