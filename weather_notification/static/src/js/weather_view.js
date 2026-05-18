/** @odoo-module **/
import {Component, onWillStart, useState} from "@odoo/owl";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { registry } from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";






export class WeatherMenu extends Component{
    static components = { Dropdown };
    static props = [];
    static template = "weather_notification.WeatherMenu";

    setup() {
        super.setup();
        this.orm = useService('orm');
        this.state = useState({
            today : null,
            temperature:null,
            main:null,
            description:null,
            place:null
        });
        var string_date=new Date().toDateString();
        const date_list = string_date.split(" ");
        console.log(date_list)
        this.state.today = `${date_list[2]} ${date_list[1]} ${date_list[3]}`;
        const date_week =date_list[0]
        onWillStart(async () => {
            this._fetch_data();
        });


    }
    async _fetch_data(){
        // console.log("test :",this.orm)
        // console.log("1234",this)
        let result = await this.orm.call("res.partner", "get_weather_data", []);
        console.log(result)
        this.state.temperature = `${result.main.temp}°C ${result.weather[0].main}`
        this.state.description = `${result.weather[0].description} in ${result.name}`
        this.state.place = `Near ${result.name}`
        }

}

registry
    .category("systray")
    .add("weather_notification.WeatherMenu", { Component: WeatherMenu }, { sequence: 20 });
