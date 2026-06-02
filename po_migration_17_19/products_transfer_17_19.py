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
products_src = models_src.execute_kw(
    db_src, uid_src, pwd_src,
    'product.product', 'search_read',
    [[]],
    {'fields': ['id','name', 'lst_price', 'standard_price', 'detailed_type'],'order':'id'}
)
print(f"Fetched {len(products_src)} Products from Odoo 18...")
# --- Transfer to Odoo 19 (Skip duplicates by id) ---
created_count = 0
skipped_count = 0
for product in products_src:
    type = product.get('detailed_type')
    name = product.get('name')
    id = product.get('id')
    # Skip if id exists in Odoo 19
    if id:
        existing = models_dest.execute_kw(
            db_dest, uid_dest, pwd_dest,
            'product.product', 'search',
            [[('id', '=', id)]],
            {'limit': 1}
        )
        if existing:
            print(f"Skipped (duplicate id): {id}")
            skipped_count += 1
            continue

    # Prepare minimal product data
    new_product = {
    	'id':id,
        'name': name or 'Unnamed',
        'type': type,
        'lst_price': product.get('lst_price'),
        'standard_price': product.get('standard_price'),

    }
    # Create in Odoo 19
    models_dest.execute_kw(
        db_dest, uid_dest, pwd_dest,
        'product.product', 'create',
        [new_product]
    )
    created_count += 1
    print(f"Created: {name}")
print(f"\nCustomer transfer complete!")
print(f"Created: {created_count}, Skipped: {skipped_count}")
