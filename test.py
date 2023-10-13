from util import *
import sql_commands
import math

sample_data = database.fetch_data(sql_commands.get_sales_record_raw)

def matched_result(source: list, reference: list):
    return [data for res in source for data in reference if set(res).issubset(data)]