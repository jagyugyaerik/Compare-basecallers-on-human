from sys import argv

def main():
    fastq = argv[1]
    common_reads = argv[2]

    common_id = []
    common_fast5 = []
    with open(common_reads) as reads:
        for line in reads:
            common_id.append(line.split('\t')[0])
            common_fast5.append(line.split('\t')[1])

    with open(fastq) as fastq:
        for line in fastq:
            if line.split(' ')[0][1:] in common_id:
                seq = next(fastq).strip()
                next(fastq)
                qual = next(fastq).strip()
                print('@' + line[:-1])
                print(seq)
                print('+')
                print(qual)


if __name__ == '__main__':
    main()