#!/usr/bin/env python
import pathlib, sys, shlex, subprocess, os

def usage():
    #default directory is: ~/Scripts/out/inputfilename)
    print("Command format: splitter.py *file*(required) *output_directory*('d' for default) *number_of_megabytes*('d'for default) *number_of_files*('d' for default)")

def get_path(fpath):
    fpath = "../Datasets/"+fpath
    return os.path.join(os.path.dirname(__file__), fpath)

def myopen(fn):
    import gzip
    try:
        h = gzip.open(fn)
    # read arbitrary bytes so check if @param fn is a gzipped file
        h.read(2)
    except:
        # cannot read in gzip format
        return open(fn)
    h.close()
    return gzip.open(fn)

def split_this_file(f, o, n, l ):
    #filename is the first parameter
    fn = f
    #default maximum number of bytes per split file and default output directory
    num_byts = 104857600
    #out_dir = "~/BashScripts/out"
    home = str(pathlib.Path.home())
    out_dir = os.path.abspath("%s/Scripts/out" % home)
    print("outdir: " + out_dir)
    num_fls = None
    #split path string to obtain file name
    split_fn = (fn.split("/")[-1]).split(".")[0]

    #if a second parameter is given, this is the output directory
    if o:
        out_dir = o.rstrip("/")
    if n:
        num_byts = int(n)*1048576
    if l:
        num_fls = int(l)

    split_nm = 0
    cum_bytes = 0
    with myopen(fn) as fin:
        #output filename is output_dir/filename/split_file.txt
        fout_name = "%s/%s/%s0.txt" % (out_dir, split_fn, split_fn)
        #check if dir exist
        checkdir(fout_name)
        fout = open(fout_name, "wb")
        for i, line in enumerate(fin):
            fout.write(line)
            cum_bytes += sys.getsizeof(fout)
            #if max number of bytes is reached, close file, open new file
            if cum_bytes >= num_byts:
                cum_bytes = 0
                split_nm += 1
                fout.close()
                if num_fls:
                    num_fls -= 1
                    if num_fls == 0:
                        exit_program(out_dir, split_fn, fout)
                        return
                fout_name = "%s/%s/%s%d.txt" % (out_dir, split_fn, split_fn, split_nm)
                #checkdir(fout_name)
                fout = open(fout_name, "wb")

        exit_program(out_dir, split_fn, fout)
        return

def exit_program(out_dir, split_fn, fout):
    fout.close()
    print("split succesful! Files in: %s/%s"%(out_dir, split_fn))


def checkdir(filename):
    #translate directory name, check if it exists, else create new
    dirname = os.path.dirname(os.path.abspath(filename))
    if not os.path.exists(dirname):
        os.makedirs(dirname)
#arguments: [0]: .py [1]: filename [2]: output_dir [3]: num_byts [4]: num_files
if __name__ == '__main__':
    #no second paramater given: output dir: None
    out_dir = None
    num_byts = None
    num_fls = None
    #if less than 1 or more than 2 params are given, call usage, exit program
    if len(sys.argv) not in range(2, 6):
        usage()
        sys.exit(1)
    #if output dir param is given, assign variable
    elif len(sys.argv) >= 3:
        if sys.argv[2] != "d":
            out_dir = sys.argv[2]
        if len(sys.argv) >= 4:
            if sys.argv[3] != "d":
                num_byts = sys.argv[3]
            if len(sys.argv) == 5:
                num_fls = sys.argv[4]
    #filename is first parameter
    fn = sys.argv[1]
    #call file splitter function
    split_this_file(fn, out_dir, num_byts, num_fls)
