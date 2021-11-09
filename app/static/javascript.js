var formPath = "/form/"
var indexPath = "/"
var pathName = location.pathname

document.addEventListener('DOMContentLoaded', function () {


  console.log("oi")

  myFunctions()

}, false);

(function (win, doc) {
  'use strict';


  // VERIFICA SE O USUÁRIO REALMENTE QUER DELETAR O DADO
  if (doc.querySelector('.btnDel') && indexPath == pathName) {
    var btnDel = doc.querySelectorAll('.btnDel');
    for (var i = 0; i < btnDel.length; i++) {
      btnDel[i].addEventListener('click', function (event) {
        if (confirm('Deseja mesmo excluir?')) {
          return true
        } else {
          event.preventDefault()
        }
      })
    }
  }

  // AJAX DO FORM
  if (doc.querySelector('#form') && indexPath == pathName) {
    var form = doc.querySelector('#form')
    function sendForm(event) {
      event.preventDefault();
      var data = new FormData(form);
      var ajax = new XMLHttpRequest();
      var token = doc.querySelectorAll('input'[0].value);
      ajax.open('POST', form.action);
      ajax.setRequestHeader('X-CSRF-TOKEN', token)
      ajax.onreadystatechange = function () {
        if (ajax.status === 200 && ajax.readyState === 4) {
          var result = doc.querySelector('#result');
          result.innerHTML = 'Operação realizada.'
          result.classList.add('alert')
          result.classList.add('alert-success')
        }
      }
      ajax.send(data);
      form.reset();
    }
    form.addEventListener('submit', sendForm, false)
  }

  if (document.querySelectorAll("#tbl-jobs td.sum").length > 0 && indexPath == pathName) {

    var goldDayColumns = document.querySelectorAll("#tbl-jobs td.sum")
    var jobColumns = document.querySelectorAll("#tbl-jobs td.job")
    var attrColumns = document.querySelectorAll("#tbl-jobs td.attr")
    var lvlColumns = document.querySelectorAll("#tbl-jobs td.lvl")
    var qntColumns = document.querySelectorAll("#tbl-jobs td.qnt")
    var levels = {
      1: 1, 2: 2, 3: 4, 4: 8, 5: 16
    }
    var subtotal = []
    var reducer = (previousValue, currentValue) => previousValue + currentValue;

    goldDayColumns.forEach((value, index) => {
      var qntHerois = parseInt(lvlColumns[index].innerHTML) * parseInt(qntColumns[index].innerHTML)
      if (jobColumns[index].innerHTML.toLowerCase() == "part-time") {
        var result = qntHerois * 288
        value.innerHTML = result
      } else {
        var fator = (((parseInt(attrColumns[index].innerHTML) - 85) * 0.005) + 0.01) * 28800
        var fatorLevel = fator * levels[parseInt(lvlColumns[index].innerHTML)]
        var result = Math.ceil(fatorLevel * parseInt(qntColumns[index].innerHTML))
        value.innerHTML = result
      }
      subtotal.push(result)
    })

    document.getElementById("golddayresult").innerHTML = `Total gold per day: ${subtotal.reduce(reducer)}`


  }

})(window, document);

function myFunctions() {


  if (document.querySelector('#generate-pwd-button') && indexPath == pathName) {
    var generatedPwd = document.getElementById('generate-pwd-button');
    generatedPwd.addEventListener('click', function (event) {
      var newPwd = generatePassword(15)
      document.getElementById("generated-pwd").innerHTML = `your new password: ${newPwd}`
      event.preventDefault();
    })
  }

  if (indexPath == pathName) {
    if (document.querySelector('#golddayresult').innerHTML != "") {
      var numberPattern = /\d+/g;
      var currency = /\d\.\d+/g;
      var parseGoldVDay = parseInt(document.getElementById('golddayresult').innerHTML.match(numberPattern).join(""))
      var parseGoldValue = parseFloat(document.getElementById('goldactualvalue').innerHTML.match(currency).join(""))

      var goldPerDay = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(parseGoldVDay * parseGoldValue)
      var goldPerWeek = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(parseGoldVDay * parseGoldValue * 7)
      var goldPerMonth = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(parseGoldVDay * parseGoldValue * 30)

      document.getElementById("earning-col1").innerHTML = `USD per day: ${goldPerDay}`
      document.getElementById("earning-col2").innerHTML = `USD per week: ${goldPerWeek}`
      document.getElementById("earning-col3").innerHTML = `USD per month: ${goldPerMonth}`
    }
  }


  function generatePassword(length) {
    var chars = `0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!"#$%&'()*+,-./:;<=>?@[\]^_{|}~`;
    var string_length = length;
    var randomstring = '';
    for (var i = 0; i < string_length; i++) {
      var rnum = Math.floor(Math.random() * chars.length);
      randomstring += chars.substring(rnum, rnum + 1);
    }
    return randomstring;
  };

};