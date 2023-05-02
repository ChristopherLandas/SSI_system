get_inventory_by_group = f"SELECT item_general_info.name,\
                                  CAST(SUM(item_inventory_info.Stock) AS INT) AS stocks,\
                                  item_settings.Price,\
                                  DATE_FORMAT(item_inventory_info.Expiry_Date, '%Y-%m-%d') AS expiry,\
                                  case when SUM(item_inventory_info.Stock) < item_settings.Safe_stock * item_settings.Crit_factor\
                                      then 'Critical'\
                                  when SUM(item_inventory_info.Stock) < item_settings.Safe_stock * item_settings.Reorder_factor\
                                      then 'Reorder'\
                                      ELSE 'Normal' END AS stats\
                          FROM item_general_info\
                          JOIN item_inventory_info ON item_general_info.UID = item_inventory_info.UID\
                          INNER JOIN item_settings ON item_general_info.UID = item_settings.UID\
                          GROUP BY item_general_info.name\
                          ORDER BY item_general_info.UID"

add_stock_with_different_expiry = 'INSERT INTO item_inventory_info VALUES (?, ?, ?)'

update_non_expiry_stock = "UPDATE item_inventory_info SET Stock = STOCK + ? WHERE UID = ? AND Expiry_Date IS NULL"
update_expiry_stock = "SET Stock = STOCK + ? WHERE UID = ? AND .Expiry_Date = ?"
add_new_instance = "INSERT INTO item_inventory_info VALUES (?, ?, ?)"