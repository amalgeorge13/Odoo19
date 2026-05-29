/** @odoo-module */
import {Dialog} from "@web/core/dialog/dialog";
import {usePos} from "@point_of_sale/app/hooks/pos_hook";
import {Component, useState} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";

/*
creating new component to create a new product record
*/
export class CreateProduct extends Component {
    static template = "pos_product_creation.CreateProduct";
    static components = {Dialog};

    setup() {
        this.pos = usePos();
        this.orm = useService('orm');


    }

    /*
    when creating product orm call will work and create a new product record
    */
    async createNewProduct() {
        const form = document.getElementById('productForm');
        const data = new FormData(form);


        // Or view all values at once
        const allValues = Object.fromEntries(data.entries());
        let result = await this.orm.call("product.product", "create_new_product", [allValues], {});
        this.props.close();


    }
    /*
    close popup screen
    */
    closeCreateProduct(){
        this.props.close();
    }


}