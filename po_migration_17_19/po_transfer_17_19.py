import xmlrpc.client
# --- Odoo 17 (Source) ---
url_src = "http://localhost:8888"
db_src = "MyDB17"
user_src = "1"
pwd_src = "1"
common_src = xmlrpc.client.ServerProxy(f"{url_src}/xmlrpc/2/common")
uid_src = common_src.authenticate(db_src, user_src, pwd_src, {})
models_src = xmlrpc.client.ServerProxy(f"{url_src}/xmlrpc/2/object")
# --- Odoo 19 (Destination) ---
url_dest = "http://localhost:8019"
db_dest = "test"
user_dest = "1"
pwd_dest = "1"
common_dest = xmlrpc.client.ServerProxy(f"{url_dest}/xmlrpc/2/common")
uid_dest = common_dest.authenticate(db_dest, user_dest, pwd_dest, {})
models_dest = xmlrpc.client.ServerProxy(f"{url_dest}/xmlrpc/2/object")
# --- Fetch customers from Odoo 17 ---
p_orders_src = models_src.execute_kw(
    db_src, uid_src, pwd_src,
    'purchase.order', 'search_read',
    [[]],
    {'fields': ['name', 'partner_id', 'order_line','state']}
)
print(f"Fetched {len(p_orders_src)} orders from Odoo 18...")
# --- Transfer to Odoo 19 (Skip duplicates by name) ---
created_count = 0
skipped_count = 0
for order in p_orders_src:
    partner_id = order.get('partner_id')
    name = order.get('name')
    order_line = order.get('order_line')
    # Prepare minimal po data
    if name:
        existing = models_dest.execute_kw(
            db_dest, uid_dest, pwd_dest,
            'purchase.order', 'search',
            [[('name', '=', name)]],
            {'limit': 1}
        )
        if existing:
            print(f"Skipped (duplicate namae): {name}")
            skipped_count += 1
            continue
    new_order = {
        'name': name,
        'partner_id': partner_id[0],
        'state': order.get('state'),
    }
    # Create in Odoo 19
    models_dest.execute_kw(
        db_dest, uid_dest, pwd_dest,
        'purchase.order', 'create',
        [new_order]
    )
    created_count += 1
    print(f"Created: {name}")
print(f"\Orders transfer complete!")
print(f"Created: {created_count}, Skipped: {skipped_count}")
