from sys import argv
from get_read_info import find_fast5_files

def main():
    fixed_reads = argv[1]

    common_reads = []

    reads_list = find_fast5_files(argv[1], ".fastq")

    for read in reads_list:
        read_ids = []
        with open(read) as fastq:
            for line in fastq:
                if line.startswith('@'):
                    read_ids.append(line[1:].strip().split(' ')[0])
        if common_reads == []:
            common_reads = read_ids
        else:
            common_reads = list(set(common_reads).intersection(read_ids))

    for read in reads_list:
        out_read = []
        with open(read) as fastq:
            for line in fastq:
                if line.startswith('@'):
                    read_id = line[1:].strip().split()[0]
                    if read_id in common_reads:
                        seq = next(fastq)
                        _ = next(fastq)
                        qual = next(fastq)
                        out_read.append([line, seq, _, qual])

            with open("04_extract_reads/" + read.split('/')[-1], "wt") as out:
                for row in out_read:
                    for r in row:
                        out.write(r)

if __name__ == '__main__':
    main()