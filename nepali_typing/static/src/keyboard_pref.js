console.log("((((")

import { Dropdown } from "@web/core/dropdown/dropdown";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { browser } from "@web/core/browser/browser";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

import { Component } from "@odoo/owl";

import {UserMenu} from '@web/webclient/user_menu/user_menu'

export class KeyboardPreferenceMenu extends Component {
    setup() {
        console.log("((())))")
    }

}
KeyboardPreferenceMenu.template = "nepali_typing.keyboard_opt";
export const systrayItem = {
    Component: KeyboardPreferenceMenu,
};

registry.category("systray").add("nepali_typing.keyboard_opt", systrayItem, { sequence: 1 });