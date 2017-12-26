import cs50
import sys

# Main function
def main():
    # check correct number of arguments
    if len(sys.argv) != 2:
        print("Usage: python caesar.py k")
        exit(1)
    # assign the 2nd arguement as key
    k = int(sys.argv[1])
    # get plaintext from user
    print("plaintext: ", end = "")
    s = cs50.get_string();
    # pass string and key to a function that ciphers it
    print("ciphertext: ", end = "")
    print_cipher(k, s)
    return 0

def print_cipher(key, string):
    for c in string:
        # if i'th char is a letter
        if c.isalpha():
            # if is lower case
            if c.islower():
                print(chr(((ord(c) - 97 + key) % 26) + 97), end = "")
            # if is upper case
            else:
                print(chr(((ord(c) - 65 + key) % 26) + 65), end = "")
        # else just print the character
        else:
            print("{}".format(c), end = "")
    # print newline
    print("")


if __name__ == "__main__":
    main()