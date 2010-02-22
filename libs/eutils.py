# -*- coding: utf-8 -*-

# This file is part of unmaskit

# Copyright (c) 2010 - Fabiano Francesconi
# encomiabile.it (c) 2010 - www.encomiabile.it

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import portage
from portage.exception import InvalidAtom

PORTDB = portage.db[portage.root]["porttree"].dbapi

def expand_package_name(pname):
	"""
		Checkes if pname is a valid atom. If it is, then returns a list containing
		all the found atom in portage. The last is taken.
		Example:
			expand_package_name("nagios") will return
			[u'net-analyzer/nagios-2.12', u'net-analyzer/nagios-3.0.6',
				u'net-analyzer/nagios-3.2.0']
	"""
	matches = PORTDB.xmatch("match-all",pname)
	if matches:
		return matches[len(matches)-1]
	else:
		raise portage.exception.InvalidAtom

def get_version_from_atom(aname):
	"""
		Returns the version of the given atom
		Example:
			dev-util/ktigcc-completion-data-0.96_beta7 => 0.96_beta7
	"""
	import re
	regstr = "^([a-zA-Z0-9\-_\/\+]*)-([0-9\._]+[a-zA-Z0-9]+)"
	return re.search(regstr, aname).group(2)

def get_package_name_from_atom(aname):
	"""
		Returns the package name of the given atom
		Example:
			dev-util/ktigcc-completion-data-0.96_beta7 => dev-util/ktigcc-completion-data
	"""
	import re
	regstr = "^([a-zA-Z0-9\-_\/\+]*)-([0-9\._]+[a-zA-Z0-9]+)"
	return re.search(regstr, aname).group(1)

def get_arch():
	return portage.settings['ARCH']

def get_package_status(aname):
	"""
		Return the status of a package: stable, unstable, hardmasked, unkeyworded
		Notice that "stable" could mean "previously unmasked" as well.
	"""
	arch = get_arch()
	archstatus = "~%s keyword" % arch
	try:
		res = portage.getmaskingstatus(aname)
		if not res:
			return "STABLE"
		if ( res[0] == "missing keyword" ):
			return "UNKEYWORDED"
		if ( res[0] == archstatus):
			return "UNSTABLE"
		if (( res[0] == "package.mask" )&(res[1] == archstatus)):
			return "HARDMASKED"
	except ValueError, e:
		print "Unable to parse the status of %s.\n%s" % (aname,e)

def get_atom_deps(aname):
	return PORTDB.aux_get(aname,['DEPEND','RDEPEND','PDEPEND'])
