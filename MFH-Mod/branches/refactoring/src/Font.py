#####################################################################
# -*- coding: iso-8859-1 -*-                                        #
#                                                                   #
# Frets on Fire                                                     #
# Copyright (C) 2006 Sami Ky�stil�                                  #
#               2008 evilynux <evilynux@gmail.com>                  #
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

import pygame
from OpenGL.GL import *
import sys
from Texture import Texture, TextureAtlas, TextureAtlasFullException

DEFAULT_SCALE = 0.002

class CacheElement(object):
    def __init__(self,content):
        self.content = content
        self.accessed()

    def accessed(self):
        self.lastUse = pygame.time.get_ticks()

class Cache(object):
    def __init__(self,maxCount=1024):
        self.elements = {}
        self.maxCount = maxCount

    def get(self,key):
        e = self.elements[key]
        e.accessed()
        return e.content

    def add(self,key,element):
        self.elements[key] = CacheElement(element)
        if len(self.elements) > self.maxCount:
            keys = self.elements.keys()
            keys.sort(key=lambda e:-self.elements[e].lastUse)
            for k in keys[self.maxCount:]:
                del self.elements[k]

class Font:
  """A texture-mapped font."""
  def __init__(self, fileName, size, bold = False, italic = False, underline = False, outline = True,
               scale = 1.0, reversed = False, systemFont = False, shadow = False):
    pygame.font.init()
    self.size             = size
    self.scale            = scale
    self.outline          = outline
    self.reversed         = reversed
    self.shadow         = shadow
    # Try loading a system font first if one was requested
    self.font           = None
    if systemFont and sys.platform != "win32":
      try:
        self.font       = pygame.font.SysFont(None, size)
      except:
        pass
    if not self.font:
      self.font         = pygame.font.Font(fileName, size)
    self.font.set_bold(bold)
    self.font.set_italic(italic)
    self.font.set_underline(underline)
    self.stringsCache = Cache(256)

  def getStringSize(self, s, scale = DEFAULT_SCALE):
    """
    Get the dimensions of a string when rendered with this font.

    @param s:       String
    @param scale:   Scale factor
    @return:        (width, height) tuple
    """
    scale *= self.scale

    try:
        t,w,h = self.stringsCache.get(s)
    except KeyError:
        w,h = self.font.size(s)

    return (w*scale, h*scale)

  def loadCache(self):
      pass

  # evilynux - Return scaling factor needed to fit text within maxwidth
  def scaleText(self, text, maxwidth, scale = DEFAULT_SCALE):
    w, h = self.getStringSize(text)
    scale = DEFAULT_SCALE
    if w > maxwidth:
        scale = w/maxwidth
    return scale

  def getHeight(self):
    """@return: The height of this font"""
    return self.font.get_height() * self.scale

  def getLineSpacing(self, scale = DEFAULT_SCALE):
    """@return: Recommanded line spacing of this font"""
    return self.font.get_linesize() * self.scale * scale

  #MFH - needed to find the centerline of text
  def getFontAscent(self, scale = DEFAULT_SCALE):
    """@return: Return the height in pixels for the font ascent. 
    The ascent is the number of pixels from the font baseline to the top of the font. """
    return self.font.get_ascent() * self.scale * scale

  #MFH - needed to find the centerline of text
  def getFontDescent(self, scale = DEFAULT_SCALE):
    """@return: Return the height in pixels for the font descent. The descent 
    is the number of pixels from the font baseline to the bottom of the font.  """
    return self.font.get_descent() * self.scale * scale
    
  def setCustomGlyph(self, character, texture):
    """
    Replace a character with a texture.

    @param character:   Character to replace
    @param texture:     L{Texture} instance
    """
    pass

  def render(self, text, pos = (0, 0), direction = (1, 0), scale = DEFAULT_SCALE):
    """
    Draw some text.

    @param text:      Text to draw
    @param pos:       Text coordinate tuple (x, y)
    @param direction: Text direction vector (x, y, z)
    @param scale:     Scale factor
    """
    # deufeufeu : new drawing relaying only on pygame.font.render
    #           : I know me miss special unicodes characters, but the gain
    #           : is really important.
    def drawSquare(w,h,tw,th):
        glBegin(GL_TRIANGLE_STRIP)
        glTexCoord2f(0.0,th)
        glVertex2f(0,0)
        glTexCoord2f(tw,th)
        glVertex2f(w,0)
        glTexCoord2f(0.0,0.0)
        glVertex2f(0,h)
        glTexCoord2f(tw,0.0)
        glVertex2f(w,h)
        glEnd()
 
    if not text:
        return

    try:
        t,w,h = self.stringsCache.get(text)
    except KeyError:
        s = self.font.render(text, True, (255,255,255))
        t = Texture()
        t.setFilter(GL_LINEAR, GL_LINEAR)
        t.setRepeat(GL_CLAMP, GL_CLAMP)
        t.loadSurface(s, alphaChannel = True)
        del s
        w, h = self.font.size(text)
        self.stringsCache.add(text,(t,w,h))
     
    x, y = pos
    scale *= self.scale
    w, h = w*scale, h*scale
    tw,th = t.size
    glEnable(GL_TEXTURE_2D)
    glPushMatrix()
    glTranslatef(x,y,0)
    t.bind()
    if self.outline:
        glPushAttrib(GL_CURRENT_BIT)
        glPushMatrix()
        glColor4f(0, 0, 0, .25 * glGetDoublev(GL_CURRENT_COLOR)[3])

        blur = 2 * DEFAULT_SCALE
        for offset in [(-.7, -.7), (0, -1), (.7, -.7), (-1, 0), 
                       (1, 0), (-.7, .7), (0, 1), (.7, .7)]:
            glPushMatrix()
            glTranslatef(blur * offset[0], blur * offset[1], 0)
            drawSquare(w,h,tw,th)
            glPopMatrix()
        glPopMatrix()
        glPopAttrib()

    if self.shadow:
        glPushAttrib(GL_CURRENT_BIT)
        glPushMatrix()
        glColor4f(0, 0, 0, 1)
        glTranslatef(.0022, .0005, 0)
        drawSquare(w,h,tw,th)
        glPopMatrix()
        glPopAttrib()

    drawSquare(w,h,tw,th)
    glPopMatrix()

    glDisable(GL_TEXTURE_2D)
    return

