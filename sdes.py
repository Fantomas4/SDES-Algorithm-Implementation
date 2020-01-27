from collections import deque


class Sdes:

    __s0_matrix = [["01", "00", "11", "10"],
                 ["11", "10", "01", "00"],
                 ["00", "10", "01", "11"],
                 ["11", "01", "11", "10"]]

    __s1_matrix = [["00", "01", "10", "11"],
                 ["10", "00", "01", "11"],
                 ["11", "00", "01", "00"],
                 ["10", "01", "00", "11"]]

    def __init__(self, key):
        self.__subkey_1 = None
        self.__subkey_2 = None
        self.__generate_subkeys(key)

    def __binary_list_xor(self, list_1, list_2):
        """ Performs the bit-by-bit XOR operation between two binary lists
        of equal size and returns a list containing the result """

        xor_res = []
        for bit in range(len(list_1)):
            if list_1[bit] == list_2[bit]:
                xor_res.append(0)
            else:
                xor_res.append(1)

        return xor_res

    def __generate_subkeys(self, key):
        """ Receives a 10-bit key and generates 2 subkeys """

        # Perform P10 (Permutation-10)
        p_10 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        p_10[0] = int(key[2])
        p_10[1] = int(key[4])
        p_10[2] = int(key[1])
        p_10[3] = int(key[6])
        p_10[4] = int(key[3])
        p_10[5] = int(key[9])
        p_10[6] = int(key[0])
        p_10[7] = int(key[8])
        p_10[8] = int(key[7])
        p_10[9] = int(key[5])

        # Split the 10-bit p_10 binary sequence into 2 binary sequences
        # with 5 bits each
        subseq_1 = p_10[:5]
        subseq_2 = p_10[5:]

        # Perform a 1-bit circular Left Shift to each of the subsequences
        ls1_subseq_1 = deque(subseq_1)
        # d.rotate(3)  # to the right
        ls1_subseq_1.rotate(-1)  # rotate 1-bit to the left

        ls1_subseq_2 = deque(subseq_2)
        ls1_subseq_2.rotate(-1)  # rotate 1-bit to the left

        # Combine subsequences ls1_subseq_1 and ls1_subseq_2 into the subsequence that will be
        # used to calculate P8 (Permutation-8)
        temp_seq = list(ls1_subseq_1 + ls1_subseq_2)

        # Perform P8 (Permutation-8)
        p_8 = [0, 0, 0, 0, 0, 0, 0, 0]
        p_8[0] = temp_seq[5]
        p_8[1] = temp_seq[2]
        p_8[2] = temp_seq[6]
        p_8[3] = temp_seq[3]
        p_8[4] = temp_seq[7]
        p_8[5] = temp_seq[4]
        p_8[6] = temp_seq[9]
        p_8[7] = temp_seq[8]

        # Store the result of P8 as subkey_1
        self.subkey_1 = p_8

        # Perform a 2-bit circular Left Shift to ls1_subseq_1 and ls1_subseq_2
        ls2_subseq_1 = ls1_subseq_1.copy()
        ls2_subseq_1.rotate(-2)

        ls2_subseq_2 = ls1_subseq_2.copy()
        ls2_subseq_2.rotate(-2)

        # Combine subsequences ls2_subseq_1 and ls2_subseq_2 into the subsequence that will be
        # used to calculate P8 (Permutation-8)
        temp_seq = list(ls2_subseq_1 + ls2_subseq_2)

        # Perform P8 (Permutation-8)
        p_8 = [0, 0, 0, 0, 0, 0, 0, 0]
        p_8[0] = temp_seq[5]
        p_8[1] = temp_seq[2]
        p_8[2] = temp_seq[6]
        p_8[3] = temp_seq[3]
        p_8[4] = temp_seq[7]
        p_8[5] = temp_seq[4]
        p_8[6] = temp_seq[9]
        p_8[7] = temp_seq[8]

        # Store the result of P8 as subkey_2
        self.subkey_2 = p_8

    def __initial_permutation(self, plaintext_str):
        """Performs the Initial Permutation (IP)"""

        ip = [0, 0, 0, 0, 0, 0, 0, 0]
        ip[0] = int(plaintext_str[1])
        ip[1] = int(plaintext_str[5])
        ip[2] = int(plaintext_str[2])
        ip[3] = int(plaintext_str[0])
        ip[4] = int(plaintext_str[3])
        ip[5] = int(plaintext_str[7])
        ip[6] = int(plaintext_str[4])
        ip[7] = int(plaintext_str[6])

        # Divide the 8-bit ip into a left sublist containing
        # the first 4 bits and a right sublist containing the final 4 bits.
        l_sublist = ip[:4]
        r_sublist = ip[4:]

        return l_sublist, r_sublist

    def __initial_permutation_inverse(self, fk_output):
        """ Performs the Inverse of Initial Permutation """

        # Combine both 4-bit lists given by the fk function into one
        # 8-bit binary sequence list.
        binary_seq = fk_output[0] + fk_output[1]

        ip_inv = [0, 0, 0, 0, 0, 0, 0, 0]
        ip_inv[0] = binary_seq[3]
        ip_inv[1] = binary_seq[0]
        ip_inv[2] = binary_seq[2]
        ip_inv[3] = binary_seq[4]
        ip_inv[4] = binary_seq[6]
        ip_inv[5] = binary_seq[1]
        ip_inv[6] = binary_seq[7]
        ip_inv[7] = binary_seq[5]

        # Return the result (ciphertext) as a string.
        return "".join(str(bit) for bit in ip_inv)

    def __switch_function(self, first_list, second_list):
        return second_list, first_list

    def __fk_function(self, l_sublist, r_sublist, subkey):

        # Perform the Expansion/Permutation (E/P) operation using r_sublist
        ep = [0, 0, 0, 0, 0, 0, 0, 0]
        ep[0] = r_sublist[3]
        ep[1] = r_sublist[0]
        ep[2] = r_sublist[1]
        ep[3] = r_sublist[2]
        ep[4] = r_sublist[1]
        ep[5] = r_sublist[2]
        ep[6] = r_sublist[3]
        ep[7] = r_sublist[0]

        # Perform the bit-by-bit XOR operation between E/P and the subkey
        # given to the Fk method.
        xor_res = self.__binary_list_xor(ep, subkey)

        # Split the 8-bit xor_res list into 2 subsequences, with the first subsequence
        # containing the first 4 bits of the original list and the second
        # subsequence containing the last 4 bits of the original list.
        subseq_1 = xor_res[:4]
        subseq_2 = xor_res[4:]

        # For the first subsequence, get the value of the S0 matrix
        # that is indicated by the subsequence's bits as follows:
        # subseq_1 = [bit0, bit1, bit2, bit3] --> get S0[bit0bit3, bit1bit2]
        s0_x = int(str(subseq_1[0]) + str(subseq_1[3]), 2)
        s0_y = int(str(subseq_1[1]) + str(subseq_1[2]), 2)
        s0_res_str = self.__s0_matrix[s0_x][s0_y]

        # For the second subsequence, get the value of the S1 matrix
        # that is indicated by the subsequence's bits as follows:
        # subseq_2 = [bit0, bit1, bit2, bit3] --> get S1[bit0bit3, bit1bit2]
        s1_x = int(str(subseq_2[0]) + str(subseq_2[3]), 2)
        s1_y = int(str(subseq_2[1]) + str(subseq_2[2]), 2)
        s1_res_str = self.__s1_matrix[s1_x][s1_y]

        # Combine both strings containing binary numbers into one that
        # will be given as input to P4 (Permutation-4)
        comb_str = s0_res_str + s1_res_str

        # Convert to a list for easier manipulation
        comb_list = list(int(bit) for bit in comb_str)

        # Perform the P4 (Permutation-4) using comb_list as input
        p4 = [0, 0, 0, 0]
        p4[0] = comb_list[1]
        p4[1] = comb_list[3]
        p4[2] = comb_list[2]
        p4[3] = comb_list[0]

        # Perform the bit-by-bit XOR operation between the left sublist (l_sublist) of the initial input
        # given to Fk and P4's result to get the final result returned by Fk
        xor_res = self.__binary_list_xor(l_sublist, p4)

        return xor_res, r_sublist

    def encrypt(self, plaintext):
        """ Receives an 8-bit plaintext and encrypts it using the SDES algorithm.

        :param plaintext: The plaintext that will be encrypted
        :return: The result ciphertext of the encryption

        """

        l_sublist, r_sublist = self.__initial_permutation(plaintext)

        addition_list, r_sublist = self.__fk_function(l_sublist, r_sublist, self.subkey_1)

        l_sublist, r_sublist = self.__switch_function(addition_list, r_sublist)

        l_sublist, r_sublist = self.__fk_function(l_sublist, r_sublist, self.subkey_2)

        return self.__initial_permutation_inverse((l_sublist, r_sublist))

    def decrypt(self, ciphertext):
        """ Receives an 8-bit plaintext and decrypts it using the SDES algorithm.

        :param ciphertext: The ciphertext that will be decrypted
        :return: The result plaintext of the decryption

        """

        l_sublist, r_sublist = self.__initial_permutation(ciphertext)

        addition_list, r_sublist = self.__fk_function(l_sublist, r_sublist, self.subkey_2)

        l_sublist, r_sublist = self.__switch_function(addition_list, r_sublist)

        l_sublist, r_sublist = self.__fk_function(l_sublist, r_sublist, self.subkey_1)

        return self.__initial_permutation_inverse((l_sublist, r_sublist))

def menu():
    title = """ 
     ___________ _____ _____    ___  _                  _ _   _                 _____       _            _       _             
    /  ___|  _  \  ___/  ___|  / _ \| |                (_) | | |               /  __ \     | |          | |     | |            
    \ `--.| | | | |__ \ `--.  / /_\ \ | __ _  ___  _ __ _| |_| |__  _ __ ___   | /  \/ __ _| | ___ _   _| | __ _| |_ ___  _ __ 
     `--. \ | | |  __| `--. \ |  _  | |/ _` |/ _ \| '__| | __| '_ \| '_ ` _ \  | |    / _` | |/ __| | | | |/ _` | __/ _ \| '__|
    /\__/ / |/ /| |___/\__/ / | | | | | (_| | (_) | |  | | |_| | | | | | | | | | \__/\ (_| | | (__| |_| | | (_| | || (_) | |   
    \____/|___/ \____/\____/  \_| |_/_|\__, |\___/|_|  |_|\__|_| |_|_| |_| |_|  \____/\__,_|_|\___|\__,_|_|\__,_|\__\___/|_|   
                                        __/ |                                                                                  
                                       |___/                                                                                   
    """
    print(title)
    print("\n\n> This is an example implementation of the SDES algorithm for binary data. \n")
    print("> Please choose one of the following: \n"
          "  1) Encrypt a binary sequence\n"
          "  2) Decrypt a binary sequence\n"
          "  3) Exit")

    while True:
        user_choice = int(input("\n> Enter your choice number: "))
        if 0 < user_choice < 4:
            break
        else:
            print("> Invalid menu choice. Please choose one of the given options.")

    return user_choice


def enter_key_prompt():
    while True:
        input_key = input("> Please enter the 10-bit key you want to use: ")

        if len(input_key) != 10:
            print("> Invalid key size. Key should consist of 10 bits.")
        else:
            break

    return input_key


def enter_plaintext_prompt():
    while True:
        plaintext = input("> Please enter the 8-bit plaintext binary sequence you want to encrypt: ")

        if len(plaintext) != 8:
            print("> Invalid sequence size. Sequence should consist of 8 bits.")
        else:
            break

    return plaintext


def enter_ciphertext_prompt():
    while True:
        ciphertext = input("> Please enter the 8-bit ciphertext binary sequence you want to decrypt: ")

        if len(ciphertext) != 8:
            print("> Invalid sequence size. Sequence should consist of 8 bits.")
        else:
            break

    return ciphertext


def print_encryption_result(ciphertext):
    print("> The result ciphertext from the encryption is: ", ciphertext)
    input("\n> Press Enter to continue...")


def print_decryption_result(plaintext):
    print("> The result plaintext from the decryption is: ", plaintext)
    input("\n> Press Enter to continue...")


def main():
    # *** START - For Testing Purposes only ***

    # Comment out if you want to test the algorithm's functionality
    # without interacting with the menus

    # # Encryption example
    # key = "1010000010"
    # sdes_obj = Sdes(key)
    # plaintext = "01110010"
    # ciphertext = sdes_obj.encrypt(plaintext)
    # print("> Encryption example: ")
    # print("- Using key: ", key)
    # print("- Using plaintext: ", plaintext)
    # print("- The result ciphertext is: ", ciphertext)
    #
    # # Decryption example
    # key = "1010000010"
    # sdes_obj = Sdes(key)
    # ciphertext = "01110111"
    # plaintext = sdes_obj.decrypt(ciphertext)
    # print("\n\n> Decryption example: ")
    # print("- Using key: ", key)
    # print("- Using ciphertext: ", ciphertext)
    # print("- The result plaintext is: ", plaintext)

    # *** END - For Testing Purposes only ***

    while True:
        mode = menu()
        if mode == 1:
            # If mode == 1 the encryption method is called

            # Request the 10-bit key from the user and use it
            # to initialize the Sdes class object
            sdes_obj = Sdes(enter_key_prompt())
            print_encryption_result(sdes_obj.encrypt(enter_plaintext_prompt()))
        elif mode == 2:
            # If mode == 2 the decryption method is called

            # Request the 10-bit key from the user and use it
            # to initialize the Sdes class object
            sdes_obj = Sdes(enter_key_prompt())
            print_decryption_result(sdes_obj.decrypt(enter_ciphertext_prompt()))
        elif mode == 3:
            # If mode == 3 the user has requested to exit
            return


if __name__ == "__main__":
    main()






