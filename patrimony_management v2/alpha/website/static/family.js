const container = document.getElementById("inputs-container");
const btn = document.getElementById("add-inputs-btn");
let blockCount = 0;

btn.addEventListener("click", () => {
    blockCount++;
    const block = document.createElement("div");
    block.classList.add("input-block");
    block.innerHTML = `
    <form method="POST">
        <div class="form-row">
            <div class="form-group col-md-6">
            <label for="nome-${blockCount}">Nome:</label>
            <input id="nome-${blockCount}" type="text" class="form-control" name="nome-${blockCount}">
            </div>
            <div class="form-group col-md-6">
            <label for="data-nascimento-${blockCount}">Data de nascimento:</label>
            <input id="data-nascimento-${blockCount}" type="date" class="form-control" name="data-nascimento-${blockCount}">
            </div>
        </div>
        <div class="form-row">
            <div class="form-group col-md-6">
            <label for="parentesco-${blockCount}">Parentesco:</label>
            <select id="parentesco-${blockCount}" class="form-control" name="parentesco-${blockCount}">
                <option value="conjuge">Cônjuge</option>
                <option value="filho">Filho(a)</option>
                <option value="irmao">Irmão</option>
                <option value="paimae">Pai/Mãe</option>
            </select>
            </div>
            <div class="form-group col-md-6">
            <label for="regime-casamento-${blockCount}">Regime de casamento:</label>
            <select id="regime-casamento-${blockCount}" class="form-control" name="regime-casamento-${blockCount}">
                <option value="nsa">Não se aplica</option>
                <option value="comunhão-parcial">Comunhão parcial de bens</option>
                <option value="comunhão-universal">Comunhão universal de bens</option>
                <option value="separação-bens">Separação total de bens</option>
                <option value="participação-final-nos-aquestos">Participação final nos aquestos</option>
            </select>
            </div>
        </div>
    </form>
    <button class="btn btn-danger delete-btn">Deletar bloco</button>
    `;
    container.appendChild(block);

    const deleteBtn = block.querySelector(".delete-btn");
    deleteBtn.addEventListener("click", () => {
        const blocks = document.querySelectorAll(".input-block");
        const index = Array.from(blocks).indexOf(block);
        if (index > -1) {
            block.remove();
            --blockCount;
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

