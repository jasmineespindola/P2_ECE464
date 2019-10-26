# import math is used to access ceil function
import math


# decimal to binary conversion function
def decimalToBinary(n): 
# Remove 0b from built-in binary conversion function
		return bin(n).replace("0b","")


def Number_of_input_bits(bench_file):
# open benchfile
	net_File = open(bench_file, "r")
	input_bits = 0
# count number of INPUTs
	for line in net_File:
		if(line[0:5] == 'INPUT'):
			input_bits += 1
		else:
			input_bits += 0
# return the number of input bits
	return input_bits


def tv_generation(bench_file, integer_seed ):
# generating TV_A.txt
		OutputFile = open('TV_A.txt', 'w')
#Calculate the number of input bits in bench file
		number_of_input_bits = Number_of_input_bits(bench_file)
# use seed as starting point and extend zeros until length

		temp = integer_seed
#Generate 255 test vectors    
		for i in range(255):
				binary_value = decimalToBinary(temp)
				rem = number_of_input_bits-len(binary_value)
				binary_value = '0'*rem + binary_value
#Writing in Output file to generate TV_A.txt
				OutputFile.write(binary_value + '\n')
# Incrementing Counter
				temp += 1
# generating TV_B.txt
#resetting back to seed 
		temp = integer_seed
		OutputFile=open('TV_B.txt', 'w')
		for i in range(255):
				if(temp == 256):
					temp = 0
				else:
					temp = temp
				binary_value = decimalToBinary(temp)
# Making each seed 8 bits
				rem = 8-len(binary_value)
				binary_value = '0'*rem + binary_value
#determining and looping the number of times it needs to be appended
				for j in range(math.ceil(number_of_input_bits/8)):
					binary_value = binary_value + binary_value
				OutputFile.write(binary_value[0:number_of_input_bits] + '\n')
				temp += 1
# generating TV_C.txt
		temp = integer_seed
		OutputFile = open('TV_C.txt', 'w')
		for i in range(255):
				if(temp == 256):
					temp = 0
				else:
					temp = temp
#storing temp in another variabel for the sake of looping
				temp1 = temp
				bits_per_line = 0
#run the loop till we get binary_value == number_of_input_bits 
				for j in range(math.ceil(number_of_input_bits/8)):
#Converting decimal temp1 to binary
						binary_value = decimalToBinary(temp1)
#find out number of zeros to append to binary value
						rem = 8-len(binary_value)
#append zeros to value
						binary_value = '0'*rem + binary_value
						if(bits_per_line + 8 <= number_of_input_bits):
								OutputFile.write(binary_value)
						else:
								OutputFile.write(binary_value[0:(number_of_input_bits - bits_per_line )])
								OutputFile.write('\n')
						bits_per_line += 8
						temp1 += 1
				temp += 1
# generating TV_D.txt
# generating TV_E.txt


def main():
	print("\t\t\tProject 2: Fault Coverage of Pseudo Random TV's  \n")
	user_choice = 0
	while user_choice <= 0 or user_choice > 2:
		print(" Options:\n")
		print("******************************\n")
		print("1. Test Vector Generation \n")
		print("2. Fault Coverage Simulation \n")
		user_choice = input("choose what you'd like to do (1,2): \n ")
		user_choice = int(user_choice)
		if user_choice < 1 or user_choice > 2:
			print(" ERROR. INVALID USER OPTION. TRY AGAIN\n")

	# 1: test vector generation
	if user_choice == 1:
		print("performing test vector generation")
		# input : circuit.bench  integer seed
		# validate input   JEM- to do
		bench_file = input("input bench file name: \n ")
		integer_seed = int(input("input integer seed: \n "))
		tv_generation(bench_file, integer_seed)
	elif user_choice == 2:
		print("performing fault coverage \n")


main()





