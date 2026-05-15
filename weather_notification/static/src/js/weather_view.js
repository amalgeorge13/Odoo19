/** @odoo-module **/
import {Component, useState} from "@odoo/owl";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { registry } from "@web/core/registry";
import { useDiscussSystray } from "@mail/utils/common/hooks";
import { useDropdownState } from "@web/core/dropdown/dropdown_hooks";
import { useService } from "@web/core/utils/hooks";
import { Domain } from "@web/core/domain";
import { user } from "@web/core/user";
import { useCommand } from "@web/core/commands/command_hook";
import { _t } from "@web/core/l10n/translation";




export class WeatherMenu extends Component{
    static components = { Dropdown };
    static props = [];
    static template = "weather_notification.WeatherMenu";

    setup() {
        super.setup();
        this.state = useState({
            today : null
        });
        var string_date=new Date().toDateString();
        const date_list = string_date.split(" ");
        console.log(date_list)
        this.state.today = `${date_list[2]} ${date_list[1]} ${date_list[3]}`;
        const date_week =date_list[0    ]

        console.log(date_week)





    }

}

registry
    .category("systray")
    .add("weather_notification.WeatherMenu", { Component: WeatherMenu }, { sequence: 20 });
