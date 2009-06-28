# -*- coding: iso-8859-1 -*-                                        
"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

import sys, SceneFactory, Version
import glob

APP = ['FoFiX.py']

def songFiles(song, extra = []):
  return ["../data/songs/%s/%s" % (song, f) for f in ["guitar.ogg", "notes.mid", "song.ini", "song.ogg"] + extra]

dataFiles = [
  (".", ["../AUTHORS", "../COPYING", "../CREDITS", "../ChangeLog", "../Makefile", "../NEWS", "../README", "../fretsonfire.ini"]),
  ("doc", glob.glob("../doc/*")),
  ("data", glob.glob("../data/*"))
]

OPTIONS = {
 'argv_emulation': True,
 'dist_dir': '../dist',
 'frameworks' : '../../glew/lib/libGLEW.dylib',
 'iconfile': '../icon_mac_composed.icns',
 'plist': dict(CFBundleIdentifier='org.pythonmac.FoFiX.FretsonFire',
      CFBundleSignature='FoFX',
      NSHumanReadableCopyright=u"\xa9 2008-2009 FoFiX Team.  GNU GPL v2 or later."),
 'includes': SceneFactory.scenes,
 'excludes': ["glew.gl.apple",
      "glew.gl.ati",
      "glew.gl.atix",
      "glew.gl.hp",
      "glew.gl.ibm",
      "glew.gl.ingr",
      "glew.gl.intel",
      "glew.gl.ktx",
      "glew.gl.mesa",
      "glew.gl.oml",
      "glew.gl.pgi",
      "glew.gl.rend",
      "glew.gl.s3",
      "glew.gl.sgi",
      "glew.gl.sgis",
      "glew.gl.sgix",
      "glew.gl.sun",
      "glew.gl.sunx",
      "glew.gl.threedfx",
      "glew.gl.win",
      "ode",
      "unicodedata",
      "_ssl",
      "bz2",
      "email",
      "calendar",
      "bisect",
      "difflib",
      "doctest",
      "ftplib",
      "getpass",
      "gopherlib",
      "heapq",
      "macpath",
      "macurl2path",
      "GimpGradientFile",
      "GimpPaletteFile",
      "PaletteFile"
 ]
}
import GameEngine
fullVersionString = GameEngine.version

setup(
    version=fullVersionString[7:],
    description="Frets on Fire X",
    name="FoFiX",
    url="http://www.unrealvoodoo.org",
    app=APP,
    data_files=dataFiles,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
