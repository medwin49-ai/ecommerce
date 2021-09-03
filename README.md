# JoeWebsite

# How to populate tables

Run: **python manage.py populatedb --file_path [path_to_file] --table [table_to_populate]**

[path_to_file] must be a file that follows the below formats for a given table.
<br>
[table_to_populate] must be the name of a table from the list below.

### File Formats (**NOTE**: There must be no spaces between the commas):
* **[product table](products.txt)**: product_name,product_description
* **[potency table](potency.txt)**: product_id,potency_value,price,supply

### Valid Table Names:
* product
* potency
