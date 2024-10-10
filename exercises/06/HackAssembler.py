import re

def main():
    
    instruction = 0

    while True:
        try:
            file_name = input("asm file name: ").lower().title()

            source_file_path = f"{file_name}.asm"

            with open(source_file_path, "r") as source_file:
                reader = source_file.readlines()
                asm_content = []
            
            break

        except FileNotFoundError:
            pass
    

    destination_file_path = f"{file_name}.hack"

    with open(destination_file_path, "w") as destination_file:

        #first pass on code. Adds labels to symboltable and removes comments.
        label_counter = 0

        for i in range(len(reader)):

            cleaned_line = remove_comments(reader[i])
            
            if len(cleaned_line) == 0:
                continue

            if cleaned_line[0] == "(" and cleaned_line[-1] == ")":
                label = str(cleaned_line[1:-1])
                symbol_table[label] = label_counter
                continue
        
            asm_content.append(cleaned_line)
            label_counter += 1

        #second pass on code. Translates everything into binary.
        for line in asm_content:

            if line[0] == "@":
                a_value = line[1:]

                if not a_value.isnumeric():
                    a_value = int(symboltable(a_value))
                else:
                    a_value = int(a_value)
                
                instruction = f"0{a_value:015b}"

            else:
                c_value = line

                parsed_values = parser(c_value)

                c_code = code(parsed_values)

                instruction = f"111{c_code}"
            
            destination_file.write(f"{instruction}\n")


#remove everything from start of '//'
def remove_comments(line):
    comment_index = line.find("//")
    line = line[:comment_index]

    line = line.replace(" ", "")
    
    return line


#symbolic syntax dest=comp;jump goes in. symbol seperated into list and returned.
def parser(symbolic_input):
    
    instruction_list = ["null", "", "null"]

    equal_sign = symbolic_input.find("=")
    if equal_sign != -1:
        dest = symbolic_input[:equal_sign]
        instruction_list[0] = str(dest)

    jump_sign = symbolic_input.find(";")
    if jump_sign != -1:
        jump = symbolic_input[jump_sign+1:]
        instruction_list[2] = str(jump)
    else:
        jump_sign = len(symbolic_input)

    comp = symbolic_input[equal_sign+1:jump_sign]
    instruction_list[1] = str(comp)

    return instruction_list


comp_dict_0 = {
    "0":"101010",
    "1":"111111",
    "-1":"111010",
    "D":"001100",
    "A":"110000",
    "!D":"001101",
    "!A":"110001",
    "-D":"001111",
    "-A":"110011",
    "D+1":"011111",
    "A+1":"110111",
    "D-1":"001110",
    "A-1":"110010",
    "D+A":"000010",
    "D-A":"010011",
    "A-D":"000111",
    "D&A":"000000",
    "D|A":"010101"
}

comp_dict_1 = {
    "M":"110000",
    "!M":"110001",
    "-M":"110011",
    "M+1":"110111",
    "M-1":"110010",
    "D+M":"000010",
    "D-M":"010011",
    "M-D":"000111",
    "D&M":"000000",
    "D|M":"010101"
}

dest_dict = {
    "null":"000",
    "M":"001",
    "D":"010",
    "MD":"011",
    "A":"100",
    "AM":"101",
    "AD":"110",
    "AMD":"111"
}

jump_dict = {
    "null":"000",
    "JGT":"001",
    "JEQ":"010",
    "JGE":"011",
    "JLT":"100",
    "JNE":"101",
    "JLE":"110",
    "JMP":"111"
}

def code(parsed_values):

    c_code = ""

    dest = dest_dict[parsed_values[0]]
    jump = jump_dict[parsed_values[2]]

    comp_symbolic = parsed_values[1]

    if  comp_symbolic.find("M") != -1:
        comp = f"1{comp_dict_1[comp_symbolic]}"
    else:
        comp = f"0{comp_dict_0[comp_symbolic]}"

    c_code = f"{comp}{dest}{jump}"

    return c_code


#take in a symbol. compare with symboltable to return address. update table if not found. 
symbol_table = {
        "R0":0,
        "R1":1,
        "R2":2,
        "R3":3,
        "R4":4,
        "R5":5,
        "R6":6,
        "R7":7,
        "R8":8,
        "R9":9,
        "R10":10,
        "R11":11,
        "R12":12,
        "R13":13,
        "R14":14,
        "R15":15,
        "screen": 16384,
        "kbd": 24576,
        "SP": 0,
        "LCL": 1,
        "ARG": 2,
        "THIS": 3,
        "THAT": 4
    }

var_counter = [16]

def symboltable(symbol):
    
    #if symbol not present in table, add symbol - address pair to table. Then return address
    if symbol_table.get(symbol) == None:
        symbol_table[symbol] = var_counter[0]
        address = var_counter[0]
        var_counter[0] += 1

    else:
        address = symbol_table.get(symbol)
    
    return address


main()
