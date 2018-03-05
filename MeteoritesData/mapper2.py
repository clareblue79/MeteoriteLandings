#!/usr/bin/env python


import sys

for line in sys.stdin:
    line = line.split(",")
    print '%s\t%s' % (line[9], 1)
