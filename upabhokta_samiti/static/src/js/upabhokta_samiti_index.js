odoo.define("upabhokta_samiti.index", function (require) {
    'use strict';

    var publicWidget = require("web.public.widget");
    var core = require("web.core");

    var _t = core._t;

    publicWidget.registry.DriversUnMode = publicWidget.Widget.extend({
        selector: ".multisteps-form__progress",
        event: {
            "click button#.form__progress_btn": "_click_handler"
        },
        _click_handler: function (e) {
            console.log(e);
        },

    })

    $('.dropdown-toggle').dropdown();


})


var navbarDropdownMenuLink = document.getElementById('navbarDropdownMenuLink');
var dropdownMenu = document.getElementById('dropdownMenu');
navbarDropdownMenuLink.addEventListener('click', () => {
    dropdownMenu.classList.toggle('show');
});

document.addEventListener('click', function (event) {
    const isClickInsideMenu = dropdownMenu.contains(event.target);
    const isClickOnToggle = navbarDropdownMenuLink.contains(event.target);

    if (!isClickInsideMenu && !isClickOnToggle) {
        dropdownMenu.classList.remove('show');
    }
});

const navToggleBtn = document.getElementById("navToggleBtn");
const top_menu = document.getElementById("top_menu");
navToggleBtn.addEventListener('click', () => {
    top_menu.classList.toggle("show-primary-nav");
    document.getElementById("primaryNav").classList.toggle("h-auto");
});





