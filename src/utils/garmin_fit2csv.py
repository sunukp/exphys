
import glob
import getopt
import sys
import garmin_utils as garmin_utils

def main():
    '''
    Decodes .fit files within fitdir (specified by -i) and writes to .csv to outdir (specified by -o).
    Default fitdir, outdir are the g_metabolic.
    XXX flag -f to be implemented.
    '''

    fitdir = '/mnt/g/.shortcut-targets-by-id/1-6mtIysTt6KZ8hY5Og2yon-5n2U-QKtW/fenix_sunuk_shared/metabolic/garmin/daily'
    activity_files = glob.glob(fitdir + "/*ACTIVITY.fit")
    outdir = fitdir
    fname = None

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'i:o:f:')
        for opt, arg in opts:
            if opt in ['-i']:
                fitdir = arg
                activity_files = glob.glob(fitdir + "/*.fit")
            elif opt in ['-o']:
                outdir = arg
            elif opt in ['-f']:
                # process only the specified file
                fname = arg
    except Exception as err:
        print(err)

    if fname is not None:
        activity_files = [fname]
    
    for full in activity_files:
        fn = full.split('/')[-1]
        
        outfn = fn.replace('.fit', '.csv')

        try:
            lines = garmin_utils.read_fit_acvitity(full)
            full_outfn = outdir + '/' + outfn
            print(full_outfn)
            with open(full_outfn, 'w') as outf:
                outf.write(','.join(garmin_utils.ACTIVITY_FEATURE_NAMES) + '\n')
                outf.writelines('\n'.join(lines))
                outf.write('\n')

        except Exception as err:
            print(fn, err)


if __name__ ==  '__main__':
    main()

