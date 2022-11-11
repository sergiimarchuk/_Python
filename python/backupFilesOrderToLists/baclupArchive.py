#!/usr/bin/python
import sys, getopt
import os, fnmatch
import shutil

print ('Number of arguments:', len(sys.argv), 'arguments.')
print ('Argument List:', str(sys.argv))
#print(sys.argv[1])



def listingFileFunct1():
  with open("listFile.txt", "rb") as lf:
      for var_path in lf:
          print("- - - - - - - - Working finding file name : - " + var_path.rstrip().decode("utf-8") + " - File name"); print()
          with open("listPath.txt", "rb") as lp:
              for var_file in lp:
                  print(var_file.rstrip().decode("utf-8"), " . + . + . + . + . + . Directory where we have to find files"); print()
                  
                  collected = []
                  for root, dirnames, filenames in os.walk(var_file.rstrip().decode("utf-8")):
                        for filename in fnmatch.filter(filenames, var_path.rstrip().decode("utf-8")):
                              collected.append(os.path.join(root, filename))
                  for i in collected:
                        #print(type(i))
                        
                        if var_path.rstrip().decode("utf-8")[-3:] in i:
                              print(i)
                             
                              if len(sys.argv) > 1:
                                try:
                                  shutil.copy(i, sys.argv[1])
                                except shutil.SameFileError:
                                  pass
                                                               
                              else:
                                print(shutil.SameFileError)
                                print('Directory Path for archive backup has not provided ')
                                
                                  
                              #shutil.copy(i, sys.argv[1])
                              #archivePath()
                  print()
                  print("Next dir for finding files is : - ")
                  
print('\n' * 2)

#listingFileFunct1()


def main():
  if len(sys.argv) > 1:
    if os.path.isdir(sys.argv[1]) == True:
      listingFileFunct1()
    else:
      print('Directory has been provided does not exists in file system, code exit 0')
  else:
    print('Argument for directory archive path has not been provided via comman line, code exit 2')
    sys.exit(2)

if __name__ == "__main__":
    main()





