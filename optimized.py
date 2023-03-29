import tracemalloc
import time

from operator import getitem
from collections import OrderedDict

from bruteforce import CommonFunctions


class Optimized:
    def __init__(self, common_functions: CommonFunctions):
        self.common_functions = common_functions

    @staticmethod
    def sort_dict_by_gain(stocks_dict: dict) -> dict:
        """
        Sorts a dictionary by gain values
        :param stocks_dict: all stocks to be sorted by gain
        :type stocks_dict: dict
        :return: stocks dict sorted by gain
        :rtype: dict
        """
        return OrderedDict(sorted(stocks_dict.items(), key=lambda x: getitem(x[1], 'Benefice'), reverse=True))

    def optimized_calculation(
            self,
            purchase_limit: int,
            stock_names_list: list,
            stocks_dict: dict) -> list:
        """
                Calculates the best purchase option for a given limit and a given list of stock prices and expected gains
                :param purchase_limit: maximum amount to be expended in stock purchases
                :type purchase_limit: int
                :param stock_names_list: all stock names
                :type stock_names_list: list
                :param stocks_dict: all stock data
                :type stocks_dict: dict
                :return: nothing
                :rtype:
                """

        shortlist = []

        for stock_index in range(len(stock_names_list)):
            stock_name = self.common_functions.get_stock_name(stock_index, stock_names_list)
            stock_price = self.common_functions.get_stock_price(stock_name, stocks_dict)
            remaining_limit = self.common_functions.calculate_remaining_limit(purchase_limit, shortlist, stocks_dict)
            if remaining_limit > stock_price:
                shortlist.append(stock_name)
            else:
                pass
        return shortlist

    def run_optimized(self):
        tracemalloc.start()

        # save start time
        start_time = time.time()

        # Modifier ici la valeur du dataset à utiliser
        dict_stocks = self.common_functions.csv_to_dict(self.common_functions.DATASET_FILE0)
        dict_stocks_sorted = self.sort_dict_by_gain(dict_stocks)
        stock_names_list = self.common_functions.stock_dict_to_stock_name_list(dict_stocks_sorted)
        print("--- %s seconds de triage ---" % (time.time() - start_time))

        # save start time
        start_time2 = time.time()

        best_shortlist = self.optimized_calculation(
            50000,
            stock_names_list,
            dict_stocks_sorted
        )

        print("--- %s seconds de recherche de solution---" % (time.time() - start_time2))

        # print(stock_names_list)
        # print(best_list)
        best_gain = self.common_functions.calculate_total_gain(best_shortlist, dict_stocks_sorted)
        total_cost = self.common_functions.calculate_total_cost(best_shortlist, dict_stocks)
        print(f"best gain {best_gain}")
        print(f"total cost {total_cost/100}")
        print(best_shortlist)

        print("--- %s seconds au total---" % (time.time() - start_time))

        current, peak = tracemalloc.get_traced_memory()
        print(f"{round(peak / 1000):,} ko".replace(",", " "))

def main():
    # Initialize controllers
    common_functions = CommonFunctions()
    optimized_calculation = Optimized(common_functions)

    # Run optimized
    optimized_calculation.run_optimized()


if __name__ == "__main__":
    main()
