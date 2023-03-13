import csv
import time


class CommonFunctions:

    DATASET_FILE = "test_datasets/dataset0.csv"

    @staticmethod
    def csv_to_dict(file_path: str) -> dict:
        """
        Transforms csv data into a dictionary
        :param file_path: path for the file to ve converted
        :type file_path: str
        :return: dictionary with csv file data
        :rtype: dict
        """
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            dict_stocks = {}
            for line in reader:
                dict_stocks[line['Action']] = {'Cout': int(line['Cout']), 'Benefice': int(line['Benefice'])}
            return dict_stocks

    @staticmethod
    def stock_dict_to_stock_name_list(stock_dict: dict) -> list:
        """
        Gets a list of stock names from a dict
        :param stock_dict: dictionary containing all stocks data
        :type stock_dict: dict
        :return: list of stock names
        :rtype: list
        """
        return list(stock_dict.keys())

    @staticmethod
    def get_price_dict(stock_dict: dict) -> dict:
        """
        Gets a list of stock names from a dict
        :param stock_dict: dictionary containing all stocks data
        :type stock_dict: dict
        :return: list of stock names
        :rtype: list
        """
        return dict({key: value['Cout'] for key, value in stock_dict.items()})

    @staticmethod
    def get_stock_price(stock_name: str, stock_dict: dict) -> int:
        """
        Gets the price of a given stock
        :param stock_name: name of the stock for which we want to obtain the price
        :type stock_name: str
        :param stock_dict: dictionary containing all stock data
        :type stock_dict: dict
        :return: price for the stock requested
        :rtype: int
        """
        return int(stock_dict[stock_name]['Cout'])

    @staticmethod
    def get_stock_predicted_gain(stock_name: str, stock_dict: dict) -> int:
        """
        Gets the predicted gain for a given stock
        :param stock_name: name of the stock for which we want to obtain a predicted gain
        :type stock_name: str
        :param stock_dict: dictionary containing all stocks data
        :type stock_dict: dict
        :return: expected gain in 2 years time
        :rtype: int
        """
        return int(stock_dict[stock_name]['Benefice'])

    @staticmethod
    def get_stock_name(stock_index: int, stock_names_list: list) -> str:
        """
        Gets the name of the stock in a given position in the list
        :param stock_index: index ou position du stock dans la liste
        :type stock_index: int
        :param stock_names_list: liste des noms des stocks
        :type stock_names_list: list
        :return: nom du stock
        :rtype: str
        """
        return stock_names_list[stock_index]

    def calculate_stock_gain(self, quantity: int, stock_name: str, stock_dict: dict) -> int:
        """
        Calculates stock for the purchase of a single stock value
        :param quantity: purchase quantity for the stock
        :type quantity: int
        :param stock_name: name of the stock being purchased
        :type stock_name: str
        :param stock_dict: dictionary containing all stock data
        :type stock_dict: dict
        :return: stock gain up to 2 numbers below 1
        :rtype: int
        """
        stock_price = self.get_stock_price(stock_name, stock_dict)
        stock_gain = self.get_stock_predicted_gain(stock_name, stock_dict)
        return quantity * stock_price * stock_gain

    def calculate_total_gain(self, stock_names_list: list, stocks_dict: dict, purchase_list: list = []) -> int:
        """
        Calculates total gains for a list of stocks purchases
        :param purchase_list: list of stocks purchases
        :type purchase_list: list
        :param stock_names_list: all names of stocks
        :type stock_names_list: list
        :param stocks_dict: dictionary containing all stocks data
        :type stocks_dict: dict
        :return: total gain obtained with the purchase list up to 2 numbers below 1
        :rtype: int
        """
        gain = 0
        for purchase_index in range(len(purchase_list)):
            stock_name = stock_names_list[purchase_index]
            gain += self.calculate_stock_gain(purchase_list[purchase_index], stock_name, stocks_dict)
        return gain

    def calculate_remaining_limit(
            self, initial_limit: int, purchase_list: list, stocks_names_list: list, stocks_dict: dict) -> int:
        """
        Calculates remaining purchase limit after a list of purchases. Initial limit - sum_all(stock_purchase * price)
        :param initial_limit: initial given limit for operations
        :type initial_limit: int
        :param purchase_list: list of stock purchases
        :type purchase_list: list
        :param stocks_names_list: all stocks names
        :type stocks_names_list: list
        :param stocks_dict: all stocks data
        :type stocks_dict: dict
        :return: remaining limit after purchases
        :rtype: int
        """
        total_cost = self.calculate_total_cost(purchase_list, stocks_names_list, stocks_dict)
        return initial_limit - total_cost

    @staticmethod
    def calculate_total_cost(purchase_list: list, stocks_names_list: list, stocks_dict: dict) -> int:
        """
        Calculates total cost of a series of purchases
        :param purchase_list: contains all purchases
        :type purchase_list: list
        :param stocks_names_list: all stock names
        :type stocks_names_list: list
        :param stocks_dict: all stock data
        :type stocks_dict: dict
        :return: total cost of all purchases
        :rtype: int
        """
        total_cost = 0
        for purchase_index in range(len(purchase_list)):
            total_cost += purchase_list[purchase_index] * int(stocks_dict[stocks_names_list[purchase_index]]['Cout'])
        return total_cost


class BruteForceCalculation:
    """
    Class containing the main Brute Force Calculation Function
    """

    def __init__(self, common_functions: CommonFunctions):
        self.common_functions = common_functions

    def brute_force_calculation(
            self,
            purchase_limit: int,
            stock_index: int,
            stock_names_list: list,
            stocks_dict: dict,
            purchase_list: list = None,
            best_list: list = None
    ):
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
        best_list = best_list if best_list else [0] * 20

        purchase_list = purchase_list if purchase_list else [0] * 20

        # Declaration of the remaining limit value
        remaining_limit = self.common_functions.calculate_remaining_limit(
                    purchase_limit, purchase_list, stock_names_list, stocks_dict)

        # Save stock name and value for a given iteration
        stock_name = self.common_functions.get_stock_name(stock_index, stock_names_list)
        stock_price = self.common_functions.get_stock_price(stock_name, stocks_dict)

        # We test all purchases quantity options possible in the remaining purchase limit
        for purchase_quantity in range(0, min(int(remaining_limit/stock_price + 1), 2)):
            # We update the purchases quantity in the purchase list position of the given stock
            purchase_list[stock_index] = purchase_quantity

            # We update the remaining limit based on the ongoing quantity purchase test
            remaining_limit = self.common_functions.calculate_remaining_limit(
                purchase_limit, purchase_list, stock_names_list, stocks_dict)

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
                new_best_list = self.brute_force_calculation(
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
            # print(best_list)
            # print(best_gain)
            # print(purchase_list)
            # print(remaining_limit)

        # We set the stock purchase quantity back to 0 in the purchase list in order to test over from zéro with
        # a higher previous index.
        purchase_list[stock_index] = 0

        # return best list
        return best_list


def main():
    common_functions = CommonFunctions()
    brute_force_calculation = BruteForceCalculation(common_functions)
    dict_stocks = common_functions.csv_to_dict(common_functions.DATASET_FILE)
    stock_names_list = common_functions.stock_dict_to_stock_name_list(dict_stocks)
    best_list = brute_force_calculation.brute_force_calculation(500, 0, stock_names_list, dict_stocks)
    print(best_list)
    print(stock_names_list)
    # print(common_functions.get_price_dict(dict_stocks))


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
