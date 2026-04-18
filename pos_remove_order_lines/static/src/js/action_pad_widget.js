/**@odoo-module **/
import { patch } from "@web/core/utils/patch";
import { ActionpadWidget } from "@point_of_sale/app/screens/product_screen/action_pad/action_pad";



patch(ActionpadWidget.prototype, {

    /* clear all lines from order lines */
    async onClickClr() {
        const order =this.pos.getOrder()
        const lines =this.pos.getOrder().lines
        for (let i = 0; i < lines.length; i++) {
            order.removeOrderline(lines[i])
        }

   },

});