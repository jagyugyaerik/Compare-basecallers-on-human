from sys import argv, exit
from re import search


def load_fastq(input_fastq):
    reads = []

    with open(input_fastq, "rt") as fastq:
        for line in fastq:
            name = line.strip()[1:]
            seq = next(fastq).strip()
            _ = next(fastq).strip()
            qual = next(fastq).strip()
            reads.append([name, seq, qual])
    return reads


def main():
    input_reads_filename = argv[1]
    read_id_to_fast5_filename = argv[2]

    read_id_to_fast5, fast5_to_read_id = {}, {}
    with open(read_id_to_fast5_filename, "rt") as read_id_to_fast5_file:
        for line in read_id_to_fast5_file.readlines():
            read_id, fast5 = line.split('\t')
            if fast5.endswith('\n'):
                fast5 = fast5[:-1]
            if fast5.endswith(".fast5"):
                fast5 = fast5[:-6]
            if read_id in read_id_to_fast5_file:
                exit("Error: duplicate read ID in: " + read_id_to_fast5_filename + ": " + read_id)
            if fast5 in read_id_to_fast5_file:
                exit("Error: duplicate fast5 file in: " + read_id_to_fast5_filename + ": " + fast5)
            read_id_to_fast5[read_id] = fast5
            fast5_to_read_id[fast5] = read_id


    reads = load_fastq(input_reads_filename)

    output_reads = []


    for header, seq, qual in reads:
        read_id, fast5_name = None, None
        try:
            read_id = search(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", header).group(0)
        except AttributeError:
            read_id = None
        try:
            fast5_name = search(r'\w+_ch\d+_read\d+_\w+', header).group(0)
        except AttributeError:
            fast5_name = None
        if read_id is None and fast5_name is None:
            exit('Error: could not parse read header\n' + header)

        if read_id is not None:
            new_header = read_id + ' ' + read_id_to_fast5[read_id]
        else:
            new_header = fast5_to_read_id[fast5_name] + ' ' + fast5_name

        output_reads.append([new_header, seq, qual])

    output_reads = sorted(output_reads)

    for header, seq, qual in output_reads:
        print('@' + header.strip())
        print(seq)
        print('+')
        print(qual)


if __name__ == '__main__':
    main()