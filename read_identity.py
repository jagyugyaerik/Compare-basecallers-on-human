from collections import defaultdict
from sys import argv
from statistics import mean


def get_read_lengths(read_filename):
    read_lengths = {}

    with open(read_filename, "rt") as read:
        for line in read:
            name = line.strip()[1:].split()[0]
            seq = next(read).strip()
            next(read)
            next(read)
            read_lengths[name] = len(seq)
    return read_lengths


def main():
    read_alignments = defaultdict(list)

    read_filename = argv[1]
    paf_filename = argv[2]

    read_lengths = get_read_lengths(read_filename)

    with open(paf_filename) as paf:
        for line in paf:
            paf_parts = line.strip().split('\t')

            read_name = paf_parts[0]
            read_length = int(paf_parts[1])
            read_start = int(paf_parts[2])
            read_end = int(paf_parts[3])
            ref_start = int(paf_parts[7])
            ref_end = int(paf_parts[8])
            identity = 100.0 * int(paf_parts[9]) / int(paf_parts[10])

            read_alignments[read_name].append((read_start, read_end, ref_start, ref_end, identity))

    print('\t'.join(['Name', 'Length', 'Identity', 'Relative length']))
    read_names = sorted(read_lengths.keys())
    for read_name in read_names:
        read_length = read_lengths[read_name]
        alignments = read_alignments[read_name]
        identity_by_base = [0.0] * read_length

        total_read_length = 0
        total_ref_length = 0

        for read_start, read_end, ref_start, ref_end, identity in alignments:
            for i in range(read_start, read_end):
                if identity > identity_by_base[i]:
                    identity_by_base[i] = identity
            total_read_length += read_end - read_start
            total_ref_length += ref_end - ref_start

        # If less than half the read aligned, then we call it an unaligned read.
        if identity_by_base.count(0.0) > read_length / 2.0:
            whole_read_identity = 0.0

        # Otherwise, the read's identity is the average of the aligned parts.
        else:
            whole_read_identity = mean([x for x in identity_by_base if x > 0.0])

        if whole_read_identity > 0.0:
            relative_length = str(100.0 * total_read_length / total_ref_length)
        else:
            relative_length = ''

        print('\t'.join([read_name, str(read_length), str(whole_read_identity), relative_length]))


if __name__ == '__main__':
    main()