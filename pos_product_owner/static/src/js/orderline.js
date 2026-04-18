import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { patch } from "@web/core/utils/patch";
console.log("qwert")

patch(PosOrderline.prototype, {

    getDisplayClasses() {
        console.log("This :",this)
        console.log('owner:',this.getProduct().product_owner_id)
        console.log("ownerName:",this.product_id.product_owner_id?.name)
        return {
            ...super.getDisplayClasses(),
            product_owner_id: this.getProduct().product_owner_id,
        };
    }
});
