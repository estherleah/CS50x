import cs50

# Main function
def main():
    # prompt for input
    while True:
        print("How much change is owed? ", end="")
        change = cs50.get_float();
        if change >= 0:
            break

    # declare variables
    quarter = 25
    dime = 10
    nickel = 5
    penny = 1
    total = 0

    # calculate change
    cents = change * 100
    while cents >= quarter:
        cents = cents - quarter
        total += 1
    while cents >= dime:
        cents = cents - dime
        total += 1
    while cents >= nickel:
        cents = cents - nickel
        total += 1
    while cents >= penny:
        cents = cents - penny
        total += 1

    # return output
    print("{}".format(total))


if __name__ == "__main__":
    main()