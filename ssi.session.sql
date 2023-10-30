SELECT item_general_info.brand, item_general_info.name, item_general_info.unit,
                                         CAST(SUM(item_inventory_info.Stock) as INT),   
                                         CONCAT('₱', FORMAT((item_settings.Cost_Price * (item_settings.Markup_Factor + 1)), 2))   
                                 FROM item_general_info JOIN item_inventory_info ON item_general_info.UID = item_inventory_info.UID   
                                 INNER	JOIN item_settings ON item_general_info.UID = item_settings.UID   
                                 WHERE item_inventory_info.Stock != 0 AND (item_inventory_info.Expiry_Date > CURRENT_DATE OR item_inventory_info.Expiry_Date IS null)   
                                 GROUP BY item_general_info.UID