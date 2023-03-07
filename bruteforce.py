import csv

DATASET_FILE = "test_datasets/dataset0.csv"


def csv_to_dict(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        dict_stocks = {}
        for line in reader:
            dict_stocks[line['Action']] = {'Cout': line['Cout'], 'Benefice': line['Benefice']}
        return dict_stocks


def stock_dict_to_stock_name_list(stock_dict: dict) -> list:
    return list(stock_dict.keys())


def get_stock_price(stock_name: str, stock_dict: dict) -> int:
    return int(stock_dict[stock_name]['Cout'])


def get_stock_predicted_gain(stock_name: str, stock_dict: dict) -> int:
    return int(stock_dict[stock_name]['Benefice'])


def get_stock_name(stock_index: int, stock_names_list: list) -> str:
    return stock_names_list[stock_index]


def calculate_stock_gain(quantity: int, stock_name: str, stock_dict: dict) -> int:
    stock_price = get_stock_price(stock_name, stock_dict)
    stock_gain = get_stock_predicted_gain(stock_name, stock_dict)
    return quantity * stock_price * stock_gain


def calculate_total_gain(purchase_list: list, stock_names_list: list, stocks_dict: dict) -> int:
    gain = 0
    for purchase_index in range(len(purchase_list)):
        stock_name = stock_names_list[purchase_index]
        gain += calculate_stock_gain(purchase_list[purchase_index], stock_name, stocks_dict)
    return gain


def brute_force_calculation(
        purchase_limit: int,
        stock_index: int,
        stock_names_list: list,
        stocks_dict: dict,
        purchase_list: list = [0] * 20
):
    best_gain = 0
    best_list = []
    stock_name = get_stock_name(stock_index, stock_names_list)
    stock_price = get_stock_price(stock_name, stocks_dict)
    for purchase_quantity in range(int(purchase_limit/stock_price)):
        if purchase_limit > stock_price:
            print(purchase_limit)
            print(int(purchase_limit / stock_price))
            purchase_list[stock_index] = purchase_quantity
            print(f"purchase list {purchase_list}")
            purchase_amount = purchase_quantity * stock_price
            purchase_limit -= purchase_amount
            if stock_index < len(stock_names_list) - 1:
                stock_index += 1
                print(f"stock index {stock_index}")
                brute_force_calculation(
                    purchase_limit=purchase_limit,
                    stock_index=stock_index,
                    stock_names_list=stock_names_list,
                    purchase_list=purchase_list,
                    stocks_dict=stocks_dict
                )
            else:
                current_gain = calculate_total_gain(purchase_list, stock_names_list, stocks_dict)
                if current_gain > best_gain:
                    best_gain = current_gain
                    best_list = purchase_list.copy()
    print(f"best list {best_list}")
    print(f"best gain {best_gain/100}")


def main():
    dict_stocks = csv_to_dict(DATASET_FILE)
    stock_names_list = stock_dict_to_stock_name_list(dict_stocks)
    brute_force_calculation(500, 0, stock_names_list, dict_stocks)


if __name__ == "__main__":
    main()
