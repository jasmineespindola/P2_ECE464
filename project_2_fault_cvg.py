# user interface
#comment testing
#comment test sai
#comment test jasmine
print("\t\t\tProject 2: Fault Coverage of Pseudo Random TV's  /n")
user_choice = 0
while user_choice <= 0 | user_choice > 2:
	user_choice = input("choose what you'd like to do (1,2): \n ")
	int(user_choice)
	print(" error. invalid user option. try again")

# 1: test vector generation
if user_choice == 1:
	print("performing test vector generation")
# input : circuit.bench  integer seed
# validate input   JEM- to do
bench_file = input("input bench file name: \n ")
integer_seed = input("input integer seed: \n ")
int(integer_seed)

tv_generation(bench_file, integer_seed ) //function call

# generating TV_A.txt
# use seed as starting point and extend zeros until length
# Nbitcounter function
# generating TV_B.txt
# generating TV_C.txt
# generating TV_D.txt
# generating TV_E.txt


# 2: fault coverage
else:
	print("performing test vector generation")



