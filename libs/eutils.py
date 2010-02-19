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

def expand_package_name(pname):
	"""
		Checkes if pname is a valid atom. If it is, then returns a list containing
		all the found atom in portage. The last is taken.
		Example:
			expand_package_name("nagios") will return
			[u'net-analyzer/nagios-2.12', u'net-analyzer/nagios-3.0.6',
				u'net-analyzer/nagios-3.2.0']
	"""

	PORTDB = portage.portdb
	matches = PORTDB.xmatch("match-all", pname)

	if matches:
		return matches[len(matches)-1]
	else:
		raise portage.exception.InvalidAtom
