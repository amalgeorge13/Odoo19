/**@odoo-module **/
import { patch } from "@web/core/utils/patch";
import { ProductCard } from "@point_of_sale/app/components/product_card/product_card";
import { useService } from "@web/core/utils/hooks";
import {useState} from "@odoo/owl";


patch(ProductCard.prototype, {
    async setup() {
        super.setup();
        this.orm = useService("orm");
        this.state = useState({
            qty: 0,
        });

        const result =await this.orm.call("product.template","fetch_qty",[this.props.productId]);
        this.state.qty=result

    },


});
