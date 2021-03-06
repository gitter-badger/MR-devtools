#!/usr/bin/python

## Make a directory based on input parent directory and desired directory name ##
## mkDir(parentDir, dirName)

############################################################################################
## (c) 2012 The Johns Hopkins University / Applied Physics Laboratory.  All Rights Reserved.
## Proprietary Until Publicly Released
############################################################################################

from sys import argv
import string
import datetime
import os
import csv
import fnmatch
import shutil
import tarfile

# read in command line args
params = list(argv)

pipeOutputDir = params[3]
dataSet = params[4]
pipelineVers = params[5]
packageOutputLoc = params[6]
raw_files = params[1]
mni_files = params[2]

print pipeOutputDir
print packageOutputLoc

# Make master output directory
outDir = os.path.join(packageOutputLoc,(dataSet + "_" + pipelineVers + "_" + datetime.datetime.now().strftime("%Y-%m-%d")))

print outDir

if not os.path.exists(outDir):
	os.makedirs(outDir)

# Sub-Dir and Re-Pack functions
def create_sub(dname):
	outSubDir = os.path.join(outDir, dname)
	print outSubDir
	if not os.path.exists(outSubDir):
		os.makedirs(outSubDir)
	return outSubDir

def package_output(outDir, dirMatch, fileMatch, newLabel):
	for root, dirnames, fnames in os.walk(pipeOutputDir):	
		for dirname in fnmatch.filter(dirnames, dirMatch):
				
			subject = os.path.basename(os.path.normpath(root))
	
			for r, d, filenames in os.walk(os.path.join(root,dirname)):
				for filename in fnmatch.filter(filenames, fileMatch):
					filetitle, fileExtension = os.path.splitext(filename)
			
					oldFile = os.path.join(r,filename)
					print oldFile

					newFile = os.path.join(outDir,(dataSet + '_' + subject + '_' + newLabel + fileExtension))
					print newFile

					shutil.copyfile(oldFile,newFile)
	return 'Success'

def make_tarfile(output_filename, source_dir):
	tar = tarfile.open(output_filename, "w:gz")
	tar.add(source_dir)
	tar.close()

# Raw Inputs
out_raw = create_sub('preproc_raw')
if os.path.exists(out_raw):
	shutil.rmtree(out_raw)
shutil.copytree(raw_files, out_raw)

# Make output sub-directories and re-package output

# Tensors
package_output(create_sub('tensors'),'slabtovolume','*Tensor*','tensors')

# Fibers
package_output(create_sub('fibers'),'fibertracker','*FA_fbr*','fibers')

# Graphs
package_output(create_sub('big_graphs'),'biggraph','*biggraph*','big_graph')
package_output(create_sub('small_graphs'),'smallgraph','*70_smgr*','small_graph')

# LCC
package_output(create_sub('big_lcc'),'*bigLCC*','*concomp*','big_lcc')
package_output(create_sub('small_lcc'),'*smallLCC*','*concomp*','small_lcc')

# Embeddings
package_output(create_sub('embeddings'), '*bigLCC*','*embed*','embed')

# Invariants
big_inv_dir = 'big_invariants'
big_inv_match = '*biginvariant*'
package_output(create_sub(big_inv_dir),big_inv_match,'*clustcoeff*','clustcoeff')
package_output(os.path.join(outDir, big_inv_dir),big_inv_match,'*degree*','degree')
package_output(os.path.join(outDir, big_inv_dir),big_inv_match,'*eigvect*','eigvect')
package_output(os.path.join(outDir, big_inv_dir),big_inv_match,'*eigvl*','eigvl')
package_output(os.path.join(outDir, big_inv_dir),big_inv_match,'*numedges*','numedges')
package_output(os.path.join(outDir, big_inv_dir),big_inv_match,'*numvert*','numvert')
package_output(os.path.join(outDir, big_inv_dir),big_inv_match,'*mad*','mad')
package_output(os.path.join(outDir, big_inv_dir),big_inv_match,'*scanstat1*','scanstat')
package_output(os.path.join(outDir, big_inv_dir),big_inv_match,'*triangles*','triangles')

small_inv_dir = 'small_invariants'
small_inv_match = '*smallinvariant*'
package_output(create_sub(small_inv_dir),small_inv_match,'*clustcoeff*','clustcoeff')
package_output(os.path.join(outDir, small_inv_dir),small_inv_match,'*degree*','degree')
package_output(os.path.join(outDir, small_inv_dir),small_inv_match,'*eigvect*','eigvect')
package_output(os.path.join(outDir, small_inv_dir),small_inv_match,'*eigvl*','eigvl')
package_output(os.path.join(outDir, small_inv_dir),small_inv_match,'*numedges*','numedges')
package_output(os.path.join(outDir, small_inv_dir),small_inv_match,'*numvert*','numvert')
package_output(os.path.join(outDir, small_inv_dir),small_inv_match,'*mad*','mad')
package_output(os.path.join(outDir, small_inv_dir),small_inv_match,'*scanstat1*','scanstat')
package_output(os.path.join(outDir, small_inv_dir),small_inv_match,'*triangles*','triangles')

# MNI
out_mni = create_sub('mni_data')
if os.path.exists(out_mni):
	shutil.rmtree(out_mni)
shutil.copytree(mni_files, out_mni)

# TAR File
outTar = outDir+'.tar.gz'
print outTar
print outDir
make_tarfile(outTar,outDir)


