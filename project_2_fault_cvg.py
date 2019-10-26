from __future__ import print_function
# import math is used to access ceil function
import math
import os

# Function List:
# 1. netRead: read the benchmark file and build circuit netlist
# 2. gateCalc: function that will work on the logic of each gate
# 3. inputRead: function that will update the circuit dictionary made in netRead to hold the line values
# 4. basic_sim: the actual simulation
# 5. main: The main function


# -------------------------------------------------------------------------------------------------------------------- #
# FUNCTION: Reading in the Circuit gate-level netlist file: aka ckt file
def netRead(netName):
	# Opening the netlist file:
	netFile = open(netName, "r")

	# temporary variables
	inputs = []  # array of the input wires
	outputs = []  # array of the output wires
	gates = []  # array of the gate list
	inputBits = 0  # the number of inputs needed in this given circuit

	# main variable to hold the circuit netlist, this is a dictionary in Python, where:
	# key = wire name; value = a list of attributes of the wire
	circuit = {}

	# Reading in the netlist file line by line
	for line in netFile:

		# NOT Reading any empty lines
		if (line == "\n"):
			continue

		# Removing spaces and newlines
		line = line.replace(" ", "")
		line = line.replace("\n", "")

		# NOT Reading any comments
		if (line[0] == "#"):
			continue

		# @ Here it should just be in one of these formats:
		# INPUT(x)
		# OUTPUT(y)
		# z=LOGIC(a,b,c,...)

		# Read a INPUT wire and add to circuit:
		if (line[0:5] == "INPUT"):
			# Removing everything but the line variable name
			line = line.replace("INPUT", "")
			line = line.replace("(", "")
			line = line.replace(")", "")

			# Format the variable name to wire_*VAR_NAME*
			line = "wire_" + line

			# Error detection: line being made already exists
			if line in circuit:
				msg = "NETLIST ERROR: INPUT LINE \"" + line + "\" ALREADY EXISTS PREVIOUSLY IN NETLIST"
				print(msg + "\n")
				return msg

			# Appending to the inputs array and update the inputBits
			inputs.append(line)

			# add this wire as an entry to the circuit dictionary
			circuit[line] = ["INPUT", line, False, 'U']

			inputBits += 1
			print(line)
			print(circuit[line])
			continue

		# Read an OUTPUT wire and add to the output array list
		# Note that the same wire should also appear somewhere else as a GATE output
		if line[0:6] == "OUTPUT":
			# Removing everything but the numbers
			line = line.replace("OUTPUT", "")
			line = line.replace("(", "")
			line = line.replace(")", "")

			# Appending to the output array
			outputs.append("wire_" + line)
			continue

		# Read a gate output wire, and add to the circuit dictionary
		lineSpliced = line.split("=")  # splicing the line at the equals sign to get the gate output wire
		gateOut = "wire_" + lineSpliced[0]

		# Error detection: line being made already exists
		if gateOut in circuit:
			msg = "NETLIST ERROR: GATE OUTPUT LINE \"" + gateOut + "\" ALREADY EXISTS PREVIOUSLY IN NETLIST"
			print(msg + "\n")
			return msg

		# Appending the dest name to the gate list
		gates.append(gateOut)

		lineSpliced = lineSpliced[1].split("(")  # splicing the line again at the "("  to get the gate logic
		logic = lineSpliced[0].upper()

		lineSpliced[1] = lineSpliced[1].replace(")", "")
		terms = lineSpliced[1].split(",")  # Splicing the the line again at each comma to the get the gate terminals
		# Turning each term into an integer before putting it into the circuit dictionary
		terms = ["wire_" + x for x in terms]

		# add the gate output wire to the circuit dictionary with the dest as the key
		circuit[gateOut] = [logic, terms, False, 'U']
		print(gateOut)
		print(circuit[gateOut])

	# now after each wire is built into the circuit dictionary,
	# add a few more non-wire items: input width, input array, output array, gate list
	# for convenience

	circuit["INPUT_WIDTH"] = ["input width:", inputBits]
	circuit["INPUTS"] = ["Input list", inputs]
	circuit["OUTPUTS"] = ["Output list", outputs]
	circuit["GATES"] = ["Gate list", gates]

	print("\n bookkeeping items in circuit: \n")
	print(circuit["INPUT_WIDTH"])
	print(circuit["INPUTS"])
	print(circuit["OUTPUTS"])
	print(circuit["GATES"])

	return circuit


# -------------------------------------------------------------------------------------------------------------------- #
# FUNCTION: calculates the output value for each logic gate
def gateCalc(circuit, node):
	# terminal will contain all the input wires of this logic gate (node)
	terminals = list(circuit[node][1])

	# temporarily changes a wire's value for -in-SA
	if len(unnamedSA) > 0:
		if node == unnamedSA[0]:  # if same output wire of gate as SA
			for term in terminals:  # find the input terminal that is SA
				if term == unnamedSA[1]:
					holdTheWire = list(circuit[term]).copy()  # copy the wire attributes before change
					circuit[term][3] = unnamedSA[2]  # change bit value of wire
					continue

	# If the node is an Inverter gate output, solve and return the output
	if circuit[node][0] == "NOT":
		if circuit[terminals[0]][3] == '0':
			circuit[node][3] = '1'
		elif circuit[terminals[0]][3] == '1':
			circuit[node][3] = '0'
		elif circuit[terminals[0]][3] == "U":
			circuit[node][3] = "U"
		else:  # Should not be able to come here
			return -1
		return circuit

	# If the node is an AND gate output, solve and return the output
	elif circuit[node][0] == "AND":
		# Initialize the output to 1
		circuit[node][3] = '1'
		# Initialize also a flag that detects a U to false
		unknownTerm = False  # This will become True if at least one unknown terminal is found

		# if there is a 0 at any input terminal, AND output is 0. If there is an unknown terminal, mark the flag
		# Otherwise, keep it at 1
		for term in terminals:
			if circuit[term][3] == '0':
				circuit[node][3] = '0'
				break
			if circuit[term][3] == "U":
				unknownTerm = True

		if unknownTerm:
			if circuit[node][3] == '1':
				circuit[node][3] = "U"
		return circuit

	# If the node is a NAND gate output, solve and return the output
	elif circuit[node][0] == "NAND":
		# Initialize the output to 0
		circuit[node][3] = '0'
		# Initialize also a variable that detects a U to false
		unknownTerm = False  # This will become True if at least one unknown terminal is found

		# if there is a 0 terminal, NAND changes the output to 1. If there is an unknown terminal, it
		# changes to "U" Otherwise, keep it at 0
		for term in terminals:
			if circuit[term][3] == '0':
				circuit[node][3] = '1'
				break
			if circuit[term][3] == "U":
				unknownTerm = True
				break

		if unknownTerm:
			if circuit[node][3] == '0':
				circuit[node][3] = "U"
		return circuit

	# If the node is an OR gate output, solve and return the output
	elif circuit[node][0] == "OR":
		# Initialize the output to 0
		circuit[node][3] = '0'
		# Initialize also a variable that detects a U to false
		unknownTerm = False  # This will become True if at least one unknown terminal is found

		# if there is a 1 terminal, OR changes the output to 1. Otherwise, keep it at 0
		for term in terminals:
			if circuit[term][3] == '1':
				circuit[node][3] = '1'
				break
			if circuit[term][3] == "U":
				unknownTerm = True

		if unknownTerm:
			if circuit[node][3] == '0':
				circuit[node][3] = "U"
		return circuit

	# If the node is an NOR gate output, solve and return the output
	if circuit[node][0] == "NOR":
		# Initialize the output to 1
		circuit[node][3] = '1'
		# Initialize also a variable that detects a U to false
		unknownTerm = False  # This will become True if at least one unknown terminal is found

		# if there is a 1 terminal, NOR changes the output to 0. Otherwise, keep it at 1
		for term in terminals:
			if circuit[term][3] == '1':
				circuit[node][3] = '0'
				break
			if circuit[term][3] == "U":
				unknownTerm = True
		if unknownTerm:
			if circuit[node][3] == '1':
				circuit[node][3] = "U"
		return circuit

	# If the node is an XOR gate output, solve and return the output
	if circuit[node][0] == "XOR":
		# Initialize a variable to zero, to count how many 1's in the terms
		count = 0

		# if there are an odd number of terminals, XOR outputs 1. Otherwise, it should output 0
		for term in terminals:
			if circuit[term][3] == '1':
				count += 1  # For each 1 bit, add one count
			if circuit[term][3] == "U":
				circuit[node][3] = "U"
				return circuit

		# check how many 1's we counted
		if count % 2 == 1:  # if more than one 1, we know it's going to be 0.
			circuit[node][3] = '1'
		else:  # Otherwise, the output is equal to how many 1's there are
			circuit[node][3] = '0'
		return circuit

	# If the node is an XNOR gate output, solve and return the output
	elif circuit[node][0] == "XNOR":
		# Initialize a variable to zero, to count how many 1's in the terms
		count = 0

		# if there is a single 1 terminal, XNOR outputs 0. Otherwise, it outputs 1
		for term in terminals:
			if circuit[term][3] == '1':
				count += 1  # For each 1 bit, add one count
			if circuit[term][3] == "U":
				circuit[node][3] = "U"
				return circuit

		# check how many 1's we counted
		if count % 2 == 1:  # if more than one 1, we know it's going to be 0.
			circuit[node][3] = '1'
		else:  # Otherwise, the output is equal to how many 1's there are
			circuit[node][3] = '0'
		return circuit

	circuit[unnamedSA[1]] = list(holdTheWire).copy()
	# Error detection... should not be able to get at this point
	return circuit[node][0]


# -------------------------------------------------------------------------------------------------------------------- #
# FUNCTION: Updating the circuit dictionary with the input line, and also resetting the gates and output lines
def inputRead(circuit, line):
	# Checking if input bits are enough for the circuit
	if len(line) < circuit["INPUT_WIDTH"][1]:
		return -1

	# Getting the proper number of bits:
	line = line[(len(line) - circuit["INPUT_WIDTH"][1]):(len(line))]

	# Adding the inputs to the dictionary
	# Since the for loop will start at the most significant bit, we start at input width N
	i = circuit["INPUT_WIDTH"][1] - 1
	inputs = list(circuit["INPUTS"][1])
	# dictionary item: [(bool) If accessed, (int) the value of each line, (int) layer number, (str) origin of U value]
	for bitVal in line:
		bitVal = bitVal.upper()  # in the case user input lower-case u
		circuit[inputs[i]][3] = bitVal  # put the bit value as the line value
		circuit[inputs[i]][2] = True  # and make it so that this line is accessed

		# In case the input has an invalid character (i.e. not "0", "1" or "U"), return an error flag
		if bitVal != "0" and bitVal != "1" and bitVal != "U":
			return -2
		i -= 1  # continuing the increments

	return circuit


# -------------------------------------------------------------------------------------------------------------------- #
# FUNCTION: the actual simulation #
def basic_sim(circuit):
	# QUEUE and DEQUEUE
	# Creating a queue, using a list, containing all of the gates in the circuit
	queue = list(circuit["GATES"][1])
	i = 1

	while True:
		i -= 1
		# If there's no more things in queue, done
		if len(queue) == 0:
			break

		# Remove the first element of the queue and assign it to a variable for us to use
		curr = queue[0]
		queue.remove(curr)

		# initialize a flag, used to check if every terminal has been accessed
		term_has_value = True

		# Check if the terminals have been accessed
		for term in circuit[curr][1]:
			if not circuit[term][2]:
				term_has_value = False
				break

		##part2 skip this cuz this is a SA wire
		if circuit[curr][2] == True:
			continue

		if term_has_value:
			circuit[curr][2] = True
			circuit = gateCalc(circuit, curr)

			# ERROR Detection if LOGIC does not exist
			if isinstance(circuit, str):
				print(circuit)
				return circuit

			print("Progress: updating " + curr + " = " + circuit[curr][3] + " as the output of " + circuit[curr][
				0] + " for:")
			for term in circuit[curr][1]:
				print(term + " = " + circuit[term][3])
		# print("\nPress Enter to Continue...")
		# input()

		else:
			# If the terminals have not been accessed yet, append the current node at the end of the queue
			queue.append(curr)

	return circuit


def fault_cvg_result ( ckt_file , f_list_name , tv_file ) :
	fs_result = open("fault_sim_result.txt", "w+")
	fs_result.write("#input: " + ckt_file + "\n")
	fs_result.write("#input: " + f_list_name + "\n")
	fs_result.write("#input: " + input_name + "\n")
	fs_result.write("\n")
	# simulate no faults circuit
	circuit = basic_sim(circuit)
	print("\n *** Finished simulation - resulting circuit: \n")
	print(circuit)
	# Jasmine-this shows output
	for y in circuit["OUTPUTS"][1]:
		if not circuit[y][2]:
			output = "NETLIST ERROR: OUTPUT LINE \"" + y + "\" NOT ACCESSED"
			break
		output = str(circuit[y][3]) + output

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
					if(len(binary_value) > 8):
						binary_value = '00000000'
						temp1 = 0
					else:
						binary_value = binary_value
#find out number of zeros to append to binary value
					rem = 8-len(binary_value)
#append zeros to value
					binary_value = '0'*rem + binary_value
					if (bits_per_line + 8 <= number_of_input_bits):
							OutputFile.write(binary_value)
					else:
							OutputFile.write(binary_value[0:(number_of_input_bits - bits_per_line )])
							OutputFile.write('\n')
					bits_per_line += 8
					temp1 += 1
			temp += 1
# generating TV_D.txt

# generating TV_E.txt


def fault_coverage(batch_size, bench_file):
	TVS = ["TV_A.txt", "TV_B.txt", "TV_C.txt", "TV_D.txt", "TV_E.txt"]
	tvs = [tv_a[0:24], tv_b[0:24], tv_c[0:24], tv_d[0:24], tv_e[0:24]]
	# print first line stuff to f_cvg.csv
	# JEM-Creating fault cvg file to write,read, append to
	f_cvg = open("f_cvg.csv", "w+")
	f_cvg.write("|BATCH #|    A    |    B    |    C    |    D    |    E    | seed=")
	# open tv_a file
	# get first line
	# convert binary to dec and f_cvg.write
	# print seed ? grab line from first file? or how do i know seed from first file --- TODO - sai
	f_cvg.write("| batch size = batch_size  |\n")
	f_cvg.write("---------------------------------------------------------------------------------------------------")
	batch = 0
	while batch < 25:
		print("currently testing batch #:" + (batch+1) + "\n")
		for tv_num in TVS:
			current_tv_file = TVS[tv_num]
			netFile = open(current_tv_file, "r")
			print("opened" + current_tv_file + "\n")
			while i < batch_size:
				# iterate thru TVS in each file
				#run prev script and append every time new tvs and pull new fault cvg value
					# need to save variable in list of prev percent covered by list

				i += 1

		batch += 1


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
		# validate input to do optional
		bench_file = input("input bench file name: \n ")
		integer_seed = int(input("input integer seed: \n "))
		tv_generation(bench_file, integer_seed)
	elif user_choice == 2:
		print("performing fault coverage \n")
		batch_size = int(input("input batch size: \n "))
		bench_file = input("input bench file name: \n ")
		fault_coverage(batch_size, bench_file)

main()





