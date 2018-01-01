from __future__ import division
from sys import argv
from re import  findall

from statistics import mean

def main():
    sam_file = argv[1]
    read_indel = []

    cigar = {'M':0, 'I':0, 'D':0, 'S':0, 'H':0}
    with open(sam_file, "rt") as sfile:
        next(sfile)
        next(sfile)
        for line in sfile:
            cline = line.split('\t')
            matches = findall(r'(\d+)(\w)', cline[5])
            for row in matches:
                cigar[row[1]] += int(row[0])

            all = cigar['M'] + cigar['I'] + cigar['D']

            read_indel.append([cline[0], str(cigar['I']/all), str(cigar['D']/all), str(cigar['M']/all)])

    insertions = []
    deletions = []
    matches = []
    for row in read_indel:
        print('\t'.join(row))
        insertions.append(float(row[1]))
        deletions.append(float(row[2]))
        matches.append(float(row[3]))

    print('\t'.join(["statistics:", str(mean(insertions)), str(mean(deletions)), str(mean(matches))]))

if __name__ == '__main__':
    main()