/**@odoo-module **/
import { patch } from "@web/core/utils/patch";
import { ProductCard } from "@point_of_sale/app/components/product_card/product_card";
import { PosStore } from "@point_of_sale/app/services/pos_store";
import { Orderline } from "@point_of_sale/app/components/orderline/orderline";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";
import { PosConfig } from "@point_of_sale/app/models/pos_config";
import {useState} from "@odoo/owl";


patch(PosStore.prototype, {

    async processServerData() {
        await super.processServerData();
        console.log(this.models)

    },
});

console.log(this.models)
patch(ProductCard.prototype, {
    setup() {
        super.setup();
        this.state = useState({
            hierarchy: 23,
        });




    },

});

