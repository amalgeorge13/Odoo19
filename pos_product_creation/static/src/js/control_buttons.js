/**@odoo-module **/
import { patch } from "@web/core/utils/patch";
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";



patch(ControlButtons.prototype, {

    /*
    * button function to open new window
    * */
    async ListProduct() {
        console.log("1234567898765432123456789")

   },

});