dico = {"A" : "0000",   "B" : "0001",   "C" : "0010",   "D" : "0011",  "E" : "0100",   "F" : "0101",   "G" : "0110",   "H" : "0111",   "I" : "1000",   "J" : "1001",   "K" : "1010",   "L" : "1011",   "M" : "1100",   "N" : "1101",   "O" : "1110",   "P" : "1111"}
def convert_to_binary(string):
    binary = ""
    for letter in string:
        binary += dico[letter]
    return binary

def convert_to_string(binary):
    string = ""
    for i in range(0, len(binary), 4):
        string += list(dico.keys())[list(dico.values()).index(binary[i:i+4])]
    return string

def xor(binary1, binary2):
    result = ""
    for i in range(len(binary1)):
        if binary1[i] == binary2[i]:
            result += "0"
        else:
            result += "1"
    return result

class Block:
    def __init__(self, sentence):
        self.sentence = sentence
        self.binary = convert_to_binary(sentence)
        self.blocks = [self.binary[i:i+4] for i in range(0, len(self.binary), 4)]
        self.current_block = 0

    def display_blocks(self):
        print(self.blocks)

    def display_binary(self):
        print(self.binary)

    def xor_iv(self, iv):
        self.blocks[0] = xor(self.blocks[0], iv)

    def encrypt_block(self, key):
        self.blocks[self.current_block] = bin((int(self.blocks[self.current_block], 2) + int(key, 2)) % 16)[2:].zfill(4)

    def xor_blocks(self, block1, block2):
        return xor(block1, block2)

    # create a function
    def encrypt(self, key, iv):
        self.xor_iv(iv)
        for i in range(len(self.blocks)):
            self.encrypt_block(key)
            if i < len(self.blocks) - 1:
                self.blocks[i+1] = self.xor_blocks(self.blocks[i], self.blocks[i+1])
            self.current_block += 1
        self.current_block = 0
        return self.blocks

    def decrypt_block(self, key):
        self.blocks[self.current_block] = bin((int(self.blocks[self.current_block], 2) - int(key, 2) + 16) % 16)[2:].zfill(4)

    def decrypt(self, key, iv):
        self.current_block = len(self.blocks) - 1
        for i in range(len(self.blocks)):
            self.decrypt_block(key)
            if i < len(self.blocks) - 1:
                self.blocks[self.current_block] = self.xor_blocks(self.blocks[self.current_block], self.blocks[self.current_block - 1])
            self.current_block -= 1
        self.current_block = 0
        self.xor_iv(iv)
        return self.blocks

    def set_blocks(self, blocks):
        self.blocks = blocks

    def print_current_blocks_as_string(self):
        print(convert_to_string("".join(self.blocks)))




# initialize with the sentence "BOBALICE"
sentence = "BOBALICE"
# create a block object
block = Block(sentence)
# display the blocks
block.display_blocks()
# encrypt the sentence with the key "0011" and IV "0010"
print(block.encrypt("0011", "1010"))
# decrypt the sentence
block.print_current_blocks_as_string()
print(block.decrypt("0011", "1010"))
block.print_current_blocks_as_string()

print ("-------------------")
block2 = Block("BOBALICE")
block2.set_blocks(['0010', '1010', '0100', '1100', '1100', '0000', '1011', '1110'])
block2.decrypt("0011", "0011")
block2.print_current_blocks_as_string()
