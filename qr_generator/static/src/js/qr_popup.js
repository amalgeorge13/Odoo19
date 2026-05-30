import {Dialog} from "@web/core/dialog/dialog";
import {Component, useState} from "@odoo/owl";

/*
*/
export class QrPopup extends Component {
    static template = "qr_generator.QrPopup";
    static components = {Dialog};

    setup() {
        super.setup();

    }

    async generateQR(ev) {
        const textValue = document.getElementById("text").value;
        console.log(textValue)

        const qrcode = new QRCode(document.getElementById('qrcode'), {
            text: textValue,
            width: 128,
            height: 128,
            colorDark: '#000',
            colorLight: '#fff',
            correctLevel: QRCode.CorrectLevel.H
        });

    }

    resetQR() {
        document.getElementById("text").value = null;
        document.getElementById("qrcode").value = null;
    }

    /*
    close popup screen
    */

    closeQrPopup() {
        this.props.close();
    }


}

