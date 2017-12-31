from sys import argv

def get_reads(fastq):
    data = []
    with open(fastq, "rt") as read:
        for line in read:
            if line.startswith('@'):
                data.append(line[1:])
        return data


def main():
    read_list = []
    common_reads = None

    for fastq in argv:
        if not ("find_read_names.py" in fastq):
            data = get_reads(fastq)
            common_reads = data if common_reads is None else list(set(common_reads).intersection(data))

    for row in common_reads:
        print row.strip()


if __name__ == '__main__':
    main()