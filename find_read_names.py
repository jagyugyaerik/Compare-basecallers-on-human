from sys import argv

def main():
    read_info = argv[1]
    read_list = []
    common_reads = []


    with open("02_basecalled_reads/chiron.fastq") as fq_file:
        data = fq_file.readlines()
        for line in data:
            if line.startswith('@'):
                read_list.append(line[1:-1])

    with open(read_info, "rt") as read_file:
        header = read_file.readline()
        reads = read_file.readlines()
        for read in reads:
            sread = read.split('\t')
            if sread[1] in read_list:
                common_reads.append([sread[0], sread[1]])

    print('\t'.join(["Name", "Fast5 name"]))
    for row in common_reads:
        print('\t'.join(row))


if __name__ == '__main__':
    main()