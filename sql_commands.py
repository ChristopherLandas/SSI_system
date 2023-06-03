#SHOWING INFORMATION OF ITEM IN INVENTORY
get_inventory_by_group = f"SELECT item_general_info.name,\
                                  CAST(SUM(item_inventory_info.Stock) AS INT) AS stocks,\
                                  CAST((item_settings.Cost_Price * (item_settings.Markup_Factor + 1)) as DECIMAL(10,2)),\
                                  DATE_FORMAT(item_inventory_info.Expiry_Date, '%Y-%m-%d') AS expiry,\
                                  case when SUM(item_inventory_info.Stock) < 1\
                                      then 'Out Of Stock'\
                                  when SUM(item_inventory_info.Stock) < item_settings.Safe_stock * item_settings.Crit_factor\
                                      then 'Critical'\
                                  when SUM(item_inventory_info.Stock) < item_settings.Safe_stock * item_settings.Reorder_factor\
                                      then 'Reorder'\
                                      ELSE 'Normal' END AS stats\
                          FROM item_general_info\
                          JOIN item_inventory_info ON item_general_info.UID = item_inventory_info.UID\
                          INNER JOIN item_settings ON item_general_info.UID = item_settings.UID\
                          WHERE item_inventory_info.Expiry_Date > CURRENT_DATE OR item_inventory_info.Expiry_Date IS NULL\
                          GROUP BY item_general_info.name\
                          ORDER BY item_general_info.UID"

get_inventory_by_expiry = f"SELECT DISTINCT item_general_info.name,\
                                  item_inventory_info.Stock,\
                                  CAST((item_settings.Cost_Price * (item_settings.Markup_Factor + 1)) as DECIMAL(10,2)),\
                                  DATE_FORMAT(item_inventory_info.Expiry_Date, '%Y-%m-%d') AS expiry,\
                                  case when item_inventory_info.Expiry_Date < CURRENT_DATE\
                                      then 'Expired'\
                                  when item_inventory_info.Expiry_Date < DATE_ADD(CURRENT_DATE, INTERVAL 14 DAY)\
                                      then 'Nearly Expire'\
                                  when item_inventory_info.Expiry_Date IS NULL\
                                  	  then 'Does not expire'\
                                      ELSE 'Safe' END AS stats\
                          FROM item_general_info\
                          JOIN item_inventory_info ON item_general_info.UID = item_inventory_info.UID\
                          INNER JOIN item_settings ON item_general_info.UID = item_settings.UID\
                          WHERE item_inventory_info.stock > 0\
                          ORDER BY case when item_inventory_info.Expiry_Date < CURRENT_DATE\
                                      then 3\
                                  when item_inventory_info.Expiry_Date < DATE_ADD(CURRENT_DATE, INTERVAL 14 DAY)\
                                      then 2\
                                  when item_inventory_info.Expiry_Date IS NULL\
                                  	  then 0\
                                      ELSE 1 END DESC"

#FOR CREATING A LIST OF ITEM AND/OR SERVICES FOR TRANSACTION
get_item_and_their_total_stock = 'SELECT item_general_info.name,\
                                         CAST(SUM(item_inventory_info.Stock) as INT)\
                                 FROM item_general_info JOIN item_inventory_info ON item_general_info.UID = item_inventory_info.UID\
                                 WHERE item_inventory_info.Stock != 0 AND (item_inventory_info.Expiry_Date > CURRENT_DATE OR item_inventory_info.Expiry_Date IS null)\
                                 GROUP BY item_general_info.UID'

get_item_data_for_transaction = "SELECT item_general_info.UID,\
                                         item_general_info.name,\
                                         CAST((item_settings.Cost_Price * (item_settings.Markup_Factor + 1)) as DECIMAL(10,2))  \
                                 FROM item_general_info\
                                 JOIN item_inventory_info ON item_general_info.UID = item_inventory_info.UID\
                                 INNER JOIN item_settings ON item_general_info.UID = item_settings.UID\
                                 WHERE item_general_info.name = ?\
                                 GROUP BY item_general_info.UID"

get_services_and_their_price = "SELECT UID, service_name, Item_needed, price FROM service_info WHERE state = 1"
get_services_data_for_transaction = "SELECT uid,\
                                             service_name,\
                                             CAST(price AS DECIMAL(10, 2))\
                                     FROM service_info\
                                     WHERE service_name = ?;"


#RESTOCKING
add_stock_with_different_expiry = 'INSERT INTO item_inventory_info VALUES (?, ?, ?)'
update_non_expiry_stock = "UPDATE item_inventory_info SET Stock = STOCK + ? WHERE UID = ? AND Expiry_Date IS NULL"
update_expiry_stock = "UPDATE item_inventory_info SET Stock = STOCK + ? WHERE UID = ? AND Expiry_Date = ?"
add_new_instance = "INSERT INTO item_inventory_info VALUES (?, ?, ?)"
show_all_items = "SELECT NAME FROM item_general_info"

#ADDING ITEMS THROUGH THE INVENTORY
add_item_general = "INSERT INTO item_general_info VALUES (?, ?, ?, ?)"
add_item_inventory = "INSERT INTO item_inventory_info VALUES (?, ?, ?)"
add_item_settings = "INSERT INTO item_settings VALUES(?, ?, ?, ?, ?, ?)"
add_item_supplier = "INSERT INTO item_supplier_info VALUES(?, ?, ?)"

#RECORDING ANY TRANSACTION
generate_id_transaction = "SELECT COUNT(*) FROM transaction_record"
record_transaction = "INSERT INTO transaction_record VALUES(?, ?, ?)"
record_item_transaction_content = "INSERT INTO item_transaction_content VALUES(?, ?, ?, ?, ?, ?)"
record_services_transaction_content = "INSERT INTO services_transaction_content VALUES(?, ?, ?, ?, ?, ?, ?)"

#UPDATING STOCK AFTER TRANSACTION
get_specific_stock = "SELECT * FROM item_inventory_info WHERE UID = ? AND (Expiry_Date > CURRENT_DATE OR Expiry_Date IS NULL) ORDER BY Expiry_Date ASC"

#FOR SALES
get_transaction_data = "SELECT * FROM transaction_record"

#FOR SERVICES
get_service_data = "SELECT service_name, price, date_added FROM service_info"

#FOR LOG AUDIT
get_log_audit_for_today = "SELECT * FROM log_history WHERE date_logged = CURRENT_DATE"

#FOR INVENTORY STATE
get_reorder_items = "SELECT  item_inventory_info.UID,\
                             SUM(item_inventory_info.Stock)\
                     FROM item_inventory_info JOIN item_settings ON item_inventory_info.UID = item_settings.UID\
                     WHERE item_inventory_info.Stock < item_settings.Safe_stock * item_settings.Reorder_factor AND\
                           item_inventory_info.Stock > item_settings.Safe_stock * item_settings.Critical_factor\
                     GROUP BY item_inventory_info.UID"

get_reorder_items = "SELECT  item_inventory_info.UID,\
                             SUM(item_inventory_info.Stock)\
                     FROM item_inventory_info JOIN item_settings ON item_inventory_info.UID = item_settings.UID\
                     WHERE item_inventory_info.Stock < item_settings.Safe_stock * item_settings.Reorder_factor\
                     GROUP BY item_inventory_info.UID"
