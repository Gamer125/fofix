#####################################################################
# -*- coding: iso-8859-1 -*-                                        #
#                                                                   #
# Frets on Fire                                                     #
# Copyright (C) 2006 Sami Ky�stil�                                  #
#                                                                   #
# This program is free software; you can redistribute it and/or     #
# modify it under the terms of the GNU General Public License       #
# as published by the Free Software Foundation; either version 2    #
# of the License, or (at your option) any later version.            #
#                                                                   #
# This program is distributed in the hope that it will be useful,   #
# but WITHOUT ANY WARRANTY; without even the implied warranty of    #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the     #
# GNU General Public License for more details.                      #
#                                                                   #
# You should have received a copy of the GNU General Public License #
# along with this program; if not, write to the Free Software       #
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,        #
# MA  02110-1301, USA.                                              #
#####################################################################

import sys
import os
MAJOR_VERSION = 4
MINOR_VERSION = 0
REVISION = 0
URL = 'http://fofix.googlecode.com'

def appName():
  return "fofix"

def appNameSexy():
  return "FoFiX"

def revision():
  import svntag
  try:
    revision = "development (r%d)" % int(svntag.get_svn_info(os.path.dirname(__file__))['revnum'])
  except:
    revision = "development"
  return revision

def versionNum():
  version = "%d.%d.%d" %(MAJOR_VERSION, MINOR_VERSION, REVISION)
  return version

# evilynux: Returns version number w.r.t. frozen state
def version():
  if hasattr(sys, 'frozen'):
    # stump: if we've been py2exe'd, read our version string from the exe.
    if sys.frozen == 'windows_exe':
      import win32api
      us = os.path.abspath(unicode(sys.executable, sys.getfilesystemencoding()))
      version = win32api.GetFileVersionInfo(us, r'\StringFileInfo\%04x%04x\ProductVersion' % win32api.GetFileVersionInfo(us, r'\VarFileInfo\Translation')[0])
    else:
      version = VERSION
  else:
    version = "%d.%d.%d %s" % ( MAJOR_VERSION, MINOR_VERSION, REVISION, revision() )
  return version

#stump: VFS will take care of this
def dataPath():
  # Determine whether were running from an exe or not
  if hasattr(sys, "frozen"):
    if os.name == "posix":
      dataPath = os.path.join(os.path.dirname(sys.argv[0]), "../lib/fofix")
      if not os.path.isdir(dataPath):
        dataPath = "data"
    else:
      dataPath = "data"
  else:
    dataPath = os.path.join("..", "data")
  dataPath = os.path.abspath(dataPath)
  return dataPath
  
