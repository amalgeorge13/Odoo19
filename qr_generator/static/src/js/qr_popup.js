import {Dialog} from "@web/core/dialog/dialog";
import {Component, useState} from "@odoo/owl";

/*
*/
export class QrPopup extends Component {
    static template = "qr_generator.QrPopup";
    static components = {Dialog};

    setup() {
        super.setup();
        this.state = useState({
            qrcode : null
        });

    }
    /*
    Generate qrcode based on text
    */
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
        this.state.qrcode=qrcode


    }

    /*
    clear the text field and qrcode
    */
    resetQR() {
        document.getElementById("text").value = null;
        const qr_image = document.getElementById("qrcode");
        qr_image.replaceChildren();
        this.state.qrcode = null
    }

    /*
    Download QR code
    */
    downloadQR() {
        var printContents = document.getElementById('qr_body').innerHTML;
        var originalContents = document.body.innerHTML;

        document.body.innerHTML = printContents;
        console.log(printContents)

        print();

        document.body.innerHTML = originalContents;
        location.reload();
    }


    /*
    close popup screen
    */

    closeQrPopup() {
        this.props.close();
    }


}

