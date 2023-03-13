import multiprocessing
import time
import copy

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

    def find_all_combinations(
            self,
            purchase_limit: int,
            current_sum: int,
            stock_price_dict: dict,
            price_dict_result: dict = None,
            stock_name_list_result: list = None,
            output: list = None
    ):
        price_dict_result = price_dict_result if price_dict_result else {}
        stock_name_list_result = stock_name_list_result if stock_name_list_result else []
        output = output if output else []

        if not stock_price_dict:
            output.append(copy.copy(stock_name_list_result))

        for key, value in stock_price_dict.items():
            if current_sum + value < purchase_limit:
                temp_sum = current_sum + value
                print(key + " - " + str(value))
                print(type(price_dict_result))
                price_dict_result[key] = value
                stock_name_list_result.append(key)
                remaining_dict = stock_price_dict.copy()
                for key2, value2 in remaining_dict.items():
                    print("remaining dict")
                    print(key2 + " - " + str(value2))
                del remaining_dict[key]
                remaining_possible_stocks = {
                    key: value for key, value in remaining_dict.items() if value < (purchase_limit - current_sum)}
                self.find_all_combinations(
                    purchase_limit,
                    temp_sum,
                    remaining_possible_stocks,
                    price_dict_result,
                    output
                )
                del price_dict_result[key]

        print(f" output: {output}")

    def optimized_calculation(
            self,
            purchase_limit: int,
            current_sum: int,
            stock_index: int,
            stock_names_list: list,
            stock_price_list: list,
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
                :param current_sum: ongoing sum of prices
                :type current_sum: int
                :param stock_index: stock position for which we try all purchase options
                :type stock_index: int
                :param stock_names_list: all stock names
                :type stock_names_list: list
                :param stock_price_list: all stock prices
                :type stock_price_list: list
                :param stocks_dict: all stock data
                :type stocks_dict: dict
                :param purchase_list: ongoing list of purchases
                :type purchase_list: list
                :return: best purchase list
                :rtype: list
                """
        # Declaration of best list variable that will stock the best solution found by the algo
        # Empty list if not provided
        best_list = best_list if best_list else [0] * len(stock_price_list)
        best_gain = self.common_functions.calculate_total_gain(stock_names_list, stocks_dict, best_list)

        purchase_list = purchase_list if purchase_list else [1] * len(stock_price_list)

        # Declaration of the remaining limit value
        total_cost = self.common_functions.calculate_total_cost(
            purchase_list, stock_names_list, stocks_dict
        )

        if not stock_price_list:
            output.append(copy.copy(result))

        for price in stock_price_list:
            temp_sum = current_sum + price


        # We test all purchases quantity options possible in the remaining purchase limit
        max_range = min(int((total_cost - purchase_limit) / stock_price_list[stock_index] + 1), 2)
        for purchase_quantity in reversed(range(0, max_range)):
            # We update the purchases quantity in the purchase list position of the given stock
            purchase_list[stock_index] = purchase_quantity

            # We update the remaining limit based on the ongoing quantity purchase test
            total_cost = self.common_functions.calculate_total_cost(
                purchase_list, stock_names_list, stocks_dict
            )

            # if we come below the purchase limit, then we calculate the gain and compare
            # it to the best gain obtained
            if total_cost < purchase_limit:
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
            print(best_list)
            # print(best_gain)
            # print(purchase_list)
            # print(remaining_limit)

        # We set the stock purchase quantity back to initial value in order to test over
        purchase_list[stock_index] = 1

        return best_list

    def run_optimized(self):
        dict_stocks = self.common_functions.csv_to_dict(self.common_functions.DATASET_FILE)
        dict_stocks_sorted = self.sort_dict_by_gain(dict_stocks)
        stock_names_list = self.common_functions.stock_dict_to_stock_name_list(dict_stocks_sorted)
        best_list = self.optimized_calculation(
            500,
            0,
            stock_names_list,
            dict_stocks_sorted
        )
        print(stock_names_list)
        print(best_list)
        best_gain = self.common_functions.calculate_total_gain(stock_names_list, dict_stocks_sorted, best_list)
        print(best_gain)
        return best_list


def main():
    # save start time
    start_time = time.time()

    # Initialize controllers
    common_functions = CommonFunctions()
    optimized_calculation = Optimized(common_functions)

    # Start run as a process
    p = multiprocessing.Process(target=optimized_calculation.run_optimized, name="run_optimized")
    p.start()

    # Wait x seconds for the process
    # time.sleep(10)
    p.join(3)

    # Terminate foo
    if p.is_alive():
        print("foo is running... let's kill it...")

        # Terminate foo
        p.terminate()
        p.join()

    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    # main()
    common_functions = CommonFunctions()
    optimized_calculation = Optimized(common_functions)
    dict_stocks = common_functions.csv_to_dict(common_functions.DATASET_FILE)
    dict_stocks_sorted = optimized_calculation.sort_dict_by_gain(dict_stocks)
    stock_names_list = common_functions.stock_dict_to_stock_name_list(dict_stocks_sorted)
    stock_price_dict = common_functions.get_price_dict(dict_stocks_sorted)
    optimized_calculation.find_all_combinations(500, 0, stock_price_dict, None, [], [])
