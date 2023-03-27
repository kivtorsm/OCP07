import multiprocessing
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
            stock_index: int,
            stock_names_list: list,
            stocks_dict: dict,
            purchase_list: list = None,
            best_list: list = None
    ) -> list:
        """
                Calculates the best purchase option for a given limit and a given list of stock prices and expected gains
                :param best_list: takes into account the last bast_list found so far. Empty if not declared.
                :type best_list: list
                :param purchase_limit: maximum amount to be expended in stock purchases
                :type purchase_limit: int
                :param stock_index: stock position for which we try all purchase options
                :type stock_index: int
                :param stock_names_list: all stock names
                :type stock_names_list: list
                :param stocks_dict: all stock data
                :type stocks_dict: dict
                :param purchase_list: ongoing list of purchases
                :type purchase_list: list
                :return: nothing
                :rtype:
                """
        # Declaration of best list variable that will stock the best solution found by the algo
        # Empty list if not provided
        best_list = best_list if best_list else [0] * len(stock_names_list)
        best_gain = self.common_functions.calculate_total_gain(stock_names_list, stocks_dict, best_list)

        purchase_list = purchase_list if purchase_list else [0] * len(stock_names_list)

        # Declaration of the remaining limit value
        remaining_limit = self.common_functions.calculate_remaining_limit(
            purchase_limit, purchase_list, stock_names_list, stocks_dict)

        # print(f"remaining limit {remaining_limit}")

        # Save stock name and value for a given iteration
        stock_name = self.common_functions.get_stock_name(stock_index, stock_names_list)
        stock_price = self.common_functions.get_stock_price(stock_name, stocks_dict)

        # We test all purchases quantity options possible in the remaining purchase limit
        max_range = min(int(remaining_limit / stock_price + 1), 2)
        for purchase_quantity in reversed(range(0, max_range)):
            # We update the purchases quantity in the purchase list position of the given stock
            purchase_list[stock_index] = purchase_quantity

            # We update the remaining limit based on the ongoing quantity purchase test
            remaining_limit = self.common_functions.calculate_remaining_limit(
                purchase_limit, purchase_list, stock_names_list, stocks_dict)
            total_cost = self.common_functions.calculate_total_cost(
                purchase_list, stock_names_list, stocks_dict
            )
            excess_purchase = total_cost - purchase_limit

            # if we come below the purchase limit, then we calculate the gain and compare
            # it to the best gain obtained
            if excess_purchase < 0:
                # Calculate best gain seen so far
                best_gain = self.common_functions.calculate_total_gain(
                    stock_names_list=stock_names_list,
                    stocks_dict=stocks_dict,
                    purchase_list=best_list
                )

                # Calculate current gain
                current_gain = self.common_functions.calculate_total_gain(
                    purchase_list=purchase_list,
                    stock_names_list=stock_names_list,
                    stocks_dict=stocks_dict
                )

                # If the current gain is better than the best found so far, we update
                # the best purchase list with the ongoing purchase test
                # print(f"current gain {current_gain}")
                # print(f"best gain {best_gain}")
                if current_gain > best_gain:
                    best_list = purchase_list.copy()

            # if we are not at then end of the list of stocks we recursively call the function
            if stock_index < len(stock_names_list) - 1:
                new_best_list = self.optimized_calculation(
                    purchase_limit=purchase_limit,
                    stock_index=stock_index + 1,
                    stock_names_list=stock_names_list,
                    purchase_list=purchase_list,
                    stocks_dict=stocks_dict,
                    best_list=best_list
                )
                new_best_gain = self.common_functions.calculate_total_gain(
                    purchase_list=new_best_list, stock_names_list=stock_names_list, stocks_dict=stocks_dict)
                if new_best_gain > best_gain:
                    best_list = new_best_list.copy()
                    best_gain = self.common_functions.calculate_total_gain(stock_names_list, stocks_dict, best_list)
                    total_cost = self.common_functions.calculate_total_cost(best_list, stock_names_list, stocks_dict)
                    return best_list
            # print(best_list)
            # print(best_gain)
            # print(total_cost)
            # print(purchase_list)
            # print(remaining_limit)

        # We set the stock purchase quantity back to initial value in order to test over
        purchase_list[stock_index] = 0

        return best_list

    def run_optimized(self):
        # save start time
        start_time = time.time()
        dict_stocks = self.common_functions.csv_to_dict(self.common_functions.DATASET_FILE1)
        dict_stocks_sorted = self.sort_dict_by_gain(dict_stocks)
        # for key, value in dict_stocks_sorted.items():
        #     print(f"{key} - {value}")
        stock_names_list = self.common_functions.stock_dict_to_stock_name_list(dict_stocks_sorted)
        print("--- %s seconds de triage ---" % (time.time() - start_time))

        # save start time
        start_time2 = time.time()

        best_list = self.optimized_calculation(
            50000,
            0,
            stock_names_list,
            dict_stocks_sorted
        )

        print("--- %s seconds de recherche de solution---" % (time.time() - start_time2))

        # print(stock_names_list)
        # print(best_list)
        best_gain = self.common_functions.calculate_total_gain(stock_names_list, dict_stocks_sorted, best_list)
        total_cost = self.common_functions.calculate_total_cost(best_list, stock_names_list, dict_stocks)
        purchase_stock_name_list = self.common_functions.purchase_list_to_stock_name_list(best_list, stock_names_list)
        print(f"best gain {best_gain}")
        print(f"total cost {total_cost/100}")
        print(purchase_stock_name_list)

        print("--- %s seconds au total---" % (time.time() - start_time))


def main():
    # Initialize controllers
    common_functions = CommonFunctions()
    optimized_calculation = Optimized(common_functions)

    # Run optimized
    optimized_calculation.run_optimized()


if __name__ == "__main__":
    main()
