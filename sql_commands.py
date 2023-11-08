#GENERAL
get_uid = "SELECT UID FROM item_general_info where name = ? and unit = ?"
get_uid_null_unit = "SELECT UID FROM item_general_info where name = ? and unit is NULL"
get_item_info = "SELECT * FROM item_general_info where name = ? and unit = ?"
get_item_info_null_unit = "SELECT * FROM item_general_info where name = ? and unit is NULL"
get_service_uid = "SELECT UID FROM service_info where service_name = ?"
get_item_brand = "SELECT brand FROM item_general_info WHERE UID = ?"


#SHOWING INFORMATION OF ITEM IN INVENTORY
get_inventory_by_group = f"SELECT item_general_info.brand, item_general_info.name, item_general_info.unit,\
                                  CAST(SUM(item_inventory_info.Stock) AS INT) AS stocks,\
                                  CONCAT('₱', FORMAT((item_settings.Cost_Price * (item_settings.Markup_Factor + 1)),2)) as cost_price,\
                                  DATE_FORMAT(item_inventory_info.Expiry_Date, '%b %d, %Y') AS expiry,\
                                  CASE WHEN SUM(item_inventory_info.Stock) < 1\
                                      then 'Out of Stock'\
                                  when SUM(item_inventory_info.Stock) <= item_settings.Safe_stock * item_settings.Crit_factor\
                                      then 'Critical'\
                                  when SUM(item_inventory_info.Stock) <= item_settings.Safe_stock * item_settings.Reorder_factor\
                                      then 'Reorder'\
                                      ELSE 'Normal' END AS stats\
                          FROM item_general_info\
                          JOIN item_inventory_info ON item_general_info.UID = item_inventory_info.UID\
                          INNER JOIN item_settings ON item_general_info.UID = item_settings.UID\
                          WHERE (item_inventory_info.Expiry_Date > CURRENT_DATE OR item_inventory_info.Expiry_Date IS NULL)\
                            AND item_inventory_info.state = 1\
                          GROUP BY item_general_info.name, item_general_info.unit\
                          ORDER BY CASE\
                          WHEN SUM(item_inventory_info.Stock) < 1 THEN 1\
                          WHEN SUM(item_inventory_info.Stock) <= item_settings.Safe_stock * item_settings.Crit_factor THEN 2\
                          WHEN SUM(item_inventory_info.Stock) <= item_settings.Safe_stock * item_settings.Reorder_factor THEN 3\
                            ELSE 4 End ASC"

get_normal_inventory = "SELECT item_general_info.brand, item_general_info.name, item_general_info.unit,\
                            CAST(SUM(item_inventory_info.Stock) AS INT) AS stocks,\
                            CONCAT('₱', FORMAT((item_settings.Cost_Price * (item_settings.Markup_Factor + 1)),2)),\
                            DATE_FORMAT(item_inventory_info.Expiry_Date, '%b %d, %Y') AS expiry,\
                            case when SUM(item_inventory_info.Stock) > item_settings.Safe_stock * item_settings.Reorder_factor then 'Normal' ELSE null END AS status\
                        FROM item_general_info\
                        JOIN item_inventory_info ON item_general_info.UID = item_inventory_info.UID\
                        INNER JOIN item_settings ON item_general_info.UID = item_settings.UID\
                        WHERE (item_inventory_info.Expiry_Date > CURRENT_DATE OR item_inventory_info.Expiry_Date IS NULL)\
                        GROUP BY item_general_info.name, item_general_info.unit\
                        HAVING STATUS = 'Normal'\
                        ORDER BY item_general_info.UID"

get_reorder_inventory = "SELECT item_general_info.brand, item_general_info.name, item_general_info.unit,\
                            CAST(SUM(item_inventory_info.Stock) AS INT) AS stocks,\
                            CONCAT('₱', FORMAT((item_settings.Cost_Price * (item_settings.Markup_Factor + 1)),2)),\
                            DATE_FORMAT(item_inventory_info.Expiry_Date, '%b %d, %Y') AS expiry,\
                            case when SUM(item_inventory_info.Stock) <= item_settings.Safe_stock * item_settings.Reorder_factor AND SUM(item_inventory_info.Stock) > item_settings.Safe_stock * item_settings.Crit_factor then 'Reorder' ELSE null END AS status\
                        FROM item_general_info\
                        JOIN item_inventory_info ON item_general_info.UID = item_inventory_info.UID\
                        INNER JOIN item_settings ON item_general_info.UID = item_settings.UID\
                        WHERE (item_inventory_info.Expiry_Date > CURRENT_DATE OR item_inventory_info.Expiry_Date IS NULL)\
                        GROUP BY item_general_info.name, item_general_info.unit\
                        HAVING STATUS = 'Reorder'\
                        ORDER BY item_general_info.UID"

get_critical_inventory = "SELECT item_general_info.brand, item_general_info.name, item_general_info.unit,\
                                CAST(SUM(item_inventory_info.Stock) AS INT) AS stocks,\
                                CONCAT('₱', FORMAT((item_settings.Cost_Price * (item_settings.Markup_Factor + 1)),2)),\
                                DATE_FORMAT(item_inventory_info.Expiry_Date, '%b %d, %Y') AS expiry,\
                                case when SUM(item_inventory_info.Stock) <= item_settings.Safe_stock * item_settings.Crit_factor AND SUM(item_inventory_info.Stock) > 0 then 'Critical' ELSE null END AS status\
                          FROM item_general_info\
                          JOIN item_inventory_info ON item_general_info.UID = item_inventory_info.UID\
                          INNER JOIN item_settings ON item_general_info.UID = item_settings.UID\
                          WHERE (item_inventory_info.Expiry_Date > CURRENT_DATE OR item_inventory_info.Expiry_Date IS NULL)\
                          GROUP BY item_general_info.name, item_general_info.unit\
                          HAVING STATUS = 'Critical'\
                          ORDER BY item_general_info.UID"
                          
get_out_of_stock_inventory = f"SELECT item_general_info.brand, item_general_info.name, item_general_info.unit,\
                                CAST(SUM(item_inventory_info.Stock) AS INT) AS stocks,\
                                CONCAT('₱', FORMAT((item_settings.Cost_Price * (item_settings.Markup_Factor + 1)),2)),\
                                DATE_FORMAT(item_inventory_info.Expiry_Date, '%b %d, %Y') AS expiry,\
                                case when item_inventory_info.Stock = 0 then 'Out of Stock' END AS status\
                                FROM item_general_info\
                                JOIN item_inventory_info ON item_general_info.UID = item_inventory_info.UID\
                                INNER JOIN item_settings ON item_general_info.UID = item_settings.UID\
                                WHERE (item_inventory_info.Expiry_Date > CURRENT_DATE OR item_inventory_info.Expiry_Date IS NULL)\
                                GROUP BY item_general_info.name, item_general_info.unit\
                                HAVING STATUS = 'Out of Stock'\
                                ORDER BY item_general_info.UID"

get_inventory_by_expiry = f"SELECT DISTINCT item_general_info.brand, item_general_info.name, item_general_info.unit,\
                                  item_inventory_info.Stock,\
                                  CONCAT('₱', FORMAT((item_settings.Cost_Price * (item_settings.Markup_Factor + 1)),2)),\
                                  DATE_FORMAT(item_inventory_info.Expiry_Date, '%b %d, %Y') AS expiry,\
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

get_expired_inventory = "SELECT DISTINCT item_general_info.brand, item_general_info.name, item_general_info.unit,\
                            item_inventory_info.Stock,\
                            CONCAT('₱', FORMAT((item_settings.Cost_Price * (item_settings.Markup_Factor + 1)),2)),\
                            DATE_FORMAT(item_inventory_info.Expiry_Date, '%b %d, %Y') AS expiry,\
                            case when item_inventory_info.Expiry_Date <= CURRENT_DATE\
                                then 'Expired' ELSE null END AS stat\
                         FROM item_general_info\
                         JOIN item_inventory_info ON item_general_info.UID = item_inventory_info.UID\
                         INNER JOIN item_settings ON item_general_info.UID = item_settings.UID\
                         WHERE item_inventory_info.stock > 0 AND item_inventory_info.state = 1\
                         HAVING stat = 'Expired'"

get_near_expire_inventory = "SELECT DISTINCT item_general_info.brand, item_general_info.name, item_general_info.unit,\
                                     item_inventory_info.Stock,\
                                     CONCAT('₱', FORMAT((item_settings.Cost_Price * (item_settings.Markup_Factor + 1)),2)),\
                                     DATE_FORMAT(item_inventory_info.Expiry_Date, '%b %d, %Y') AS expiry,\
                                     case when item_inventory_info.Expiry_Date > CURRENT_DATE AND item_inventory_info.Expiry_Date < DATE_ADD(CURRENT_DATE, INTERVAL 14 DAY)\
                                         then 'Nearly Expire' ELSE null END AS stat\
                             FROM item_general_info\
                             JOIN item_inventory_info ON item_general_info.UID = item_inventory_info.UID\
                             INNER JOIN item_settings ON item_general_info.UID = item_settings.UID\
                             WHERE item_inventory_info.stock > 0\
                             HAVING stat = 'Nearly Expire'"

get_safe_expire_inventory = "SELECT DISTINCT item_general_info.brand, item_general_info.name, item_general_info.unit,\
                                     item_inventory_info.Stock,\
                                     CONCAT('₱', FORMAT((item_settings.Cost_Price * (item_settings.Markup_Factor + 1)),2)),\
                                     DATE_FORMAT(item_inventory_info.Expiry_Date, '%b %d, %Y') AS expiry,\
                                     case when item_inventory_info.Expiry_Date > DATE_ADD(CURRENT_DATE, INTERVAL 14 DAY)\
                                         then 'Safe' ELSE null END AS stat\
                             FROM item_general_info\
                             JOIN item_inventory_info ON item_general_info.UID = item_inventory_info.UID\
                             INNER JOIN item_settings ON item_general_info.UID = item_settings.UID\
                             WHERE item_inventory_info.stock > 0\
                             HAVING stat = 'Safe'"

get_non_expiry_inventory = "SELECT DISTINCT item_general_info.brand, item_general_info.name, item_general_info.unit,\
                                    item_inventory_info.Stock,\
                                    CONCAT('₱', FORMAT((item_settings.Cost_Price * (item_settings.Markup_Factor + 1)),2)),\
                                    DATE_FORMAT(item_inventory_info.Expiry_Date, '%b %d, %Y') AS expiry,\
                                    case when item_inventory_info.Expiry_Date IS null\
                                        then 'N/A' ELSE null END AS stat\
                            FROM item_general_info\
                            JOIN item_inventory_info ON item_general_info.UID = item_inventory_info.UID\
                            INNER JOIN item_settings ON item_general_info.UID = item_settings.UID\
                            WHERE item_inventory_info.stock > 0\
                            HAVING stat = 'N/A'"

get_category_specific_inventory = "SELECT item_general_info.brand, item_general_info.name, item_general_info.unit,\
                                            CAST(SUM(item_inventory_info.Stock) AS INT) AS stocks,\
                                            CONCAT('₱', FORMAT((item_settings.Cost_Price * (item_settings.Markup_Factor + 1)),2)),\
                                            DATE_FORMAT(item_inventory_info.Expiry_Date, '%b %d, %Y') AS expiry,\
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
                                    WHERE item_general_info.Category = ?\
                                    GROUP BY item_general_info.name, item_general_info.unit\
                                    ORDER BY item_general_info.UID"

#FOR CREATING A LIST OF ITEM AND/OR SERVICES FOR TRANSACTION
get_item_and_their_total_stock = "SELECT item_general_info.brand, item_general_info.name, item_general_info.unit,\
                                         CAST(SUM(item_inventory_info.Stock) as INT),\
                                         CONCAT('₱', FORMAT((item_settings.Cost_Price * (item_settings.Markup_Factor + 1)), 2))\
                                 FROM item_general_info JOIN item_inventory_info ON item_general_info.UID = item_inventory_info.UID\
                                 INNER	JOIN item_settings ON item_general_info.UID = item_settings.UID\
                                 WHERE item_inventory_info.Stock != 0 AND (item_inventory_info.Expiry_Date > CURRENT_DATE OR item_inventory_info.Expiry_Date IS null)\
                                 GROUP BY item_general_info.UID"

get_item_and_their_uid_and_stock = "SELECT SUM(stock) FROM item_inventory_info WHERE item_inventory_info.Stock != 0 AND (item_inventory_info.Expiry_Date > CURRENT_DATE OR item_inventory_info.Expiry_Date IS null) AND UID = ? GROUP BY UID"

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

check_item_if_it_expire_by_categ = "SELECT categories.does_expire\
                                    FROM item_general_info JOIN categories\
                                    ON item_general_info.Category = categories.categ_name\
                                    WHERE item_general_info.UID = ?"

#RESTOCKING
update_non_expiry_stock = "UPDATE item_inventory_info SET Stock = STOCK + ? WHERE UID = ? AND Expiry_Date IS NULL"
update_expiry_stock = "UPDATE item_inventory_info SET Stock = STOCK + ? WHERE UID = ? AND Expiry_Date = ?"
show_all_items = "SELECT name, unit FROM item_general_info"
insert_receiving_history = f"INSERT INTO receiving_history_info VALUES(?, ?, ?, ?, CURRENT_TIMESTAMP)"

get_order_info_history = "SELECT receiving_id, order_quantity, expiry, receiver, CAST(date_received AS DATE) FROM receiving_history_info WHERE receiving_id = ?"
get_order_info_history_id = "SELECT id, NAME, CAST(date_set AS DATE),ordered_by FROM recieving_item WHERE id = ?"

show_receiving_hist = "SELECT NAME, initial_stock, supp_name, date_recieved, reciever FROM recieving_item WHERE state = 2"

show_receiving_hist_by_date = f"SELECT id, NAME, CASE WHEN state = 2 then initial_stock WHEN state = 3 then initial_stock - current_stock\
                                WHEN (state = -1  AND initial_stock != current_stock) then initial_stock - current_stock\
                                END AS received_stock,\
                                supplier_info.supp_name, CAST(date_recieved AS DATE) AS received_date, reciever\
                                FROM recieving_item INNER JOIN supplier_info ON recieving_item.supp_id = supplier_info.supp_id\
                                WHERE (state = 2 OR state = 3 OR state = -1)\
                                AND DATE_FORMAT(date_recieved, '%M %Y') = ?\
                                ORDER BY date_recieved DESC"


#ADDING ITEMS THROUGH THE INVENTORY
add_item_general = "INSERT INTO item_general_info (UID, name, Category, brand, unit, added_by, added_date) VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)"
add_item_inventory = "INSERT INTO item_inventory_info (uid, Stock, Expiry_Date, state, added_date) VALUES (?, ?, ?, 1, CURRENT_DATE)"


add_item_settings = "INSERT INTO item_settings VALUES(?, ?, ?, ?, ?, ?, ?)"
add_item_supplier = "INSERT INTO item_supplier_info VALUES(?, ?)"

add_item_statistic = "INSERT INTO item_statistic_info VALUES(?, MONTH(CURRENT_DATE), 0, 'm')"

#RECORDING ANY TRANSACTION
generate_id_transaction = "SELECT COUNT(*) FROM transaction_record"
record_transaction = "INSERT INTO transaction_record VALUES(?, ?, ?, ?, CURRENT_DATE, 1)"
record_item_transaction_content = "INSERT INTO item_transaction_content VALUES(?, ?, ?, ?, ?, ?, 1)"
record_services_transaction_content = "INSERT INTO services_transaction_content VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

#UPDATING STOCK AFTER TRANSACTION
get_specific_stock = "SELECT * FROM item_inventory_info WHERE UID = ? AND (Expiry_Date > CURRENT_DATE OR Expiry_Date IS NULL) ORDER BY Expiry_Date ASC"
get_specific_stock_ordered_by_expiry = "SELECT * FROM item_inventory_info WHERE UID = ? AND (Expiry_Date > CURRENT_DATE OR Expiry_Date IS NULL) AND state = 1 ORDER BY Expiry_Date ASC"
get_specific_stock_ordered_by_date_added = "SELECT * FROM item_inventory_info WHERE UID = ? AND (Expiry_Date > CURRENT_DATE OR Expiry_Date IS NULL) AND state = 1 ORDER BY added_date"
delete_stocks_by_id = "DELETE FROM item_inventory_info WHERE id = ?"
deduct_stocks_by_id = "UPDATE item_inventory_info SET Stock = Stock - ? WHERE id = ?"
null_stocks_by_id = "UPDATE item_inventory_info SET Stock = 0 WHERE id = ?"

#FOR SALES
get_transaction_data = "SELECT * FROM transaction_record"

#FOR SERVICES
get_service_data = "SELECT service_name, price, date_added FROM service_info"
get_services_names = "SELECT DISTINCT service_name FROM service_info"

#FOR LOG AUDIT
get_log_audit_for_today = "SELECT * FROM log_history WHERE date_logged = CURRENT_DATE"

#FOR INVENTORY STATE

get_safe_state = "SELECT item_general_info.brand, item_general_info.name, item_general_info.unit,\
                            case when sum(item_inventory_info.stock) > item_settings.Reorder_factor * item_settings.Safe_stock\
                                        then sum(item_inventory_info.stock) ELSE 0 END AS stock\
                    FROM item_general_info JOIN item_inventory_info ON item_general_info.UID = item_inventory_info.UID\
                        INNER JOIN item_settings ON item_inventory_info.UID = item_settings.UID\
                    GROUP BY item_inventory_info.uid\
                    HAVING stock"

get_reorder_state= "SELECT item_general_info.brand, item_general_info.name, item_general_info.unit,\
                            case when sum(item_inventory_info.stock) <= item_settings.Reorder_factor * item_settings.Safe_stock\
                                    AND sum(item_inventory_info.stock) > item_settings.Crit_factor * item_settings.Safe_stock\
                                        then sum(item_inventory_info.stock) ELSE 0 END AS stock\
                    FROM item_general_info JOIN item_inventory_info ON item_general_info.UID = item_inventory_info.UID\
                        INNER JOIN item_settings ON item_inventory_info.UID = item_settings.UID\
                    GROUP BY item_inventory_info.uid\
                    HAVING stock;"

get_critical_state = "SELECT item_general_info.brand, item_general_info.name, item_general_info.unit,\
                            case when sum(item_inventory_info.stock) <= item_settings.Crit_factor * item_settings.Safe_stock\
                                        then sum(item_inventory_info.stock) ELSE 0 END AS stock\
                    FROM item_general_info JOIN item_inventory_info ON item_general_info.UID = item_inventory_info.UID\
                        INNER JOIN item_settings ON item_inventory_info.UID = item_settings.UID\
                    GROUP BY item_inventory_info.uid\
                    HAVING stock;"

get_out_of_stock_state = "SELECT item_general_info.brand, item_general_info.name, item_general_info.unit,\
                                 case when sum(item_inventory_info.stock) = 0\
                                           then sum(item_inventory_info.stock) ELSE -1 END AS stock\
                          FROM item_general_info JOIN item_inventory_info ON item_general_info.UID = item_inventory_info.UID\
                              INNER JOIN item_settings ON item_inventory_info.UID = item_settings.UID\
                          GROUP BY item_inventory_info.uid\
                          HAVING stock >= 0;"

get_near_expire_state = "SELECT item_general_info.brand, item_general_info.name, item_general_info.unit,\
                                 item_inventory_info.Stock,\
                                 case when item_inventory_info.Expiry_Date <= DATE_ADD(CURRENT_DATE, INTERVAL 15 DAY)\
                                             AND item_inventory_info.Expiry_Date > CURRENT_DATE\
                                             AND item_inventory_info.Expiry_Date IS NOT NULL \
                                             then item_inventory_info.Expiry_Date ELSE 0 END AS EXP\
                         FROM item_general_info JOIN item_inventory_info ON item_general_info.UID = item_inventory_info.UID\
                         HAVING exp;"


get_expired_state = "SELECT item_general_info.brand, item_general_info.name, item_general_info.unit,\
                             item_inventory_info.Stock,\
                             case when item_inventory_info.Expiry_Date <= CURRENT_DATE\
                                         AND item_inventory_info.Expiry_Date IS NOT NULL \
                                         then item_inventory_info.Expiry_Date ELSE NULL END AS EXP\
                     FROM item_general_info JOIN item_inventory_info ON item_general_info.UID = item_inventory_info.UID\
                     HAVING exp;"

#FOR DAILY SALES
get_todays_transaction_count = "SELECT COUNT(*)  FROM transaction_record WHERE transaction_date = CURRENT_DATE"

get_services_daily_sales = "SELECT CAST(SUM(services_transaction_content.price) AS DECIMAL(10,2))\
                            FROM transaction_record JOIN services_transaction_content ON transaction_record.transaction_uid = services_transaction_content.transaction_uid\
                            WHERE transaction_record.transaction_date = CURRENT_DATE;"

get_items_daily_sales = "SELECT CAST(SUM(item_transaction_content.price * item_transaction_content.quantity) AS DECIMAL(10,2))\
                         FROM transaction_record JOIN item_transaction_content ON transaction_record.transaction_uid = item_transaction_content.transaction_uid\
                         WHERE transaction_record.transaction_date = CURRENT_DATE AND item_transaction_content.state = 1;"

get_services_daily_sales_sp = "SELECT CAST(SUM(services_transaction_content.price) AS DECIMAL(10,2))\
                            FROM transaction_record JOIN services_transaction_content ON transaction_record.transaction_uid = services_transaction_content.transaction_uid\
                            WHERE transaction_record.transaction_date = ?;"

get_items_daily_sales_sp = "SELECT CAST(SUM(item_transaction_content.price * item_transaction_content.quantity) AS DECIMAL(10,2))\
                            FROM transaction_record JOIN item_transaction_content ON transaction_record.transaction_uid = item_transaction_content.transaction_uid\
                            WHERE transaction_record.transaction_date = ? AND item_transaction_content.state = 1;"

get_items_monthly_sales_sp = "SELECT CAST(SUM(item_transaction_content.price * item_transaction_content.quantity) AS DECIMAL(10,2))\
                              FROM transaction_record JOIN item_transaction_content ON transaction_record.transaction_uid = item_transaction_content.transaction_uid\
                              WHERE MONTH(transaction_record.transaction_date) = ? AND YEAR(transaction_record.transaction_date) = ? AND item_transaction_content.state = 1;"

get_services_monthly_sales_sp = "SELECT CAST(SUM(services_transaction_content.price) AS DECIMAL(10,2))\
                                 FROM transaction_record JOIN services_transaction_content ON transaction_record.transaction_uid = services_transaction_content.transaction_uid\
                                 WHERE MONTH(transaction_record.transaction_date) = ? AND YEAR(transaction_record.transaction_date) = ?;"

#ORACCESS
get_or = 'SELECT COUNT(*)+1 FROM transaction_record'

#LOGIN REPORT
record_login_report = "INSERT INTO login_report VALUES(?, ?, CURRENT_TIMESTAMP)"
get_usn = "SELECT usn FROM acc_cred WHERE usn = ?"

#USER LEVEL ACCESS
get_level_acessess = "SELECT * FROM user_level_access WHERE title = ?"
get_all_position_titles = "SELECT Title from user_level_access"

#RECIEVING ITEMS
record_recieving_item = "INSERT INTO recieving_item VALUES (?, ?, ?, ?, ?, ?, ? , NULL, ?, 1, CURRENT_TIMESTAMP, Null)"
get_recieving_items = "SELECT id, NAME, initial_stock, current_stock, supp_id from recieving_item where state = 1"

get_recieving_items_state = f"SELECT id, case When state = 3 then 'Partial' when state = 1 then 'On Order' END AS stats,\
                                NAME, current_stock, supplier_info.supp_name, ordered_by\
                                FROM recieving_item INNER JOIN supplier_info ON recieving_item.supp_id = supplier_info.supp_id\
                                WHERE state = 1 OR state = 3 ORDER BY state asc"

get_supplier = "SELECT * from item_supplier_info where UID = ?"
get_receiving_expiry_by_id = "SELECT date_format(exp_date, '%Y-%m-%d') from recieving_item WHERE id = ?"
update_recieving_item = "UPDATE recieving_item SET reciever = ?, state = 2, date_recieved = CURRENT_TIMESTAMP WHERE id = ?"
update_recieving_item_partially_received = "UPDATE recieving_item SET state = 3, current_stock = current_stock - ? WHERE id = ?"
record_partially_received_item = "INSERT INTO partially_recieving_item VALUES (?, ?, ?, ?, ?, ?, Current_date)"

update_recieving_item_partially_received_with_date_receiver = f"UPDATE recieving_item SET state = 3, current_stock = current_stock - ?, date_recieved = CURRENT_TIMESTAMP,\
                                                                reciever = ?\
                                                                WHERE id = ?"

get_pending_items = f"SELECT id, recieving_item.NAME, current_stock, CAST(date_set AS DATE) AS date_set, supp_name FROM recieving_item where state = 3 AND DATE_FORMAT(date_set, '%M %Y') = ?"

get_order_info = f"SELECT id, CAST(date_set AS DATE), item_uid, NAME,\
                    CASE WHEN state = 1 THEN 'Waiting' WHEN state = 3 THEN 'Pending' END as state,\
                    initial_stock, current_stock, ordered_by,\
                    supplier_info.supp_id, supplier_info.supp_name,\
                    supplier_info.contact_person, supplier_info.contact_number\
                    FROM recieving_item LEFT JOIN supplier_info\
                    ON recieving_item.supp_id = supplier_info.supp_id WHERE id = ?"

#DISPOSAL
get_for_disposal_items = "SELECT item_name, initial_quantity, current_quantity, DATE_FORMAT(date_of_disposal, '%m-%d-%Y at %H:%i %p'), disposed_by FROM disposal_history WHERE full_dispose_date IS NULL"
record_disposal_process = "INSERT INTO disposal_history (id, receive_id, item_uid, item_name, initial_quantity, reason, date_of_disposal, disposed_by) VALUES (?, ?, ?, ?, ?, ?, CURRENT_DATE, ?);" #?, ?, ?, ?, ?, ?, CURRENT_DATE, ?
delete_disposing_items = "DELETE FROM item_inventory_info where uid = ? and stock = ? and expiry_date <= CURRENT_DATE"
get_disposal_hist = "SELECT item_name, initial_quantity, current_quantity, DATE_FORMAT(full_dispose_date, '%m-%d-%Y at %H:%i %p'), disposed_by FROM disposal_history WHERE full_dispose_date IS NOT NULL"


get_disposal_items = "SELECT id, item_name, initial_quantity, reason, CAST(date_of_disposal as DATE), disposed_by\
                        FROM disposal_history ORDER BY item_name ASC"

#ACCOUNT CREATION

#PET INFO
get_owners = "SELECT owner_name, address, contact_number FROM pet_owner_info"

get_pet_name = "SELECT id, p_name FROM pet_info"

get_ids_pi = "SELECT id FROM pet_info"

get_pet_info = f"SELECT id, p_name FROM  pet_info INNER JOIN pet_owner_info ON pet_info.owner_id = pet_owner_info.owner_id WHERE pet_owner_info.owner_name = ?"
                
get_pet_id_by_name_owner = f"SELECT pet_info.id FROM pet_info INNER JOIN pet_owner_info ON pet_info.owner_id = pet_owner_info.owner_id\
                            WHERE p_name = ? AND pet_owner_info.owner_name = ?"  
                
get_pet_record=f"SELECT pet_info.id, pet_info.p_name, pet_owner_info.owner_name, pet_owner_info.contact_number\
                FROM pet_info INNER JOIN pet_owner_info\
                ON pet_info.owner_id = pet_owner_info.owner_id\
                ORDER BY pet_owner_info.owner_name ASC"

get_pet_info_for_cust_info = "SELECT breed FROM pet_info WHERE p_name = ?"
insert_new_pet_info = "INSERT INTO pet_info VALUES(?, ?, ?, ?, ?, ?, ?, ?)"

insert_new_pet_owner = f"INSERT INTO pet_owner_info (owner_name, address, contact_number) VALUES (? , ?, ?)"

insert_new_pet_breed = f"INSERT INTO pet_breed VALUES(?,?)"
#PET INFO SORT
get_pet_info_sort_by_pet_name = f"SELECT pet_info.id, pet_info.p_name, pet_owner_info.owner_name, pet_owner_info.contact_number FROM pet_info INNER JOIN pet_owner_info\
                            ON pet_info.owner_id = pet_owner_info.owner_id ORDER BY p_name asc"

get_pet_info_sort_by_id = f"SELECT pet_info.id, pet_info.p_name, pet_owner_info.owner_name, pet_owner_info.contact_number FROM pet_info INNER JOIN pet_owner_info\
                            ON pet_info.owner_id = pet_owner_info.owner_id ORDER BY id asc"

#HIST LOG
get_hist_log = "SELECT CONCAT(acc_info.usn, ' (', acc_info.full_name, ')'),\
                       log_history.date_logged,\
                       log_history.time_in,\
                       log_history.time_out\
                FROM acc_info JOIN log_history ON acc_info.usn = log_history.usn"

#DATES
get_active_year_transaction = "SELECT DISTINCT Year(transaction_date) FROM transaction_record"
get_first_date = "SELECT DISTINCT transaction_date FROM transaction_record ORDER BY transaction_date ASC"


#GET INVENTORY_REPORT
get_current_stock_group_by_name = "SELECT item_general_info.name,\
                                       CAST(SUM(item_inventory_info.Stock) AS INT) AS current_stocks\
                                   FROM item_general_info\
                                   JOIN item_inventory_info ON item_general_info.UID = item_inventory_info.UID\
                                   INNER JOIN item_settings ON item_general_info.UID = item_settings.UID\
                                   WHERE item_inventory_info.Expiry_Date > CURRENT_DATE OR item_inventory_info.Expiry_Date IS NULL\
                                   GROUP BY item_general_info.name\
                                   ORDER BY item_general_info.UID;"
                                   
get_inventory_report = "SELECT item_general_info.UID, item_general_info.name,\
                                       CAST(SUM(item_inventory_info.Stock) AS INT) AS current_stocks\
                                   FROM item_general_info\
                                   JOIN item_inventory_info ON item_general_info.UID = item_inventory_info.UID\
                                   INNER JOIN item_settings ON item_general_info.UID = item_settings.UID\
                                   WHERE item_inventory_info.Expiry_Date > CURRENT_DATE OR item_inventory_info.Expiry_Date IS NULL\
                                   GROUP BY item_general_info.name\
                                   ORDER BY item_general_info.UID"

get_inventory_info_with_uid = "SELECT item_general_info.name,\
                                       CAST(SUM(item_inventory_info.Stock) AS INT) AS current_stocks,\
                                    item_general_info.UID FROM item_general_info\
                                   JOIN item_inventory_info ON item_general_info.UID = item_inventory_info.UID\
                                   INNER JOIN item_settings ON item_general_info.UID = item_settings.UID\
                                   WHERE item_inventory_info.Expiry_Date > CURRENT_DATE OR item_inventory_info.Expiry_Date IS NULL\
                                   GROUP BY item_general_info.name\
                                   ORDER BY item_general_info.UID;"

get_all_bought_items_group_by_name = "SELECT item_transaction_content.item_name,\
                                      		 CAST(SUM(item_transaction_content.quantity) AS INT) AS quantity\
                                      FROM item_transaction_content\
                                      JOIN transaction_record ON item_transaction_content.transaction_uid = transaction_record.transaction_uid\
                                      WHERE transaction_record.transaction_date = current_date AND item_transaction_content.state = 1\
                                      GROUP BY item_transaction_content.item_name\
                                      ORDER BY transaction_record.transaction_uid"

get_items_daily_sales_sp_temp = "SELECT CAST(SUM(item_transaction_content.price * item_transaction_content.quantity) AS FLOAT)\
                         FROM transaction_record JOIN item_transaction_content ON transaction_record.transaction_uid = item_transaction_content.transaction_uid\
                         WHERE transaction_record.transaction_date = ? AND item_transaction_content.state = 1;"

get_services_daily_sales_sp_temp = "SELECT CAST(SUM(services_transaction_content.price) AS FLOAT)\
                            FROM transaction_record JOIN services_transaction_content ON transaction_record.transaction_uid = services_transaction_content.transaction_uid\
                            WHERE transaction_record.transaction_date = ?;"

get_items_monthly_sales_sp_temp = "SELECT CAST(SUM(item_transaction_content.price * item_transaction_content.quantity) AS FLOAT)\
                         FROM transaction_record JOIN item_transaction_content ON transaction_record.transaction_uid = item_transaction_content.transaction_uid\
                         WHERE MONTH(transaction_record.transaction_date) = ? AND YEAR(transaction_record.transaction_date) = ? AND item_transaction_content.state = 1;"

get_services_monthly_sales_sp_temp = "SELECT CAST(SUM(services_transaction_content.price) AS FLOAT)\
                            FROM transaction_record JOIN services_transaction_content ON transaction_record.transaction_uid = services_transaction_content.transaction_uid\
                            WHERE MONTH(transaction_record.transaction_date) = ? AND YEAR(transaction_record.transaction_date) = ?;"

#REPORT TREEVIEWS
daily_report_treeview_data = "SELECT transaction_record.transaction_uid,\
                                      transaction_record.client_name,\
                                      CONCAT('₱', FORMAT(COALESCE(sum(services_transaction_content.price), 0) ,2)) AS service,\
                                      CONCAT('₱', FORMAT(COALESCE(SUM(item_transaction_content.price * item_transaction_content.quantity), 0) ,2)) AS item,\
                                      CONCAT('₱', FORMAT(transaction_record.Total_amount ,2)) AS total\
                              FROM transaction_record\
                              left JOIN services_transaction_content\
                                          ON transaction_record.transaction_uid = services_transaction_content.transaction_uid\
                              LEFT JOIN item_transaction_content\
                                          ON transaction_record.transaction_uid = item_transaction_content.transaction_uid\
                              WHERE transaction_date = ? AND item_transaction_content.state = 1\
                              GROUP BY transaction_record.transaction_uid"

monthly_report_treeview_data = "SELECT DATE_FORMAT(transaction_record.transaction_date, '%M %d, %Y') AS 'date',\
                                        CONCAT('₱', FORMAT(COALESCE(sum(item_transaction_content.price * item_transaction_content.quantity), 0), 2)) AS item,\
                                        CONCAT('₱', FORMAT(COALESCE(sum(services_transaction_content.price), 0) ,2)) AS service,\
                                        CONCAT('₱', FORMAT(COALESCE(sum(item_transaction_content.price * item_transaction_content.quantity), 0) + coalesce(sum(services_transaction_content.price), 0), 2))\
                                FROM transaction_record\
                                left JOIN services_transaction_content\
                                    ON transaction_record.transaction_uid = services_transaction_content.transaction_uid\
                                LEFT JOIN item_transaction_content\
                                    ON transaction_record.transaction_uid = item_transaction_content.transaction_uid\
                                WHERE MONTH(transaction_record.transaction_date) = ?\
                                    AND YEAR(transaction_record.transaction_date) = ?\
                                        AND item_transaction_content.state = 1\
                                GROUP BY transaction_record.transaction_date\
                                ORDER BY transaction_record.transaction_date;"

yearly_report_treeview_data = "SELECT DATE_FORMAT(transaction_record.transaction_date, '%M') AS 'date',\
                                      CONCAT('₱', FORMAT(COALESCE(sum(item_transaction_content.price * item_transaction_content.quantity), 0), 2)) AS item,\
                                      CONCAT('₱', FORMAT(COALESCE(SUM(services_transaction_content.price), 0) ,2)) AS service,\
                                      CONCAT('₱', FORMAT(COALESCE(sum(item_transaction_content.price * item_transaction_content.quantity), 0) + COALESCE(SUM(services_transaction_content.price), 0), 2)) AS total\
                               FROM transaction_record\
                               left JOIN services_transaction_content\
                                           ON transaction_record.transaction_uid = services_transaction_content.transaction_uid\
                               LEFT JOIN item_transaction_content\
                                           ON transaction_record.transaction_uid = item_transaction_content.transaction_uid\
                               WHERE YEAR(transaction_record.transaction_date) = 2023\
                                   AND item_transaction_content.state = 1\
                               GROUP BY month(transaction_record.transaction_date)\
                               ORDER BY transaction_record.transaction_date;"

#invoices
insert_invoice_data = "INSERT INTO invoice_record VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
insert_invoice_service_data = "INSERT INTO invoice_service_content values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
insert_invoice_item_data = "INSERT INTO invoice_item_content VALUES (? ,? ,? ,?, ?, ?)"
cancel_invoice = "UPDATE invoice_record SET State = -1 WHERE invoice_uid = ?"

get_invoice_info_item = "SELECT invoice_record.invoice_uid,\
                            invoice_record.client_name,\
                            CONCAT('₱', format(SUM(COALESCE(invoice_service_content.price, 0)), 2)) AS service,\
                            CONCAT('₱', FORMAT(SUM(COALESCE(invoice_item_content.price * invoice_item_content.quantity, 0)), 2)) AS items,\
                            CONCAT('₱', FORMAT(invoice_record.Total_amount, 2)) AS price,\
                            DATE_FORMAT(invoice_record.transaction_date, '%M %d, %Y') AS date\
                        FROM invoice_record\
                        LEFT JOIN invoice_service_content\
                            ON invoice_record.invoice_uid = invoice_service_content.invoice_uid\
                        LEFT JOIN invoice_item_content\
                            ON invoice_record.invoice_uid = invoice_item_content.invoice_uid\
                        WHERE invoice_record.State = 0\
                        GROUP BY invoice_record.invoice_uid"

get_invoice_info = "SELECT invoice_record.invoice_uid,\
                           invoice_record.client_name,\
                           CONCAT('₱', FORMAT(invoice_record.Total_amount, 2)) AS price,\
                           DATE_FORMAT(invoice_record.transaction_date, '%M %d, %Y') AS date\
                    FROM invoice_record\
                    LEFT JOIN invoice_service_content\
                        ON invoice_record.invoice_uid = invoice_service_content.invoice_uid\
                    LEFT JOIN invoice_item_content\
                        ON invoice_record.invoice_uid = invoice_item_content.invoice_uid\
                    WHERE invoice_record.State = 0\
                        AND process_type = 0\
                    GROUP BY invoice_record.invoice_uid"

get_invoice_info_service = "SELECT invoice_record.invoice_uid,\
                                invoice_record.client_name,\
                                invoice_service_content.patient_name,\
                                invoice_service_content.service_name,\
                                CONCAT('₱', FORMAT(invoice_record.Total_amount, 2)) AS price,\
                                DATE_FORMAT(invoice_service_content.scheduled_date, '%M %d, %Y') AS date\
                            FROM invoice_record\
                            LEFT JOIN invoice_service_content\
                                ON invoice_record.invoice_uid = invoice_service_content.invoice_uid\
                            LEFT JOIN invoice_item_content\
                                ON invoice_record.invoice_uid = invoice_item_content.invoice_uid\
                            WHERE invoice_record.State = 0\
                                AND process_type = 1\
                            GROUP BY invoice_record.invoice_uid\
                            ORDER BY invoice_service_content.scheduled_date"
#Currently obsolete


get_invoice_info_queued = "SELECT invoice_record.invoice_uid,\
                                invoice_record.client_name,\
                                invoice_service_content.patient_name,\
                                CONCAT(invoice_service_content.service_name, case when service_info_test.duration_type != 0 then ' (Initial)' ELSE '' END),\
                                CONCAT('₱', FORMAT(invoice_record.Total_amount, 2)) AS price,\
                                DATE_FORMAT(invoice_record.transaction_date, '%M %d, %Y') AS date\
                            FROM invoice_record\
                            LEFT JOIN invoice_service_content\
                                ON invoice_record.invoice_uid = invoice_service_content.invoice_uid\
                            LEFT JOIN invoice_item_content\
                                ON invoice_record.invoice_uid = invoice_item_content.invoice_uid\
                            LEFT JOIN service_info_test\
                            	ON invoice_service_content.service_name = service_info_test.service_name\
                            WHERE invoice_record.State = 0\
                                AND process_type = 1\
                            GROUP BY invoice_record.invoice_uid"


get_payment_invoice_info = "SELECT invoice_record.invoice_uid,\
                                   invoice_record.client_name,\
                                   CONCAT('₱', format(SUM(COALESCE(invoice_service_content.price, 0)), 2)) AS service,\
                                   CONCAT('₱', FORMAT(SUM(COALESCE(invoice_item_content.price * invoice_item_content.quantity, 0)), 2)) AS items,\
                                   CONCAT('₱', FORMAT(invoice_record.Total_amount, 2)) AS price,\
                                   DATE_FORMAT(invoice_record.transaction_date, '%M %d, %Y') AS date\
                            FROM invoice_record\
                            LEFT JOIN invoice_service_content\
                                ON invoice_record.invoice_uid = invoice_service_content.invoice_uid\
                            LEFT JOIN invoice_item_content\
                                ON invoice_record.invoice_uid = invoice_item_content.invoice_uid\
                            WHERE invoice_record.State = 1\
                            GROUP BY invoice_record.invoice_uid\
                            ORDER BY payment_date"

get_specific_payment_invoice_info = "SELECT invoice_record.invoice_uid,\
                                        invoice_record.client_name,\
                                        CONCAT('₱', format(SUM(COALESCE(invoice_service_content.price, 0)), 2)) AS service,\
                                        CONCAT('₱', FORMAT(SUM(COALESCE(invoice_item_content.price * invoice_item_content.quantity, 0)), 2)) AS items,\
                                        CONCAT('₱', FORMAT(invoice_record.Total_amount, 2)) AS price,\
                                        DATE_FORMAT(invoice_record.transaction_date, '%M %d, %Y') AS date\
                                    FROM invoice_record\
                                    LEFT JOIN invoice_service_content\
                                        ON invoice_record.invoice_uid = invoice_service_content.invoice_uid\
                                    LEFT JOIN invoice_item_content\
                                        ON invoice_record.invoice_uid = invoice_item_content.invoice_uid\
                                    WHERE invoice_record.State = 1\
                                        AND invoice_record.invoice_uid = ?\
                                    GROUP BY invoice_record.invoice_uid"

get_selected_payment_invoice_info = "SELECT invoice_record.invoice_uid,\
                                        invoice_record.client_name,\
                                        CONCAT('₱', format(SUM(COALESCE(invoice_service_content.price, 0)), 2)) AS service,\
                                        CONCAT('₱', FORMAT(SUM(COALESCE(invoice_item_content.price * invoice_item_content.quantity, 0)), 2)) AS items,\
                                        CONCAT('₱', FORMAT(invoice_record.Total_amount, 2)) AS price,\
                                        DATE_FORMAT(invoice_record.transaction_date, '%M %d, %Y') AS date\
                                    FROM invoice_record\
                                    LEFT JOIN invoice_service_content\
                                        ON invoice_record.invoice_uid = invoice_service_content.invoice_uid\
                                    LEFT JOIN invoice_item_content\
                                        ON invoice_record.invoice_uid = invoice_item_content.invoice_uid\
                                    WHERE invoice_record.invoice_uid = ?\
                                    GROUP BY invoice_record.invoice_uid"

set_invoice_transaction_to_payment = "UPDATE invoice_record SET state = 1, payment_date = CURRENT_TIMESTAMP  WHERE invoice_uid = ?"
set_invoice_transaction_to_queue = "UPDATE invoice_record SET state = 3 WHERE invoice_uid = ?"
set_invoice_transaction_to_recorded = "UPDATE invoice_record SET state = 2, Date_transacted = ? WHERE invoice_uid = ?"

get_invoice_by_id = "SELECT * FROM invoice_record WHERE invoice_uid = ?"
get_invoice_service_content_by_id = "SELECT service_name, patient_name, scheduled_date, END_schedule, multiple_sched_quan, instance_of_mul_sched, FORMAT(price, 2) AS total FROM invoice_service_content WHERE invoice_uid = ?;"
get_invoice_item_content_by_id = "SELECT item_name, quantity, FORMAT((price * quantity), 2) AS total FROM invoice_item_content WHERE invoice_uid = ?;"

get_current_invoice_count = "SELECT COUNT(*) FROM recieving_item where id like '?%'"

#fast or slow moving item
get_selling_rate1 = "SELECT CASE when SUM(case when MONTH(transaction_record.transaction_date) = MONTH(CURRENT_DATE)\
                                                        then item_transaction_content.quantity\
                                                        ELSE 0 END) > item_settings.rate_mode\
                                        then '🠉'\
                                    when SUM(case when MONTH(transaction_record.transaction_date) = MONTH(CURRENT_DATE)\
                                                        then item_transaction_content.quantity\
                                                        ELSE 0 END) < item_settings.rate_mode\
                                        then '🠋'\
                                        ELSE '-'end as rate,\
                    item_general_info.brand, item_general_info.name, item_general_info.unit\
                    FROM item_inventory_info\
                    JOIN item_general_info\
                        ON item_inventory_info.UID = item_general_info.UID\
                    JOIN item_settings\
                        ON item_inventory_info.UID = item_settings.UID\
                    LEFT JOIN item_transaction_content\
                        ON item_inventory_info.UID = item_transaction_content.Item_uid\
                    LEFT JOIN transaction_record\
                        ON item_transaction_content.transaction_uid = transaction_record.transaction_uid\
                    GROUP BY item_general_info.UID\
                    ORDER BY item_inventory_info.UID"

get_selling_rate = "SELECT case when item_settings.rate_mode = 0\
                                        then case when item_statistic_info.rate_symbol = 'u'\
                                                        then '🠉'\
                                                    when item_statistic_info.rate_symbol = 'd'\
                                                        then '🠋'\
                                                        ELSE '-' end\
                                    when item_settings.rate_mode = 0\
                                        then '🠉'\
                                        ELSE '🠋' END AS rate,\
                            item_general_info.brand,\
                            item_general_info.name,\
                            item_general_info.unit\
                    FROM item_general_info\
                    INNER JOIN item_statistic_info\
                        ON item_general_info.UID = item_statistic_info.UID\
                    INNER JOIN item_settings\
                        ON item_general_info.UID = item_settings.UID\
                    GROUP BY item_general_info.UID"

#LOG
get_raw_action_history = "SELECT *\
                          FROM action_history\
                          JOIN acc_info\
                              ON action_history.usn = acc_info.usn\
                          WHERE DATE(action_date) = ?\
                              AND acc_info.job_position = ?"
get_log_history = "SELECT log_history.USN, acc_info.job_position, log_history.DATE_LOGGED, log_history.TIME_IN, log_history.TIME_OUT\
                    FROM log_history\
                    JOIN acc_info\
                        ON log_history.usn = acc_info.usn\
                    WHERE log_history.DATE_LOGGED = ?"

#transaction
check_if_stock_can_accomodate = "SELECT invoice_item_content.quantity <= SUM(item_inventory_info.Stock)\
                                 FROM invoice_item_content JOIN item_inventory_info\
                                     ON invoice_item_content.Item_uid = item_inventory_info.UID\
                                 WHERE invoice_item_content.invoice_uid = ?\
                                 GROUP BY invoice_item_content.Item_uid"
                    

#get_pet_record = "SELECT * FROM pet_info WHERE id = ?"                    
update_pet_record_pet_info = "UPDATE pet_info SET p_name = ?, breed = ?, type = ?, sex = ?, weight = ?, bday = ? WHERE id = ?"
update_pet_record_pet_owner = f"UPDATE pet_owner_info\
                                INNER JOIN pet_info ON pet_owner_info.owner_id = pet_info.owner_id\
                                SET owner_name = ? ,\
                                address = ? ,\
                                contact_number = ?\
                                WHERE pet_info.id = ? "

insert_new_category = "INSERT INTO categories VALUES (?, ?, ?, 1, CURRENT_TIMESTAMP, NULL, NULL)"
update_category_deac = "Update categories Set state = 0, disabled_by = ?, disabled_date = CURRENT_TIMESTAMP where categ_name = ?"
update_category_reac = "Update categories Set state = 1 where categ_name = ?"

update_deactivate_account = "UPDATE acc_info SET state = 0 WHERE usn = ?"

#TESTING - James

get_service_data_test = "SELECT UID, service_name, category, CONCAT('₱', FORMAT(price, 2)) FROM service_info_test WHERE state = 1"
get_service_category_test = "SELECT category FROM service_category_test"

insert_service_test = "INSERT INTO service_info_test VALUES( ?, ?, ?, ?, ?, ?, ?, ?)"

get_services_and_their_price_test = "SELECT UID, service_name, CONCAT('₱', FORMAT(price, 2)) FROM service_info_test WHERE state = 1"
insert_service_test = "INSERT INTO service_info_test VALUES( ?, ?, ?, ?, ?, ?, ?)"

#ACCOUNTS
create_acc_cred = "INSERT INTO acc_cred VALUES (?, ?, ?, NULL)"
create_acc_info = "INSERT INTO acc_info VALUES (?, ?, ?, 1)"
create_acc_access_level = "INSERT INTO account_access_level VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
update_acc_access_level = "UPDATE account_access_level SET Dashboard = ?, Transaction = ?, Services = ?, Sales = ?,\
                                                           Inventory = ?, Pet_info = ?, Report = ?, User = ?, Action = ?\
                                                           WHERE usn = ?"

#dashboard
get_monthly_sales_data = "SELECT DATE_FORMAT(transaction_date, '%M %d, %Y'),\
                               CONCAT('₱', FORMAT(sum(total_amount), 2)) AS price\
                          FROM transaction_record\
                          WHERE MONTH(transaction_date) = ?\
                               AND YEAR(transaction_date) = ?\
                          GROUP BY DAY(transaction_date)"

get_specific_pet_record = "SELECT services_transaction_content.service_name,\
                                   services_transaction_content.scheduled_date,\
                                   transaction_record.Attendant_usn\
                           FROM services_transaction_content\
                           JOIN transaction_record\
                               ON services_transaction_content.transaction_uid = transaction_record.transaction_uid\
                           WHERE  services_transaction_content.pet_uid = ?"
                           #    AND services_transaction_content.`status` = 0"
                           
get_daily_sales_data_by_day = "SELECT transaction_uid, client_name, Attendant_usn, CONCAT('₱',FORMAT(Total_amount,2))AS total FROM transaction_record WHERE transaction_record.transaction_date = ?"


get_scheduled_clients_today = f"SELECT invoice_record.client_name, pet_owner_info.contact_number\
                                FROM invoice_record\
                                INNER JOIN invoice_service_content ON invoice_record.invoice_uid = invoice_service_content.invoice_uid\
                                INNER JOIN pet_info ON invoice_service_content.pet_uid = pet_info.id\
                                INNER JOIN pet_owner_info ON pet_info.owner_id = pet_owner_info.owner_id\
                                WHERE invoice_record.State = 0\
                                AND invoice_service_content.scheduled_date = CURRENT_DATE\
                                GROUP BY invoice_record.client_name"

get_pet_client_scheduled_today = f"SELECT invoice_service_content.invoice_uid, invoice_service_content.patient_name, invoice_service_content.service_name,\
                                CONCAT('₱', FORMAT(invoice_service_content.price,2)) AS price\
                                FROM invoice_record\
                                INNER JOIN invoice_service_content ON invoice_record.invoice_uid = invoice_service_content.invoice_uid\
                                WHERE invoice_record.State = 0\
                                AND invoice_service_content.scheduled_date = CURRENT_DATE\
                                AND invoice_record.client_name = ?"

get_pet_services_scheduled_today = f"SELECT invoice_service_content.invoice_uid, invoice_service_content.service_name, invoice_record.Total_amount,\
                                invoice_service_content.scheduled_date, invoice_service_content.price\
                                FROM invoice_record\
                                INNER JOIN invoice_service_content ON invoice_record.invoice_uid = invoice_service_content.invoice_uid\
                                WHERE invoice_record.State = 0\
                                AND invoice_service_content.scheduled_date = CURRENT_DATE\
                                AND invoice_record.client_name = ?\
                                AND invoice_service_content.patient_name = ?"

get_pet_service_date_sched = f"SELECT invoice_record.transaction_date, invoice_service_content.scheduled_date\
                                FROM invoice_record\
                                INNER JOIN invoice_service_content ON invoice_record.invoice_uid = invoice_service_content.invoice_uid\
                                WHERE invoice_record.State = 0\
                                AND invoice_service_content.scheduled_date = CURRENT_DATE\
                                AND invoice_record.client_name = ?\
                                AND invoice_service_content.patient_name = ?\
                                AND invoice_record.invoice_uid = ?\
                                AND invoice_service_content.service_name = ?"
get_scheduled_clients_today_service = f"SELECT invoice_service_content.patient_name, invoice_record.client_name, invoice_service_content.service_name\
                                FROM invoice_record INNER JOIN invoice_service_content\
                                ON invoice_record.invoice_uid = invoice_service_content.invoice_uid\
                                WHERE invoice_record.State = 0 AND invoice_service_content.scheduled_date = CURRENT_DATE\
                                GROUP BY invoice_service_content.patient_name"

get_pet_view_record = f"SELECT pet_info.id, pet_info.p_name, pet_info.`type`, pet_info.sex, pet_info.breed, pet_info.weight, pet_info.bday,\
                        pet_owner_info.owner_name, pet_owner_info.address, pet_owner_info.contact_number\
                        FROM pet_info\
                        INNER JOIN pet_owner_info ON pet_info.owner_id = pet_owner_info.owner_id\
                        WHERE id = ?"

get_pet_record_search_query=f"SELECT id, p_name, pet_owner_info.owner_name FROM pet_info INNER JOIN pet_owner_info ON pet_info.owner_id = pet_owner_info.owner_id\
                                   WHERE p_name LIKE '%?%' OR pet_owner_info.owner_name LIKE '%?%' ORDER BY p_name ASC"

#SALES 
get_sales_data = "SELECT transaction_uid, client_name, transaction_date, Total_amount,  Attendant_usn FROM transaction_record WHERE transaction_date = ?"

get_item_record = "SELECT  item_name, quantity, price, ROUND((quantity*price),2) AS total FROM item_transaction_content WHERE transaction_uid = ?"
get_service_record = "SELECT CONCAT(service_name,' - ',  'Pet: ',patient_name) AS service, 1 AS quantity, price, ROUND(price,2)AS total FROM services_transaction_content WHERE transaction_uid = ?"
get_service_record_temp = "SELECT CONCAT(service_name) AS service, patient_name, scheduled_date, END_schedule, price, price, ROUND(price,2)AS total FROM services_transaction_content WHERE transaction_uid = ?"


#General Settings
get_service_info = f"SELECT UID, service_name, price, category, date_added FROM service_info_test WHERE UID = ?"

get_inventory = f"SELECT item_general_info.UID, item_general_info.name, item_general_info.Category,\
                    CONCAT('₱' , FORMAT(item_settings.Cost_Price*(item_settings.Markup_Factor+1),2)) AS price\
                    FROM item_general_info INNER JOIN item_settings ON item_general_info.UID = item_settings.UID"

get_inventory_info= f"SELECT item_general_info.UID, item_general_info.name, item_general_info.Category, FORMAT(item_settings.Cost_Price,2) AS unit_cost,\
                        item_settings.Markup_Factor, FORMAT(item_settings.Cost_Price*(item_settings.Markup_Factor+1),2)AS selling, item_settings.Reorder_factor,\
                        item_settings.Crit_factor, item_settings.Safe_stock, item_settings.rate_mode\
                        FROM item_general_info INNER JOIN item_settings ON item_general_info.UID = item_settings.UID WHERE item_general_info.UID = ?"

check_if_item_does_expire = "SELECT does_expire\
                            FROM categories\
                            JOIN item_general_info\
                                ON categories.categ_name = item_general_info.Category\
                            WHERE item_general_info.UID = ?"
                            
                            
#FOR UPDATING RECORDS

update_pet_name_and_invoice_records = "UPDATE invoice_service_content SET invoice_service_content.patient_name = (SELECT pet_info.p_name FROM pet_info WHERE invoice_service_content.pet_uid = pet_info.id)"

get_invoice_item_content_by_id


'''SUPPLIER INFO SQL'''
#SET
insert_supplier_info = "INSERT INTO supplier_info VALUES(?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, NULL, NULL)"

#GET
get_last_supplier_id = "SELECT supp_id FROM supplier_info ORDER BY supp_id DESC LIMIT 1"
get_supplier_info = "SELECT supp_id, supp_name, contact_person, contact_number, address FROM supplier_info ORDER BY supp_id ASC"
get_supplier_record = f"SELECT supp_id, supp_name, telephone, contact_person, contact_number, contact_email, address, created_by, CAST(date_added AS DATE), CAST(date_modified AS DATE)\
                        FROM supplier_info WHERE supp_id = ?"
                        
get_supplier_base_item = f"SELECT item_supplier_info.supp_id, supplier_info.supp_name\
                            FROM item_supplier_info INNER JOIN supplier_info ON item_supplier_info.supp_id = supplier_info.supp_id\
                            WHERE item_supplier_info.UID = ?"
                        
#UPDATES

update_supplier_info = f"UPDATE supplier_info SET supp_name = ?, telephone = ?, contact_person = ?, contact_number = ?,\
                        contact_email = ?, address = ?, date_modified = CURRENT_TIMESTAMP WHERE supp_id = ?"


'''SALES'''

get_sales_record_by_date = f"SELECT transaction_uid, client_name , CONCAT('₱', FORMAT(Total_amount,2)) AS price, transaction_date, Attendant_usn\
                                FROM transaction_record WHERE transaction_date BETWEEN ? AND ? ORDER BY transaction_date"

get_sales_record_all =f"SELECT transaction_uid, client_name , CONCAT('₱', FORMAT(Total_amount,2)) AS price, transaction_date, Attendant_usn FROM transaction_record"

get_sales_search_query = f"SELECT transaction_uid, client_name FROM transaction_record WHERE client_name LIKE '%?%' OR transaction_uid LIKE '%?%' ORDER BY client_name"

get_sales_record_info = f"SELECT transaction_uid, client_name, CONCAT('₱', FORMAT(Total_amount,2)) AS price, transaction_date, Attendant_usn, state\
                            FROM transaction_record WHERE transaction_uid = ?"

#Tentative;                          
get_sales_attendant = f"SELECT DISTINCT Attendant_usn FROM transaction_record"

get_sales_by_attendant = f"SELECT transaction_uid, client_name , CONCAT('₱', FORMAT(Total_amount,2)) AS price, transaction_date, Attendant_usn\
                        FROM transaction_record WHERE transaction_date BETWEEN ? AND ?\
                            AND Attendant_usn = ?"
                            
get_client_by_invoice_uid = "SELECT CLIENT_name FROM invoice_record WHERE invoice_uid = ?"

get_prices_of_invoice = "SELECT COALESCE(SUM(invoice_item_content.price), 0),\
                                 COALESCE(SUM(invoice_service_content.price), 0)\
                         FROM invoice_record\
                         LEFT JOIN invoice_item_content\
                             ON invoice_record.invoice_uid = invoice_item_content.invoice_uid\
                         LEFT JOIN invoice_service_content\
                             ON invoice_record.invoice_uid = invoice_service_content.invoice_uid\
                         WHERE invoice_record.invoice_uid = ?\
                         GROUP BY invoice_record.invoice_uid"

get_services_invoice_by_id = "SELECT * FROM invoice_service_content WHERE invoice_uid = ?"
get_item_invoice_by_id = "SELECT * FROM invoice_item_content WHERE invoice_uid = ?"

add_additional_in_invoice = "INSERT INTO invoice_item_content VALUES(?, ?, ?, ?, ?, 0)"
update_existing_item_in_invoice = "UPDATE invoice_item_content SET quantity = ? WHERE invoice_uid = ? AND item_name = ?"
delete_existing_item_in_invoice = "DELETE FROM invoice_item_content WHERE item_name = ?"
update_invoice_total_amount = "UPDATE invoice_record SET Total_amount = ? WHERE invoice_uid = ?"

check_todays_accomodated_sched = "SELECT COUNT(*) FROM invoice_record WHERE state = 3"
get_duration_type = "SELECT duration_type FROM service_info_test WHERE service_name = ?"

get_preceeded_services = "SELECT CONCAT('TR# ', service_preceeding_schedule.transaction_uid),\
                             transaction_record.client_name,\
                             services_transaction_content.patient_name,\
                             CONCAT(services_transaction_content.service_name, ' ', coalesce(prefix, '')),\
                             'Paid',\
                             DATE_FORMAT(service_preceeding_schedule.scheduled_date, '%M %d, %Y')\
                         FROM service_preceeding_schedule\
                         LEFT JOIN transaction_record\
                             ON service_preceeding_schedule.transaction_uid = transaction_record.transaction_uid\
                         LEFT JOIN services_transaction_content\
                             ON service_preceeding_schedule.transaction_uid = services_transaction_content.transaction_uid\
                         WHERE service_preceeding_schedule.scheduled_date = CURRENT_DATE\
                            AND service_preceeding_schedule.status = 0\
                         ORDER BY service_preceeding_schedule.scheduled_date"

mark_preceeding_as_done = "UPDATE service_preceeding_schedule SET status = 1 WHERE transaction_uid = ? AND scheduled_date = ? "
add_preceeding_schedule = "INSERT INTO service_preceeding_schedule (transaction_uid, service_uid, service_name, prefix, scheduled_date, status) VALUES (?, ?, ?, ?, ?, 0)"
get_item_does_expiry = f"SELECT item_uid, categories.does_expire From recieving_item\
                        JOIN item_general_info ON recieving_item.item_uid = item_general_info.UID\
                        JOIN categories ON item_general_info.Category = categories.categ_name\
                        WHERE id = ?"
                        
get_supplier_items = "SELECT supplier_item_info.item_id, item_general_info.brand, item_general_info.name, item_general_info.unit\
                        FROM supplier_item_info\
                        JOIN item_general_info ON supplier_item_info.item_id = item_general_info.UID\
                        WHERE supplier_id = ?  AND active = 1"
                        
set_supplier_items = "INSERT INTO supplier_item_info VALUES (?,?,1)"

get_item_supplier_name = "SELECT  supp_name FROM supplier_item_info\
                            LEFT JOIN supplier_info ON supplier_info.supp_id = supplier_item_info.supplier_id\
                            WHERE supplier_item_info.item_id = ?"
                
update_expired_items = "UPDATE item_inventory_info SET state = -1 WHERE Expiry_Date <= CURRENT_DATE"

get_expired_items_to_dispose = "SELECT item_general_info.UID, item_general_info.name, item_general_info.unit,\
                                CAST(SUM(Stock) as INT) from item_inventory_info\
                                JOIN item_general_info ON item_general_info.UID = item_inventory_info.UID\
                                WHERE Expiry_Date <= CURRENT_DATE AND state = 1\
                                GROUP BY item_inventory_info.UID"
                                
set_expired_items_from_inventory = "INSERT INTO disposal_history (id, receive_id, item_uid, item_name, initial_quantity, reason, date_of_disposal, disposed_by)\
                                    VALUES (?, ?, ?, ?, ?, ?, CURRENT_DATE, ?)"
                                    
update_supplier_item_info_deactive = "UPDATE supplier_item_info SET active = 0\
                                    WHERE supplier_id = ? and item_id = ? "

update_supplier_item_info_active = "UPDATE supplier_item_info SET active = 1\
                                    WHERE supplier_id = ? and item_id = ? "

get_supplier_item_info_if_exist = "SELECT COUNT(1) FROM supplier_item_info\
                                    WHERE supplier_id = ? AND item_id = ?"

get_supplier_audit_trail = "SELECT created_by, CAST(date_added AS DATE), updated_by, CAST(date_modified AS DATE) FROM supplier_info\
                            WHERE supp_id = ?"
                            
get_out_of_stock_names = "SELECT item_general_info.name\
                          FROM item_general_info\
                          JOIN item_inventory_info \
                              ON item_general_info.UID = item_inventory_info.UID\
                          WHERE item_inventory_info.Stock = 0\
                          GROUP BY item_general_info.UID"

get_low_items_name = "SELECT item_general_info.name,\
                             SUM(item_inventory_info.Stock) AS price,\
                             item_settings.Reorder_factor,\
                             item_settings.Safe_stock,\
                             item_settings.Crit_factor\
                             FROM item_inventory_info\
                      JOIN item_general_info \
                            ON item_inventory_info.UID = item_general_info.UID\
                      JOIN item_settings\
                            ON item_inventory_info.UID = item_settings.UID\
                      WHERE item_inventory_info.Expiry_Date > CURRENT_DATE OR item_inventory_info.Expiry_Date IS null\
                      GROUP BY item_general_info.UID\
                      HAVING price BETWEEN 1 AND item_settings.Safe_stock * item_settings.Reorder_factor;"

get_expired_items_name = "SELECT item_general_info.name, SUM(item_inventory_info.Stock)\
                                  FROM item_inventory_info\
                          JOIN item_general_info \
                                  ON item_inventory_info.UID = item_general_info.UID\
                          JOIN item_settings\
                                  ON item_inventory_info.UID = item_settings.UID\
                          WHERE item_inventory_info.Expiry_Date <= CURRENT_DATE\
                          GROUP BY item_general_info.UID"

get_near_expired_items_name = "SELECT item_general_info.name,\
                                      SUM(item_inventory_info.Stock),\
                                      DATEDIFF(item_inventory_info.Expiry_Date, current_date)\
                               FROM item_inventory_info\
                               JOIN item_general_info\
                                       ON item_inventory_info.UID = item_general_info.UID\
                               JOIN item_settings\
                                       ON item_inventory_info.UID = item_settings.UID\
                               WHERE DATE_SUB(item_inventory_info.Expiry_Date, INTERVAL ? DAY) <= CURRENT_DATE\
                                       AND NOT item_inventory_info.Expiry_Date <= current_date\
                               GROUP BY item_general_info.UID"

get_scheduled_clients_today_names = "SELECT service_name, patient_name from services_transaction_content\
                                     WHERE scheduled_date = current_date"

get_past_scheduled_clients_names = "SELECT service_name, patient_name from services_transaction_content\
                                     WHERE scheduled_date < current_date"

get_past_scheduled_clients_names = "SELECT service_name, patient_name from services_transaction_content\
                                     WHERE scheduled_date < current_date"

get_near_scheduled_clients_names = "SELECT service_name,\
                                    patient_name,\
                                    DATEDIFF(current_date, DATE_sub(scheduled_date, INTERVAL ? DAY))\
                                    from services_transaction_content\
                                    WHERE DATE_sub(scheduled_date, INTERVAL ? DAY) <= current_date\
                                        AND scheduled_date != current_date"
                          
get_on_order_items = "SELECT item_general_info.brand, recieving_item.NAME, recieving_item.current_stock\
                        FROM recieving_item\
                        JOIN item_general_info ON recieving_item.item_uid = item_general_info.UID\
                        WHERE state = 1"

get_on_pending_items = "SELECT item_general_info.brand, recieving_item.NAME, recieving_item.current_stock\
                        FROM recieving_item\
                        JOIN item_general_info ON recieving_item.item_uid = item_general_info.UID\
                        WHERE state = 3"

get_all_schedule = "SELECT CONCAT('TR# ', service_preceeding_schedule.transaction_uid),\
                                                transaction_record.client_name,\
                                                services_transaction_content.patient_name,\
                                                CONCAT(services_transaction_content.service_name, ' ', coalesce(prefix, '')),\
                                                'Paid',\
                                                DATE_FORMAT(service_preceeding_schedule.scheduled_date, '%M %d, %Y') AS shceduled_date\
                                            FROM service_preceeding_schedule\
                                            LEFT JOIN transaction_record\
                                                ON service_preceeding_schedule.transaction_uid = transaction_record.transaction_uid\
                                            LEFT JOIN services_transaction_content\
                                                ON service_preceeding_schedule.transaction_uid = services_transaction_content.transaction_uid\
                                                AND service_preceeding_schedule.status = 0\
                    UNION ALL\
                    SELECT invoice_record.invoice_uid,\
                                                    invoice_record.client_name,\
                                                    invoice_service_content.patient_name,\
                                                    CONCAT(invoice_service_content.service_name, case when service_info_test.duration_type != 0 then ' (Initial)' ELSE '' END),\
                                                    CONCAT('₱', FORMAT(invoice_record.Total_amount, 2)) AS price,\
                                                    DATE_FORMAT(invoice_record.transaction_date, '%M %d, %Y') AS date\
                                                FROM invoice_record\
                                                LEFT JOIN invoice_service_content\
                                                    ON invoice_record.invoice_uid = invoice_service_content.invoice_uid\
                                                LEFT JOIN invoice_item_content\
                                                    ON invoice_record.invoice_uid = invoice_item_content.invoice_uid\
                                                LEFT JOIN service_info_test\
                                                    ON invoice_service_content.service_name = service_info_test.service_name\
                                                WHERE invoice_record.State = 0\
                                                    AND process_type = 1\
                                                GROUP BY invoice_record.invoice_uid\
                    ORDER BY shceduled_date"

get_updated_avg_of_old_statistics = "SELECT item_general_info.UID,\
                                         avg((COALESCE(item_transaction_content.quantity, 0))),\
                                         case when item_statistic_info.monthly_average < SUM(case when MONTH(transaction_record.transaction_date) = MONTH(CURRENT_DATE)\
                                                                                                                         then item_transaction_content.quantity ELSE 0 END)\
                                                         then 'u'\
                                                     when item_statistic_info.monthly_average = 0 AND SUM(case when MONTH(transaction_record.transaction_date) = MONTH(CURRENT_DATE)\
		 																		 			  then item_transaction_content.quantity ELSE 0 END) = 0\
                                                         then 'd'\
                                                     when item_statistic_info.monthly_average = 0\
                                                         OR round(item_statistic_info.monthly_average) = SUM(case when MONTH(transaction_record.transaction_date) = MONTH(CURRENT_DATE)\
                                                                                                                                 then item_transaction_content.quantity ELSE 0 END)\
                                                         then 'm'\
                                                     ELSE 'd' END\
                                     FROM item_general_info\
                                     INNER JOIN item_transaction_content\
                                         ON item_general_info.UID = item_transaction_content.Item_uid\
                                     INNER JOIN item_statistic_info\
                                         ON item_general_info.UID = item_statistic_info.UID\
                                     LEFT JOIN transaction_record\
                                         ON item_transaction_content.transaction_uid = transaction_record.transaction_uid\
                                     WHERE item_statistic_info.`month` != ?\
                                     GROUP BY item_general_info.UID;"

update_statistics_info = "UPDATE item_statistic_info\
                          SET month = MONTH(CURRENT_DATE),\
                              monthly_average = ?,\
                              rate_symbol = ?\
                          WHERE UID = ?"

get_rescheduling_info_invoice_by_id = "SELECT invoice_service_content.invoice_uid,\
                                               invoice_service_content.patient_name,\
                                               invoice_service_content.service_name,\
                                               CONCAT('₱', FORMAT(invoice_service_content.price, 2)),\
                                               pet_owner_info.owner_name,\
                                               pet_owner_info.contact_number,\
                                               DATE_FORMAT(invoice_record.transaction_date, '%M %d, %Y'),\
                                               invoice_service_content.scheduled_date\
                                       FROM invoice_service_content\
                                       JOIN invoice_record\
                                           ON invoice_service_content.invoice_uid = invoice_record.invoice_uid\
                                       INNER JOIN pet_info\
                                           ON invoice_service_content.pet_uid = pet_info.id\
                                       INNER JOIN pet_owner_info\
                                           ON pet_info.owner_id = pet_owner_info.owner_id\
                                       WHERE invoice_service_content.invoice_uid = ?"

get_rescheduling_info_preceeding_by_id = "SELECT service_preceeding_schedule.transaction_uid,\
                                                  pet_info.p_name,\
                                                  CONCAT(service_preceeding_schedule.service_name, ' (', service_preceeding_schedule.prefix, ')'),\
                                                  'Paid',\
                                                  pet_owner_info.owner_name,\
                                              pet_owner_info.contact_number,\
                                              DATE_FORMAT(transaction_record.transaction_date, '%M %d, %Y'),\
                                              service_preceeding_schedule.scheduled_date\
                                          FROM service_preceeding_schedule\
                                          JOIN services_transaction_content\
                                              ON service_preceeding_schedule.transaction_uid = services_transaction_content.transaction_uid\
                                          INNER JOIN transaction_record\
                                              ON service_preceeding_schedule.transaction_uid = transaction_record.transaction_uid\
                                          INNER JOIN pet_info\
                                              ON services_transaction_content.pet_uid = pet_info.id\
                                          INNER JOIN pet_owner_info\
                                              ON pet_info.owner_id = pet_owner_info.owner_id\
                                          WHERE service_preceeding_schedule.transaction_uid = ?"

set_replacement_record = "INSERT INTO replacement_record VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)"
set_replacement_items = "INSERT INTO replacement_items VALUES (? , ?, ?, ?, ?, ?)"
update_transaction_record_to_replaced = "UPDATE transaction_record SET Total_amount = ?, transaction_date = CURRENT_DATE, state = '2' WHERE transaction_uid = ?"

update_item_transaction_content_to_replaced = "UPDATE item_transaction_content SET state = 2 WHERE transaction_uid = ?"

get_item_total_by_id = "SELECT CAST(SUM(item_transaction_content.price * item_transaction_content.quantity) AS FLOAT)\
                        FROM item_transaction_content Where transaction_uid = ?  and state = 1"
                        
get_service_total_by_id = "SELECT Cast(SUM(price) AS FLOAT) FROM services_transaction_content WHERE transaction_uid = ?"
get_transaction_total_by_id = "SELECT Total_amount FROM transaction_record WHERE transaction_uid = ? and state = 1"
    
