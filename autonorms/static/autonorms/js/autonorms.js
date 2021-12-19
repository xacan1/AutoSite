let works = document.getElementsByName('work');
let toggler_vehicleunit = document.getElementsByClassName('vehicleunit');
// let toggler_nested = document.getElementsByClassName('nested');

function change_caret() {
    this.classList.toggle('caret-down');
    let current_element = this.parentElement.querySelector('.nested');

    if (current_element) {
        current_element.classList.toggle('active');
    }

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

    this.classList.add('vehicleunit-active');

    for (let i = 0; i < toggler_vehicleunit.length; i++) {
        if (toggler_vehicleunit[i] != this) {
            toggler_vehicleunit[i].classList.remove('vehicleunit-active');
        }
    }
}

function handler_work_selection() {
    let toggler_workgroup = document.getElementsByClassName('caret');

    for (let i = 0; i < toggler_workgroup.length; i++) {
        toggler_workgroup[i].addEventListener('click', change_caret);
    }

    for (let i = 0; i < toggler_vehicleunit.length; i++) {
        toggler_vehicleunit[i].addEventListener('click', select_works);
    }
}

handler_work_selection();