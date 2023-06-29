const container2 = document.getElementById("inputs-container-2");
const btn2 = document.getElementById("add-inputs-btn-2");
let blockCount2 = 0;

btn2.addEventListener("click", () => {
    blockCount2++;
    const block = document.createElement("div");
    block.classList.add("input-block-2");
    block.innerHTML = `
    <form method="POST">
        <div class="form-row">
            <div class="form-group col-md-6">
                <label for="obj-${blockCount2}">Objetivo:</label>
                <select id="obj-${blockCount2}" class="form-control">
                    <option selected>Reserva de emergência</option>
                    <option>Imóvel</option>
                    <option>Carro</option>
                    <option>Viagem</option>
                    <option>Educação Filhos</option>
                    <option>Outros</option>
                </select>
            </div>
            <div class="form-group col-md-6">
            <label for="value-${blockCount2}">Valor financeiro (R$):</label>
            <input id="value-${blockCount2}" type="text" placeholder="Valor financeiro (R$)" class="form-control" name="value-${blockCount2}">
            </div>
        </div>
        <div class="form-row">
            <div class="form-group col-md-6">
                <label for="months-${blockCount2}">Prazo (meses):</label>
                <input id="months-${blockCount2}" type="text" class="form-control" name="months-${blockCount2}">
            </div>
            <div class="form-group col-md-6">
                <label for="priority-${blockCount2}">Prioridade:</label>
                <select id="priority-${blockCount2}" class="form-control">
                    <option selected>1</option>
                    <option>2</option>
                    <option>3</option>
                </select>
            </div>
        </div>
        <div class="form-row">
            <div class="form-group col-md-6">
                <label for="init-${blockCount2}">Aporte inicial (R$):</label>
                <input id="init-${blockCount2}" type="text" class="form-control" onkeyup="${calculatePMT()}" name="init-${blockCount2}" class="form-control">
            </div>
            <div class="form-group col-md-6">
                <label for="mensalCont-${blockCount2}">Aporte mensal (R$):</label>
                <input id="mensalCont-${blockCount2}" type="text" class="form-control" name="mensalCont-${blockCount2}" class="form-control" readonly>
            </div>
        </div>
        <div class="form-row">
            <div class="form-group col-md-6">
                <label for="realValue-${blockCount2}">Aporte real (R$):</label>
                <input type="text" class="form-control" id="realValue-${blockCount2}" name="realValue-${blockCount2}" placeholder="Aporte real (R$)">
            </div>
        </div>
        <div class="form-row">
            <label for="actPlan-${blockCount2}">Plano de ação</label>
            <textarea class="form-control" rows="4" id="actPlan-${blockCount2}"></textarea>
        </div>
    </form>
    <br>
    <button class="btn btn-danger delete-btn">Deletar bloco</button>
    `;

    container2.appendChild(block);

    const deleteBtn = block.querySelector(".delete-btn");
    deleteBtn.addEventListener("click", () => {
        const blocks = document.querySelectorAll(".input-block-2");
        const index = Array.from(blocks).indexOf(block);
        if (index > -1) {
            block.remove();
            --blockCount2;
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

    const initInput = block.querySelector(`#init-${blockCount2}`);
    const mensalContInput = block.querySelector(`#mensalCont-${blockCount2}`);

    initInput.addEventListener("keyup", () => {
        updateMensalCont();
    });

    const monthsInput = block.querySelector(`#months-${blockCount2}`);
    monthsInput.addEventListener("keyup", () => {
        updateMensalCont();
    });
    const totalValue = block.querySelector(`#value-${blockCount2}`);
    totalValue.addEventListener("keyup", () => {
        updateMensalCont()
    })
    mensalContInput.addEventListener("keyup", () => {
        const blocks = document.querySelectorAll(".input-block-2");
        blocks.forEach((block) => {
        const initInput = block.querySelector(`[id^="init-"]`);
        const monthsInput = block.querySelector(`[id^="months-"]`);
        const mensalContInput = block.querySelector(`[id^="mensalCont-"]`);
        var calculatedValue = parseFloat(mensalContInput.value) || 0;
        /*
        initInput.value = "";
        monthsInput.value = "";*/
        var finalValue = calculatedValue.toLocaleString();
        mensalContInput.value = finalValue;
        });
    });
    });

    function updateMensalCont() {
    const blocks = document.querySelectorAll(".input-block-2");
    blocks.forEach((block) => {
        const initValue = block.querySelector(`[id^="init-"]`);
        const monthsValue = block.querySelector(`[id^="months-"]`);
        const mensalContInput = block.querySelector(`[id^="mensalCont-"]`);
        const finalValue = block.querySelector(`[id^="value-"]`);

        const pv = parseFloat(initValue.value) || 0;
        const nper = parseInt(monthsValue.value) || 0;
        const fv = parseFloat(finalValue.value) || 0;
        var ir = 0.003659;

        let pmt = 0
        pmt = (ir * ((-pv) * Math.pow ((ir+1), nper) + fv)) / ((ir + 1) * (Math.pow((ir+1), nper) - 1));
        mensalContInput.value = pmt.toFixed(2);
    });

};
