from src.views import main_info
from src.services import anylize_cashback
from src.utils import get_time_for_greeting, get_data_time, get_path_and_period
from src.views import main_info

if __name__ == "__main__":
    data_request = "2019-04-10 15:30:00"
    result_view = main_info(data_request)
    #print(result_view)

    result_services = anylize_cashback("../data/operations.xlsx", 2018, 4)
    print(result_services)
