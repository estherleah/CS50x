import cs50
import sys

# Main function
def main():
    # check correct number of arguments
    if len(sys.argv) != 2:
        print("Usage: python vigenere.py k")
        exit(1)
    # check argument is string
    if sys.argv[1].isalpha() == False:
        print("Usage: python vigenere.py k")
        exit(1)
    # assign the 2nd arguement as key
    k = sys.argv[1]
    # get plaintext from user
    print("plaintext: ", end = "")
    s = cs50.get_string();
    # pass string and key to a function that ciphers it
    print("ciphertext: ", end = "")
    print_cipher(k, s)
    return 0

def print_cipher(key, string):
    # set j to 0
    j = 0
    for c in string:
        # if i'th char is a letter
        if c.isalpha():
            # work out k
            k = ord(key[j].lower()) - 97
            # increment j
            j += 1
            if j == len(key):
                j = 0
            # if is lower case
            if c.islower():
                print(chr(((ord(c) - 97 + k) % 26) + 97), end = "")
            # if is upper case
            else:
                print(chr(((ord(c) - 65 + k) % 26) + 65), end = "")
        # else just print the character
        else:
            print("{}".format(c), end = "")
    # print newline
    print("")


if __name__ == "__main__":
    main()