function alert() {

    var fName = document.getElementById('fName').value
    var bday = document.getElementById('birthday').value
    /*var retAge = document.getElementById('retAge').value
    var desIncome = document.getElementById('desIncome').value
    var initCont = document.getElementById('initCont').value
    var realCont = document.getElementById('realCont').value*/

    if (fName == '') {
        alert("Insira o nome do cliente.")
    }
    else if (bday == ''){
        alert("Insira a data de nascimento do cliente.")
    }
    /*else if (retAge == ''){
        alert("Insira a idade desejada de aposentadoria.")
    }
    else if (desIncome == ''){
        alert("Insira a renda desejada na aposentadoria.")
    }
    else if (initCont == ''){
        alert("Insira o valor do aporte inicial.")
    }
    else if (realCont == ''){
        alert("Insira o valor da contribuição real.")
    }*/
}