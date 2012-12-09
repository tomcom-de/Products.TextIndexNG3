###########################################################################
# TextIndexNG V 3                
# The next generation TextIndex for Zope
#
# This software is governed by a license. See
# LICENSE.txt for the terms of this license.
###########################################################################

# Makefile for private purposes

checkout:
	svn co https://ajung@svn.sourceforge.net/svnroot/textindexng/TextIndexNG3/trunk TextIndexNG3

dist:
	cd txng3
	tar cfvz ~/TextIndexNG3-`cat TextIndexNG3/version.txt`.tar.gz TextIndexNG3

build_modules:
	cd extension_modules; python2.4 setup.py build

install_modules:
	cd extension_modules; python2.4 setup.py install
