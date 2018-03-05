#!/usr/bin/env python

from mrjob.job import MRJob


class MRyearCounter(MRJob):
    
    def mapper(self, _, line):
        line = line.split(",")
        year = "0"
        date = ""
        if len(line) == 10: 
            date = line[6]

        elif len(line) == 11: 
            date = line[7]
        else: 
            year = "0"
            
        if date:
            year = date.split('/')[2][:4]
            
        if len(year) == 4:
            decade = year[:3] + '0'
        elif len(year) == 3:
            decade = year[:2] + '0'
        else:
            decade = "0"
            
        if len(line) == 10:
            mass = line[4]
        elif len(line) == 11:
            mass = line[5]
        else:
            mass = 0
            
       
        if mass: 
            yield decade, float(mass)

    def reducer(self, country, occurrences):
        yield country, sum(occurrences)

if __name__ == '__main__':
    MRyearCounter.run()