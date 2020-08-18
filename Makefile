#
# The contents of this file are subject to the Apache 2.0 license you may not
# use this file except in compliance with the License.
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
#
# Copyright 2017 SBIT project (http://www.firmwaretoolkit.org).
# All rights reserved. Use is subject to license terms.
#
#
# Contributors list :
#
#    William Bonnet     wllmbnnt@gmail.com, wbonnet@theitmakers.com
#

# Retrieve cueeznt package version
SW_VERSION := $(shell grep sbit debian/changelog | tr \( \  | tr \) \  | tr \- \  | awk '{ print $$2 }' | sort -r | head -n 1 )
PKG_DIR    := ..
# ------------------------------------------------------------------------------
#
# Target that prints the generic top level help
#
help:
	@echo "Available targets are :"
	@echo " requirements            Install all requirements using PIP"
	@echo " package                 Build the Debian package sbit.deb"
	@echo " test(s)                 Run unit tests"
	@echo " help                    Display this help"


#
# Target : init
#
# Description :
#
#	Install all requirements using PIP
#
requirements:
	pip3 install -r requirements.txt

#
# Target : test, tests
#
# Description :
#
#	Run unit tests
#
tests: test

test:
	nosetests



#
# Target : package
#
# Description : Build the <<debian package
#
#	Run unit tests
#

package:
	rm -f ../sbit_*.orig.tar.gz
	tar cvfz ../sbit_$(SW_VERSION).orig.tar.gz --exclude=sbit/__pycache__ --exclude=build --exclude=sbit.egg-info --exclude=./.git --exclude-vcs-ignores --exclude-vcs-ignores *
	debuild -us -uc -b


#
# Target : upload
#
# Description : upload th package to a debian repository
#
#

upload:
	if [ "x" = "x$(SBIT_DEB_UPLOAD_SERVER)" ] ; then \
		echo "        Variable SBIT_DEB_UPLOAD_SERVER is not set, please define it your shell environment." ; \
	fi ;
	if [ "x" = "x$(SBIT_DEB_UPLOAD_PATH)" ] ; then \
		echo "        Variable SBIT_DEB_UPLOAD_PATH is not set, please define it your shell environment." ; \
	fi ;
	if [ "x" = "x$(SBIT_DEB_UPLOAD_USER)" ] ; then \
		echo "        Variable SBIT_DEB_UPLOAD_USER is not set, please define it your shell environment." ; \
	fi ;
	scp $(PKG_DIR)/*.deb $(PKG_DIR)/*.buildinfo $(PKG_DIR)/*.orig.tar.gz $(PKG_DIR)/*.changes $(SBIT_DEB_UPLOAD_USER)@$(SBIT_DEB_UPLOAD_SERVER):$(SBIT_DEB_UPLOAD_PATH) ;

