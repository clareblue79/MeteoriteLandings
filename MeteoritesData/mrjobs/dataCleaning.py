#!/usr/bin/env python

from mrjob.job import MRJob


class MRCountryCounter(MRJob):
    def mapper(self, _, line):
        lineL = len(line.split(','))
        yield lineL, 1

    def reducer(self, lineL, occurrences):
        yield lineL, sum(occurrences)

if __name__ == '__main__':
    MRCountryCounter.run()