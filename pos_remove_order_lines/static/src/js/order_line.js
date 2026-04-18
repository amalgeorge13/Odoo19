/**@odoo-module **/
import { patch } from "@web/core/utils/patch";
import { Orderline } from "@point_of_sale/app/components/orderline/orderline";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";




patch(Orderline.prototype, {
    setup() {
        this.pos = usePos();
    },
    /* remove the line from order lines */
    async onClickRmv() {
        const orderLines = this.pos.getOrder()
        orderLines.removeOrderline(this.line)
   },


});
