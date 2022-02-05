"use strict";
const formatter1 = new Intl.NumberFormat('ru-RU', { minimumFractionDigits: 1 });
const formatter2 = new Intl.NumberFormat('ru-RU', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
const cost_per_hour = parseFloat(document.getElementById('costPerHour').textContent.replace(/[^\d,]/g, ''));
let works = document.getElementsByName('work');
// let toggler_nested = document.getElementsByClassName('nested');

window.onbeforeunload = function () {
    let tableRef = document.getElementById('tableOfOrder').getElementsByTagName('tbody')[0];
    if (tableRef.rows.length > 0) {
        return true;
    }
}

// обработчики выбора групп работ
// ******************************

// поиск по работам
function work_search(inp) {
    inp.value = inp.value.replace(/^[\s\A-z\\\-=_''""\.]+|[\s\A-z\\\-=_''""\.]+$/gi, '');
    let search_string = inp.value.toUpperCase();

    if (search_string.length < 3) {
        return;
    }

    let works = document.querySelectorAll('#generalWorksUL > li.work');
    let found_string;

    for (let work of works) {
        found_string = work.textContent.toUpperCase().includes(search_string);

        if (found_string) {
            work.classList.remove('hidden');
        }
        else {
            work.classList.add('hidden');
        }
    }
}

// очищает поле поиска
function clear_search_field() {
    document.getElementById('workSearch').value = '';
}

function change_caret() {
    this.classList.toggle('caret-down');
    let current_element = this.parentElement.querySelector('.nested');

    if (current_element) {
        current_element.classList.toggle('active');
    }

    let groups_active = document.getElementsByClassName('workgroup-active');

    for (let i = 0; i < groups_active.length; i++) {
        groups_active[i].classList.remove('workgroup-active');
    }

    this.classList.add('workgroup-active');
    clear_search_field();

    // for (let i = 0; i < toggler_nested.length; i++) {
    //     if (toggler_nested[i] != current_element) {
    //         toggler_nested[i].classList.remove('active');
    //     }
    // }
}

function select_works() {
    // покажу только работы относящиеся к активному узлу работ
    let pk = this.getAttribute('data-vehicleunit-pk');

    for (let i = 0; i < works.length; i++) {
        if (works[i].getAttribute('data-vehicleunit-pk') == pk) {
            works[i].classList.remove('hidden');
        }
        else {
            works[i].classList.add('hidden');
        }
    }

    // выделю цветом активный узел работ
    let vehicleunits_active = document.getElementsByClassName('vehicleunit-active');

    for (let i = 0; i < vehicleunits_active.length; i++) {
        vehicleunits_active[i].classList.remove('vehicleunit-active');
    }

    this.classList.add('vehicleunit-active');
    clear_search_field();
}

function handler_work_selection() {
    let toggler_workgroup = document.getElementsByClassName('caret');
    let toggler_vehicleunit = document.getElementsByClassName('vehicleunit');

    for (let i = 0; i < toggler_workgroup.length; i++) {
        toggler_workgroup[i].addEventListener('click', change_caret);
    }

    for (let i = 0; i < toggler_vehicleunit.length; i++) {
        toggler_vehicleunit[i].addEventListener('click', select_works);
    }
}

// *******************************
// Конец обработчика выбора групп

// Обработчики таблицы заказ-наряда
// ********************************

function getCookie(name) {
    let matches = document.cookie.match(new RegExp("(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"));
    return matches ? decodeURIComponent(matches[1]) : undefined;
}

function checkMaxRows() {
    let tableRef = document.getElementById('tableOfOrder').getElementsByTagName('tbody')[0];
    return tableRef.rows.length >= 30;
}

// если есть хоть одна строка в заказ-наряде, то спрашивать подтверждение перехода
// function checkMinRows() {
//     let tableRef = document.getElementById('tableOfOrder').getElementsByTagName('tbody')[0];
//     if (tableRef.rows.length > 0) {
//         return confirm('Вы потеряете данные заказ наряда. Покинуть страницу?');
//     }
// }

function calculateSumOrder() {
    let tableRef = document.getElementById('tableOfOrder').getElementsByTagName('tbody')[0];
    let sum_order = 0;

    for (let row of tableRef.rows) {
        sum_order += parseFloat(row.cells[4].textContent.replace(/[^\d,]/g, ''));
    }

    document.getElementById('sumOrder').textContent = formatter2.format(sum_order);
}

// ограничу ввод количества работ от 1 до 15
function handlerInputCount() {
    this.value = this.value.replace(/[^\d]/g, '');

    if (this.value < 1) {
        this.value = 1;
    }
    else if (this.value > 15) {
        this.value = 15;
    }

    let costWorkCell = this.parentElement.parentElement.cells[4];
    let hoursWorkCell = this.parentElement.parentElement.cells[3];
    let hoursWork = hoursWorkCell.textContent.replace(',', '.');
    hoursWork = hoursWork.replace(/[^\d.]/g, '');
    costWorkCell.textContent = formatter2.format(parseFloat(hoursWork) * this.value * cost_per_hour);

    calculateSumOrder();
}

// Получаю полную инфу о выбранной работе из БД сайта
async function get_work(btn) {
    if (checkMaxRows() & !btn.classList.contains('btn-added-work')) {
        return; //если максимальное число строк в заказ-наряде, то нчиего не делаю
    }

    btn.classList.toggle('btn-add-work');
    btn.classList.toggle('btn-added-work');

    if (!btn.classList.contains('btn-added-work')) {
        delete_work(btn); // если кнопка при нажатии сменила класс на btn-add-work, то просто удалю работу из заказ-наряда
        return;
    }

    let work = { work_pk: btn.parentElement.parentElement.parentElement.getAttribute('data-work-pk') };
    let options = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json;charset=utf-8', 'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': getCookie('csrftoken') },
        credentials: 'same-origin',
        body: JSON.stringify(work)
    };

    let response = await fetch('/add-work-to-order', options);

    if (response.ok) {
        let work_info = await response.json();
        add_work(work_info);
    }
    else {
        console.log('Ошибка HTTP: ' + response.status);
    }
}

// добавлю строку в таблицу работ
// root_work - название корневой работы если текущая работа является дополнительной
function add_row(work, root_work = '') {
    let tableRef = document.getElementById('tableOfOrder').getElementsByTagName('tbody')[0];
    let newRow = tableRef.insertRow();

    newRow.insertCell(0).textContent = ''; // tableRef.rows.length;
    let nameCell = newRow.insertCell(1);
    nameCell.textContent = work.name;

    if (root_work) {
        nameCell.classList.add('subwork');

        if (work.optional) {
            nameCell.textContent = '(дополнительно) ' + work.name;
        }
    }

    let countWorksCell = newRow.insertCell(2);
    let inputCount = document.createElement('input');
    inputCount.setAttribute('name', 'inputCount');
    inputCount.setAttribute('type', 'number');
    inputCount.setAttribute('step', '1');
    inputCount.setAttribute('min', '1');
    inputCount.setAttribute('max', '15');
    inputCount.value = 1;
    inputCount.addEventListener('input', handlerInputCount);
    countWorksCell.appendChild(inputCount);
    newRow.insertCell(3).textContent = formatter1.format(work.working_hour) + ' н-ч';
    newRow.insertCell(4).textContent = formatter2.format(work.working_hour * cost_per_hour);
    let btnDel = document.createElement('button');
    btnDel.classList.add('btn', 'btn-secondary', 'btn-sm', 'btn-delete-work');
    btnDel.setAttribute('onclick', 'delete_work(this);');
    let delWorkCell = newRow.insertCell(5);
    delWorkCell.appendChild(btnDel);

    if (root_work) {
        newRow.setAttribute('data-bs-toggle', 'tooltip');
        newRow.setAttribute('data-bs-placemant', 'bottom');
        newRow.setAttribute('title', 'Относится к работе: ' + root_work);
        delWorkCell.setAttribute('data-work-pk', work.work_id);
        delWorkCell.setAttribute('data-subwork-pk', work.pk);
    }
    else {
        delWorkCell.setAttribute('data-work-pk', work.pk);
    }
}

//Добавляю работу в таблицу Заказ-наряда
function add_work(work_info) {
    add_row(work_info);

    for (let subwork of work_info.subworks) {
        add_row(subwork, work_info.name);
    }

    calculateSumOrder();
}

function delete_work(btn) {
    let tableRef = document.getElementById('tableOfOrder').getElementsByTagName('tbody')[0];
    let del_work_is_root = !btn.parentElement.hasAttribute('data-subwork-pk');
    let del_work_pk = btn.parentElement.getAttribute('data-work-pk') | btn.parentElement.parentElement.parentElement.getAttribute('data-work-pk');
    let del_subwork_pk = btn.parentElement.getAttribute('data-subwork-pk');
    let delete_rows = [];

    //удаляет работу из Заказ-наряда, если работа содержит составные работы, то удаляет и их.
    for (let row of tableRef.rows) {
        for (let cell of row.cells) {
            if (del_work_is_root & cell.getAttribute('data-work-pk') == del_work_pk) {
                delete_rows.push(row);
                break;
            }
            else if (!del_work_is_root & cell.getAttribute('data-subwork-pk') == del_subwork_pk) {
                delete_rows.push(row);
                break;
            }
        }
    }

    for (let row of delete_rows) {
        row.remove();
    }

    calculateSumOrder();

    //удаляет галочку из окна выбора путем замены класса btn-added-work на btn-add-work
    if (del_work_is_root) {
        let work_buttons = document.getElementsByClassName('btn-added-work');

        for (let button of work_buttons) {
            if (button.parentElement.parentElement.parentElement.getAttribute('data-work-pk') == del_work_pk) {
                button.classList.remove('btn-added-work');
                button.classList.add('btn-add-work');
                break;
            }
        }
    }
}

let tableToExcel = (function () {
    let uri = 'data:application/vnd.ms-excel;base64,'
        , template = '<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:x="urn:schemas-microsoft-com:office:excel" xmlns="http://www.w3.org/TR/REC-html40"><head><!--[if gte mso 9]><xml><x:ExcelWorkbook><x:ExcelWorksheets><x:ExcelWorksheet><x:Name>{worksheet}</x:Name><x:WorksheetOptions><x:DisplayGridlines/></x:WorksheetOptions></x:ExcelWorksheet></x:ExcelWorksheets></x:ExcelWorkbook></xml><![endif]--><meta http-equiv="content-type" content="text/plain; charset=UTF-8"/></head><body><table>{table}</table></body></html>'
        , base64 = function (s) { return window.btoa(unescape(encodeURIComponent(s))) }
        , format = function (s, c) {
            return s.replace(/{(\w+)}/g, function (m, p) { return c[p]; })
        }
        , downloadURI = function (uri, name) {
            let link = document.createElement("a");
            link.download = name;
            link.href = uri;
            link.click();
        }

    return function (table, name, fileName) {
        if (!table.nodeType) table = document.getElementById(table);
        let ctx = { worksheet: name || 'Worksheet', table: table.innerHTML }
        let resuri = uri + base64(format(template, ctx));
        downloadURI(resuri, fileName);
    }
})();

function exportTableToExcel(tableID, filename = '') {
    let downloadLink;
    let dataType = 'application/vnd.ms-excel';
    let tableSelect = document.getElementById(tableID);
    let tableHTML = tableSelect.outerHTML.replace(/ /g, '%20');

    // Specify file name
    filename = filename ? filename + '.xls' : 'excel_data.xls';

    // Create download link element
    downloadLink = document.createElement('a');

    document.body.appendChild(downloadLink);

    if (navigator.msSaveOrOpenBlob) {
        let blob = new Blob(['\ufeff', tableHTML], { type: dataType });
        navigator.msSaveOrOpenBlob(blob, filename);
    }
    else {
        // Create a link to the file
        downloadLink.href = 'data:' + dataType + ', ' + tableHTML;

        // Setting the file name
        downloadLink.download = filename;

        //triggering the function
        downloadLink.click();
    }
}

function saveToExcel() {
    // params: element id, sheet name, file name
    // tableToExcel('tableOfOrder', 'Заказ-наряд', 'order.xls');
    exportTableToExcel('tableOfOrder', 'table_order');
}

handler_work_selection();