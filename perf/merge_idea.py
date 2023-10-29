# Import the perf module
import perf

# Define the input files
perf_file = "perf.data" # The file that contains the perf annotation
test_file = "test.org" # The file that contains the test case name
lisp_file = "lisp.el" # The file that contains the lisp code

# Define the output file
bpf_file = "bpf.bt" # The file that will contain the bpftrace script

# Open the input files
perf_data = open(perf_file, "r")
test_data = open(test_file, "r")
lisp_data = open(lisp_file, "r")

# Read the test case name from the test file
test_case = test_data.readline().strip()

# Parse the perf annotation using the perf module
perf_parser = perf.PerfParse(perf_data)
perf_parser.parse()

# Get the first event from the perf annotation
event = perf_parser.events[0]

# Get the function name, address, instruction, and cycles from the event
func_name = event.symbol.name
func_addr = event.ip
instr = event.line
cycles = event.cycles

# Read the lisp code from the lisp file
lisp_code = lisp_data.read()

# Find the lisp function definition that matches the function name
lisp_func = "(defun " + func_name + " "
lisp_start = lisp_code.find(lisp_func)

# Find the end of the lisp function definition
lisp_end = lisp_code.find(")", lisp_start)

# Extract the lisp function definition
lisp_def = lisp_code[lisp_start:lisp_end+1]

# Split the lisp function definition by whitespace
lisp_parts = lisp_def.split()

# Get the lisp function name and arguments from the lisp parts
lisp_name = lisp_parts[1]
lisp_args = lisp_parts[2:-1]

# Generate a bpftrace script that attaches a user probe to the function address
bpf_script = f"""
uprobe:/usr/bin/emacs:{func_addr}
{{
    // Print out the function name, instruction, cycles, test case name, and arguments
    printf("%s %s %d %s", {func_name}, {instr}, {cycles}, {test_case});
    // Loop through each argument of the lisp function
    foreach (arg in {lisp_args})
    {{
        // Get the value of the argument from user memory using usym
        $val = usym(arg);
        // Print out a comma and then the value of the argument
        printf(", %s", $val);
    }}
    // Print out a newline at the end
    printf("\\n");
}}
"""

# Open the output file
bpf_data = open(bpf_file, "w")

# Write the bpftrace script to the output file
bpf_data.write(bpf_script)

# Close all files
perf_data.close()
test_data.close()
lisp_data.close()
bpf_data.close()
