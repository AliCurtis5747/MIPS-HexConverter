import sys

registers = [
    "$zero", "$at", "$v0", "$v1", "$a0", "$a1", "$a2", "$a3",
    "$t0", "$t1", "$t2", "$t3", "$t4", "$t5", "$t6", "$t7",
    "$s0", "$s1", "$s2", "$s3", "$s4", "$s5", "$s6", "$s7",
    "$t8", "$t9", "$k0", "$k1", "$gp", "$sp", "$fp", "$ra"
]
r_type_instructions = [
    "add", "addu", "sub", "subu", "and", "or", "xor", "nor",
    "slt", "sltu", "sll", "srl", "sra", "sllv", "srlv", "srav",
    "jr", "jalr", "mult", "multu", "div", "divu", 
    "mfhi", "mflo", "mthi", "mtlo", "syscall", "break"
]

i_type_instructions = [
    "addi", "addiu", "slti", "sltiu", "andi", "ori", "xori",
    "lui", "lw", "lh", "lhu", "lb", "lbu", "sw", "sh", "sb",
    "beq", "bne", "blez", "bgtz", "bltz", "bgez", "bltzal", "bgezal"
]

j_type_instructions = [
    "j", "jal"
]

r_type_function_codes = [
    32, 33, 34, 35, 36, 37, 38, 39,  # add, addu, sub, subu, and, or, xor, nor
    42, 43, 0, 2, 3, 4, 6, 7,        # slt, sltu, sll, srl, sra, sllv, srlv, srav
    8, 9, 24, 25, 26, 27,            # jr, jalr, mult, multu, div, divu
    16, 18, 17, 19, 12, 13           # mfhi, mflo, mthi, mtlo, syscall, break
]

i_type_opcodes = [
    8, 9, 10, 11, 12, 13, 14,        # addi, addiu, slti, sltiu, andi, ori, xori
    15, 35, 33, 37, 32, 36, 43, 41, 40,  # lui, lw, lh, lhu, lb, lbu, sw, sh, sb
    4, 5, 6, 7, 1, 1, 1, 1           # beq, bne, blez, bgtz, bltz, bgez, bltzal, bgezal
]

j_type_opcodes = [
    2, 3  # j, jal
]

def binaryConvert(x): #Converts numbers TO binary
    value = bin(x)[2:]
    return value

def binaryConvert(value, bits): #Converts to binary and fills bits as needed
    if value < 0:
        value = (1 << bits) + value
    return format(value, f'0{bits}b')

def parseLoadStore(instruction_part): # Parses LoadStore methods separately to save on lines
    if '(' in instruction_part and ')' in instruction_part:
        offset_str = instruction_part.split('(')[0]
        register_str = instruction_part.split('(')[1].rstrip(')')
        offset = int(offset_str) if offset_str else 0
        return offset, register_str
    return 0, instruction_part


def binaryReverse(x): #Converts numbers FROM binary
    return int(x, 2)

def hexConverter(x): # Converts FROM hex to binary
    if x.startswith('0x') or x.startswith('0X'):
        x = x[2:]
    decimal_value = int(x, 16)
    binary_str = bin(decimal_value)[2:]
    binary_str = binary_str.zfill(32)
    return binary_str

def hexReverser(x): #Converts from Binary TO Hex
    # Pad to multiple of 4 bits
    while len(x) % 4 != 0:
        x = '0' + x
    
    hex_digits = []
    for i in range(0, len(x), 4):
        chunk = x[i:i+4]
        hex_digit = hex(int(chunk, 2))[2:].upper()
        hex_digits.append(hex_digit)
    
    return '0x' + ''.join(hex_digits)
    

def mipConvert():
    result = ""
    instruction = command.split() # separates the command string into individual elements
    
    match instruction[0]:
        case s if instruction[0] in r_type_instructions: # Determines to use the r type instruction method 
            if instruction[0] == "sll" or instruction[0] == "srl" or instruction[0] == "sra": #Determines to use the sll parsing method
                result = "000000"
                register_s = "00000"
                register_t = binaryConvert(registers.index(instruction[2]), 5) # converts the register to a corresponding value, and then to binary
                register_d = binaryConvert(registers.index(instruction[1]), 5)
                shamt = binaryConvert(int(instruction[3]), 5) #converts shamt to binary
                funct = r_type_instructions.index(instruction[0])
                func = binaryConvert(r_type_function_codes[funct], 6)
                result += register_s + register_t + register_d + shamt + func
                return result
            else:
                result = "000000"
                register_s = binaryConvert(registers.index(instruction[2]), 5)  # converts the register to a corresponding value, and then to binary
                register_t = binaryConvert(registers.index(instruction[3]), 5)
                register_d = binaryConvert(registers.index(instruction[1]), 5)
                funct = r_type_instructions.index(instruction[0])
                func = binaryConvert(r_type_function_codes[funct], 6)
                result += register_s + register_t + register_d + "00000" + func
                return result
        case s if instruction[0] in i_type_instructions: # determines to use the i type instruction method
            if instruction[0] and instruction[0][0] == "b":
                if instruction[0] == "bne" or instruction[0] == "beq":
                    spot = i_type_instructions.index(instruction[0])
                    head = binaryConvert(i_type_opcodes[spot], 6)
                    register_s = binaryConvert(registers.index(instruction[1]), 5)  # converts the register to a corresponding value, and then to binary
                    register_t = binaryConvert(registers.index(instruction[2]), 5)
                    immediate = binaryConvert(int(instruction[3]), 16)
                    result += head + register_s + register_t + immediate
                    return result
                else:
                    spot = i_type_instructions.index(instruction[0])
                    head = binaryConvert(i_type_opcodes[spot], 6)
                    register_s = binaryConvert(registers.index(instruction[1]), 5)  # converts the register to a corresponding value, and then to binary
                    register_t = "00000"
                    immediate = binaryConvert(int(instruction[2]), 16)
                    result += head + register_s + register_t + immediate
                    return result
            elif instruction[0] == "lw" or instruction[0] == "lh" or instruction[0] == "lhu" or instruction[0] == "lb" or instruction[0] == "lbu" or instruction[0] == "sw" or instruction[0] == "sh" or instruction[0] == "sb": #converts using the parsing method for load/store
                spot = i_type_instructions.index(instruction[0])
                head = binaryConvert(i_type_opcodes[spot], 6)
                register_t = binaryConvert(registers.index(instruction[1]), 5)
                offset, base_reg = parseLoadStore(instruction[2])
                register_s = binaryConvert(registers.index(base_reg), 5)
                immediate = binaryConvert(offset, 16)
                result += head + register_s + register_t + immediate
                return result
            else: #generic i type instruction parser
                spot = i_type_instructions.index(instruction[0]) 
                head = binaryConvert(i_type_opcodes[spot], 6)
                register_s = binaryConvert(registers.index(instruction[2]), 5)
                register_t = binaryConvert(registers.index(instruction[1]), 5)
                immediate = binaryConvert(int(instruction[3]), 16)
                result += head + register_s + register_t + immediate
                return result
        case s if instruction[0] in j_type_instructions: # s type instruction parser
            spot = j_type_instructions.index(instruction[0])
            head = binaryConvert(j_type_opcodes[spot], 6)
            address_str = instruction[1]
            if address_str.startswith('0x'):
                address = int(address_str, 16)
            else:
                address = int(address_str)
            address = address >> 2
            addr_field = binaryConvert(address, 26)
            result += head + addr_field
            return result
    
    return "Invalid instruction"

def machinConvert():
    result = ""
    num = binaryReverse(command[0:6])
    match num:
        case s if num == 0:
            print("R-Type")
            funct = binaryReverse(command[26:])
            spot = r_type_function_codes.index(funct) #checks the value of the opcode value and pulls the corresponding string
            head = r_type_instructions[spot]

            register_s = registers[binaryReverse(command[6:11])] #checks the value of the register_s and pulls the corresponding string
            register_t = registers[binaryReverse(command[11:16])]
            register_d = registers[binaryReverse(command[16:21])]

            
            if head == "sll" or head == "srl" or head == "sra":
                shamt = str(binaryReverse(command[21:26]))
                result = "" + head + " " + register_d + ", " + register_t + ", " + shamt # assembles the assembly string
                return result


            result = "" + head +" "+ register_d + ", " + register_s + ", " + register_t 
        case s if num in i_type_opcodes:
            spot = i_type_opcodes.index(num) #checks the value of the opcode value and pulls the corresponding string
            head = i_type_instructions[spot]

            register_s = registers[binaryReverse(command[6:11])] #checks the value of the register_s and pulls the corresponding string
            register_t = registers[binaryReverse(command[11:16])]
            immediate = str(binaryReverse(command[16:])) #derives the immediate's value

            if head == "lw" or head == "sw" or head == "sb" or head == "lb":
                result  = "" + head + " " + register_s + ", " + immediate +"("+ register_t +")"
                return result

            result = "" + head + " " + register_s + ", " + register_t + ", " + immediate
            return result

        case s if num in j_type_opcodes:
            print("J-Type")
            spot = j_type_opcodes.index(num) #checks the value of the opcode value and pulls the corresponding string
            head = j_type_instructions[spot]

            address = str(binaryReverse(command[6:]))
            result = head + " " + address
            return result
            

    return "Invalid instruction"

# Reads the command arguments and executes the corresponding code

rawHex = sys.argv[2] # raw input string
if sys.argv[1] == "-a":
    command = rawHex.replace(",", "")
    print(hexReverser(mipConvert())) # calls to convert the binary representation to hex before printing

if sys.argv[1] == "-m": 
    rawHex = sys.argv[2]
    command = hexConverter(rawHex) #converts from hex to binary before parsingy
    print(machinConvert())
