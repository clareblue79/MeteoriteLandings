#!/usr/bin/env python


import sys

def read_input(file):
    for line in file:
 
        yield line.split(",")

def main(separator='\t'):

    data = read_input(sys.stdin)
    print data[9] + "\t" + "1" 

if __name__ == "__main__":
    main()