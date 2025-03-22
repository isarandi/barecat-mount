# Mounting Barecat archives via FUSE

## Background
[Barecat](https://github.com/isarandi/barecat) is a simple and highly scalable aggregate storage format for storing many (tens of millions and more) small files, with focus on fast random access and minimal overhead. You can think of it as a filesystem-in-file, or as a key-value store. Data is stored sequentially in a flat file (or multiple shard files) and an SQLite database is used to index the data. The index is used to quickly locate the data of a file by its path and to 
provide directory listings, file statistics, and other metadata. It can handle at least tens of millions of files and terabytes of data, even over 100k files in
single directories. Directory listing is written to produce the results in a streaming fashion,
so entries will start appearing even in huge directories fairly quickly. 

Barecat archives can be mounted via FUSE, allowing it to be used like a filesystem locally. This is useful for browsing the contents of the archive, for reading and writing files. This is mostly for inspecting the data and making smaller changes, but for the main workload (e.g. training a deep learning model), you should use the Python API, which is more efficient as it directly accesses the data without the overhead of FUSE.

## Installation

```bash
sudo apt-get install libfuse-dev  # or its equivalent with other package managers
pip install git+https://github.com/isarandi/barecat-mount.git
```

## Usage

```bash

# readonly:
barecat-mount mydata.barecat mountpoint/

# read-write:
barecat-mount --writable mydata.barecat mountpoint/

# unmount:
fusermount -u mountpoint/
# or
umount mountpoint/
```  

### A Note on Fragmentation

Since Barecat always adds new files at the end of the archive, many deletions and insertions
will lead to fragmentation. The general idea is to write once, read many times, and do
deletions only when you need to fix a mistake. There is basic heuristic auto-defragmentation
that can be enabled as follows:

```bash
barecat-mount --writable --enable-defrag mydata.barecat mountpoint/
```

This way, the filesystem will periodically defragment itself after significant amount of deletions.
You can also perform a defrag with:

```bash
barecat-defrag mydata.barecat
```

This will go in sequence and move all the files towards the beginning of the archive, leaving
no gaps. This may take very long, since even closing one byte gap requires moving all the
following data. A quick option is available with:

```bash
barecat-defrag --quick mydata.barecat
```

This will proceed backwards, starting from the end of the archive, and will move each file
into the first available gap, counted from the beginning of the archive (first-fit). The 
algorithm stops after meeting the first file that has no gap that can fit it.
