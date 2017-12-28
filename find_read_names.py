from sys import argv

def main():
    read_info = argv[1]
    read_list = []
    common_reads = []

    with open("03_read_information/chiron.fastq") as fq_file:
        for line in fq_file:
            if line.startswith('@'):
                read_list.append(line.split(' ')[0][1:])

    with open(read_info, "rt") as read_file:
        for read in read_file:
            read_id, fast5 = read.split('\t')
            if read_id in read_list:
                common_reads.append([read_id, fast5[:-1]])

    for row in common_reads:
        print('\t'.join(row))


if __name__ == '__main__':
    main()