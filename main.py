from currency.currency import CurrencyConverter


def get_user_inputs():
    from_country = raw_input("Enter a country to convert from: ")
    to_country = raw_input("Enter a country to convert to: ")
    amount = raw_input("Enter an amount to convert: ")
    return (from_country, to_country, int(amount))


def run_conversion():
    from_country, to_country, amount = get_user_inputs()
    c = CurrencyConverter(from_country, to_country, amount)
    conversion = c.convert()
    print "{} moneys in {} converts to {} moneys in {}".format(
        amount, from_country, str(conversion), to_country)


def check_continue():
    cont = raw_input("Do you want to continue? y/n ")
    if cont is 'y':
        return True
    if cont is 'n':
        return False
    else:
        print("Please enter y or n\n")


def main():
    run = True
    while run:
        run_conversion()
        run = check_continue()

if __name__ == '__main__':
    main()
