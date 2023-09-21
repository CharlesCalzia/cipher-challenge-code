from bs4 import BeautifulSoup as bs4
import requests
import sys
import time
import os

path = os.path.dirname(os.path.realpath(__file__))


def inputs():
    symbols = [
        ",",
        "",
        "£",
        "!",
        "$",
        "*",
        "&",
        "%",
        "@",
        "{",
        "<",
        ">",
        ";",
        ":",
        "}",
        "[",
        "]",
        "^",
        "'",
        " ",
        "-",
        "?",
        "=",
        "(",
        ")",
        "`",
        "’",
        "\\",
        " ",
        "_",
        ".",
        "\n",
        "\t",
    ]
    ciphertext = ""

    def cipher_chal_get(
        chal,
    ):  # Gets the ciphertext from cipher challenge site, according to the specified challenge
        link = f"https://www.cipherchallenge.org/challenge/challenge-{str(int(chal))}"
        print(link)
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
        }  # Headers needed for cipher challenge site, else rejected
        page = requests.get(link, headers=headers)
        soup = bs4(page.text, "html.parser")
        x = soup.findAll(
            "div", {"class": "challenge__content"}
        )  # two divs with the classes challenge_content: challenge a, challenge b
        c1 = x[0].text
        c2 = x[1].text
        return c1, c2

    ## INPUT

    x = input(
        "Enter mode for input (1 = manual, 2 = cipher challenge webscrape, 3 = read from file): "
    )

    if x == "1":  # Manual
        print("Enter text to decode: ")
        input0 = sys.stdin.readlines()  # Allows multiple lines of input

        input0 = [(i.lower()).strip() for i in input0]
        for item in input0:
            ciphertext += item
        ciphertext = " ".join(ciphertext.splitlines())

    elif x == "2":  # Webscrape
        x = input("Enter cipher challenge number: ")
        c1, c2 = cipher_chal_get(x)
        with open(path + "/challenge1.txt", "w+") as file:  # save ciphertext to file
            file.write(c1)
        with open(path + "/challenge2.txt", "w+") as file:
            file.write(c2)
        print("\n", c1, "\n\n")
        print(c2, "\n\n")
        c1_c2 = input("Enter which cipher to break: ")
        if c1_c2 == "1":
            ciphertext = c1
        elif c1_c2 == "2":
            ciphertext = c2

    elif x == "3":  # Read ciphertext from file
        c1 = input("Enter challenge: ")
        with open(path + "/challenge" + c1 + ".txt", "r") as file:
            x = "".join([i.strip() for i in file.readlines()])
            ciphertext = x

    else:
        quit()

    # Puts all ciphertext in lower case and removes all symbols, new lines, spaces... (which could cause problems in decryption and are not really necessary)
    ciphertext = ciphertext.lower()
    for i in symbols:
        ciphertext = ciphertext.replace(i, "")

    print("Ciphertext: ", ciphertext)

    return ciphertext
