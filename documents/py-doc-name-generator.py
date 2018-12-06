import os
import random
from shutil import copyfile

previously_assigned = []

def sum_digits(n):
    s = 0
    while n:
        s += n % 10
        n //= 10
    return s

def generate_random_number_digits_sum_is_even():
    random_number = random.randint(1000000000,9999999999)
    ds = sum_digits(random_number)
    if ds % 2 == 0:
        return [random_number, True]
    else:
        return [random_number, False]

def generate_random_odd():
    [random_number, is_even] =  generate_random_number_digits_sum_is_even()
    while (is_even == True) and (random_number not in previously_assigned):
        [random_number, is_even] =  generate_random_number_digits_sum_is_even()
    previously_assigned.append(random_number)
    return random_number

def generate_random_even():
    [random_number, is_even] =  generate_random_number_digits_sum_is_even()
    while (is_even == False) and (random_number not in previously_assigned):
        [random_number, is_even] =  generate_random_number_digits_sum_is_even()
    previously_assigned.append(random_number)
    return random_number

def rename_cvs(input_dir, output_dir):
    for filename in os.listdir(input_dir):
        fname, file_extension = os.path.splitext(filename)
        src = input_dir + fname + file_extension
        newFileName = generate_random_even()
        dest = output_dir + str(newFileName) + file_extension
        print "renaming "+ src+ " to "+dest + " sum digits = "+ str(sum_digits(newFileName))
        copyfile(src, dest) 

def rename_invoices(input_dir, output_dir):
    for filename in os.listdir(input_dir):
        fname, file_extension = os.path.splitext(filename)
        src = input_dir + fname + file_extension
        newFileName = generate_random_odd()
        dest = output_dir + str(newFileName) + file_extension
        print "renaming "+ src+ " to "+dest + " sum digits = "+ str(sum_digits(newFileName))
        copyfile(src, dest) 


if __name__ == '__main__':
    pwd = os.path.dirname(os.path.realpath(__file__))
    rename_cvs(pwd + "\\cvs\\", os.path.dirname(os.path.realpath(__file__))+"\\output\\")
    rename_invoices(pwd +"\\invoices\\", os.path.dirname(os.path.realpath(__file__))+"\\output\\")
