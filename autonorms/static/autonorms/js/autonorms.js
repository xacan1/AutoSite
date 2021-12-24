const formatter1 = new Intl.NumberFormat('ru-RU', { minimumFractionDigits: 1 });
const formatter2 = new Intl.NumberFormat('ru-RU', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
const cost_per_hour = parseFloat(document.getElementById('costPerHour').textContent);
let works = document.getElementsByName('work');
// let toggler_nested = document.getElementsByClassName('nested');

function getCookie(name) {
    let matches = document.cookie.match(new RegExp("(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"));
    return matches ? decodeURIComponent(matches[1]) : undefined;
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

    // for (let i = 0; i < toggler_nested.length; i++) {
    //     if (toggler_nested[i] != current_element) {
    //         toggler_nested[i].classList.remove('active');
    //     }
    // }
}

function select_works() {
    let pk = this.getAttribute('data-vehicleunit-pk');

    for (let i = 0; i < works.length; i++) {
        if (works[i].getAttribute('data-vehicleunit-pk') == pk) {
            works[i].classList.remove('hidden');
        }
        else {
            works[i].classList.add('hidden');
        }
    }

    let vehicleunits_active = document.getElementsByClassName('vehicleunit-active');

    for (let i = 0; i < vehicleunits_active.length; i++) {
        vehicleunits_active[i].classList.remove('vehicleunit-active');
    }

    this.classList.add('vehicleunit-active');
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

// Получаю полную инфу о выбранной работе из БД сайта
async function get_work(btn) {
    btn.classList.toggle('btn-add-work');
    btn.classList.toggle('btn-added-work');

    let work = {
        work_pk: btn.parentElement.parentElement.parentElement.getAttribute('data-work-pk'),
        add: btn.classList.contains('btn-added-work')
    };
    let options = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json;charset=utf-8', 'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': getCookie('csrftoken') },
        credentials: 'same-origin',
        body: JSON.stringify(work)
    };
    let response = await fetch('/add-work-to-order', options);

    if (response.ok) {
        let work_info = await response.json();

        if (work.add) {
            add_work(work_info);
        }
        else {
            delete_work(btn);
        }
    }
    else {
        console.log('Ошибка HTTP: ' + response.status);
    }
}

// добавлю строку в таблицу работ
// work_is_root - признак, что работа является корневой, а не дополнительной
function add_row(work, work_is_root) {
    let tableRef = document.getElementById('tableOfOrder').getElementsByTagName('tbody')[0];

    let newRow = tableRef.insertRow();
    newRow.insertCell(0).textContent = tableRef.rows.length;
    newRow.insertCell(1).textContent = work.name;
    newRow.insertCell(2).textContent = 1;
    newRow.insertCell(3).textContent = formatter1.format(work.working_hour) + ' н-ч';
    newRow.insertCell(4).textContent = formatter2.format(work.working_hour * cost_per_hour);
    let btnDel = document.createElement('button');
    btnDel.classList.add('btn', 'btn-secondary', 'btn-sm', 'btn-delete-work');
    btnDel.setAttribute('onclick', 'delete_work(this);');
    let delWorkCell = newRow.insertCell(5);
    delWorkCell.appendChild(btnDel);

    if (work_is_root) {
        delWorkCell.setAttribute('data-work-pk', work.pk);
    }
    else {
        delWorkCell.setAttribute('data-work-pk', work.work_id);
        delWorkCell.setAttribute('data-subwork-pk', work.pk);
    }
}

//Добавляю работу в таблицу Заказ-наряда
function add_work(work_info) {
    add_row(work_info, true);

    for (let subwork of work_info.subworks) {
        add_row(subwork, false);
    }
}

function delete_work(btn) {
    let tableRef = document.getElementById('tableOfOrder').getElementsByTagName('tbody')[0];
    let del_work_is_root = !btn.parentElement.hasAttribute('data-subwork-pk');
    let del_work_pk = btn.parentElement.getAttribute('data-work-pk') | btn.parentElement.parentElement.parentElement.getAttribute('data-work-pk');
    let del_subwork_pk = btn.parentElement.getAttribute('data-subwork-pk');
    let delete_rows = [];

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

handler_work_selection();