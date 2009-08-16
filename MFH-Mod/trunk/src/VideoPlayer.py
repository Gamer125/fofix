#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#####################################################################
# Video Playback Layer for FoFiX                                    #
# Copyright (C) 2009 Pascal Giard <evilynux@gmail.com>              #
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
import os
import sys

from math import fabs as abs # Absolute value

# Almighty GStreamer
import gobject
import gst

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from View import View, BackgroundLayer
import Log

# Simple video player
class VideoPlayer(BackgroundLayer):
  def __init__(self, engine, framerate, vidSource, (vidWidth, vidHeight), mute = False, loop = False):
    self.updated = False
    self.videoList = None
    self.videoTex = None
    self.videoBuffer = None
    self.videoSrc = os.path.join(os.getcwd(), vidSource)
    self.engine = engine
    self.mute = mute
    self.loop = loop
    self.winWidth, self.winHeight = engine.view.geometry[2:4]
    self.fps = framerate
    self.textureSetup((vidWidth, vidHeight))
    self.vidSetup()
    self.clock = pygame.time.Clock()
    self.paused = False
    self.finished = False

  def textureSetup(self, (vidWidth, vidHeight)):
    self.vidWidth = vidWidth
    self.vidHeight = vidHeight
    blankSurface = pygame.Surface((vidWidth, vidHeight),
                                  HWSURFACE, 24)
    blankSurface.fill((0,0,0))

    surfaceData = pygame.image.tostring(blankSurface, "RGB", True)
    self.videoBuffer = surfaceData
    self.videoTex = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, self.videoTex)
    gluBuild2DMipmaps(GL_TEXTURE_2D, GL_RGB,
                      vidWidth, vidHeight, GL_RGB,
                      GL_UNSIGNED_BYTE, surfaceData)
    glTexParameteri(GL_TEXTURE_2D, 
                    GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D,
                    GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    # Resize video (polygon) to respect resolution ratio
    # (The math is actually simple, take the time to draw it down if required)
    winRes = float(self.winWidth)/float(self.winHeight)
    vidRes = float(vidWidth)/float(vidHeight)
    vtxX = 1.0
    vtxY = 1.0
    if winRes > vidRes:
      r = float(self.winHeight)/float(vidHeight)
      vtxX = 1.0 - abs(self.winWidth-r*vidWidth) / (float(self.winWidth))
    elif winRes < vidRes:
      r = float(self.winWidth)/float(vidWidth)
      vtxY = 1.0 - abs(self.winHeight-r*vidHeight) / (float(self.winHeight))

    # Create a compiled OpenGL call list
    self.videoList = glGenLists(1)
    glNewList(self.videoList, GL_COMPILE)
    glEnable(GL_TEXTURE_2D)
    glColor3f(1., 1., 1.)
    # Could have used GL_QUADS but IIRC triangles are recommended
    glBegin(GL_TRIANGLE_STRIP)
    glNormal3f(0.0, 0.0, 1.0)
    glTexCoord2f(0.0, 1.0); glVertex3f(-vtxX,  vtxY, 0)
    glTexCoord2f(1.0, 0.0); glVertex3f( vtxX, -vtxY, 0)
    glTexCoord2f(1.0, 1.0); glVertex3f( vtxX,  vtxY, 0)
    glTexCoord2f(0.0, 1.0); glVertex3f(-vtxX,  vtxY, 0)
    glTexCoord2f(0.0, 0.0); glVertex3f(-vtxX, -vtxY, 0)
    glTexCoord2f(1.0, 0.0); glVertex3f( vtxX, -vtxY, 0)
    glEnd()
    glDisable(GL_TEXTURE_2D)
    glEndList()

  # Setup GStreamer's pipeline
  def vidSetup(self):
    if not os.path.exists(self.videoSrc):
      Log.error("Video %s does not exist!" % self.videoSrc)
    with_audio = ""
    if not self.mute:
      with_audio = "! queue ! audioconvert ! audiorate ! autoaudiosink"
    s = "filesrc name=input ! decodebin name=dbin dbin. ! ffmpegcolorspace ! video/x-raw-rgb ! fakesink name=output signal-handoffs=true sync=true dbin. %s" % with_audio
    self.player = gst.parse_launch(s)
    self.input  = self.player.get_by_name('input')
    self.fakeSink = self.player.get_by_name('output')
    self.input.set_property("location", self.videoSrc)
    self.fakeSink.connect ("handoff", self.texUpdate)
    # Catch the end of file as well as errors
    # FIXME: Doesn't work!?! The event is never received
    # Ok, messages are sent if i use the following in run():
    #  gobject.MainLoop().get_context().iteration(True)
    # BUT the fakesink synch events then stop working... why?!
    # See run() for the current hackish workaround.
#     bus = self.player.get_bus()
#     bus.add_signal_watch()
#     bus.enable_sync_message_emission()
#     bus.connect("message", self.onMessage)
#     bus.connect("message::eos", self.onEndOfStream)

  # Handle end of video
  def onEndOfStream(self):
    print "The END"

  # Handle bus event e.g. end of video or unsupported formats/codecs
  def onMessage(self, bus, message):
    type = message.type
    print "Message %s" % type
    if type == gst.MESSAGE_EOS:
      print "End of video"
      self.player.set_state(gst.STATE_NULL)
      self.finished = True
    elif type == gst.MESSAGE_ERROR:
      err, debug = message.parse_error()
      Log.error("Error: %s" % err, debug)
      self.player.set_state(gst.STATE_NULL)
      self.finished = True

  # Handle new video frames coming from the decoder
  def texUpdate(self, sink, buffer, pad):
    self.videoBuffer = buffer
    self.updated = True

  def shown(self):
    gobject.threads_init()
  
  def hidden(self):
    self.player.set_state(gst.STATE_NULL)

  def run(self, ticks):
    if self.paused == True:
      self.player.set_state(gst.STATE_PAUSED)
    else:
      self.player.set_state(gst.STATE_PLAYING)
      self.finished = False
    # HACKISH: The following is a freakin' ugly hack to workaround the gst
    # threading issue (see comments at the bottom of vidSetup).
    # It'd be nice to get this working properly i.e. using onMessage.
    s = self.fakeSink.get_property("last-message")
    if s and s.find("type: 86") != -1: # 86 means EndOfStream (EOS)
      if self.loop:
        self.player.set_state(gst.STATE_NULL)
        # HACKISH: Need to recreate the pipepile altogether...
        # For some reason going through STATE_NULL, STATE_READY, STATE_PLAYING
        # doesn't work as I would expect.
        self.vidSetup()
      else:
        self.player.set_state(gst.STATE_NULL)
        self.finished = True
    self.clock.tick(self.fps)
    
  def render(self, visibility, topMost):
    try:
      if self.updated:
        img = pygame.image.frombuffer(self.videoBuffer,
                                      (self.vidWidth, self.vidHeight),
                                      'RGB')
        glBindTexture(GL_TEXTURE_2D, self.videoTex)
        surfaceData = pygame.image.tostring(img ,'RGB', True)
        gluBuild2DMipmaps(GL_TEXTURE_2D,
                          GL_RGB, self.vidWidth, self.vidHeight,
                          GL_RGB, GL_UNSIGNED_BYTE,
                          surfaceData)
        glTexParameteri(GL_TEXTURE_2D,
                        GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D,
                        GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        self.updated = False

      # Save and clear both transformation matrices
      glMatrixMode(GL_PROJECTION)
      glPushMatrix()
      glLoadIdentity()
      glMatrixMode(GL_MODELVIEW)
      glPushMatrix()
      glLoadIdentity()
      # Draw the polygon and apply texture
      glBindTexture(GL_TEXTURE_2D, self.videoTex)
      glCallList(self.videoList)
      # Restore both transformation matrices
      glPopMatrix()
      glMatrixMode(GL_PROJECTION)
      glPopMatrix()
    except:
      Log.error("Error attempting to play video")
