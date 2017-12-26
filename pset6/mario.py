import cs50

# Main function
def main():
    # prompt for input
    while True:
        print("Height: ", end="")
        height = cs50.get_int()
        if height >= 0 and height <= 23:
            break
    # return output
    for i in range (height):
        for j in range (height - i - 1):
            print(" ", end="")
        for k in range (height, height - i - 1, -1):
            print ("#", end="")
        print (" ", end="")
        for k in range (height, height - i - 1, -1):
            print ("#", end="")
        print("")

if __name__ == "__main__":
    main()