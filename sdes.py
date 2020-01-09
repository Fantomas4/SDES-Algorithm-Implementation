from collections import deque


class Sdes:

    s0_matrix = [["01", "00", "11", "10"],
                 ["11", "10", "01", "00"],
                 ["00", "10", "01", "11"],
                 ["11", "01", "11", "10"]]

    s1_matrix = [["00", "01", "10", "11"],
                 ["10", "00", "01", "11"],
                 ["11", "00", "01", "00"],
                 ["10", "01", "00", "11"]]

    def __init__(self):
        self.subkey_1 = None
        self.subkey_2 = None

    # Receives a 10-bit key and generates 2 subkeys
    def generate_subkeys(self, key):

        # Perform P10 (Permutation-10)
        p_10 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        p_10[0] = key[2]
        p_10[1] = key[4]
        p_10[2] = key[1]
        p_10[3] = key[6]
        p_10[4] = key[3]
        p_10[5] = key[9]
        p_10[6] = key[0]
        p_10[7] = key[8]
        p_10[8] = key[7]
        p_10[9] = key[5]

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
        ls2_subseq_1 = ls1_subseq_2.copy()
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

    def initial_permutation(self, plaintext_bits):

        # Perform the Initial Permutation (IP)
        ip = [0, 0, 0, 0, 0, 0, 0, 0]
        ip[0] = plaintext_bits[1]
        ip[1] = plaintext_bits[5]
        ip[2] = plaintext_bits[2]
        ip[3] = plaintext_bits[0]
        ip[4] = plaintext_bits[3]
        ip[5] = plaintext_bits[7]
        ip[6] = plaintext_bits[4]
        ip[7] = plaintext_bits[6]

        return ip

    def fk_function(self, ip):

        # Divide the 8-bit ip into a left sublist containing
        # the first 4 bits and a right sublist containing the final 4 bits.
        l_sublist = ip[:4]
        r_sublist = ip[4:]

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

        # Perform binary addition between E/P and Subkey 1
        # Convert ep list and subkey_1 list to strings
        ep_str = "".join(str(b) for b in ep)
        subkey_1_str = "".join(str(b) for b in self.subkey_1)
        binary_sum_str = bin(int(ep_str, 2) + int(subkey_1_str, 2))

        # Convert the binary sum string result to a list for easier manipulation
        binary_sum_list = list(binary_sum_str)

        # Split the 8-bit list into 2 subsequences, with the first subsequence
        # containing the first 4 bits of the original list and the second
        # subsequence containing the last 4 bits of the original list.
        sum_subseq_1 = binary_sum_list[:4]
        sum_subseq_2 = binary_sum_list[4:]

        # For the first subsequence, get the value of the S0 matrix
        # that is indicated by the subsequence's bits as follows:
        # sum_subseq_1 = [bit0, bit1, bit2, bit3] --> get S0[bit0bit3, bit1bit2]
        s0_x = int(str(sum_subseq_1[0]) + str(sum_subseq_1[3]), 2)
        s0_y = int(str(sum_subseq_1[1]) + str(sum_subseq_1[2]), 2)
        s0_res_str = self.s0_matrix[s0_x][s0_y]

        # For the second subsequence, get the value of the S1 matrix
        # that is indicated by the subsequence's bits as follows:
        # sum_subseq_2 = [bit0, bit1, bit2, bit3] --> get S1[bit0bit3, bit1bit2]
        s1_x = int(str(sum_subseq_2[0]) + str(sum_subseq_2[3]), 2)
        s1_y = int(str(sum_subseq_2[1]) + str(sum_subseq_2[2]), 2)
        s1_res_str = self.s1_matrix[s1_x][s1_y]

        # Combine both strings containing binary numbers into one that
        # will be given as input to P4 (Permutation-4)
        comb_str = s0_res_str + s1_res_str

        # Convert to a list for easier manipulation
        comb_list = list(comb_str)

        # Perform the P4 (Permutation-4) using comb_list as input
        # P4
        # 2
        # 4
        # 3
        # 1
        p4 = [0, 0, 0, 0]
        p4[0] = comb_list[1]
        p4[1] = comb_list[3]
        p4[2] = comb_list[2]
        p4[3] = comb_list[0]

        # Perform a binary addition between the left sublist (l_sublist) of the initial input
        # given to Fk and P4's result to get the final result returned by Fk
        # Convert l_sublist list and p4 list to strings
        l_sublist_str = "".join(str(b) for b in l_sublist)
        p4_str = "".join(str(b) for b in p4)
        result_str = bin(int(l_sublist_str, 2) + int(p4_str, 2))

        return result_str









