import inputs
import utils
import substitution
import quick_ciphers
import transposition
import vigenere
import square_ciphers
import binary
import bifid
import beaufort
import porta

ciphertext = (
    inputs.inputs()
)  # Get ciphertext (allows user to select one of 3 input methods)


def auto(ciphertext):
    print(f"Atbash: {quick_ciphers.decrypt_atbash(ciphertext)[:20]}")

    print("Affine: ")
    affine = quick_ciphers.bruteforce_affine(ciphertext)
    if not affine:
        print("No key found")
    else:
        for i in affine:
            print(f"a: {i[0]}, b: {i[1]}, plaintext: {i[2]}")

    print("Railfence: ")
    print(transposition.bruteforce_railfence(ciphertext))

    print("Substitution: ")
    substitution.bruteforce_sub(ciphertext)

    print("Vigenere: ")
    vigenere.bruteforce_vigenere(ciphertext)

    print("Transposition: ")
    transposition.bruteforce_transposition(ciphertext, 20)

    try:
        print("Polybius: ")
        square_ciphers.bruteforce_polybius(ciphertext)
    except:
        pass

    print("Bifid: ")
    try:
        print(bifid.bruteforce_bifid(ciphertext)[:20])
    except:
        pass

    binary.decrypt_bacon(ciphertext)
    binary.bruteforce_bacon(ciphertext)


def automatic(ciphertext):
    # Useful information about the ciphertext
    print("IOC: {}".format(utils.ioc(ciphertext)))
    print("Possible keys: {}".format(utils.factorise(len(ciphertext))))
    print(f"Ciphertext length: {len(ciphertext)}")

    # Run frequency analysis and display data
    utils.frequency(ciphertext)
    for i in range(1, 15):
        utils.ngram_plot(i, ciphertext, i, False)

    # Finally, run automatic decryption (and then run it on the reversed ciphertext)
    auto(ciphertext)
    print("\n##  Trying in reverse  ##\n")
    auto(ciphertext[::-1])


def manual(ciphertext):
    cipher_type = input(
        "Type of cipher: \n1. Substitution\n2. Transposition\n3. Vigenere\n4. Affine\n5. Railfence\n6. Atbash\n7. Polybius\n8. Bifid\n9. Bacon\n"
    )

    if cipher_type == "1":
        key = input("Enter key: ")
        answer = substitution.decrypt_substitution(key, ciphertext)
    elif cipher_type == "2":
        key = int(input("Enter key: "))
        answer = transposition.decrypt_transposition(key, ciphertext)
    elif cipher_type == "3":
        key = input("Enter key: ")
        answer = vigenere.decrypt_vigenere(key, ciphertext)
    elif cipher_type == "4":
        a = int(input("Enter a: "))
        b = int(input("Enter b: "))
        answer = quick_ciphers.decrypt_affine(a, b, ciphertext)
    elif cipher_type == "5":
        key = int(input("Enter key: "))
        answer = transposition.decrypt_railfence(key, ciphertext)
    elif cipher_type == "6":
        answer = quick_ciphers.decrypt_atbash(ciphertext)
    elif cipher_type == "7":
        key = input("Enter key: ")
        answer = square_ciphers.decrypt_polybius(key, ciphertext)
    elif cipher_type == "8":
        key = input("Enter key: ")
        answer = bifid.decrypt_bifid(key, ciphertext)
    elif cipher_type == "9":
        binary.decrypt_bacon(ciphertext)

    return utils.split_text(answer)


def manual_bruteforce(ciphertext):
    cipher_type = input(
        "Type of cipher: \n1. Substitution\n2. Transposition\n3. Vigenere\n4. Affine\n5. Railfence\n"
    )

    if cipher_type == "1":
        substitution.bruteforce_sub(ciphertext)
    elif cipher_type == "2":
        transposition.bruteforce_transposition(ciphertext, 20)
    elif cipher_type == "3":
        vigenere.bruteforce_vigenere(ciphertext)
    elif cipher_type == "4":
        quick_ciphers.bruteforce_affine(ciphertext)
    elif cipher_type == "5":
        transposition.bruteforce_railfence(ciphertext)


try:  # First run automatic
    automatic(ciphertext)
except Exception as error:
    print(f"Error: {error}")
try:  # Then run manual bruteforce
    manual_bruteforce(ciphertext)
except Exception as error:  # If it fails, run on completely manual
    print(f"Error: {error}")
    manual(ciphertext)
