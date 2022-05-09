'''
Test if the zip files are not corrected
'''

from __future__ import print_function
from __future__ import division

import sys
import zipfile
import glob
import os
import time

def test_zipfile(filepath):
    '''
    Test whether a zipfile is valid
    Some lines were taken from http://stackoverflow.com/questions/4875747/python-script-to-check-if-a-zip-file-is-corrupt
    '''
    start_time = time.time()
    filesize = os.path.getsize(filepath)
    print('Starting testing file: {0} ({1:.2f} MB)'.format(filepath,filesize/10**6), end='')
    the_zip_file = zipfile.ZipFile(filepath)
    ret = the_zip_file.testzip()
    time_spent = time.time() - start_time
    print('\tTest ended. Time spent: {0:.2f} s'.format(time_spent))
    if ret is not None:
        print("First bad file in zip {0}: {1}".format(filepath,ret))
        is_valid = False
    else:
        #print "Zip file is good."
        is_valid = True

    return is_valid, time_spent, filesize


def main():

    # Parameters
    zipfiles_root_folder = '.'
    log_filepath_corrupted = 'result_corrupted.log'
    log_file_corrupted = open(log_filepath_corrupted, 'w')
    log_filepath_valid = 'result_valid.log'
    log_file_valid = open(log_filepath_valid, 'w')
    zipfile_filepaths = sorted(glob.iglob(os.path.join(zipfiles_root_folder, '*', '*.zip'))) # Modify this to whatever folders you need

    # Testing zipfiles
    start_time = time.time()
    total_filesize = 0
    number_of_corrupted_zipfile = 0
    for zipfile_filepath in zipfile_filepaths: # generator, search immediate subdirectories
        is_valid, test_zipfile_time_spent, filesize = test_zipfile(zipfile_filepath)
        total_filesize += filesize
        if is_valid:
            log_file_valid.write('{0}\n'.format(zipfile_filepath))
        else:
            log_file_corrupted.write('{0}\n'.format(zipfile_filepath))
            number_of_corrupted_zipfile += 1

    # Cleaning  
    log_file_corrupted.close()
    log_file_valid.close()

    time_spent = time.time() - start_time
    print('Total time spent was {0:.2f} seconds, checking {1} files, totaling {2:.2f} GB, among which {3} were corrupted.'.format(time_spent, len(zipfile_filepaths),total_filesize/10**9,number_of_corrupted_zipfile))


if __name__ == "__main__":
    main()
    #cProfile.run('main()') # if you want to do some profiling