#!/usr/bin/env python

from mrjob.job import MRJob


class MRCountryCounter(MRJob):
    def mapper(self, _, line):
        line = line.split(",")
        country = line[-1]
        print line[0], country
        yield country, 1

    def reducer(self, country, occurrences):
        yield country, sum(occurrences)

if __name__ == '__main__':
    MRCountryCounter.run()