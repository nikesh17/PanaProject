/** @odoo-module **/

import { Dropdown } from "@web/core/dropdown/dropdown";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { browser } from "@web/core/browser/browser";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

import { Component } from "@odoo/owl";

import {UserMenu} from '@web/webclient/user_menu/user_menu'


export class FarmerUserMenu extends Component {
    setup() {
        this.company = useService('company');
    }

}
FarmerUserMenu.template = "farmer.UserCompany";
export const systrayItem = {
    Component: FarmerUserMenu,
};

console.log(registry.category("systray").entries)
registry.category("systray").add("farmer.UserCompany", systrayItem, { sequence: 200 });
