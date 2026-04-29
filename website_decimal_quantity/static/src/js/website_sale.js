import { patch } from '@web/core/utils/patch';
import { WebsiteSale } from '@website_sale/interactions/website_sale';
patch(WebsiteSale.prototype, {
    /**
     * Event handler to increase or decrease quantity from the product page.
     *
     * @param {MouseEvent} ev
     */
    onChangeQuantity(ev) {
        const input = ev.currentTarget.closest('.input-group').querySelector('input');
            const min = parseFloat(input.dataset.min || 0);
            const max = parseFloat(input.dataset.max || Infinity);
            const previousQty = parseFloat(input.value || 0);
            const quantity = (
                ev.currentTarget.name === 'remove_one' ? -.1 : .1
            ) + previousQty;

            const newQty = quantity > min ? (quantity < max ? quantity : max) : min;
            const result = newQty.toFixed(1)
            if (newQty !== previousQty) {
                input.value = result;
                // Trigger `onChangeAddQuantity`.
                input.dispatchEvent(new Event('change', { bubbles: true }));
            }
    },
});

