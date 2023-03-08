from bruteforce import CommonFunctions

class Optimized:
    def __init__(self, common_functions: CommonFunctions):
        self.common_functions = common_functions

    def optimized_calculation(self):


def main():
    common_functions = CommonFunctions()
    optimized_calculation = Optimized(common_functions)
    dict_stocks = common_functions.csv_to_dict(common_functions.DATASET_FILE)
    stock_names_list = common_functions.stock_dict_to_stock_name_list(dict_stocks)
    purchase_list = [0] * len(stock_names_list)
    best_list = optimized_calculation.optimized_calculation()
    print(best_list)


if __name__ == "__main__":
    main()