
import sys


output_number = sys.argv[1]

with open('output.txt', 'r') as output:
    with open(f'output_{output_number}.txt', 'r') as right_output:
        line = output.readline()
        right_line = right_output.readline()
        while(line):
            if line != right_line:
                print(f'my line:    {line}\nright line: {right_line}\n\n')
            line = output.readline()
            right_line = right_output.readline()
print("end")
