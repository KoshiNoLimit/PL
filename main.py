from work_creator import funcs_from_file, samples_from_func
from enclosure import *

funcs = funcs_from_file('program.txt')

funcs_samples = [samples_from_func(func) for func in funcs]

print(funcs_samples)

for func_samples in funcs_samples:

    for i in range(len(func_samples)):
        for j in range(i + 1, len(func_samples)):
            print('\033[32m' + func_samples[i] + ' \033[33m;\t' +
                  '\033[32m' + func_samples[j] + ' \033[33m:\t' +
                  '\033[30m' + str(enclosure(func_samples[i], func_samples[j])))
