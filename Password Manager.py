# Code File Begins

# A password manager using Python That uses AES-256-GCM Cipher
# This is Menu Driven Program

# importing required libraries
import pickle
from pbkdf2 import PBKDF2
from Crypto.Cipher import AES

#Master Key for checking Master Password at each step
#Masterkey Generated using PBKDF2
#EUID - vd0208
key = b'\x11:!\x89\xea d6\xf7\xdd\x14l\x0e;\xdfm"Vn\x98\x88gcKuI\x90\xefc\x90\xc0\xd7'


#Real program Begins
print("Please Enter Master Password to login")

#Using While loop for Infinite usage
while True:

    #Checking Master Password before starting
    if key == PBKDF2(input("Enter Master Password "), "").read(32):
        print("correct password")
        break
    else:
        print("Incorrect password. Please Try Again")
#Using While loop for Infinite usage
while True:

    #displaying options to the user
    print("1 - Add new Website")
    print("2 - Retrieve Password")
    print("3 - Exit")
    a = input("Enter the option number ")

    #code executed when user chose to exit program
    if a == "3":
        if key == PBKDF2(input("Enter Master Password "), "").read(32):
            print("correct password")
            exit()
        else:
            print("Incorrect password")

    #code executed when user chose to add a new website to the database
    elif a == "1":
        #taking input
        website = input("Enter Website ")
        password = input("Enter Website Password ")
        header = b"header"
        #creating Cipher
        cipher = AES.new(key, AES.MODE_GCM)
        cipher.update(header)
        pass_cipher, tag = cipher.encrypt_and_digest(password.encode("utf8"))

        # checking Master Password
        # if user enter correct master password
        # changes are saved
        if key == PBKDF2(input("Enter Master Password "), "").read(32):
            print("correct password")
            f = open('pw.dat', 'ab')
            pickle.dump([website, pass_cipher, cipher.nonce, tag, header], f)
            f.close()
            # add website case
        else:
            print("Incorrect password. Please Try Again")
    #code executed when user chose to retrieve a password
    elif a == "2":
        # taking input
        website = input("Enter Website ")
        #opening database
        f = open('pw.dat', 'rb')
        rlist = [] #empty list
        sta = 0 # making status to 0

        # while loop for using till end
        while True:
            try:
                rec = pickle.load(f)
                rlist.append(rec)

                # checking the records
                if rec[0] == website:
                    pass_cipher = rec[1]
                    nonce = rec[2]
                    tag = rec[3]
                    header = rec[4]
                    sta = 1 # updating status

            except EOFError:
                # end file to stop loop
                break
        f.close()
        # Adding entries to the database again
        if len(rlist) != 0:
            f = open('pw.dat', 'ab')
            for x in rlist: pickle.dump(x, f)
            f.close()
        if sta == 0:
            print("Website Not Found")
            continue

        # checking the Master Password
        if key == PBKDF2(input("Enter Master Password "), "").read(32):
            print("correct password")
            try:
                # decrypting Cipher
                cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
                cipher.update(header)
                plaintext = cipher.decrypt_and_verify(pass_cipher, tag)
                password = plaintext.decode("utf8")
            except ValueError:
                print("Invalid Decryption err-Value Error")
            except KeyError:
                print("Invalid Decryption err-Key Error")

            # giving output
            print("Password for", website, "is-", password)
        else:
            print("Incorrect password")
    else:
        print("invalid usage")

#   program Ends
#    _*_*_*_*_*_*_*_*_*_
