#!/usr/bin/env python
import pathlib2, sys, os, argparse, re

parser = argparse.ArgumentParser()
parser.add_argument('-i', dest='I', action='store', type=str, nargs=1, help='input (gziped) file')
parser.add_argument('-o', dest='O', action='store', type=str, nargs='?',
                    help='output directory for your split file, default= home/Scripts/out')
parser.add_argument('-m', dest='B', action='store', type=int, nargs='?', default=1, help='number of megabytes for your chunks, default= 1')
parser.add_argument('-n', dest='N', action='store', type=int, nargs='?', default=None,
                    help='number of outputfiles, 1 for a sample, default= total mb/chunk size')


def open_up(fn):
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
    #out_dir = 'home/Scripts/out/filename/file'
    home = str(pathlib2.Path.home())
    out_dir = os.path.abspath("%s/Scripts/out" % home).rstrip('/')
    num_fls = None
    #split path string to obtain file name
    split_fn = re.split(r'\\|/', fn)[-1].split(".")[0]
    print(split_fn)

    #if a second parameter is given, this is the output directory
    if o:
        out_dir = o.rstrip("/")
    if n:
        # number of bytes equal to 1 mb
        num_byts = int(n)*1048576
    if l:
        # number of wanted ouput files
        num_fls = int(l)

    split_nm = 0
    cum_bytes = 0
    with open_up(fn) as fin:
        #output filename is output_dir/filename/split_file.txt
        fout_dir = "%s/%s/%s" % (out_dir, split_fn, split_fn)
        fout = "%s_%d%s" % (fout_dir, 0, '.txt')
        print('fout %s '%(fout) )
        #check if dir exist
        checkdir(fout)
        fout = open(fout, "w")
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
                fout = "%s_%d%s" % (fout_dir, split_nm, '.txt')
                fout = open(fout, "w")

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

#call from command line to initiate program
if __name__ == '__main__':
    #defaults for the params
    out_dir = None
    num_byts = None
    num_fls = None

    args = parser.parse_args()

    fn = args.I
    if args.I:
        fn = args.I[0]
    else:
        # if input file is not given, print info, close
        parser.print_help()
        exit(1)
    if args.O:
        out_dir = args.O[0]
    if args.B:
        num_byts = args.B
    if args.N:
        num_fls = args.N
    # do the thing
    split_this_file(fn, out_dir, num_byts, num_fls)
