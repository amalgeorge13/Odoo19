/** @odoo-module */
import { Dialog } from "@web/core/dialog/dialog";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";
import { Component, useState } from "@odoo/owl";
export class ProductsPopup extends Component {
    static template = "pos_product_creation.ProductsPopup";
    static components = { Dialog };
    setup() {
        this.pos = usePos();
        // console.log(this.pos)
        // const partner = this.props.order.getPartner?.() || {};
        // console.log(partner)
        this.state = useState({
            products: null
        });
        this.state.products=this.pos.models["product.product"].records
        console.log(this.state.products)
    }
    closePopupScreen() {
       this.props.close();
   }
    // async confirm() {
    //     this.props.getPayload(this.state);
    //     this.props.close();
    // }
}
