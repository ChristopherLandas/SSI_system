#GENERAL
get_uid = "SELECT UID FROM item_general_info where name = ?"
get_service_uid = "SELECT UID FROM service_info where service_name = ?"

#SHOWING INFORMATION OF ITEM IN INVENTORY
get_inventory_by_group = f"SELECT item_general_info.name,\
                                  CAST(SUM(item_inventory_info.Stock) AS INT) AS stocks,\
                                  CONCAT('₱', FORMAT((item_settings.Cost_Price * (item_settings.Markup_Factor + 1)),2)),\
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

get_normal_inventory = "SELECT item_general_info.name,\
                            CAST(SUM(item_inventory_info.Stock) AS INT) AS stocks,\
                            CONCAT('₱', FORMAT((item_settings.Cost_Price * (item_settings.Markup_Factor + 1)),2)),\
                            DATE_FORMAT(item_inventory_info.Expiry_Date, '%Y-%m-%d') AS expiry,\
                            case when SUM(item_inventory_info.Stock) > item_settings.Safe_stock * item_settings.Reorder_factor then 'Normal' ELSE null END AS status\
                        FROM item_general_info\
                        JOIN item_inventory_info ON item_general_info.UID = item_inventory_info.UID\
                        INNER JOIN item_settings ON item_general_info.UID = item_settings.UID\
                        WHERE (item_inventory_info.Expiry_Date > CURRENT_DATE OR item_inventory_info.Expiry_Date IS NULL)\
                        GROUP BY item_general_info.name\
                        HAVING STATUS = 'Normal'\
                        ORDER BY item_general_info.UID"

get_reorder_inventory = "SELECT item_general_info.name,\
                            CAST(SUM(item_inventory_info.Stock) AS INT) AS stocks,\
                            CONCAT('₱', FORMAT((item_settings.Cost_Price * (item_settings.Markup_Factor + 1)),2)),\
                            DATE_FORMAT(item_inventory_info.Expiry_Date, '%Y-%m-%d') AS expiry,\
                            case when SUM(item_inventory_info.Stock) <= item_settings.Safe_stock * item_settings.Reorder_factor AND SUM(item_inventory_info.Stock) > item_settings.Safe_stock * item_settings.Crit_factor then 'Reorder' ELSE null END AS status\
                        FROM item_general_info\
                        JOIN item_inventory_info ON item_general_info.UID = item_inventory_info.UID\
                        INNER JOIN item_settings ON item_general_info.UID = item_settings.UID\
                        WHERE (item_inventory_info.Expiry_Date > CURRENT_DATE OR item_inventory_info.Expiry_Date IS NULL)\
                        GROUP BY item_general_info.name\
                        HAVING STATUS = 'Reorder'\
                        ORDER BY item_general_info.UID"

get_critical_inventory = "SELECT item_general_info.name,\
                                CAST(SUM(item_inventory_info.Stock) AS INT) AS stocks,\
                                CONCAT('₱', FORMAT((item_settings.Cost_Price * (item_settings.Markup_Factor + 1)),2)),\
                                DATE_FORMAT(item_inventory_info.Expiry_Date, '%Y-%m-%d') AS expiry,\
                                case when SUM(item_inventory_info.Stock) <= item_settings.Safe_stock * item_settings.Crit_factor then 'Critical' ELSE null END AS status\
                          FROM item_general_info\
                          JOIN item_inventory_info ON item_general_info.UID = item_inventory_info.UID\
                          INNER JOIN item_settings ON item_general_info.UID = item_settings.UID\
                          WHERE (item_inventory_info.Expiry_Date > CURRENT_DATE OR item_inventory_info.Expiry_Date IS NULL)\
                          GROUP BY item_general_info.name\
                          HAVING STATUS = 'Critical'\
                          ORDER BY item_general_info.UID"

get_inventory_by_expiry = f"SELECT DISTINCT item_general_info.name,\
                                  item_inventory_info.Stock,\
                                  CONCAT('₱', FORMAT((item_settings.Cost_Price * (item_settings.Markup_Factor + 1)),2)),\
                                  DATE_FORMAT(item_inventory_info.Expiry_Date, '%Y-%m-%d') AS expiry,\
                                  case when item_inventory_info.Expiry_Date <= CURRENT_DATE\
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
                          ORDER BY case when item_inventory_info.Expiry_Date <= CURRENT_DATE\
                                      then 3\
                                  when item_inventory_info.Expiry_Date < DATE_ADD(CURRENT_DATE, INTERVAL 14 DAY)\
                                      then 2\
                                  when item_inventory_info.Expiry_Date IS NULL\
                                  	  then 0\
                                      ELSE 1 END DESC"

get_expired_inventory = "SELECT DISTINCT item_general_info.name,\
                            item_inventory_info.Stock,\
                            CONCAT('₱', FORMAT((item_settings.Cost_Price * (item_settings.Markup_Factor + 1)),2)),\
                            DATE_FORMAT(item_inventory_info.Expiry_Date, '%Y-%m-%d') AS expiry,\
                            case when item_inventory_info.Expiry_Date <= CURRENT_DATE\
                                then 'Expired' ELSE null END AS stat\
                         FROM item_general_info\
                         JOIN item_inventory_info ON item_general_info.UID = item_inventory_info.UID\
                         INNER JOIN item_settings ON item_general_info.UID = item_settings.UID\
                         WHERE item_inventory_info.stock > 0\
                         HAVING stat = 'Expired'"

get_near_expire_inventory = "SELECT DISTINCT item_general_info.name,\
                                     item_inventory_info.Stock,\
                                     CONCAT('₱', FORMAT((item_settings.Cost_Price * (item_settings.Markup_Factor + 1)),2)),\
                                     DATE_FORMAT(item_inventory_info.Expiry_Date, '%Y-%m-%d') AS expiry,\
                                     case when item_inventory_info.Expiry_Date > CURRENT_DATE AND item_inventory_info.Expiry_Date < DATE_ADD(CURRENT_DATE, INTERVAL 14 DAY)\
                                         then 'Nearly Expire' ELSE null END AS stat\
                             FROM item_general_info\
                             JOIN item_inventory_info ON item_general_info.UID = item_inventory_info.UID\
                             INNER JOIN item_settings ON item_general_info.UID = item_settings.UID\
                             WHERE item_inventory_info.stock > 0\
                             HAVING stat = 'Nearly Expire'"

get_safe_expire_inventory = "SELECT DISTINCT item_general_info.name,\
                                     item_inventory_info.Stock,\
                                     CONCAT('₱', FORMAT((item_settings.Cost_Price * (item_settings.Markup_Factor + 1)),2)),\
                                     DATE_FORMAT(item_inventory_info.Expiry_Date, '%Y-%m-%d') AS expiry,\
                                     case when item_inventory_info.Expiry_Date > DATE_ADD(CURRENT_DATE, INTERVAL 14 DAY)\
                                         then 'Safe' ELSE null END AS stat\
                             FROM item_general_info\
                             JOIN item_inventory_info ON item_general_info.UID = item_inventory_info.UID\
                             INNER JOIN item_settings ON item_general_info.UID = item_settings.UID\
                             WHERE item_inventory_info.stock > 0\
                             HAVING stat = 'Safe'"

get_non_expiry_inventory = "SELECT DISTINCT item_general_info.name,\
                                    item_inventory_info.Stock,\
                                    CONCAT('₱', FORMAT((item_settings.Cost_Price * (item_settings.Markup_Factor + 1)),2)),\
                                    DATE_FORMAT(item_inventory_info.Expiry_Date, '%Y-%m-%d') AS expiry,\
                                    case when item_inventory_info.Expiry_Date IS null\
                                        then 'N/A' ELSE null END AS stat\
                            FROM item_general_info\
                            JOIN item_inventory_info ON item_general_info.UID = item_inventory_info.UID\
                            INNER JOIN item_settings ON item_general_info.UID = item_settings.UID\
                            WHERE item_inventory_info.stock > 0\
                            HAVING stat = 'N/A'"

#FOR CREATING A LIST OF ITEM AND/OR SERVICES FOR TRANSACTION
get_item_and_their_total_stock = "SELECT item_general_info.name,\
                                         CAST(SUM(item_inventory_info.Stock) as INT),\
                                         CONCAT('₱', FORMAT((item_settings.Cost_Price * (item_settings.Markup_Factor + 1)), 2))\
                                 FROM item_general_info JOIN item_inventory_info ON item_general_info.UID = item_inventory_info.UID\
                                 INNER	JOIN item_settings ON item_general_info.UID = item_settings.UID\
                                 WHERE item_inventory_info.Stock != 0 AND (item_inventory_info.Expiry_Date > CURRENT_DATE OR item_inventory_info.Expiry_Date IS null)\
                                 GROUP BY item_general_info.UID"

get_item_data_for_transaction = "SELECT item_general_info.UID,\
                                         item_general_info.name,\
                                         CAST((item_settings.Cost_Price * (item_settings.Markup_Factor + 1)) as DECIMAL(10,2))  \
                                 FROM item_general_info\
                                 JOIN item_inventory_info ON item_general_info.UID = item_inventory_info.UID\
                                 INNER JOIN item_settings ON item_general_info.UID = item_settings.UID\
                                 WHERE item_general_info.name = ?\
                                 GROUP BY item_general_info.UID"

get_services_and_their_price = "SELECT UID, service_name, Item_needed, CONCAT('₱', FORMAT(price, 2)) FROM service_info WHERE state = 1"
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
show_reveiving_hist = "SELECT NAME, stock, supp_name, date_recieved, reciever FROM recieving_item WHERE state != 1"

#ADDING ITEMS THROUGH THE INVENTORY
add_item_general = "INSERT INTO item_general_info VALUES (?, ?, ?)"
add_item_inventory = "INSERT INTO item_inventory_info VALUES (?, ?, ?)"
add_item_settings = "INSERT INTO item_settings VALUES(?, ?, ?, ?, ?, ?)"
add_item_supplier = "INSERT INTO item_supplier_info VALUES(?, ?, ?)"

#RECORDING ANY TRANSACTION
generate_id_transaction = "SELECT COUNT(*) FROM transaction_record"
record_transaction = "INSERT INTO transaction_record VALUES(?, ?, ?, ?, CURRENT_DATE)"
record_item_transaction_content = "INSERT INTO item_transaction_content VALUES(?, ?, ?, ?, ?, ?)"
record_services_transaction_content = "INSERT INTO services_transaction_content VALUES(?, ?, ?, ?, ?, ?, ?, ?)"

#UPDATING STOCK AFTER TRANSACTION
get_specific_stock = "SELECT * FROM item_inventory_info WHERE UID = ? AND (Expiry_Date > CURRENT_DATE OR Expiry_Date IS NULL) ORDER BY Expiry_Date ASC"

#FOR SALES
get_transaction_data = "SELECT * FROM transaction_record"

#FOR SERVICES
get_service_data = "SELECT service_name, price, date_added FROM service_info"
get_services_names = "SELECT DISTINCT service_name FROM service_info"

#FOR LOG AUDIT
get_log_audit_for_today = "SELECT * FROM log_history WHERE date_logged = CURRENT_DATE"

#FOR INVENTORY STATE
get_reorder_state= "SELECT item_general_info.name,\
                            case when sum(item_inventory_info.stock) <= item_settings.Reorder_factor * item_settings.Safe_stock\
                                    AND sum(item_inventory_info.stock) > item_settings.Crit_factor * item_settings.Safe_stock\
                                        then sum(item_inventory_info.stock) ELSE 0 END AS stock,\
                            'Stock' AS _type\
                    FROM item_general_info JOIN item_inventory_info ON item_general_info.UID = item_inventory_info.UID\
                        INNER JOIN item_settings ON item_inventory_info.UID = item_settings.UID\
                    GROUP BY item_inventory_info.uid\
                    HAVING stock;"

get_critical_state = "SELECT item_general_info.name,\
                            case when sum(item_inventory_info.stock) <= item_settings.Crit_factor * item_settings.Safe_stock\
                                        then sum(item_inventory_info.stock) ELSE 0 END AS stock,\
                            'Stock' AS _type\
                    FROM item_general_info JOIN item_inventory_info ON item_general_info.UID = item_inventory_info.UID\
                        INNER JOIN item_settings ON item_inventory_info.UID = item_settings.UID\
                    GROUP BY item_inventory_info.uid\
                    HAVING stock;"

get_out_of_stock_state = "SELECT item_general_info.name,\
                                 case when sum(item_inventory_info.stock) = 0\
                                           then sum(item_inventory_info.stock) ELSE -1 END AS stock,\
                                 'Stock' AS _type\
                          FROM item_general_info JOIN item_inventory_info ON item_general_info.UID = item_inventory_info.UID\
                              INNER JOIN item_settings ON item_inventory_info.UID = item_settings.UID\
                          GROUP BY item_inventory_info.uid\
                          HAVING stock >= 0;"

get_near_expire_state = "SELECT item_general_info.name,\
                                 item_inventory_info.Stock,\
                                 case when item_inventory_info.Expiry_Date <= DATE_ADD(CURRENT_DATE, INTERVAL 15 DAY)\
                                             AND item_inventory_info.Expiry_Date > CURRENT_DATE\
                                             AND item_inventory_info.Expiry_Date IS NOT NULL \
                                             then item_inventory_info.Expiry_Date ELSE 0 END AS EXP,\
                                 'Expiry' AS _type\
                         FROM item_general_info JOIN item_inventory_info ON item_general_info.UID = item_inventory_info.UID\
                         HAVING exp;"


get_expired_state = "SELECT item_general_info.name,\
                             item_inventory_info.Stock,\
                             case when item_inventory_info.Expiry_Date <= CURRENT_DATE\
                                         AND item_inventory_info.Expiry_Date IS NOT NULL \
                                         then item_inventory_info.Expiry_Date ELSE NULL END AS EXP,\
                             'Expiry' AS _type\
                     FROM item_general_info JOIN item_inventory_info ON item_general_info.UID = item_inventory_info.UID\
                     HAVING exp;"

#FOR DAILY SALES
get_services_daily_sales = "SELECT CAST(SUM(services_transaction_content.price) AS DECIMAL(10,2))\
                            FROM transaction_record JOIN services_transaction_content ON transaction_record.transaction_uid = services_transaction_content.transaction_uid\
                            WHERE transaction_record.transaction_date = CURRENT_DATE;"

get_items_daily_sales = "SELECT CAST(SUM(item_transaction_content.price * item_transaction_content.quantity) AS DECIMAL(10,2))\
                         FROM transaction_record JOIN item_transaction_content ON transaction_record.transaction_uid = item_transaction_content.transaction_uid\
                         WHERE transaction_record.transaction_date = CURRENT_DATE;"

get_services_daily_sales_sp = "SELECT CAST(SUM(services_transaction_content.price) AS DECIMAL(10,2))\
                            FROM transaction_record JOIN services_transaction_content ON transaction_record.transaction_uid = services_transaction_content.transaction_uid\
                            WHERE transaction_record.transaction_date = ?;"

get_items_daily_sales_sp = "SELECT CAST(SUM(item_transaction_content.price * item_transaction_content.quantity) AS DECIMAL(10,2))\
                         FROM transaction_record JOIN item_transaction_content ON transaction_record.transaction_uid = item_transaction_content.transaction_uid\
                         WHERE transaction_record.transaction_date = ?;"

get_items_monthly_sales_sp = "SELECT CAST(SUM(item_transaction_content.price * item_transaction_content.quantity) AS DECIMAL(10,2))\
                         FROM transaction_record JOIN item_transaction_content ON transaction_record.transaction_uid = item_transaction_content.transaction_uid\
                         WHERE MONTH(transaction_record.transaction_date) = ? AND YEAR(transaction_record.transaction_date) = ?;"
get_services_monthly_sales_sp = "SELECT CAST(SUM(services_transaction_content.price) AS DECIMAL(10,2))\
                            FROM transaction_record JOIN services_transaction_content ON transaction_record.transaction_uid = services_transaction_content.transaction_uid\
                            WHERE MONTH(transaction_record.transaction_date) = ? AND YEAR(transaction_record.transaction_date) = ?;"

#OR
get_or = 'SELECT COUNT(*)+1 FROM transaction_record'

#LOGIN REPORT
record_login_report = "INSERT INTO login_report VALUES(?, ?, CURRENT_TIMESTAMP)"
get_usn = "SELECT usn FROM acc_cred WHERE usn = ?"

#USER LEVEL ACCESS
get_level_acessess = "SELECT * FROM user_level_access WHERE title = ?"

#RECIEVING ITEMS
record_recieving_item = "INSERT INTO recieving_item VALUES (?, ?, ?, ?, ? ,?, ?, ?)"
get_recieving_items = "SELECT id, NAME, stock, supp_name from recieving_item where state = 1"
get_supplier = "SELECT Supplier from item_supplier_info where UID = ?"
get_receiving_expiry_by_id = "SELECT date_format(exp_date, '%Y-%m-%d') from recieving_item WHERE id = ?"
update_recieving_item = "UPDATE recieving_item SET reciever = ?, state = 2, date_recieved = CURRENT_TIMESTAMP WHERE id = ?"

#DISPOSAL
get_for_disposal_items = "SELECT DISTINCT item_general_info.name,\
                              item_inventory_info.Stock\
                          FROM item_general_info\
                          JOIN item_inventory_info ON item_general_info.UID = item_inventory_info.UID\
                          INNER JOIN item_settings ON item_general_info.UID = item_settings.UID\
                          WHERE item_inventory_info.Expiry_Date <= CURRENT_DATE"
record_disposal_process = "INSERT INTO disposal_history (item_name, quan, date_of_disposal, disposed_by) VALUES (?, ?, CURRENT_TIMESTAMP, ?);"
delete_disposing_items = "DELETE FROM item_inventory_info where uid = ? and stock = ? and expiry_date <= CURRENT_DATE"
get_disposal_hist = "SELECT item_name, quan, DATE_FORMAT(date_of_disposal, '%m-%d-%Y at %H:%i %p'), disposed_by FROM disposal_history"

#ACCOUNT CREATION

#PET INFO
get_owners = "SELECT DISTINCT o_name FROM pet_info"
get_pet_name = "SELECT id, p_name FROM pet_info"

get_ids_pi = "SELECT id FROM pet_info"
get_pet_info = "SELECT * FROM pet_info WHERE o_name = ?"
get_pet_info_for_cust_info = "SELECT breed FROM pet_info WHERE p_name = ?"
record_patient = "INSERT INTO pet_info VALUES(?, ?, ?, ?, ?, ?, ?, ?)"

#HIST LOG
get_hist_log = "SELECT CONCAT(acc_info.usn, ' (', acc_info.full_name, ')'),\
                       log_history.date_logged,\
                       log_history.time_in,\
                       log_history.time_out\
                FROM acc_info JOIN log_history ON acc_info.usn = log_history.usn"
