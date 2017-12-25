from h5py import File
from os import walk, path
from sys import argv
from re import compile


def find_fast5_files(directory):
    fast5 = []
    for dir, _, filenames in walk(directory):
        for filename in filenames:
            if filename.endswith(".fast5"):
                fast5.append(path.join(dir, filename))
    return  fast5


def get_hdf5_keys(read):
    keys = []
    read.visit(keys.append)
    return keys


def get_hdf5_read_id(read, keys):
    r = compile(r"Raw/Reads/Read_\d+$")
    key = [x for x in keys if r.search(x)]
    key = key[0]
    return read[key].attrs["read_id"].decode()


def get_hdf5_signal_length(read, keys):
    key = [x for x in keys if x.endswith("Signal")]
    assert len(key) == 1
    key = key[0]
    return read[key].shape[0]


def get_hdf5_start_time(read, keys):
    r = compile(r"Raw/Reads/Read_\d+$")
    key = [x for x in keys if r.search(x)]
    key = key[0]
    return read[key].attrs["start_time"]


def main():
    print("\t".join(["Name", "Fast5 name", "Signal lenght", "Start time"]))
    rows = []
    count = 0
    for fast5 in find_fast5_files(argv[1]):
        fast5_name = fast5.split("/")[-1][:-6]
        with File(fast5) as read:
            keys = get_hdf5_keys(read)
            read_id = get_hdf5_read_id(read, keys)
            singal_length = get_hdf5_signal_length(read, keys)
            start_time = get_hdf5_start_time(read, keys)
            count += 1
            rows.append([read_id, fast5_name, str(singal_length), str(start_time)])

    rows = sorted(rows)
    for row in rows:
        print("\t".join(row))


if __name__ == '__main__':
    main()