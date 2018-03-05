#!/usr/bin/env python

from mrjob.job import MRJob


class MRMassCounter(MRJob):
    def mapper(self, _, line):
        line = line.split(",")
        country = line[-1]
        
        if len(line) == 10:
            mass = line[4]
        elif len(line) == 11:
            mass = line[5]
        else:
            mass = 0
        
        if mass:
            print mass, line[0]
            yield country, float(mass)

    def reducer(self, country, occurrences):
        yield country, sum(occurrences)

if __name__ == '__main__':
    MRMassCounter.run()