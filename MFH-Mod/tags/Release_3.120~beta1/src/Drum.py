#####################################################################
# -*- coding: iso-8859-1 -*-                                        #
#                                                                   #
# Frets on Fire                                                     #
# Copyright (C) 2006 Sami Kyostila                                  #
#               2008 Alarian                                        #
#               2008 myfingershurt                                  #
#               2008 Glorandwarf                                    #
#               2008 Capo                                           #
#               2008 Blazingamer                                    #
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

#altered by myfingershurt to adapt to Alarian mod

import Player
from Song import Note, Tempo, Bars
from Mesh import Mesh
import Theme
import Config
import Log
import pygame
import Shader

from OpenGL.GL import *
import math
import os
import random

import Song   #need the base song defines as well

#Normal guitar key color order: Green, Red, Yellow, Blue, Orange
#Drum fret color order: Red, Yellow, Blue, Green
#actual drum note numbers:
#0 = bass drum (stretched Orange fret), normally Green fret
#1 = drum Red fret, normally Red fret
#2 = drum Yellow fret, normally Yellow fret
#3 = drum Blue fret, normally Blue fret
#4 = drum Green fret, normally Orange fret
#
#So, with regard to note number coloring, swap note.number 0's color wih note.number 4.

#akedrou - 5-drum support is now available.
# to enable it, only here and Player.drums should need changing.


class Drum:
  def __init__(self, engine, playerObj, editorMode = False, player = 0):
    self.engine         = engine
    
    #self.starPowerDecreaseDivisor = 200.0*self.engine.audioSpeedFactor
    self.starPowerDecreaseDivisor = 200.0/self.engine.audioSpeedFactor

    
    self.isDrum = True
    self.isBassGuitar = False

    self.bassDrumPedalDown = False
  
    self.lastFretWasBassDrum = False
    self.lastFretWasT1 = False   #Faaa Drum sound
    self.lastFretWasT2 = False
    self.lastFretWasT3 = False
    self.lastFretWasC = False

    self.useMidiSoloMarkers = False
    self.canGuitarSolo = False
    self.guitarSolo = False
    self.sameNoteHopoString = False
    self.hopoProblemNoteNum = -1
    self.currentGuitarSoloHitNotes = 0

    self.matchingNotes = None

    self.bigRockEndingMarkerSeen = False

    #MFH - I do not understand fully how the handicap scorecard works at the moment, nor do I have the time to figure it out.
    #... so for now, I'm just writing some extra code here for the early hitwindow size handicap.
    self.earlyHitWindowSizeFactor = 0.5


    self.oNeckovr = None    #MFH - needs to be here to prevent crashes!    

    self.starNotesInView = False
    self.openStarNotesInView = False

    self.cappedScoreMult = 0

    self.isStarPhrase = False
    self.finalStarSeen = False

    self.freestyleActive = False
    
    # Volshebnyi - BRE scoring variables
    self.freestyleEnabled = False
    self.freestyleStart = 0
    self.freestyleFirstHit = 0
    self.freestyleLength = 0
    self.freestyleLastHit = 0
    self.freestyleBonusFret = -2
    self.freestyleLastFretHitTime = range(5)
    self.freestyleBaseScore = 750
    self.freestylePeriod = 1000
    self.freestylePercent = 50
    self.drumFillsCount = 0
    self.drumFillsTotal = 0
    self.drumFillsHits = 0
    self.drumFillsActive = False
    self.drumFillsReady = False
    self.freestyleReady = False
    self.freestyleOffset = 5
    self.freestyleSP = False
    
    self.neckAlpha=[] # necks transparency
    self.neckAlpha.append( self.engine.config.get("game", "necks_alpha") ) # all necks
    self.neckAlpha.append( self.neckAlpha[0] * self.engine.config.get("game", "neck_alpha") ) # solo neck
    self.neckAlpha.append( self.neckAlpha[0] * self.engine.config.get("game", "solo_neck_alpha") ) # solo neck
    self.neckAlpha.append( self.neckAlpha[0] * self.engine.config.get("game", "overlay_neck_alpha") ) # overlay neck
    self.neckAlpha.append( self.neckAlpha[0] * self.engine.config.get("game", "fail_neck_alpha") ) # fail neck
    

    #self.drumFillOnScreen = False   #MFH 
    self.drumFillEvents = []
    self.drumFillWasJustActive = False

    self.accThresholdWorstLate = 0
    self.accThresholdVeryLate = 0
    self.accThresholdLate = 0
    self.accThresholdSlightlyLate = 0
    self.accThresholdExcellentLate = 0
    self.accThresholdPerfect = 0
    self.accThresholdExcellentEarly = 0
    self.accThresholdSlightlyEarly = 0
    self.accThresholdEarly = 0
    self.accThresholdVeryEarly = 0


    self.tempoBpm = 120   #MFH - default is NEEDED here...
    
    self.beatsPerBoard  = 5.0
    self.strings        = 4
    self.fretWeight     = [0.0] * self.strings
    self.fretActivity   = [0.0] * self.strings
    self.fretColors     = Theme.fretColors
    self.spColor        = self.fretColors[5]
    self.playedNotes    = []
    self.missedNotes    = []
    self.editorMode     = editorMode
    self.selectedString = 0
    self.time           = 0.0
    self.pickStartPos   = 0
    self.leftyMode      = False

    self.freestyleHitFlameCounts = [0 for n in range(self.strings+1)]    #MFH


    self.logClassInits = self.engine.config.get("game", "log_class_inits")
    if self.logClassInits == 1:
      Log.debug("Drum class initialization!")

    self.incomingNeckMode = self.engine.config.get("game", "incoming_neck_mode")
    self.guitarSoloNeckMode = self.engine.config.get("game", "guitar_solo_neck")
    self.bigRockEndings = self.engine.config.get("game", "big_rock_endings")


    
    #self.actualBpm = 0.0
    self.currentBpm     = 120.0   #MFH - need a default 120BPM to be set in case a custom song has no tempo events.
    self.currentPeriod  = 60000.0 / self.currentBpm
    #self.targetBpm      = self.currentBpm
    #self.targetPeriod   = 60000.0 / self.targetBpm
    self.lastBpmChange  = -1.0
    self.baseBeat       = 0.0

    #########For Animations
    self.Animspeed      = 30#Lower value = Faster animations
    #For Animated Starnotes
    self.indexCount     = 0
    #Alarian, For animated hitglow
    self.HCount         = 0
    self.Hitanim        = True

    #myfingershurt: to keep track of pause status here as well
    self.paused = False

    self.spEnabled = True
    self.starPower = 0
    self.starPowerActive = False
    self.starPowerGained = False

    self.starpowerMode = self.engine.config.get("game", "starpower_mode") #MFH

    self.killPoints = False
    
    if self.starpowerMode == 1:
      self.starNotesSet = False
    else:
      self.starNotesSet = True

    self.maxStars = []
    self.starNotes = []
    self.totalNotes = 0

    #get difficulty
    self.difficulty = playerObj.getDifficultyInt()
    self.controlType = playerObj.controlType

    self.scoreMultiplier = 1

      
    #myfingershurt:
    self.hopoStyle = 0    
    self.LastStrumWasChord = False
    self.spRefillMode = self.engine.config.get("game","sp_notes_while_active")
    self.hitglow_color = self.engine.config.get("video", "hitglow_color") #this should be global, not retrieved every fret render.

    #myfingershurt: this should be retrieved once at init, not repeatedly in-game whenever tails are rendered.
    self.notedisappear = self.engine.config.get("game", "notedisappear")
    self.fretsUnderNotes  = self.engine.config.get("game", "frets_under_notes")
    self.staticStrings  = self.engine.config.get("performance", "static_strings")


    self.indexFps       = self.engine.config.get("video", "fps")

    self.twoChord       = 0
    self.twoChordApply  = False
    self.hopoActive     = 0
    
    #myfingershurt: need a separate variable to track whether or not hopos are actually active
    self.wasLastNoteHopod = False
    
    
    self.hopoLast       = -1
    self.hopoColor      = (0, .5, .5)
    self.player         = player
    self.scoreMultiplier = 1

    self.hit = [False, False, False, False, False]

    self.freestyleHit = [False, False, False, False, False]

    self.neck = str(playerObj.neck)
    playerObj = None

    #Get theme
    themename = self.engine.data.themeLabel
    #now theme determination logic is only in data.py:
    self.theme = self.engine.data.theme
    
    #check if BRE enabled
    if self.bigRockEndings == 2 or (self.theme == 2 and self.bigRockEndings == 1):
    	self.freestyleEnabled = True   

    if self.theme < 2:    #make board same size as guitar board if GH based theme so it rockmeters dont interfere
      self.boardWidth     = 3.0
      self.boardLength    = 9.0
    
    #blazingamer
    self.nstype = self.engine.config.get("game", "nstype")
    self.twoDnote = Theme.twoDnote
    self.twoDkeys = Theme.twoDkeys 
    self.threeDspin = Theme.threeDspin 
    self.opencolor = Theme.opencolor 
    self.ocount = 0
    self.noterotate = self.engine.config.get("coffee", "noterotate")
    self.isFailing = False
    self.failcount = 0
    self.failcount2 = False
    self.spcount = 0
    self.spcount2 = 0
    
    #akedrou
    self.coOpFailed = False
    self.coOpRestart = False
    self.coOpRescueTime = 0.0


    #MFH- fixing neck speed
    if self.nstype < 3:   #not constant mode: 
      self.speed = self.engine.config.get("coffee", "neckSpeed")*0.01
    else:   #constant mode
      #self.speed = self.engine.config.get("coffee", "neckSpeed")
      self.speed = 410 - self.engine.config.get("coffee", "neckSpeed")    #invert this value

      
    self.bigMax = 1

    if self.engine.config.get("game", "large_drum_neck"):
      self.boardWidth     = 4.0
      self.boardLength    = 12.0
    #death_au: fixed neck size
    elif self.twoDnote == False or self.twoDkeys == False:
      self.boardWidth     = Theme.neckWidth + 0.6
      self.boardLength    = 9.0  
    else:
      self.boardWidth     = Theme.neckWidth
      self.boardLength    = 9.0


    self.muteSustainReleases = self.engine.config.get("game", "sustain_muting") #MFH
    
    self.hitw = self.engine.config.get("game", "note_hit_window")  #this should be global, not retrieved every BPM change.
    if self.hitw == 0: 
      self.hitw = 1.2
    elif self.hitw == 1: 
      self.hitw = 1.9
    elif self.hitw == 2: 
      self.hitw = 2.3
    else:
      self.hitw = 1.2
    
    self.hitwcheat = self.engine.config.get("game", "hit_window_cheat")
    if self.hitwcheat == 1:   
      self.hitw = 0.70
    elif self.hitwcheat == 2: 
      self.hitw = 1.0

    self.keys = []
    self.actions = []
    self.soloKey = []
      
    self.setBPM(self.currentBpm)

    engine.loadImgDrawing(self, "glowDrawing", "glow.png")
    
    if not engine.data.fileExists(os.path.join("necks", self.neck + ".png")) and not engine.data.fileExists(os.path.join("necks", "Neck_" + self.neck + ".png")):
      self.neck = str(engine.mainMenu.chosenNeck) #this neck is safe!
    
    # evilynux - Fixed random neck -- MFH: further fixing random neck
    if self.neck == "0" or self.neck == "Neck_0" or self.neck == "randomneck":
      self.neck = []
      # evilynux - improved loading logic to support arbitrary filenames
      for i in os.listdir(self.engine.resource.fileName("necks")):
        # evilynux - Special cases, ignore these...
        if( str(i) == "overdriveneck.png" or str(i) == "randomneck.png"  or str(i) == "Neck_0.png" or str(i)[-4:] != ".png" ):
          continue
        else:
          self.neck.append(str(i)[:-4]) # evilynux - filename w/o extension
      i = random.randint(1,len(self.neck))
      engine.loadImgDrawing(self, "neckDrawing", os.path.join("necks",self.neck[i]+".png"),  textureSize = (256, 256))
      Log.debug("Random neck chosen: " + self.neck[i])
    else:
      try:
        # evilynux - first assume the self.neck contains the full filename
        engine.loadImgDrawing(self, "neckDrawing", os.path.join("necks",self.neck+".png"),  textureSize = (256, 256))
      except IOError:
        engine.loadImgDrawing(self, "neckDrawing", os.path.join("necks","Neck_"+self.neck+".png"),  textureSize = (256, 256))


    #MFH - making hitflames optional
    self.hitFlamesPresent = False
    try:
      engine.loadImgDrawing(self, "hitflames1Drawing", os.path.join("themes",themename,"hitflames1.png"),  textureSize = (128, 128))
      engine.loadImgDrawing(self, "hitflames2Drawing", os.path.join("themes",themename,"hitflames2.png"),  textureSize = (128, 128))
      self.hitFlamesPresent = True
    except IOError:
      self.hitFlamesPresent = False
      self.hitflames1Drawing = None
      self.hitflames2Drawing = None

    try:
      engine.loadImgDrawing(self, "hitflamesAnim", os.path.join("themes",themename,"hitflamesanimation.png"),  textureSize = (128, 128))
    except IOError:
      #engine.loadImgDrawing(self, "hitflames1Drawing", os.path.join("themes",themename,"hitflames1.png"),  textureSize = (128, 128))
      #engine.loadImgDrawing(self, "hitflames2Drawing", os.path.join("themes",themename,"hitflames2.png"),  textureSize = (128, 128))
      self.Hitanim2 = False

    try:
      engine.loadImgDrawing(self, "hitglowAnim", os.path.join("themes",themename,"hitglowanimation.png"),  textureSize = (128, 128))
    except IOError:
      try:
        engine.loadImgDrawing(self, "hitglowDrawing", os.path.join("themes",themename,"hitglow.png"),  textureSize = (128, 128))
        engine.loadImgDrawing(self, "hitglow2Drawing", os.path.join("themes",themename,"hitglow2.png"),  textureSize = (128, 128))
      except IOError:
        self.hitglowDrawing = None
        self.hitglow2Drawing = None
        self.hitFlamesPresent = False   #MFH - shut down all flames if these are missing.
      self.Hitanim = False

    
    if self.twoDkeys == True: #death_au
      #myfingershurt: adding drumfretshacked.png for image-corrected drum fret angles in RB:
      try:
        engine.loadImgDrawing(self, "fretButtons", os.path.join("themes",themename,"drumfretshacked.png"))
      except IOError:
        engine.loadImgDrawing(self, "fretButtons", os.path.join("themes",themename,"fretbuttons.png"))
      #death_au: adding drumfrets.png (with bass drum frets seperate)
      try:
        engine.loadImgDrawing(self, "drumFretButtons", os.path.join("themes",themename,"drumfrets.png"))
      except IOError:
        self.drumFretButtons = None
    else: #death_au
      #MFH - can't use IOError for fallback logic for a Mesh() call... 
      if self.engine.fileExists(os.path.join("themes", themename, "key.dae")):
        engine.resource.load(self,  "keyMesh",  lambda: Mesh(engine.resource.fileName("themes", themename, "key.dae")))
      else:
        engine.resource.load(self,  "keyMesh",  lambda: Mesh(engine.resource.fileName("key.dae")))

      try:
        engine.loadImgDrawing(self,  "keytexa",  os.path.join("themes", themename, "keytex_a.png"))
        engine.loadImgDrawing(self,  "keytexb",  os.path.join("themes", themename, "keytex_b.png"))
        engine.loadImgDrawing(self,  "keytexc",  os.path.join("themes", themename, "keytex_c.png"))
        engine.loadImgDrawing(self,  "keytexd",  os.path.join("themes", themename, "keytex_d.png"))
        engine.loadImgDrawing(self,  "keytexe",  os.path.join("themes", themename, "keytex_e.png"))
        self.keytex = True

      except IOError:
        self.keytexa = False
        self.keytexb = False
        self.keytexc = False
        self.keytexd = False
        self.keytexe = False
        self.keytex = False
        
    #Spinning starnotes or not?
    self.starspin = False

    if self.twoDnote == True:  
      try:
        engine.loadImgDrawing(self, "noteButtons", os.path.join("themes",themename,"drumnotes.png"))
        self.separateDrumNotes = True
      except IOError:
        engine.loadImgDrawing(self, "noteButtons", os.path.join("themes",themename,"notes.png"))
        self.separateDrumNotes = False
    else:
      #MFH - can't use IOError for fallback logic for a Mesh() call... 
      if self.engine.fileExists(os.path.join("themes", themename, "note.dae")):
        engine.resource.load(self,  "noteMesh",  lambda: Mesh(engine.resource.fileName("themes", themename, "note.dae")))
      else:
        engine.resource.load(self,  "noteMesh",  lambda: Mesh(engine.resource.fileName("note.dae")))
        
      try:
        engine.loadImgDrawing(self,  "notetexa",  os.path.join("themes", themename, "notetex_a.png"))
        engine.loadImgDrawing(self,  "notetexb",  os.path.join("themes", themename, "notetex_b.png"))
        engine.loadImgDrawing(self,  "notetexc",  os.path.join("themes", themename, "notetex_c.png"))
        engine.loadImgDrawing(self,  "notetexd",  os.path.join("themes", themename, "notetex_d.png"))
        engine.loadImgDrawing(self,  "notetexe",  os.path.join("themes", themename, "notetex_e.png"))
        self.notetex = True

      except IOError:
        self.notetexa = False
        self.notetexb = False
        self.notetexc = False
        self.notetexd = False
        self.notetexe = False
        self.notetex = False
        
      if self.engine.fileExists(os.path.join("themes", themename, "star.dae")):  
        engine.resource.load(self,  "starMesh",  lambda: Mesh(engine.resource.fileName("themes", themename, "star.dae")))
      else:  
        self.starMesh = None

      try:
        engine.loadImgDrawing(self,  "startexa",  os.path.join("themes", themename, "startex_a.png"))
        engine.loadImgDrawing(self,  "startexb",  os.path.join("themes", themename, "startex_b.png"))
        engine.loadImgDrawing(self,  "startexc",  os.path.join("themes", themename, "startex_c.png"))
        engine.loadImgDrawing(self,  "startexd",  os.path.join("themes", themename, "startex_d.png"))
        engine.loadImgDrawing(self,  "startexe",  os.path.join("themes", themename, "startex_e.png"))
        self.startex = True

      except IOError:
        self.startexa = False
        self.startexb = False
        self.startexc = False
        self.startexd = False
        self.startexe = False
        self.startex = False

      if self.engine.fileExists(os.path.join("themes", themename, "open.dae")):
        engine.resource.load(self,  "openMesh",  lambda: Mesh(engine.resource.fileName("themes", themename, "open.dae")))
      else:  
        self.openMesh = None

      try:
        engine.loadImgDrawing(self,  "opentexture",  os.path.join("themes", themename, "opentex.png"))
        self.opentex = True
      except IOError:
        self.opentex = False


    try:
      engine.loadImgDrawing(self, "centerLines", os.path.join("themes",themename,"drumcenterlines.png"))
    except IOError:
      #engine.loadImgDrawing(self, "centerLines", os.path.join("themes",themename,"center_lines.png"))
      self.centerLines = None


    engine.loadImgDrawing(self, "sideBars", os.path.join("themes",themename,"side_bars.png"))
    engine.loadImgDrawing(self, "bpm_halfbeat", os.path.join("themes",themename,"bpm_halfbeat.png"))
    engine.loadImgDrawing(self, "bpm_beat", os.path.join("themes",themename,"bpm_beat.png"))
    engine.loadImgDrawing(self, "bpm_measure", os.path.join("themes",themename,"bpm_measure.png"))
    try:
      engine.loadImgDrawing(self, "freestyle1", os.path.join("themes", themename, "freestyletail1.png"),  textureSize = (128, 128))
      engine.loadImgDrawing(self, "freestyle2", os.path.join("themes", themename, "freestyletail2.png"),  textureSize = (128, 128))
    except IOError:
      engine.loadImgDrawing(self, "freestyle1", "freestyletail1.png",  textureSize = (128, 128))
      engine.loadImgDrawing(self, "freestyle2", "freestyletail2.png",  textureSize = (128, 128))

    if self.theme == 0 or self.theme == 1:
      engine.loadImgDrawing(self, "hitlightning", os.path.join("themes",themename,"lightning.png"),  textureSize = (128, 128))

      #myfingershurt: the starpower neck file should be in the theme folder... and also not required:
      try:
        engine.loadImgDrawing(self, "oNeck", os.path.join("themes",themename,"starpowerneck_drum.png"),  textureSize = (256, 256))
      except IOError:
        try:
          engine.loadImgDrawing(self, "oNeck", os.path.join("themes",themename,"starpowerneck.png"),  textureSize = (256, 256))
        except IOError:
          self.oNeck = None

    elif self.theme == 2:
      try:
        engine.loadImgDrawing(self, "oSideBars", os.path.join("themes",themename,"drum_overdrive_side_bars.png"),  textureSize = (256, 256))
      except IOError:
        self.oSideBars = None
  
      try:
        engine.loadImgDrawing(self, "oCenterLines", os.path.join("themes",themename,"drum_overdrive_center_lines.png"))
      except IOError:
        #engine.loadImgDrawing(self, "centerLines", os.path.join("themes",themename,"center_lines.png"))
        self.oCenterLines = None

      
      #myfingershurt: the overdrive neck file should be in the theme folder... and also not required:
      try:
        engine.loadImgDrawing(self, "oNeck", os.path.join("themes",themename,"overdriveneck_drum.png"),  textureSize = (256, 256))
      except IOError:
        try:
          engine.loadImgDrawing(self, "oNeck", os.path.join("themes",themename,"overdriveneck.png"),  textureSize = (256, 256))
        except IOError:
          self.oNeck = None

      #MFH: support for optional drum_overdrive_string_flash.png
      self.overdriveFlashCounts = self.indexFps/4   #how many cycles to display the oFlash: self.indexFps/2 = 1/2 second
      self.overdriveFlashCount = self.overdriveFlashCounts
      try:
        engine.loadImgDrawing(self, "oFlash", os.path.join("themes",themename,"drum_overdrive_string_flash.png"),  textureSize = (256, 256))
      except IOError:
        self.oFlash = None


    #myfingershurt: Guitar Solo neck:
    if self.guitarSoloNeckMode > 0:
      if self.guitarSoloNeckMode == 1:  #replace neck
        try:
          engine.loadImgDrawing(self, "guitarSoloNeck", os.path.join("themes",themename,"guitarsoloneck.png"),  textureSize = (256, 256))
        except IOError:
          self.guitarSoloNeck = None
      elif self.guitarSoloNeckMode == 2:  #overlay neck
        try:
          engine.loadImgDrawing(self, "guitarSoloNeck", os.path.join("themes",themename,"guitarsoloneckovr.png"),  textureSize = (256, 256))
        except IOError:
          self.guitarSoloNeck = None
    else:
      self.guitarSoloNeck = None

    try:
      engine.loadImgDrawing(self, "failNeck", os.path.join("themes",themename,"failneck.png"))
    except IOError:
      engine.loadImgDrawing(self, "failNeck", os.path.join("failneck.png"))
                                                           




    #t'aint no tails in drums, yo.
    self.simpleTails = True
    self.tail1 = None
    self.tail2 = None
    self.bigTail1 = None
    self.bigTail2 = None  

    self.meshColor  = Theme.meshColor    
    self.hopoColor  = Theme.hopoColor
    self.spotColor = Theme.spotColor   
    self.keyColor = Theme.keyColor
    self.key2Color = Theme.key2Color
    self.tracksColor = Theme.tracksColor
    self.barsColor = Theme.barsColor
    self.flameColors = Theme.flameColors
    self.gh3flameColor = Theme.gh3flameColor
    self.flameSizes = Theme.flameSizes
    self.glowColor  = Theme.glowColor
    self.twoChordMax = False
    self.disableVBPM  = self.engine.config.get("game", "disable_vbpm")
    self.disableNoteSFX  = self.engine.config.get("video", "disable_notesfx")
    self.disableFretSFX  = self.engine.config.get("video", "disable_fretsfx")
    self.disableFlameSFX  = self.engine.config.get("video", "disable_flamesfx")

    self.fretboardHop = 0.00  #stump


  def selectPreviousString(self):
    self.selectedString = (self.selectedString - 1) % self.strings

  def selectString(self, string):
    self.selectedString = string % self.strings

  def selectNextString(self):
    self.selectedString = (self.selectedString + 1) % self.strings

  def noteBeingHeld(self):
    noteHeld = False
    return noteHeld

  def isKillswitchPossible(self):
    possible = False
    return possible

  def setBPM(self, bpm):
    if bpm > 200:
      bpm = 200

    #MFH - Filter out unnecessary BPM settings (when currentBPM is already set!)
    #if self.actualBpm != bpm:
    #  self.actualBpm = bpm
    self.currentBpm = bpm   #update current BPM as well

    #MFH - Neck speed determination:
    if self.nstype == 0:    #BPM mode
      self.neckSpeed = (340 - bpm)/self.speed
    elif self.nstype == 1:   #Difficulty mode
      if self.difficulty == 0:    #expert
        self.neckSpeed = 220/self.speed
      elif self.difficulty == 1:
        self.neckSpeed = 250/self.speed
      elif self.difficulty == 2:
        self.neckSpeed = 280/self.speed
      else:   #easy
        self.neckSpeed = 300/self.speed
    elif self.nstype == 2:   #BPM & Diff mode
      if self.difficulty == 0:    #expert
        self.neckSpeed = (226-(bpm/10))/self.speed
      elif self.difficulty == 1:
        self.neckSpeed = (256-(bpm/10))/self.speed
      elif self.difficulty == 2:
        self.neckSpeed = (286-(bpm/10))/self.speed
      else:   #easy
        self.neckSpeed = (306-(bpm/10))/self.speed
    else: #Percentage mode - pre-calculated
      self.neckSpeed = self.speed

    self.earlyMargin       = 250 - bpm/5 - 70*self.hitw
    self.lateMargin        = 250 - bpm/5 - 70*self.hitw
    #self.earlyMargin = self.lateMargin * self.earlyHitWindowSizeFactor    #MFH - scale early hit window here

    #self.noteReleaseMargin = 200 - bpm/5 - 70*self.hitw
    #if (self.noteReleaseMargin < (200 - bpm/5 - 70*1.2)):   #MFH - enforce "tight" hitwindow minimum note release margin
    #  self.noteReleaseMargin = (200 - bpm/5 - 70*1.2)
    if self.muteSustainReleases == 4:   #tight
      self.noteReleaseMargin = (200 - bpm/5 - 70*1.2)
    elif self.muteSustainReleases == 3: #standard
      self.noteReleaseMargin = (200 - bpm/5 - 70*1.0)
    elif self.muteSustainReleases == 2: #wide
      self.noteReleaseMargin = (200 - bpm/5 - 70*0.7)
    else:  #ultra-wide 
      self.noteReleaseMargin = (200 - bpm/5 - 70*0.5)

    #MFH - TODO - only calculate the below values if the realtime hit accuracy feedback display is enabled - otherwise this is a waste!
    self.accThresholdWorstLate = (0-self.lateMargin)
    self.accThresholdVeryLate = (0-(3*self.lateMargin/4))
    self.accThresholdLate = (0-(2*self.lateMargin/4))
    self.accThresholdSlightlyLate = (0-(1*self.lateMargin/4))
    self.accThresholdExcellentLate = -1.0
    self.accThresholdPerfect = 1.0
    self.accThresholdExcellentEarly = (1*self.lateMargin/4)
    self.accThresholdSlightlyEarly = (2*self.lateMargin/4)
    self.accThresholdEarly = (3*self.lateMargin/4)
    self.accThresholdVeryEarly = (4*self.lateMargin/4)


  def setMultiplier(self, multiplier):
    self.scoreMultiplier = multiplier
    
    
  #volshebnyi
  def renderFreestyleLanes(self, visibility, song, pos, controls):
    if not song:
      return
    if not song.readyToGo:
      return


    #MFH - check for [section big_rock_ending] to set a flag to determine how to treat the last drum fill marker note:
    #for time, event in song.eventTracks[Song.TK_SECTIONS].getEvents(pos - self.lateMargin*2, pos):
    #  if event.text.find("big rock ending") > 0:
    if song.breMarkerTime and pos > song.breMarkerTime:
      self.bigRockEndingMarkerSeen = True
          
          


    #boardWindowMin = pos - self.currentPeriod * 2
    boardWindowMax = pos + self.currentPeriod * self.beatsPerBoard
    track = song.midiEventTrack[self.player]
    #self.currentPeriod = self.neckSpeed
    beatsPerUnit = self.beatsPerBoard / self.boardLength
    if self.freestyleEnabled:
      freestyleActive = False
      self.drumFillsActive = False
      #drumFillOnScreen = False
      drumFillEvents = []
      #for time, event in track.getEvents(boardWindowMin, boardWindowMax):
      for time, event in track.getEvents(pos - self.freestyleOffset, boardWindowMax + self.freestyleOffset):
        if isinstance(event, Song.MarkerNote):
          if event.number == Song.freestyleMarkingNote and (not event.happened or self.bigRockEndingMarkerSeen):  #MFH - don't kill the BRE!
            #drumFillOnScreen = True
            drumFillEvents.append(event)
            length     = (event.length - 50) / self.currentPeriod / beatsPerUnit
            w = self.boardWidth / self.strings
            self.freestyleLength = event.length #volshebnyi
            self.freestyleStart = time # volshebnyi
            z  = ((time - pos) / self.currentPeriod) / beatsPerUnit
            z2 = ((time + event.length - pos) / self.currentPeriod) / beatsPerUnit
      
            if z > self.boardLength * .8:
              f = (self.boardLength - z) / (self.boardLength * .2)
            elif z < 0:
              f = min(1, max(0, 1 + z2))
            else:
              f = 1.0
             
            time -= self.freestyleOffset 
            #volshebnyi - allow tail to move under frets
            if time > pos:
            	self.drumFillsHits = -1
            if self.starPower>=50 and not self.starPowerActive:
              self.drumFillsReady = True
                
            else:
              self.drumFillsReady = False
            if self.bigRockEndingMarkerSeen: # and ( (self.drumFillsCount == self.drumFillsTotal and time+event.length>pos) or (time > pos and self.drumFillsCount == self.drumFillsTotal-1) ):
              self.freestyleReady = True
              self.drumFillsReady = False
            else:
              self.freestyleReady = False
            if time < pos:
              if self.bigRockEndingMarkerSeen:  # and self.drumFillsCount == self.drumFillsTotal:
              	freestyleActive = True
              else:
                #if self.drumFillsCount <= self.drumFillsTotal and self.drumFillsReady:
                if self.drumFillsReady:
                	self.drumFillsActive = True
                	self.drumFillWasJustActive = True
                if self.drumFillsHits<0:
                	self.drumFillsCount += 1
                	self.drumFillsHits = 0

              if z < -1.5:
              	length += z +1.5
              	z =  -1.5
              	
            #if time+event.length>pos and time+event.length-0.5>pos:
            #	if controls.getState(self.keys[4]) or controls.getState(self.keys[8]):
            #		self.starPowerActive = True
            	
            #volshebnyi - render 4 freestyle tails
            if self.freestyleReady or self.drumFillsReady:
              for theFret in range(1,5):
                x = (self.strings / 2 + .5 - theFret) * w
                if theFret == 4:
                  c = self.fretColors[0]
                else:
                  c = self.fretColors[theFret]
                color      = (.1 + .8 * c[0], .1 + .8 * c[1], .1 + .8 * c[2], 1.0 * visibility * f)
                glPushMatrix()
                glTranslatef(x, (1.0 - visibility) ** (theFret + 1), z)
                freestyleTailMode = 1
                
                self.renderTail(length = length, color = color, fret = theFret, freestyleTail = freestyleTailMode, pos = pos)
                glPopMatrix()
                 
            
            if ( self.drumFillsActive and self.drumFillsHits >= 4 and z + length<self.boardLength ):
              glPushMatrix()
              color      = (.1 + .8 * c[0], .1 + .8 * c[1], .1 + .8 * c[2], 1.0 * visibility * f)
              glTranslatef(x, 0.0, z + length)
              self.renderNote(length, sustain = False, color = color, flat = False, tailOnly = False, isTappable = False, fret = 4, spNote = False, isOpen = False)
              glPopMatrix()
              
      self.freestyleActive = freestyleActive
      #self.drumFillOnScreen = drumFillOnScreen
      self.drumFillEvents = drumFillEvents
    

  def renderIncomingNeck(self, visibility, song, pos, time, neckTexture):   #MFH - attempt to "scroll" an incoming guitar solo neck towards the player
    if not song:
      return
    if not song.readyToGo:
      return
    
    def project(beat):
      return 0.125 * beat / beatsPerUnit    # glorandwarf: was 0.12

    v            = visibility
    w            = self.boardWidth
    l            = self.boardLength

    beatsPerUnit = self.beatsPerBoard / self.boardLength

    #offset       = (pos - self.lastBpmChange) / self.currentPeriod + self.baseBeat 
    offset = 0

    z  = ((time - pos) / self.currentPeriod) / beatsPerUnit

    color = (1,1,1)

    glEnable(GL_TEXTURE_2D)
    if neckTexture:
      neckTexture.texture.bind()


    glBegin(GL_TRIANGLE_STRIP)
    glColor4f(color[0],color[1],color[2], 0)
    glTexCoord2f(0.0, project(offset - 2 * beatsPerUnit))
    #glVertex3f(-w / 2, 0, -2)
    glVertex3f(-w / 2, 0, z)   #point A
    glTexCoord2f(1.0, project(offset - 2 * beatsPerUnit))
    #glVertex3f( w / 2, 0, -2)
    glVertex3f( w / 2, 0, z)   #point B

    
    glColor4f(color[0],color[1],color[2], v)
    glTexCoord2f(0.0, project(offset - 1 * beatsPerUnit))
    #glVertex3f(-w / 2, 0, -1)
    glVertex3f(-w / 2, 0, z+1)   #point C
    glTexCoord2f(1.0, project(offset - 1 * beatsPerUnit))
    #glVertex3f( w / 2, 0, -1)
    glVertex3f( w / 2, 0, z+1)   #point D
    
    glTexCoord2f(0.0, project(offset + l * beatsPerUnit * .7))
    #glVertex3f(-w / 2, 0, l * .7)
    glVertex3f(-w / 2, 0, z+2+l * .7) #point E
    glTexCoord2f(1.0, project(offset + l * beatsPerUnit * .7))
    #glVertex3f( w / 2, 0, l * .7)
    glVertex3f( w / 2, 0, z+2+l * .7) #point F
    
    glColor4f(color[0],color[1],color[2], 0)
    glTexCoord2f(0.0, project(offset + l * beatsPerUnit))
    #glVertex3f(-w / 2, 0, l)
    glVertex3f(-w / 2, 0, z+2+l)    #point G
    glTexCoord2f(1.0, project(offset + l * beatsPerUnit))
    #glVertex3f( w / 2, 0, l)
    glVertex3f( w / 2, 0, z+2+l)    #point H
    glEnd()
    
    glDisable(GL_TEXTURE_2D)

  def renderNeckMethod(self, visibility, offset, beatsPerUnit, neck, alpha = False): #blazingamer: New neck rendering method

    def project(beat):
      return 0.125 * beat / beatsPerUnit    # glorandwarf: was 0.12
    
    if self.starPowerActive and self.theme == 0:#8bit
      color = self.spColor #(.3,.7,.9)
    elif self.starPowerActive and self.theme == 1:
      color = self.spColor #(.3,.7,.9)
    else:
      color = (1,1,1)

    v            = visibility
    w            = self.boardWidth
    l            = self.boardLength

    beatsPerUnit = beatsPerUnit
    offset       = offset
    
    glEnable(GL_TEXTURE_2D)

    if alpha == True:
      glBlendFunc(GL_ONE, GL_ONE)
    neck.texture.bind()
    glBegin(GL_TRIANGLE_STRIP)
    glColor4f(color[0],color[1],color[2], 0)
    glTexCoord2f(0.0, project(offset - 2 * beatsPerUnit))
    glVertex3f(-w / 2, 0, -2)
    glTexCoord2f(1.0, project(offset - 2 * beatsPerUnit))
    glVertex3f( w / 2, 0, -2)
    
    glColor4f(color[0],color[1],color[2], v)
    glTexCoord2f(0.0, project(offset - 1 * beatsPerUnit))
    glVertex3f(-w / 2, 0, -1)
    glTexCoord2f(1.0, project(offset - 1 * beatsPerUnit))
    glVertex3f( w / 2, 0, -1)
    
    glTexCoord2f(0.0, project(offset + l * beatsPerUnit * .7))
    glVertex3f(-w / 2, 0, l * .7)
    glTexCoord2f(1.0, project(offset + l * beatsPerUnit * .7))
    glVertex3f( w / 2, 0, l * .7)
    
    glColor4f(color[0],color[1],color[2], 0)
    glTexCoord2f(0.0, project(offset + l * beatsPerUnit))
    glVertex3f(-w / 2, 0, l)
    glTexCoord2f(1.0, project(offset + l * beatsPerUnit))
    glVertex3f( w / 2, 0, l)
    glEnd()
    if alpha == True:
      glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
      
    glDisable(GL_TEXTURE_2D)
    
  def renderNeck(self, visibility, song, pos):
    if not song:
      return
    if not song.readyToGo:
      return
    
    def project(beat):
      return 0.125 * beat / beatsPerUnit    # glorandwarf: was 0.12

    v            = visibility
    w            = self.boardWidth
    l            = self.boardLength

    beatsPerUnit = self.beatsPerBoard / self.boardLength
    offset       = (pos - self.lastBpmChange) / self.currentPeriod + self.baseBeat 

    #myfingershurt: every theme can have oNeck:

    if self.guitarSolo and self.guitarSoloNeck != None and self.guitarSoloNeckMode == 1:
      neck = self.guitarSoloNeck
    elif self.starPowerActive and not (self.spcount2 != 0 and self.spcount < 1.2) and self.oNeck:
      neck = self.oNeck
    else:
      neck = self.neckDrawing

    if not (self.guitarSolo and self.guitarSoloNeck != None and self.guitarSoloNeckMode == 2):
      self.renderNeckMethod(v*self.neckAlpha[1], offset, beatsPerUnit, neck)
      
    if self.guitarSolo and self.guitarSoloNeck != None and self.guitarSoloNeckMode == 2:   #static overlay
      self.renderNeckMethod(v*self.neckAlpha[2], 0, beatsPerUnit, self.guitarSoloNeck)
      
    if self.spcount2 != 0 and self.spcount < 1.2 and self.oNeck:   #static overlay
      if self.oNeckovr != None and (self.scoreMultiplier > 4 or self.guitarSolo):
        neck = self.oNeckovr
      else:
        neck = self.oNeck
          
      self.renderNeckMethod(self.spcount*self.neckAlpha[3], offset, beatsPerUnit, neck)
      
    if self.starPowerActive and not (self.spcount2 != 0 and self.spcount < 1.2) and self.oNeck and (self.scoreMultiplier > 4 or self.guitarSolo):   #static overlay

      if self.oNeckovr != None:
        neck = self.oNeckovr
      else:
        neck = self.oNeck
        alpha = True

      self.renderNeckMethod(v*self.neckAlpha[3], offset, beatsPerUnit, neck, alpha)

    if Shader.list.enabled:
      posx = Shader.list.time()
      fade=0.2
      drum = []
      for i in range(5):
        drum.append(3*max(posx - Shader.list.var["drum"][i] + fade,0.01))
      r = 0.8 / drum[0] + 1.2 / drum[1] + 0.6 / drum[2]
      g = 0.8 / drum[0] + 0.6 / drum[2] + 1.2 / drum[4]
      b = 0.8 / drum[0] + 1.2 / drum[3]
      a = (r+g+b)/70.0
      Shader.list.var["drumcolor"]=(r,g,b,a)
          
    if Shader.list.enable("neck"): 
      Shader.list.setVar("fretcol",(r,g,b,a*1.5))
      Shader.list.setVar("fail",self.isFailing)
      Shader.list.update()
      
      glBegin(GL_TRIANGLE_STRIP)
      glVertex3f(-w / 2, 0.1, -2)
      glVertex3f(w / 2, 0.1, -2)
      glVertex3f(-w / 2, 0.1, l)
      glVertex3f(w / 2, 0.1, l)
      glEnd()
      Shader.list.disable() 
    else:
      if self.isFailing:
        self.renderNeckMethod(self.failcount*self.neckAlpha[4], 0, beatsPerUnit, self.failNeck)

  def drawTrack(self, visibility, song, pos):
    if not song:
      return
    if not song.readyToGo:
      return

    def project(beat):
      return 0.125 * beat / beatsPerUnit    # glorandwarf: was 0.12

    if self.theme == 0 or self.theme == 1:
      size = 2
    else:
      size = 0

    v            = visibility
    w            = self.boardWidth
    l            = self.boardLength

    beatsPerUnit = self.beatsPerBoard / self.boardLength
    offset       = (pos - self.lastBpmChange) / self.currentPeriod + self.baseBeat 

    glEnable(GL_TEXTURE_2D)

    #MFH - logic to briefly display oFlash
    if self.theme == 2 and self.overdriveFlashCount < self.overdriveFlashCounts and self.oFlash:
      self.overdriveFlashCount = self.overdriveFlashCount + 1
      self.oFlash.texture.bind()
    elif self.theme == 2 and self.starPowerActive and self.oCenterLines:
      self.oCenterLines.texture.bind()
    elif self.centerLines != None:
      self.centerLines.texture.bind()

    if self.staticStrings:    #MFH
    
      glBegin(GL_TRIANGLE_STRIP)
      glColor4f(1, 1, 1, v)
      glTexCoord2f(0.0, project(-2 * beatsPerUnit))
      glVertex3f(-w / 2, 0, -2+size)
      glTexCoord2f(1.0, project(-2 * beatsPerUnit))
      glVertex3f( w / 2, 0, -2+size)
      
      glColor4f(1, 1, 1, v)
      glTexCoord2f(0.0, project(-1 * beatsPerUnit))
      glVertex3f(-w / 2, 0, -1+size)
      glTexCoord2f(1.0, project(-1 * beatsPerUnit))
      glVertex3f( w / 2, 0, -1+size)
      
      glTexCoord2f(0.0, project(l * beatsPerUnit * .7))
      glVertex3f(-w / 2, 0, l * .7)
      glTexCoord2f(1.0, project(1 * beatsPerUnit * .7))
      glVertex3f( w / 2, 0, l * .7)
      
      glColor4f(1, 1, 1, 0)
      glTexCoord2f(0.0, project(l * beatsPerUnit))
      glVertex3f(-w / 2, 0, l)
      glTexCoord2f(1.0, project(1 * beatsPerUnit))
      glVertex3f( w / 2, 0, l)

    else:   #MFH: original moving strings

      glBegin(GL_TRIANGLE_STRIP)
      glColor4f(1, 1, 1, v)
      glTexCoord2f(0.0, project(offset - 2 * beatsPerUnit))
      glVertex3f(-w / 2, 0, -2+size)
      glTexCoord2f(1.0, project(offset - 2 * beatsPerUnit))
      glVertex3f( w / 2, 0, -2+size)
      
      glColor4f(1, 1, 1, v)
      glTexCoord2f(0.0, project(offset - 1 * beatsPerUnit))
      glVertex3f(-w / 2, 0, -1+size)
      glTexCoord2f(1.0, project(offset - 1 * beatsPerUnit))
      glVertex3f( w / 2, 0, -1+size)
      
      glTexCoord2f(0.0, project(offset + l * beatsPerUnit * .7))
      glVertex3f(-w / 2, 0, l * .7)
      glTexCoord2f(1.0, project(offset + l * beatsPerUnit * .7))
      glVertex3f( w / 2, 0, l * .7)
      
      glColor4f(1, 1, 1, 0)
      glTexCoord2f(0.0, project(offset + l * beatsPerUnit))
      glVertex3f(-w / 2, 0, l)
      glTexCoord2f(1.0, project(offset + l * beatsPerUnit))
      glVertex3f( w / 2, 0, l)

    glEnd()

    glDisable(GL_TEXTURE_2D)

  def drawSideBars(self, visibility, song, pos):
    if not song:
      return
    if not song.readyToGo:
      return

    def project(beat):
      return 0.125 * beat / beatsPerUnit  # glorandwarf: was 0.12

    v            = visibility
    w            = self.boardWidth + 0.15
    l            = self.boardLength

    beatsPerUnit = self.beatsPerBoard / self.boardLength
    offset       = (pos - self.lastBpmChange) / self.currentPeriod + self.baseBeat 

    c = (1,1,1)

    glEnable(GL_TEXTURE_2D)
    if self.theme == 2 and self.starPowerActive and self.oSideBars:
      self.oSideBars.texture.bind()
    else:
      self.sideBars.texture.bind()
    
    glBegin(GL_TRIANGLE_STRIP)
    glColor4f(c[0], c[1], c[2], 0)
    glTexCoord2f(0.0, project(offset - 2 * beatsPerUnit))
    glVertex3f(-w / 2, 0, -2)
    glTexCoord2f(1.0, project(offset - 2 * beatsPerUnit))
    glVertex3f( w / 2, 0, -2)
    
    glColor4f(c[0], c[1], c[2], v)
    glTexCoord2f(0.0, project(offset - 1 * beatsPerUnit))
    glVertex3f(-w / 2, 0, -1)
    glTexCoord2f(1.0, project(offset - 1 * beatsPerUnit))
    glVertex3f( w / 2, 0, -1)
    
    glTexCoord2f(0.0, project(offset + l * beatsPerUnit * .7))
    glVertex3f(-w / 2, 0, l * .7)
    glTexCoord2f(1.0, project(offset + l * beatsPerUnit * .7))
    glVertex3f( w / 2, 0, l * .7)
    
    glColor4f(c[0], c[1], c[2], 0)
    glTexCoord2f(0.0, project(offset + l * beatsPerUnit))
    glVertex3f(-w / 2, 0, l)
    glTexCoord2f(1.0, project(offset + l * beatsPerUnit))
    glVertex3f( w / 2, 0, l)
    glEnd()

    glDisable(GL_TEXTURE_2D)

  def drawBPM(self, visibility, song, pos):
    if not song:
      return
    if not song.readyToGo:
      return

    v            = visibility
    w            = self.boardWidth

    beatsPerUnit = self.beatsPerBoard / self.boardLength
    track = song.track[self.player]

    glEnable(GL_TEXTURE_2D)

    for time, event in track.getEvents(pos - self.currentPeriod * 2, pos + self.currentPeriod * self.beatsPerBoard):
      if not isinstance(event, Bars):
        continue   

      glPushMatrix()

      z  = ((time - pos) / self.currentPeriod) / beatsPerUnit
      z2 = ((time + event.length - pos) / self.currentPeriod) / beatsPerUnit

      if z > self.boardLength:
        f = (self.boardLength - z) / (self.boardLength * .2)
      elif z < 0:
        f = min(1, max(0, 1 + z2))
      else:
        f = 1.0
        
      if event.barType == 0: #half-beat
        sw  = 0.1 #width
        self.bpm_halfbeat.texture.bind()
      elif event.barType == 1: #beat
        sw  = 0.1 #width
        self.bpm_beat.texture.bind()
      elif event.barType == 2: #measure
        sw  = 0.1 #width
        self.bpm_measure.texture.bind()

      glColor4f(1, 1, 1, v)
      glBegin(GL_TRIANGLE_STRIP)
      glTexCoord2f(0.0, 1.0)
      glVertex3f(-(w / 2), 0, z + sw)
      glTexCoord2f(0.0, 0.0)
      glVertex3f(-(w / 2), 0, z - sw)
      glTexCoord2f(1.0, 1.0)
      glVertex3f(w / 2,    0, z + sw)
      glTexCoord2f(1.0, 0.0)
      glVertex3f(w / 2,    0, z - sw)
      glEnd()
      glPopMatrix()

    glDisable(GL_TEXTURE_2D)
    
  def renderTracks(self, visibility):
    if self.tracksColor[0] == -1:
      return
    w = self.boardWidth / self.strings
    v = 1.0 - visibility

    if self.editorMode:
      x = (self.strings / 2 - self.selectedString) * w
      s = 2 * w / self.strings
      z1 = -0.5 * visibility ** 2
      z2 = (self.boardLength - 0.5) * visibility ** 2
      
      glColor4f(1, 1, 1, .15)
      
      glBegin(GL_TRIANGLE_STRIP)
      glVertex3f(x - s, 0, z1)
      glVertex3f(x + s, 0, z1)
      glVertex3f(x - s, 0, z2)
      glVertex3f(x + s, 0, z2)
      glEnd()

    sw = 0.025
    for n in range(self.strings - 1, -1, -1):
      glBegin(GL_TRIANGLE_STRIP)
      glColor4f(self.tracksColor[0], self.tracksColor[1], self.tracksColor[2], 0)
      glVertex3f((n - self.strings / 2) * w - sw, -v, -2)
      glVertex3f((n - self.strings / 2) * w + sw, -v, -2)
      glColor4f(self.tracksColor[0], self.tracksColor[1], self.tracksColor[2], (1.0 - v) * .75)
      glVertex3f((n - self.strings / 2) * w - sw, -v, -1)
      glVertex3f((n - self.strings / 2) * w + sw, -v, -1)
      glColor4f(self.tracksColor[0], self.tracksColor[1], self.tracksColor[2], (1.0 - v) * .75)
      glVertex3f((n - self.strings / 2) * w - sw, -v, self.boardLength * .7)
      glVertex3f((n - self.strings / 2) * w + sw, -v, self.boardLength * .7)
      glColor4f(self.tracksColor[0], self.tracksColor[1], self.tracksColor[2], 0)
      glVertex3f((n - self.strings / 2) * w - sw, -v, self.boardLength)
      glVertex3f((n - self.strings / 2) * w + sw, -v, self.boardLength)
      glEnd()
      v *= 2   

  def renderBars(self, visibility, song, pos):
    if not song or self.tracksColor[0] == -1:
      return

    w = self.boardWidth
    v = 1.0 - visibility
    sw = 0.02

    beatsPerUnit = self.beatsPerBoard / self.boardLength
    pos         -= self.lastBpmChange
    offset       = pos / self.currentPeriod * beatsPerUnit
    currentBeat  = pos / self.currentPeriod
    beat         = int(currentBeat)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glPushMatrix()  
    while beat < currentBeat + self.beatsPerBoard:
      z = (beat - currentBeat) / beatsPerUnit

      if z > self.boardLength * .8:
        c = (self.boardLength - z) / (self.boardLength * .2)
      elif z < 0:
        c = max(0, 1 + z)
      else:
        c = 1.0
        
      glRotate(v * 90, 0, 0, 1)

      if (beat % 1.0) < 0.001:
        glColor4f(self.barsColor[0], self.barsColor[1], self.barsColor[2], visibility * c * .75)
      else:
        glColor4f(self.barsColor[0], self.barsColor[1], self.barsColor[2], visibility * c * .5)

      glBegin(GL_TRIANGLE_STRIP)
      glVertex3f(-(w / 2), -v, z + sw)
      glVertex3f(-(w / 2), -v, z - sw)
      glVertex3f(w / 2,    -v, z + sw)
      glVertex3f(w / 2,    -v, z - sw)
      glEnd()      

      if self.editorMode:
        beat += 1.0 / 4.0
      else:
        beat += 1
    glPopMatrix()

    Theme.setSelectedColor(visibility * .5)
    glBegin(GL_TRIANGLE_STRIP)
    glVertex3f(-w / 2, 0,  sw)
    glVertex3f(-w / 2, 0, -sw)
    glVertex3f(w / 2,  0,  sw)
    glVertex3f(w / 2,  0, -sw)
    glEnd()
    
  def renderTail(self, length, color, flat = False, fret = 0, freestyleTail = 0, pos = 0):

    #volshebnyi - if freestyleTail == 1, render an freestyle tail
    #  if freestyleTail == 2, render highlighted freestyle tail

    beatsPerUnit = self.beatsPerBoard / self.boardLength

    if flat:
      tailscale = (1, .1, 1)
    else:
      tailscale = None
      
    size = (.08, length + 0.00001)

    if size[1] > self.boardLength:
      s = self.boardLength
    else:
      s = (length + 0.00001)
      
    # render an inactive freestyle tail  (self.freestyle1 & self.freestyle2)
    zsize = .25  
    size = (.15, s - zsize)
    
    if self.drumFillsActive:
      if self.drumFillsHits >= 4:
        size = (.30, s - zsize)
      if self.drumFillsHits >= 3:
        size = (.25, s - zsize)
      elif self.drumFillsHits >= 2:
        size = (.21, s - zsize)
      elif self.drumFillsHits >= 1:
        size = (.17, s - zsize)
    
    if self.freestyleActive:
    	size = (.30, s - zsize)
       
    
    tex1 = self.freestyle1
    tex2 = self.freestyle2
    if freestyleTail == 1:
      #glColor4f(*color)
      c1, c2, c3, c4 = color
      tailGlow = 1 - (pos - self.freestyleLastFretHitTime[fret] ) / self.freestylePeriod
      if tailGlow < 0:
      	tailGlow = 0
      color = (c1 + c1*2.0*tailGlow, c2 + c2*2.0*tailGlow, c3 + c3*2.0*tailGlow, c4*0.6 + c4*0.4*tailGlow)    #MFH - this fades inactive tails' color darker                   
      
    tailcol = (color)

    self.engine.draw3Dtex(tex1, vertex = (-size[0], 0, size[0], size[1]), texcoord = (0.0, 0.0, 1.0, 1.0),
                          scale = tailscale, color = tailcol)

    self.engine.draw3Dtex(tex2, vertex = (-size[0], size[1] - (.05), size[0], size[1] + (zsize)),
                          scale = tailscale, texcoord = (0.0, 0.05, 1.0, 0.95), color = tailcol)

    self.engine.draw3Dtex(tex2, vertex = (-size[0], 0-(zsize), size[0], 0 + (.05)),
                          scale = tailscale, texcoord = (0.0, 0.95, 1.0, 0.05), color = tailcol)


  #myfingershurt:
  def renderNote(self, length, sustain, color, flat = False, tailOnly = False, isTappable = False, big = False, fret = 0, spNote = False, isOpen = False):    

    if flat:
      glScalef(1, .1, 1)

    beatsPerUnit = self.beatsPerBoard / self.boardLength

    if tailOnly:
      return

    #myfingershurt: this should be retrieved once at init, not repeatedly in-game whenever tails are rendered.
    
    if self.twoDnote == True:

      if self.notedisappear == True:#Notes keep on going when missed
        notecol = (1,1,1,1)#capo
      else:
        if flat:#Notes disappear when missed
          notecol = (.1,.1,.1,1)
        else:
          notecol = (1,1,1,1)

      tailOnly == True

      #death_au: Adjusted for different image.
      if self.separateDrumNotes:
        if isOpen:
          size = (self.boardWidth/1.9, (self.boardWidth/self.strings)/3.0)
          texSize = (0,1)
          if spNote == True:
            texY = (3.0/6.0,4.0/6.0)
          elif self.starPowerActive == True: #death_au: drum sp active notes.
            texY = (5.0/6.0,1.0)
          else:
            texY = (1.0/6.0,2.0/6.0)
      
        else:
          size = (self.boardWidth/self.strings/2, self.boardWidth/self.strings/2)
          fret -= 1
          texSize = (fret/4.0,fret/4.0+0.25)
          if spNote == True:
            texY = (2.0/6.0,3.0/6.0)
          elif self.starPowerActive == True: #death_au: drum sp active notes.
            texY = (4.0/6.0,5.0/6.0)
          else:
            texY = (0.0,1.0/6.0)
    
      else:   #automatically generate drum notes from Notes.png

        #myfingershurt: swapping notes 0 and 4:
        if fret == 0:
          #fret = 4     #fret 4 is angled, get fret 2 :)
          fret = 2
        elif fret == 4:
          fret = 0

    
          size = (self.boardWidth/self.strings/2, self.boardWidth/self.strings/2)
          texSize = (fret/5.0,fret/5.0+0.2)
          if spNote == True:
            if isTappable:
              texY = (0.6, 0.8)
            else:
              texY = (0.4,0.6)
          else:
            if isTappable:
              texY = (0.2,0.4)
            else:
              texY = (0,0.2)
          if self.starPowerActive:
            texY = (0.8,1)
            if isTappable:
              texSize = (0.2,0.4)
            else:
              texSize = (0,0.2)
            
        elif self.theme == 2:
          size = (self.boardWidth/self.strings/2, self.boardWidth/self.strings/2)
          texSize = (fret/5.0,fret/5.0+0.2)
          if spNote == True:
            if isTappable:
              texY = (3*0.166667, 4*0.166667)
            else:
              texY = (2*0.166667, 3*0.166667)
          else:
            if isTappable:
              texY = (1*0.166667, 2*0.166667)
            else:
              texY = (0, 1*0.166667)
            
          #rock band fret 0 needs to be reversed just like the fret to match angles better 
          if fret == 0:
            texSize = (fret/5.0+0.2,fret/5.0)
        
          #myfingershurt: adding spNote==False conditional so that star notes can appear in overdrive
          if self.starPowerActive and spNote == False:
            if isTappable:
              texY = (5*0.166667, 1)
            else:
              texY = (4*0.166667, 5*0.166667)

        if isOpen:
          size = (self.boardWidth/2.0, (self.boardWidth/self.strings)/40.0)

      self.engine.draw3Dtex(self.noteButtons, vertex = (-size[0],size[1],size[0],-size[1]), texcoord = (texSize[0],texY[0],texSize[1],texY[1]),
                            scale = (1,1,1), multiples = True, color = (1,1,1), vertscale = .2)

    else:  

      #mesh = outer ring (black) 
      #mesh_001 = main note (key color) 
      #mesh_002 = top (spot or hopo if no mesh_003) 
      #mesh_003 = hopo bump (hopo color)

      if fret == 0:
        #fret = 4     #fret 4 is angled, get fret 2 :)
        fret = 2
      elif fret == 4:
        fret = 0
          
      if spNote == True and self.starMesh != None and isOpen == False:
        note = self.starMesh
      elif isOpen == True and self.openMesh != None:
        note = self.openMesh
      else:
        note = self.noteMesh

      glPushMatrix()
      glEnable(GL_DEPTH_TEST)
      glDepthMask(1)
      glShadeModel(GL_SMOOTH)
      
      if spNote == True and self.threeDspin == True and isOpen == False:
        glRotate(90 + self.time/3, 0, 1, 0)
      if isOpen == False and spNote == False and self.noterotate == True:
        glRotatef(90, 0, 1, 0)
        glRotatef(-90, 1, 0, 0)

      if fret == 0: 
        glRotate(Theme.noterotdegrees, 0, 0, Theme.noterot5)
      elif fret == 1:
        glRotate(Theme.noterotdegrees, 0, 0, Theme.noterot2)
      elif fret == 2:
        glRotate(Theme.noterotdegrees, 0, 0, Theme.noterot1)
      elif fret == 3:
        glRotate(Theme.noterotdegrees, 0, 0, Theme.noterot4)
      elif isOpen == True:
        glRotate(Theme.noterotdegrees, 0, 0, Theme.noterot3)
        
      if self.notetex == True and spNote == False and isOpen==False:
          
        glColor3f(1,1,1)
        glEnable(GL_TEXTURE_2D)
        if fret == 0: 
          self.notetexa.texture.bind()
        elif fret == 1:
          self.notetexb.texture.bind()
        elif fret == 2:
          self.notetexc.texture.bind()
        elif fret == 3:
          self.notetexd.texture.bind()
        glMatrixMode(GL_TEXTURE)
        glScalef(1, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        if isTappable:
          self.noteMesh.render("Mesh_001")
        else:
          self.noteMesh.render("Mesh")
        glMatrixMode(GL_TEXTURE)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
        glDisable(GL_TEXTURE_2D)

      elif self.startex == True and spNote == True and isOpen==False:
        glColor3f(1,1,1)
        glEnable(GL_TEXTURE_2D)
        if fret == 0: 
          self.startexa.texture.bind()
        elif fret == 1:
          self.startexb.texture.bind()
        elif fret == 2:
          self.startexc.texture.bind()
        elif fret == 3:
          self.startexd.texture.bind()
        glMatrixMode(GL_TEXTURE)
        glScalef(1, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        if isTappable:
          self.starMesh.render("Mesh_001")
        else:
          self.starMesh.render("Mesh")
        glMatrixMode(GL_TEXTURE)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
        glDisable(GL_TEXTURE_2D)

      elif self.opentex == True and isOpen==True:
        glColor3f(1,1,1)
        glEnable(GL_TEXTURE_2D)
        
        self.opentexture.texture.bind()

        glMatrixMode(GL_TEXTURE)
        glScalef(1, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        self.openMesh.render()
        glMatrixMode(GL_TEXTURE)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
        glDisable(GL_TEXTURE_2D)
      else: 
          #death_au: fixed 3D note colours
          glColor4f(*color)
          if self.starPowerActive and self.theme != 2 and not color == (0,0,0,1):
            glColor4f(self.spColor[0],self.spColor[1],self.spColor[2],1)
            #glColor4f(.3,.7,.9, 1)
          if isOpen == True and self.starPowerActive == False:
            glColor4f(self.opencolor[0],self.opencolor[1],self.opencolor[2], 1)

          note.render("Mesh_001")
          glColor3f(self.spotColor[0], self.spotColor[1], self.spotColor[2])
          note.render("Mesh_002")
          glColor3f(self.meshColor[0], self.meshColor[1], self.meshColor[2])
          note.render("Mesh")



      glDepthMask(0)
      glPopMatrix()

  def renderIncomingNecks(self, visibility, song, pos):
    if not song:
      return
    if not song.readyToGo:
      return

    if self.incomingNeckMode > 0:   #if enabled
      boardWindowMin = pos - self.currentPeriod * 2
      boardWindowMax = pos + self.currentPeriod * self.beatsPerBoard


      #if self.song.hasStarpowerPaths and self.song.midiStyle == Song.MIDI_TYPE_RB:  
      if self.useMidiSoloMarkers:
        track = song.midiEventTrack[self.player]
        for time, event in track.getEvents(boardWindowMin, boardWindowMax):
          if isinstance(event, Song.MarkerNote):
            if event.number == Song.starPowerMarkingNote:
              if self.guitarSoloNeck:
                if event.endMarker:   #solo end
                  if self.incomingNeckMode == 2:    #render both start and end incoming necks
                    if self.guitarSolo:   #only until the end of the guitar solo!
                      if self.starPowerActive and self.oNeck:
                        neckImg = self.oNeck
                      elif self.scoreMultiplier > 4 and self.bassGrooveNeck != None and self.bassGrooveNeckMode == 1:
                        neckImg = self.bassGrooveNeck
                      else:
                        neckImg = self.neckDrawing
                      self.renderIncomingNeck(visibility, song, pos, time, neckImg)
                else:   #solo start
                  if not self.guitarSolo:   #only until guitar solo starts!
                    neckImg = self.guitarSoloNeck
                    self.renderIncomingNeck(visibility, song, pos, time, neckImg)
              

      else:   #fall back on text-based guitar solo marking track
        for time, event in song.eventTracks[Song.TK_GUITAR_SOLOS].getEvents(boardWindowMin, boardWindowMax):
          if self.canGuitarSolo and self.guitarSoloNeck:
            if event.text.find("ON") >= 0:
              if not self.guitarSolo:   #only until guitar solo starts!
                neckImg = self.guitarSoloNeck
                self.renderIncomingNeck(visibility, song, pos, time, neckImg)
            #else: #event.text.find("OFF"):
            elif self.incomingNeckMode == 2:    #render both start and end incoming necks
              if self.guitarSolo:   #only until the end of the guitar solo!
                if self.starPowerActive and self.oNeck:
                  neckImg = self.oNeck
                elif self.scoreMultiplier > 4 and self.bassGrooveNeck != None and self.bassGrooveNeckMode == 1:
                  neckImg = self.bassGrooveNeck
                else:
                  neckImg = self.neckDrawing
                self.renderIncomingNeck(visibility, song, pos, time, neckImg)
              


  def renderOpenNotes(self, visibility, song, pos):
    if not song:
      return
    if not song.readyToGo:
      return

    self.bigMax = 0

    self.currentPeriod = self.neckSpeed
    self.targetPeriod  = self.neckSpeed

    self.killPoints = False

    beatsPerUnit = self.beatsPerBoard / self.boardLength
    w = self.boardWidth / self.strings
    track = song.track[self.player]

    num = 0
    enable = True

    self.openStarNotesInView = False
    #for time, event in track.getEvents(pos - self.currentPeriod * 2, pos + self.currentPeriod * self.beatsPerBoard):
    for time, event in reversed(track.getEvents(pos - self.currentPeriod * 2, pos + self.currentPeriod * self.beatsPerBoard)):    #MFH - reverse order of note rendering
      if isinstance(event, Tempo):
        self.tempoBpm = event.bpm
        if self.lastBpmChange > 0 and self.disableVBPM == True:
            continue
        if (pos - time > self.currentPeriod or self.lastBpmChange < 0) and time > self.lastBpmChange:
          self.baseBeat         += (time - self.lastBpmChange) / self.currentPeriod
          self.targetBpm         = event.bpm
          self.lastBpmChange     = time
        #  self.setBPM(self.targetBpm) # glorandwarf: was setDynamicBPM(self.targetBpm)
        continue
      
      if not isinstance(event, Note):
        continue

      if (event.noteBpm == 0.0):
        event.noteBpm = self.tempoBpm
      
      if self.coOpFailed:
        if self.coOpRestart:
          if time - self.coOpRescueTime < (self.currentPeriod * self.beatsPerBoard * 2):
            continue
          elif self.coOpRescueTime + (self.currentPeriod * self.beatsPerBoard * 2) < pos:
            self.coOpFailed = False
            self.coOpRestart = False
            Log.debug("Turning off coOpFailed. Rescue successful.")
        else:
          continue #can't break. Tempo.

      if event.number != 0:   #skip all regular notes
        continue

      c = self.fretColors[event.number]
      
      isOpen = False
      if event.number == 0: #treat open string note differently
        x  = (self.strings / 2 - .5 - 1.5) * w
        isOpen     = True
        c = self.fretColors[4]          #myfingershurt: need to swap note 0 and note 4 colors for drums:
      else:   #one of the other 4 drum notes
        x  = (self.strings / 2 - .5 - (event.number - 1)) * w
        if event.number == 4:
          c = self.fretColors[0]        #myfingershurt: need to swap note 0 and note 4 colors for drums:

      z  = ((time - pos) / self.currentPeriod) / beatsPerUnit
      z2 = ((time + event.length - pos) / self.currentPeriod) / beatsPerUnit

      if z > self.boardLength * .8:
        f = (self.boardLength - z) / (self.boardLength * .2)
      elif z < 0:
        f = min(1, max(0, 1 + z2))
      else:
        f = 1.0
        
      #volshebnyi - hide open notes in BRE zone if BRE enabled  
      if self.freestyleEnabled and self.freestyleStart > 0:  
        if self.drumFillsReady or self.freestyleReady:
          if time > self.freestyleStart - self.freestyleOffset and time < self.freestyleStart + self.freestyleOffset + self.freestyleLength:
            z = -2.0

      color      = (.1 + .8 * c[0], .1 + .8 * c[1], .1 + .8 * c[2], 1 * visibility * f)
      length = 0
      flat       = False
      tailOnly   = False
      spNote = False

      #myfingershurt: user setting for starpower refill / replenish notes
      #if self.starPowerActive and self.theme != 2:  #Rock Band theme allows SP notes in overdrive
      if self.starPowerActive:
        if self.spRefillMode == 0:    #mode 0 = no starpower / overdrive refill notes
          self.spEnabled = False
        elif self.spRefillMode == 1 and self.theme != 2:  #mode 1 = overdrive refill notes in RB themes only
          self.spEnabled = False
        elif self.spRefillMode == 2 and song.midiStyle != 1: #mode 2 = refill based on MIDI type
          self.spEnabled = False

      if event.star:
        #self.isStarPhrase = True
        self.openStarNotesInView = True
      if event.finalStar:
        self.finalStarSeen = True
        self.openStarNotesInView = True

      if event.star and self.spEnabled:
        spNote = True
      if event.finalStar and self.spEnabled:
        spNote = True
        if event.played or event.hopod:
          if event.flameCount < 1 and not self.starPowerGained:

            #if self.drumFillOnScreen:   #MFH - if there's a drum fill on the screen right now, skip it!
            if self.starPower < 50:   #not enough starpower to activate yet, kill existing drumfills
              for dfEvent in self.drumFillEvents:
                dfEvent.happened = True
            
            if self.starPower < 100:
              self.starPower += 25
            if self.starPower > 100:
              self.starPower = 100
            self.overdriveFlashCount = 0  #MFH - this triggers the oFlash strings & timer
            self.starPowerGained = True
            

      #if enable:
      #  self.spEnabled = True

      isTappable = False

      if self.notedisappear == True:#Notes keep on going when missed
        ###Capo###
        if event.played or event.hopod:
          tailOnly = True
          length += z
          z = 0
          if length <= 0:
            continue
        if z < 0 and not (event.played or event.hopod): 
          color = (.2 + .4, .2 + .4, .2 + .4, .5 * visibility * f)
          flat  = True
        ###endCapo###
      else:#Notes disappear when missed
        if z < 0:
          if event.played or event.hopod:
            tailOnly = True
            length += z
            z = 0
            if length <= 0:
              continue
          else:
            color = (.2 + .4, .2 + .4, .2 + .4, .5 * visibility * f)
            flat  = True

      sustain = False
        
      
      glPushMatrix()
      glTranslatef(x, (1.0 - visibility) ** (event.number + 1), z)
      self.renderNote(length, sustain = sustain, color = color, flat = flat, tailOnly = tailOnly, isTappable = isTappable, fret = event.number, spNote = spNote, isOpen = isOpen)
      glPopMatrix()

    #myfingershurt: end FOR loop / note rendering loop       
    if (not self.openStarNotesInView) and (not self.starNotesInView) and self.finalStarSeen:
      self.spEnabled = True
      self.finalStarSeen = False
      self.isStarPhrase = False

  def renderNotes(self, visibility, song, pos):
    if not song:
      return
    if not song.readyToGo:
      return

    self.bigMax = 0

    self.currentPeriod = self.neckSpeed
    self.targetPeriod  = self.neckSpeed

    self.killPoints = False

    beatsPerUnit = self.beatsPerBoard / self.boardLength
    w = self.boardWidth / self.strings
    track = song.track[self.player]

    num = 0
    enable = True
    self.starNotesInView = False
    
    #for time, event in track.getEvents(pos - self.currentPeriod * 2, pos + self.currentPeriod * self.beatsPerBoard):
    for time, event in reversed(track.getEvents(pos - self.currentPeriod * 2, pos + self.currentPeriod * self.beatsPerBoard)):    #MFH - reverse order of note rendering
      if isinstance(event, Tempo):
        self.tempoBpm = event.bpm
        if self.lastBpmChange > 0 and self.disableVBPM == True:
            continue
        if (pos - time > self.currentPeriod or self.lastBpmChange < 0) and time > self.lastBpmChange:
          self.baseBeat         += (time - self.lastBpmChange) / self.currentPeriod
          self.targetBpm         = event.bpm
          self.lastBpmChange     = time
        #  self.setBPM(self.targetBpm) # glorandwarf: was setDynamicBPM(self.targetBpm)
        continue
      
      if not isinstance(event, Note):
        continue

      if (event.noteBpm == 0.0):
        event.noteBpm = self.tempoBpm

      #volshebnyi - removed
      if event.number == 0: #MFH - skip all open notes
        continue
      
      if self.coOpFailed:
        if self.coOpRestart:
          if time - self.coOpRescueTime < (self.currentPeriod * self.beatsPerBoard * 2):
            continue
          elif self.coOpRescueTime + (self.currentPeriod * self.beatsPerBoard * 2) < pos:
            self.coOpFailed = False
            self.coOpRestart = False
            Log.debug("Turning off coOpFailed. Rescue successful.")
        else:
          continue #can't break. Tempo.

      c = self.fretColors[event.number]
      
      if event.star:
        #self.isStarPhrase = True
        self.starNotesInView = True
      if event.finalStar:
        self.finalStarSeen = True
        self.starNotesInView = True
      
      isOpen = False
      if event.number == 0: #treat open string note differently
        x  = (self.strings / 2 - .5 - 1.5) * w
        isOpen     = True
        c = self.fretColors[4]          #myfingershurt: need to swap note 0 and note 4 colors for drums:
      else:   #one of the other 4 drum notes
        x  = (self.strings / 2 - .5 - (event.number - 1)) * w
        if event.number == 4:
          c = self.fretColors[0]        #myfingershurt: need to swap note 0 and note 4 colors for drums:

      z  = ((time - pos) / self.currentPeriod) / beatsPerUnit
      z2 = ((time + event.length - pos) / self.currentPeriod) / beatsPerUnit

      if z > self.boardLength * .8:
        f = (self.boardLength - z) / (self.boardLength * .2)
      elif z < 0:
        f = min(1, max(0, 1 + z2))
      else:
        f = 1.0
        
      #volshebnyi - hide notes in BRE zone if BRE enabled  
      if self.freestyleEnabled:
        if self.drumFillsReady or self.freestyleReady:  
          if time > self.freestyleStart - self.freestyleOffset and time < self.freestyleStart + self.freestyleOffset + self.freestyleLength:
            z = -2.0

      color      = (.1 + .8 * c[0], .1 + .8 * c[1], .1 + .8 * c[2], 1 * visibility * f)
      length = 0
      flat       = False
      tailOnly   = False
      spNote = False

      #myfingershurt: user setting for starpower refill / replenish notes
      #if self.starPowerActive and self.theme != 2:  #Rock Band theme allows SP notes in overdrive
      if self.starPowerActive:
        if self.spRefillMode == 0:    #mode 0 = no starpower / overdrive refill notes
          self.spEnabled = False
        elif self.spRefillMode == 1 and self.theme != 2:  #mode 1 = overdrive refill notes in RB themes only
          self.spEnabled = False
        elif self.spRefillMode == 2 and song.midiStyle != 1: #mode 2 = refill based on MIDI type
          self.spEnabled = False


      if event.star and self.spEnabled:
        spNote = True
      if event.finalStar and self.spEnabled:
        spNote = True
        if event.played or event.hopod:
          if event.flameCount < 1 and not self.starPowerGained:

            #if self.drumFillOnScreen:   #MFH - if there's a drum fill on the screen right now, skip it!
            if self.starPower < 50:   #not enough starpower to activate yet, kill existing drumfills
              for dfEvent in self.drumFillEvents:
                dfEvent.happened = True

            if self.starPower < 100:
              self.starPower += 25
            if self.starPower > 100:
              self.starPower = 100
            self.overdriveFlashCount = 0  #MFH - this triggers the oFlash strings & timer
            self.starPowerGained = True
            if self.theme == 2 and self.oFlash != None:
              self.ocount = 0

      #if enable:
      #  self.spEnabled = True

      isTappable = False

      if self.notedisappear == True:#Notes keep on going when missed
        ###Capo###
        if event.played or event.hopod:
          tailOnly = True
          length += z
          z = 0
          if length <= 0:
            continue
        if z < 0 and not (event.played or event.hopod): 
          color = (.2 + .4, .2 + .4, .2 + .4, .5 * visibility * f)
          flat  = True
        ###endCapo###
      else:#Notes disappear when missed
        if z < 0:
          if event.played or event.hopod:
            tailOnly = True
            length += z
            z = 0
            if length <= 0:
              continue
          else:
            color = (.2 + .4, .2 + .4, .2 + .4, .5 * visibility * f)
            flat  = True

      sustain = False
        
      
      glPushMatrix()
      glTranslatef(x, (1.0 - visibility) ** (event.number + 1), z)
      self.renderNote(length, sustain = sustain, color = color, flat = flat, tailOnly = tailOnly, isTappable = isTappable, fret = event.number, spNote = spNote, isOpen = isOpen)
      glPopMatrix()

    #myfingershurt: end FOR loop / note rendering loop       
    if (not self.openStarNotesInView) and (not self.starNotesInView) and self.finalStarSeen:
      self.spEnabled = True
      self.isStarPhrase = False
      self.finalStarSeen = False

  def renderFrets(self, visibility, song, controls):
    w = self.boardWidth / self.strings
    size = (.22, .22)
    v = 1.0 - visibility
    
    glEnable(GL_DEPTH_TEST)
    
    #Hitglow color option - myfingershurt sez this should be a Guitar class global, not retrieved ever fret render in-game...
    #self.hitglow_color = self.engine.config.get("video", "hitglow_color")
    
    for n in range(self.strings):
      f = self.fretWeight[n]

      if n == 3:
        c = self.fretColors[0]
      else:
        c = self.fretColors[n + 1]

      if f and (controls.getState(self.keys[0]) or controls.getState(self.keys[5])):
        f += 0.25

      glColor4f(.1 + .8 * c[0] + f, .1 + .8 * c[1] + f, .1 + .8 * c[2] + f, visibility)
      y = v + f / 6
      x = (self.strings / 2 - .5 - n) * w

      if self.twoDkeys == True: #death_au

        size = (self.boardWidth/self.strings/2, self.boardWidth/self.strings/2.4)
        whichFret = n

        #death_au: only with old-style drum fret images
        if self.drumFretButtons == None:
          whichFret = n+1
          if whichFret == 4:
            whichFret = 0
            #reversing fret 0 since it's angled in Rock Band
            texSize = (whichFret/5.0+0.2,whichFret/5.0)
          else:
            #texSize = (n/5.0,n/5.0+0.2)
            texSize = (whichFret/5.0,whichFret/5.0+0.2)
          
          texY = (0.0,1.0/3.0)
          if controls.getState(self.keys[n+1]):
            texY = (1.0/3.0,2.0/3.0)
          #myfingershurt: also want to show when alternate drumkeys are pressed!
          if controls.getState(self.keys[n+6]):
            texY = (1.0/3.0,2.0/3.0)
          if self.hit[n]:
            texY = (2.0/3.0,1.0)
        #death_au: only with new drum fret images
        else:
          texSize = (whichFret/4.0,whichFret/4.0+0.25)
          
          texY = (0.0,1.0/6.0)
          if controls.getState(self.keys[n+1]):
            texY = (2.0/6.0,3.0/6.0)
          #myfingershurt: also want to show when alternate drumkeys are pressed!
          if controls.getState(self.keys[n+6]):
            texY = (2.0/6.0,3.0/6.0)
          if self.hit[n]:
            texY = (4.0/6.0,5.0/6.0)
        if self.drumFretButtons == None:
          self.engine.draw3Dtex(self.fretButtons, vertex = (size[0],size[1],-size[0],-size[1]), texcoord = (texSize[0], texY[0], texSize[1], texY[1]),
                              coord = (x,v,0), multiples = True,color = (1,1,1), depth = True)
        else:
          self.engine.draw3Dtex(self.drumFretButtons, vertex = (size[0],size[1],-size[0],-size[1]), texcoord = (texSize[0], texY[0], texSize[1], texY[1]),
                              coord = (x,v,0), multiples = True,color = (1,1,1), depth = True)

        
      else: #death_au
        if n == 3:
          c = self.fretColors[0]
        else:
          c = self.fretColors[n + 1]
      
        if self.keyMesh:
          glPushMatrix()
          #glTranslatef(x, y + v * 6, 0)
          glDepthMask(1)
          glEnable(GL_LIGHTING)
          glEnable(GL_LIGHT0)
          glShadeModel(GL_SMOOTH)
          glRotatef(90, 0, 1, 0)
          glLightfv(GL_LIGHT0, GL_POSITION, (5.0, 10.0, -10.0, 0.0))
          glLightfv(GL_LIGHT0, GL_AMBIENT,  (.2, .2, .2, 0.0))
          glLightfv(GL_LIGHT0, GL_DIFFUSE,  (1.0, 1.0, 1.0, 0.0))
          glRotatef(-90, 1, 0, 0)
          glRotatef(-90, 0, 0, 1)
          #glColor4f(.1 + .8 * c[0] + f, .1 + .8 * c[1] + f, .1 + .8 * c[2] + f, visibility)

          #Mesh - Main fret
          #Key_001 - Top of fret (key_color)
          #Key_002 - Bottom of fret (key2_color)
          #Glow_001 - Only rendered when a note is hit along with the glow.svg

          if n == 0: 
            glRotate(Theme.noterotdegrees, 0, 0, Theme.noterot2)
          elif n == 1:
            glRotate(Theme.noterotdegrees, 0, 0, Theme.noterot3)
          elif n == 2:
            glRotate(Theme.noterotdegrees, 0, 0, Theme.noterot4)
          elif n == 3:
            glRotate(Theme.noterotdegrees, 0, 0, Theme.noterot1)
        
          if self.keytex == True:
            glColor4f(1,1,1,visibility)
            glTranslatef(x, v, 0)
            glEnable(GL_TEXTURE_2D)
            if n == 0: 
              self.keytexb.texture.bind()
            elif n == 1:
              self.keytexc.texture.bind()
            elif n == 2:
              self.keytexd.texture.bind()
            elif n == 3:
              self.keytexa.texture.bind()
            glMatrixMode(GL_TEXTURE)
            glScalef(1, -1, 1)
            glMatrixMode(GL_MODELVIEW)
            if f and not self.hit[n]:
              self.keyMesh.render("Mesh_001")
            elif self.hit[n]:
              self.keyMesh.render("Mesh_002")
            else:
              self.keyMesh.render("Mesh")
            glMatrixMode(GL_TEXTURE)
            glLoadIdentity()
            glMatrixMode(GL_MODELVIEW)
            glDisable(GL_TEXTURE_2D)
          else:
            glColor4f(.1 + .8 * c[0] + f, .1 + .8 * c[1] + f, .1 + .8 * c[2] + f, visibility)
            glTranslatef(x, y + v * 6, 0)
            key = self.keyMesh
        
            if(key.find("Glow_001")) == True:
              key.render("Mesh")
              if(key.find("Key_001")) == True:
                glColor3f(self.keyColor[0], self.keyColor[1], self.keyColor[2])
                key.render("Key_001")
              if(key.find("Key_002")) == True:
                glColor3f(self.key2Color[0], self.key2Color[1], self.key2Color[2])
                key.render("Key_002")
            else:
              key.render()
          
          glDisable(GL_LIGHTING)
          glDisable(GL_LIGHT0)
          glDepthMask(0)
          glPopMatrix()
      ######################
      f = self.fretActivity[n]

      if f and self.disableFretSFX != True:
        glBlendFunc(GL_ONE, GL_ONE)

        if self.glowColor[0] == -1:
          s = 1.0
        else:
          s = 0.0
        
        while s < 1:
          ms = s * (math.sin(self.time) * .25 + 1)
          if self.glowColor[0] == -2:
            glColor3f(c[0] * (1 - ms), c[1] * (1 - ms), c[2] * (1 - ms))
          else:
            glColor3f(self.glowColor[0] * (1 - ms), self.glowColor[1] * (1 - ms), self.glowColor[2] * (1 - ms))
          
          glPushMatrix()
          glTranslate(x, y, 0)
          glScalef(.1 + .02 * ms * f, .1 + .02 * ms * f, .1 + .02 * ms * f)
          glRotatef( 90, 0, 1, 0)
          glRotatef(-90, 1, 0, 0)
          glRotatef(-90, 0, 0, 1)
          if self.twoDkeys == False and self.keytex == False:
            if(self.keyMesh.find("Glow_001")) == True:
              key.render("Glow_001")
            else:
              key.render()
          glPopMatrix()
          s += 0.2
        #Hitglow color
        if self.hitglow_color == 0:
          glowcol = (c[0], c[1], c[2])#Same as fret
        elif self.hitglow_color == 1:
          glowcol = (1, 1, 1)#Actual color in .svg-file

        f += 2

        self.engine.draw3Dtex(self.glowDrawing, coord = (x, y, 0.01), rot = (f * 90 + self.time, 0, 1, 0),
                              texcoord = (0.0, 0.0, 1.0, 1.0), vertex = (-size[0] * f, -size[1] * f, size[0] * f, size[1] * f),
                              multiples = True, alpha = True, color = glowcol)
      self.hit[n] = False
    
        ###############################################
    
    #death_au:
    #if we leave the depth test enabled, it thinks that the bass drum images
    #are under the other frets and openGL culls them. So I just leave it disabled
    glDisable(GL_DEPTH_TEST)
    
    if self.twoDkeys == True and self.drumFretButtons != None: #death_au
      
      x = 0.0#(self.boardWidth / 2 )

      size = (self.boardWidth/2, self.boardWidth/self.strings/2.4)

      texSize = (0.0,1.0)
      
      texY = (1.0/6.0,2.0/6.0)
      if controls.getState(self.keys[0]) or controls.getState(self.keys[5]):
        texY = (3.0/6.0,4.0/6.0)
      if self.hit[0]:
        texY = (5.0/6.0,1.0)
        
      self.engine.draw3Dtex(self.drumFretButtons, vertex = (size[0],size[1],-size[0],-size[1]), texcoord = (texSize[0], texY[0], texSize[1], texY[1]),
                              coord = (x,v,0), multiples = True,color = (1,1,1), depth = True)

    ###############################################



  def renderFlames(self, visibility, song, pos, controls):
    if not song or self.flameColors[0][0][0] == -1:
      return

    beatsPerUnit = self.beatsPerBoard / self.boardLength
    w = self.boardWidth / self.strings
    track = song.track[self.player]

    size = (.22, .22)
    v = 1.0 - visibility

    #blazingamer- hitglow logic is not required for drums since you can not perform holds with drum pads, uncomment out if you disagree with this

##    if self.disableFlameSFX != True:
##      for n in range(self.strings):
##        f = self.fretWeight[n]
##        
##        #c = self.fretColors[n]
##        c = self.fretColors[n+1]
##        if f and (controls.getState(self.keys[0]) or controls.getState(self.keys[5])):
##          f += 0.25     
##        y = v + f / 6
##
##        x = (self.strings / 2 -.5 - n) * w
##
##
##        f = self.fretActivity[n]
##
##        if f:
##          ms = math.sin(self.time) * .25 + 1
##          ff = f
##          ff += 1.2
##          
##          glBlendFunc(GL_ONE, GL_ONE)
##
##          flameSize = self.flameSizes[self.scoreMultiplier - 1][n]
##          if self.theme == 0 or self.theme == 1: #THIS SETS UP GH3 COLOR, ELSE ROCKBAND(which is DEFAULT in Theme.py)
##            flameColor = self.gh3flameColor
##          else:
##            flameColor = self.flameColors[self.scoreMultiplier - 1][n]
##          #Below was an if that set the "flame"-color to the same as the fret color if there was no specific flamecolor defined.
##
##          flameColorMod0 = 1.1973333333333333333333333333333
##          flameColorMod1 = 1.9710526315789473684210526315789
##          flameColorMod2 = 10.592592592592592592592592592593
##          
##          glColor3f(flameColor[0] * flameColorMod0, flameColor[1] * flameColorMod1, flameColor[2] * flameColorMod2)
##          if self.starPowerActive:
##            if self.theme == 0 or self.theme == 1: #GH3 starcolor
##              glColor3f(self.spColor[0],self.spColor[1],self.spColor[2])
##              #glColor3f(.3,.7,.9)
##            else: #Default starcolor (Rockband)
##              glColor3f(.9,.9,.9)
##
##          if not self.Hitanim:   
##            glEnable(GL_TEXTURE_2D)
##            self.hitglowDrawing.texture.bind()    
##            glPushMatrix()
##            glTranslate(x, y + .125, 0)
##            glRotate(90, 1, 0, 0)
##            glScalef(0.5 + .6 * ms * ff, 1.5 + .6 * ms * ff, 1 + .6 * ms * ff)
##            glBegin(GL_TRIANGLE_STRIP)
##            glTexCoord2f(0.0, 0.0)
##            glVertex3f(-flameSize * ff, 0, -flameSize * ff)
##            glTexCoord2f(1.0, 0.0)
##            glVertex3f( flameSize * ff, 0, -flameSize * ff)
##            glTexCoord2f(0.0, 1.0)
##            glVertex3f(-flameSize * ff, 0,  flameSize * ff)
##            glTexCoord2f(1.0, 1.0)
##            glVertex3f( flameSize * ff, 0,  flameSize * ff)
##            glEnd()
##            glPopMatrix()
##            glDisable(GL_TEXTURE_2D)
##            #Alarian: Animated hitflames
##          else:
##            self.HCount = self.HCount + 1
##            if self.HCount > self.Animspeed-1:
##              self.HCount = 0
##            HIndex = (self.HCount * 16 - (self.HCount * 16) % self.Animspeed) / self.Animspeed
##            if HIndex > 15:
##              HIndex = 0
##            texX = (HIndex*(1/16.0), HIndex*(1/16.0)+(1/16.0))
##
##            glColor3f(1,1,1)
##            glEnable(GL_TEXTURE_2D)
##            self.hitglowAnim.texture.bind()    
##            glPushMatrix()
##            glTranslate(x, y + .225, 0)
##            glRotate(90, 1, 0, 0)
##            
##            #glScalef(1.3, 1, 2)
##            #glScalef(1.7, 1, 2.6)
##            glScalef(2, 1, 2.9)   #worldrave correct flame size
##
##            
##            glBegin(GL_TRIANGLE_STRIP)
##            glTexCoord2f(texX[0], 0.0)#upper left corner of frame square in .png
##            glVertex3f(-flameSize * ff, 0, -flameSize * ff)#"upper left" corner of surface that texture is rendered on
##            glTexCoord2f(texX[1], 0.0)#upper right
##            glVertex3f( flameSize * ff, 0, -flameSize * ff)
##            glTexCoord2f(texX[0], 1.0)#lower left
##            glVertex3f(-flameSize * ff, 0,  flameSize * ff)
##            glTexCoord2f(texX[1], 1.0)#lower right
##            glVertex3f( flameSize * ff, 0,  flameSize * ff)
##            glEnd()
##            glPopMatrix()
##            glDisable(GL_TEXTURE_2D)
##
##          ff += .3
##
##          #flameSize = self.flameSizes[self.scoreMultiplier - 1][n]
##          #flameColor = self.flameColors[self.scoreMultiplier - 1][n]
##
##          flameColorMod0 = 1.1973333333333333333333333333333
##          flameColorMod1 = 1.7842105263157894736842105263158
##          flameColorMod2 = 12.222222222222222222222222222222
##          
##          glColor3f(flameColor[0] * flameColorMod0, flameColor[1] * flameColorMod1, flameColor[2] * flameColorMod2)
##          if self.starPowerActive:
##            if self.theme == 0 or self.theme == 1: #GH3 starcolor
##              glColor3f(self.spColor[0],self.spColor[1],self.spColor[2])
##              #glColor3f(.3,.7,.9)
##            else: #Default starcolor (Rockband)
##              glColor3f(.8,.8,.8)
##
##          if not self.Hitanim: 
##            glEnable(GL_TEXTURE_2D)
##            self.hitglow2Drawing.texture.bind()    
##            glPushMatrix()
##            glTranslate(x, y + .25, .05)
##            glRotate(90, 1, 0, 0)
##            glScalef(.40 + .6 * ms * ff, 1.5 + .6 * ms * ff, 1 + .6 * ms * ff)
##            glBegin(GL_TRIANGLE_STRIP)
##            glTexCoord2f(0.0, 0.0)
##            glVertex3f(-flameSize * ff, 0, -flameSize * ff)
##            glTexCoord2f(1.0, 0.0)
##            glVertex3f( flameSize * ff, 0, -flameSize * ff)
##            glTexCoord2f(0.0, 1.0)
##            glVertex3f(-flameSize * ff, 0,  flameSize * ff)
##            glTexCoord2f(1.0, 1.0)
##            glVertex3f( flameSize * ff, 0,  flameSize * ff)
##            glEnd()
##            glPopMatrix()
##            glDisable(GL_TEXTURE_2D)
##          
##          glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
##
##          self.hit[n] = True



    if self.disableFlameSFX != True:
      flameLimit = 10.0
      flameLimitHalf = round(flameLimit/2.0)
      for time, event in track.getEvents(pos - self.currentPeriod * 2, pos + self.currentPeriod * self.beatsPerBoard):
        if isinstance(event, Tempo):
          continue
        
        if not isinstance(event, Note):
          continue
        
        if (event.played or event.hopod) and event.flameCount < flameLimit:
          ms = math.sin(self.time) * .25 + 1

          if event.number == 0:
            x  = (self.strings / 2 - 2) * w
          else:
            x  = (self.strings / 2 +.5 - event.number) * w
          #x  = (self.strings / 2 - event.number) * w

          xlightning = (self.strings / 2 - event.number)*2.2*w
          ff = 1 + 0.25       
          y = v + ff / 6

          if self.theme == 2:
            y -= 0.5
          
          flameSize = self.flameSizes[self.scoreMultiplier - 1][event.number]
          if self.theme == 0 or self.theme == 1: #THIS SETS UP GH3 COLOR, ELSE ROCKBAND(which is DEFAULT in Theme.py)
            flameColor = self.gh3flameColor
          else:
            flameColor = self.flameColors[self.scoreMultiplier - 1][event.number]
          if flameColor[0] == -2:
            flameColor = self.fretColors[event.number]
          
          ff += 1.5 #ff first time is 2.75 after this

          if self.Hitanim2 == True:
            self.HCount2 = self.HCount2 + 1
            self.HCountAni = False
            if self.HCount2 > 12:
              if event.length <= 130:
                self.HCount2 = 0
              else:
                self.HCountAni = True
            if event.flameCount < flameLimitHalf:

                  
                HIndex = (self.HCount2 * 13 - (self.HCount2 * 13) % 13) / 13
                if HIndex > 12 and self.HCountAni != True:
                  HIndex = 0
                  
                texX = (HIndex*(1/13.0), HIndex*(1/13.0)+(1/13.0))

                self.engine.draw3Dtex(self.hitflamesAnim, coord = (x, y + .665, 0), rot = (90, 1, 0, 0), scale = (1.6, 1.6, 4.9),
                                      vertex = (-flameSize * ff,-flameSize * ff,flameSize * ff,flameSize * ff),
                                      texcoord = (texX[0],0.0,texX[1],1.0), multiples = True, alpha = True, color = (1,1,1))

            else:
              flameColorMod0 = 0.1 * (flameLimit - event.flameCount)
              flameColorMod1 = 0.1 * (flameLimit - event.flameCount)
              flameColorMod2 = 0.1 * (flameLimit - event.flameCount)
              
              flamecol = (flameColor[0] * flameColorMod0, flameColor[1] * flameColorMod1, flameColor[2] * flameColorMod2)
              spcolmod = (.7,.7,.7)
              if self.starPowerActive:
                if self.theme == 0 or self.theme == 1: 
                  flamecol = (self.spColor[0]*spcolmod[0], self.spColor[1]*spcolmod[1], self.spColor[2]*spcolmod[2])
                  #flamecol = (.3,.6,.7)#GH3 starcolor
                else:
                  flamecol = (.4,.4,.4)#Default starcolor (Rockband)
              if self.theme != 2 and event.finalStar and self.spEnabled:
                wid, hei, = self.engine.view.geometry[2:4]
                self.engine.draw3Dtex(self.hitlightning, coord = (xlightning, y, 3.3), rot = (90, 1, 0, 0),
                                      scale = (.15 + .5 * ms * ff, event.flameCount / 3.0 + .6 * ms * ff, 2), vertex = (.4,-2,-.4,2),
                                      texcoord = (0.0,0.0,1.0,1.0), multiples = True, alpha = True, color = (1,1,1))
              else:
                self.engine.draw3Dtex(self.hitflames1Drawing, coord = (x, y + .35, 0), rot = (90, 1, 0, 0),
                                      scale = (.25 + .6 * ms * ff, event.flameCount / 3.0 + .6 * ms * ff, event.flameCount / 3.0 + .6 * ms * ff),
                                      vertex = (-flameSize * ff,-flameSize * ff,flameSize * ff,flameSize * ff), texcoord = (0.0,0.0,1.0,1.0),
                                      multiples = True, alpha = True, color = flamecol)

              flameColorMod0 = 0.1 * (flameLimit - event.flameCount)
              flameColorMod1 = 0.1 * (flameLimit - event.flameCount)
              flameColorMod2 = 0.1 * (flameLimit - event.flameCount)
              
              flamecol = (flameColor[0] * flameColorMod0, flameColor[1] * flameColorMod1, flameColor[2] * flameColorMod2)      
              spcolmod = (.8,.8,.8)
              if self.starPowerActive:
                if self.theme == 0 or self.theme == 1: #GH3 starcolor
                  flamecol = (self.spColor[0]*spcolmod[0], self.spColor[1]*spcolmod[1], self.spColor[2]*spcolmod[2])
                  #flamecol = (.3,.6,.8)
                else: #Default starcolor (Rockband)
                  flamecol = (.5,.5,.5)
              self.engine.draw3Dtex(self.hitflames1Drawing, coord = (x - .005, y + .40 + .005, 0), rot = (90, 1, 0, 0),
                                    scale = (.30 + .6 * ms * ff, (event.flameCount + 1)/ 2.5 + .6 * ms * ff, (event.flameCount + 1) / 2.5 + .6 * ms * ff),
                                    vertex = (-flameSize * ff,-flameSize * ff,flameSize * ff,flameSize * ff), texcoord = (0.0,0.0,1.0,1.0),
                                    multiples = True, alpha = True, color = flamecol)

              flameColorMod0 = 0.1 * (flameLimit - event.flameCount)
              flameColorMod1 = 0.1 * (flameLimit - event.flameCount)
              flameColorMod2 = 0.1 * (flameLimit - event.flameCount)
              
              flamecol = (flameColor[0] * flameColorMod0, flameColor[1] * flameColorMod1, flameColor[2] * flameColorMod2)
              spcolmod = (.9,.9,.9)
              if self.starPowerActive:
                if self.theme == 0 or self.theme == 1: #GH3 starcolor
                  flamecol = (self.spColor[0]*spcolmod[0], self.spColor[1]*spcolmod[1], self.spColor[2]*spcolmod[2])
                  #flamecol = (.3,.7,.8)
                else: #Default starcolor (Rockband)
                  flamecol = (.6,.6,.6)
              self.engine.draw3Dtex(self.hitflames1Drawing, coord = (x + .005, y + .35 + .005, 0), rot = (90, 1, 0, 0),
                                    scale = (.35 + .6 * ms * ff, (event.flameCount + 1) / 2.0 + .6 * ms * ff, (event.flameCount + 1) / 2.0 + .6 * ms * ff),
                                    vertex = (-flameSize * ff,-flameSize * ff,flameSize * ff,flameSize * ff), texcoord = (0.0,0.0,1.0,1.0),
                                    multiples = True, alpha = True, color = flamecol)


              flameColorMod0 = 0.1 * (flameLimit - event.flameCount)
              flameColorMod1 = 0.1 * (flameLimit - event.flameCount)
              flameColorMod2 = 0.1 * (flameLimit - event.flameCount)
              
              flamecol = (flameColor[0] * flameColorMod0, flameColor[1] * flameColorMod1, flameColor[2] * flameColorMod2)
              spcolmod = (1,1,1)
              if self.starPowerActive:
                if self.theme == 0 or self.theme == 1: #GH3 starcolor
                  flamecol = (self.spColor[0]*spcolmod[0], self.spColor[1]*spcolmod[1], self.spColor[2]*spcolmod[2])
                  #flamecol = (.3,.7,.9)
                else: #Default starcolor (Rockband)
                  flamecol = (.7,.7,.7)
              self.engine.draw3Dtex(self.hitflames1Drawing, coord = (x+.005, y +.35 +.005, 0), rot = (90, 1, 0, 0),
                                    scale = (.40 + .6 * ms * ff, (event.flameCount + 1) / 1.7 + .6 * ms * ff, (event.flameCount + 1) / 1.7 + .6 * ms * ff),
                                    vertex = (-flameSize * ff,-flameSize * ff,flameSize * ff,flameSize * ff), texcoord = (0.0,0.0,1.0,1.0),
                                    multiples = True, alpha = True, color = flamecol)            
          else:
            self.HCount2 = 13
            self.HCountAni = True
            if event.flameCount < flameLimitHalf:
              flamecol = (flameColor[0], flameColor[1], flameColor[2])
              spcolmod = (.3,.3,.3)
              if self.starPowerActive:
                if self.theme == 0 or self.theme == 1: #GH3 starcolor
                  flamecol = (self.spColor[0]*spcolmod[0], self.spColor[1]*spcolmod[1], self.spColor[2]*spcolmod[2])
                  #flamecol = (.0,.2,.4)
                else: #Default starcolor (Rockband)
                  flamecol = (.1,.1,.1)
              self.engine.draw3Dtex(self.hitflames2Drawing, coord = (x, y + .20, 0), rot = (90, 1, 0, 0),
                                      scale = (.25 + .6 * ms * ff, event.flameCount/6.0 + .6 * ms * ff, event.flameCount / 6.0 + .6 * ms * ff),
                                      vertex = (-flameSize * ff,-flameSize * ff,flameSize * ff,flameSize * ff), texcoord = (0.0,0.0,1.0,1.0),
                                      multiples = True, alpha = True, color = flamecol)

              flamecol = (flameColor[0], flameColor[1], flameColor[2])
              spcolmod = (.4,.4,.4)
              if self.starPowerActive:
                if self.theme == 0 or self.theme == 1: #GH3 starcolor
                  flamecol = (self.spColor[0]*spcolmod[0], self.spColor[1]*spcolmod[1], self.spColor[2]*spcolmod[2])
                  #flamecol = (.1,.3,.5)
                else: #Default starcolor (Rockband)
                  flamecol = (.1,.1,.1)
              self.engine.draw3Dtex(self.hitflames2Drawing, coord = (x-.005, y + .255, 0), rot = (90, 1, 0, 0),
                                    scale = (.30 + .6 * ms * ff, event.flameCount/5.5 + .6 * ms * ff, event.flameCount / 5.5 + .6 * ms * ff),
                                    vertex = (-flameSize * ff,-flameSize * ff,flameSize * ff,flameSize * ff), texcoord = (0.0,0.0,1.0,1.0),
                                    multiples = True, alpha = True, color = flamecol)

              flamecol = (flameColor[0], flameColor[1], flameColor[2])
              spcolmod = (.5,.5,.5)
              if self.starPowerActive:
                if self.theme == 0 or self.theme == 1: #GH3 starcolor
                  flamecol = (self.spColor[0]*spcolmod[0], self.spColor[1]*spcolmod[1], self.spColor[2]*spcolmod[2])
                  #flamecol = (.2,.4,.7)
                else: #Default starcolor (Rockband)
                  flamecol = (.2,.2,.2)
              self.engine.draw3Dtex(self.hitflames2Drawing, coord = (x+.005, y+.255, 0), rot = (90, 1, 0, 0),
                                    scale = (.35 + .6 * ms * ff, event.flameCount/5.0 + .6 * ms * ff, event.flameCount / 5.0 + .6 * ms * ff),
                                    vertex = (-flameSize * ff,-flameSize * ff,flameSize * ff,flameSize * ff), texcoord = (0.0,0.0,1.0,1.0),
                                    multiples = True, alpha = True, color = flamecol)

              flamecol = (flameColor[0], flameColor[1], flameColor[2])
              spcolmod = (.6,.6,.6)
              if self.starPowerActive:
                if self.theme == 0 or self.theme == 1: #GH3 starcolor
                  flamecol = (self.spColor[0]*spcolmod[0], self.spColor[1]*spcolmod[1], self.spColor[2]*spcolmod[2])
                  #flamecol = (.2,.5,.7)
                else: #Default starcolor (Rockband)
                  flamecol = (.3,.3,.3)

              self.engine.draw3Dtex(self.hitflames2Drawing, coord = (x, y+.255, 0), rot = (90, 1, 0, 0),
                                    scale = (.40 + .6 * ms * ff, event.flameCount/4.7 + .6 * ms * ff, event.flameCount / 4.7 + .6 * ms * ff),
                                    vertex = (-flameSize * ff,-flameSize * ff,flameSize * ff,flameSize * ff), texcoord = (0.0,0.0,1.0,1.0),
                                    multiples = True, alpha = True, color = flamecol)
            else:
              flameColorMod0 = 0.1 * (flameLimit - event.flameCount)
              flameColorMod1 = 0.1 * (flameLimit - event.flameCount)
              flameColorMod2 = 0.1 * (flameLimit - event.flameCount)
              
              flamecol = (flameColor[0] * flameColorMod0, flameColor[1] * flameColorMod1, flameColor[2] * flameColorMod2)
              spcolmod = (.7,.7,.7)
              if self.starPowerActive:
                if self.theme == 0 or self.theme == 1: 
                  flamecol = (self.spColor[0]*spcolmod[0], self.spColor[1]*spcolmod[1], self.spColor[2]*spcolmod[2])
                  #flamecol = (.3,.6,.7)#GH3 starcolor
                else:
                  flamecol = (.4,.4,.4)#Default starcolor (Rockband)
              if self.theme != 2 and event.finalStar and self.spEnabled:
                wid, hei, = self.engine.view.geometry[2:4]
                self.engine.draw3Dtex(self.hitlightning, coord = (xlightning, y, 3.3), rot = (90, 1, 0, 0),
                                      scale = (.15 + .5 * ms * ff, event.flameCount / 3.0 + .6 * ms * ff, 2), vertex = (.4,-2,-.4,2),
                                      texcoord = (0.0,0.0,1.0,1.0), multiples = True, alpha = True, color = (1,1,1))
              else:
                self.engine.draw3Dtex(self.hitflames1Drawing, coord = (x, y + .35, 0), rot = (90, 1, 0, 0),
                                      scale = (.25 + .6 * ms * ff, event.flameCount / 3.0 + .6 * ms * ff, event.flameCount / 3.0 + .6 * ms * ff),
                                      vertex = (-flameSize * ff,-flameSize * ff,flameSize * ff,flameSize * ff), texcoord = (0.0,0.0,1.0,1.0),
                                      multiples = True, alpha = True, color = flamecol)

              flameColorMod0 = 0.1 * (flameLimit - event.flameCount)
              flameColorMod1 = 0.1 * (flameLimit - event.flameCount)
              flameColorMod2 = 0.1 * (flameLimit - event.flameCount)
              
              flamecol = (flameColor[0] * flameColorMod0, flameColor[1] * flameColorMod1, flameColor[2] * flameColorMod2)      
              spcolmod = (.8,.8,.8)
              if self.starPowerActive:
                if self.theme == 0 or self.theme == 1: #GH3 starcolor
                  flamecol = (self.spColor[0]*spcolmod[0], self.spColor[1]*spcolmod[1], self.spColor[2]*spcolmod[2])
                  #flamecol = (.3,.6,.8)
                else: #Default starcolor (Rockband)
                  flamecol = (.5,.5,.5)
              self.engine.draw3Dtex(self.hitflames1Drawing, coord = (x - .005, y + .40 + .005, 0), rot = (90, 1, 0, 0),
                                    scale = (.30 + .6 * ms * ff, (event.flameCount + 1)/ 2.5 + .6 * ms * ff, (event.flameCount + 1) / 2.5 + .6 * ms * ff),
                                    vertex = (-flameSize * ff,-flameSize * ff,flameSize * ff,flameSize * ff), texcoord = (0.0,0.0,1.0,1.0),
                                    multiples = True, alpha = True, color = flamecol)

              flameColorMod0 = 0.1 * (flameLimit - event.flameCount)
              flameColorMod1 = 0.1 * (flameLimit - event.flameCount)
              flameColorMod2 = 0.1 * (flameLimit - event.flameCount)
              
              flamecol = (flameColor[0] * flameColorMod0, flameColor[1] * flameColorMod1, flameColor[2] * flameColorMod2)
              spcolmod = (.9,.9,.9)
              if self.starPowerActive:
                if self.theme == 0 or self.theme == 1: #GH3 starcolor
                  flamecol = (self.spColor[0]*spcolmod[0], self.spColor[1]*spcolmod[1], self.spColor[2]*spcolmod[2])
                  #flamecol = (.3,.7,.8)
                else: #Default starcolor (Rockband)
                  flamecol = (.6,.6,.6)
              self.engine.draw3Dtex(self.hitflames1Drawing, coord = (x + .005, y + .35 + .005, 0), rot = (90, 1, 0, 0),
                                    scale = (.35 + .6 * ms * ff, (event.flameCount + 1) / 2.0 + .6 * ms * ff, (event.flameCount + 1) / 2.0 + .6 * ms * ff),
                                    vertex = (-flameSize * ff,-flameSize * ff,flameSize * ff,flameSize * ff), texcoord = (0.0,0.0,1.0,1.0),
                                    multiples = True, alpha = True, color = flamecol)


              flameColorMod0 = 0.1 * (flameLimit - event.flameCount)
              flameColorMod1 = 0.1 * (flameLimit - event.flameCount)
              flameColorMod2 = 0.1 * (flameLimit - event.flameCount)
              
              flamecol = (flameColor[0] * flameColorMod0, flameColor[1] * flameColorMod1, flameColor[2] * flameColorMod2)
              spcolmod = (1,1,1)
              if self.starPowerActive:
                if self.theme == 0 or self.theme == 1: #GH3 starcolor
                  flamecol = (self.spColor[0]*spcolmod[0], self.spColor[1]*spcolmod[1], self.spColor[2]*spcolmod[2])
                  #flamecol = (.3,.7,.9)
                else: #Default starcolor (Rockband)
                  flamecol = (.7,.7,.7)
              self.engine.draw3Dtex(self.hitflames1Drawing, coord = (x+.005, y +.35 +.005, 0), rot = (90, 1, 0, 0),
                                    scale = (.40 + .6 * ms * ff, (event.flameCount + 1) / 1.7 + .6 * ms * ff, (event.flameCount + 1) / 1.7 + .6 * ms * ff),
                                    vertex = (-flameSize * ff,-flameSize * ff,flameSize * ff,flameSize * ff), texcoord = (0.0,0.0,1.0,1.0),
                                    multiples = True, alpha = True, color = flamecol)
          event.flameCount += 1




  def renderFreestyleFlames(self, visibility, controls):
    if self.flameColors[0][0][0] == -1:
      return

    beatsPerUnit = self.beatsPerBoard / self.boardLength
    w = self.boardWidth / self.strings
    #track = song.track[self.player]

    size = (.22, .22)
    v = 1.0 - visibility

##    if self.disableFlameSFX != True:
##      for n in range(self.strings):
##        f = self.fretWeight[n]
##        c = self.fretColors[n+1]    #MFH shifted by 1 for most drum colors
##        if f and (controls.getState(self.keys[0]) or controls.getState(self.keys[5])):
##          f += 0.25     
##        y = v + f / 6
##        x = (self.strings / 2 -.5 - n) * w
##        f = self.fretActivity[n]
##
##        if f:
##          ms = math.sin(self.time) * .25 + 1
##          ff = f
##          ff += 1.2
##          
##          glBlendFunc(GL_ONE, GL_ONE)
##
##          flameSize = self.flameSizes[self.scoreMultiplier - 1][n]
##          if self.theme == 0 or self.theme == 1: #THIS SETS UP GH3 COLOR, ELSE ROCKBAND(which is DEFAULT in Theme.py)
##            flameColor = self.gh3flameColor
##          else:
##            flameColor = self.flameColors[self.scoreMultiplier - 1][n]
##          #Below was an if that set the "flame"-color to the same as the fret color if there was no specific flamecolor defined.
##
##          flameColorMod0 = 1.1973333333333333333333333333333
##          flameColorMod1 = 1.9710526315789473684210526315789
##          flameColorMod2 = 10.592592592592592592592592592593
##          
##          glColor3f(flameColor[0] * flameColorMod0, flameColor[1] * flameColorMod1, flameColor[2] * flameColorMod2)
##          if self.starPowerActive:
##            if self.theme == 0 or self.theme == 1: #GH3 starcolor
##              glColor3f(self.spColor[0],self.spColor[1],self.spColor[2])
##              #glColor3f(.3,.7,.9)
##            else: #Default starcolor (Rockband)
##              glColor3f(.9,.9,.9)
##
##          if not self.Hitanim:   
##            glEnable(GL_TEXTURE_2D)
##            self.hitglowDrawing.texture.bind()    
##            glPushMatrix()
##            glTranslate(x, y + .125, 0)
##            glRotate(90, 1, 0, 0)
##            glScalef(0.5 + .6 * ms * ff, 1.5 + .6 * ms * ff, 1 + .6 * ms * ff)
##            glBegin(GL_TRIANGLE_STRIP)
##            glTexCoord2f(0.0, 0.0)
##            glVertex3f(-flameSize * ff, 0, -flameSize * ff)
##            glTexCoord2f(1.0, 0.0)
##            glVertex3f( flameSize * ff, 0, -flameSize * ff)
##            glTexCoord2f(0.0, 1.0)
##            glVertex3f(-flameSize * ff, 0,  flameSize * ff)
##            glTexCoord2f(1.0, 1.0)
##            glVertex3f( flameSize * ff, 0,  flameSize * ff)
##            glEnd()
##            glPopMatrix()
##            glDisable(GL_TEXTURE_2D)
##            #Alarian: Animated hitflames
##          else:
##            self.HCount = self.HCount + 1
##            if self.HCount > self.Animspeed-1:
##              self.HCount = 0
##            HIndex = (self.HCount * 16 - (self.HCount * 16) % self.Animspeed) / self.Animspeed
##            if HIndex > 15:
##              HIndex = 0
##            texX = (HIndex*(1/16.0), HIndex*(1/16.0)+(1/16.0))
##
##            glColor3f(1,1,1)
##            glEnable(GL_TEXTURE_2D)
##            self.hitglowAnim.texture.bind()    
##            glPushMatrix()
##            glTranslate(x, y + .225, 0)
##            glRotate(90, 1, 0, 0)
##            
##            #glScalef(1.3, 1, 2)
##            #glScalef(1.7, 1, 2.6)
##            glScalef(2, 1, 2.9)   #worldrave correct flame size
##
##            
##            glBegin(GL_TRIANGLE_STRIP)
##            glTexCoord2f(texX[0], 0.0)#upper left corner of frame square in .png
##            glVertex3f(-flameSize * ff, 0, -flameSize * ff)#"upper left" corner of surface that texture is rendered on
##            glTexCoord2f(texX[1], 0.0)#upper right
##            glVertex3f( flameSize * ff, 0, -flameSize * ff)
##            glTexCoord2f(texX[0], 1.0)#lower left
##            glVertex3f(-flameSize * ff, 0,  flameSize * ff)
##            glTexCoord2f(texX[1], 1.0)#lower right
##            glVertex3f( flameSize * ff, 0,  flameSize * ff)
##            glEnd()
##            glPopMatrix()
##            glDisable(GL_TEXTURE_2D)
##
##          ff += .3
##
##          #flameSize = self.flameSizes[self.scoreMultiplier - 1][n]
##          #flameColor = self.flameColors[self.scoreMultiplier - 1][n]
##
##          flameColorMod0 = 1.1973333333333333333333333333333
##          flameColorMod1 = 1.7842105263157894736842105263158
##          flameColorMod2 = 12.222222222222222222222222222222
##          
##          glColor3f(flameColor[0] * flameColorMod0, flameColor[1] * flameColorMod1, flameColor[2] * flameColorMod2)
##          if self.starPowerActive:
##            if self.theme == 0 or self.theme == 1: #GH3 starcolor
##              glColor3f(self.spColor[0],self.spColor[1],self.spColor[2])
##              #glColor3f(.3,.7,.9)
##            else: #Default starcolor (Rockband)
##              glColor3f(.8,.8,.8)
##
##          if not self.Hitanim: 
##            glEnable(GL_TEXTURE_2D)
##            self.hitglow2Drawing.texture.bind()    
##            glPushMatrix()
##            glTranslate(x, y + .25, .05)
##            glRotate(90, 1, 0, 0)
##            glScalef(.40 + .6 * ms * ff, 1.5 + .6 * ms * ff, 1 + .6 * ms * ff)
##            glBegin(GL_TRIANGLE_STRIP)
##            glTexCoord2f(0.0, 0.0)
##            glVertex3f(-flameSize * ff, 0, -flameSize * ff)
##            glTexCoord2f(1.0, 0.0)
##            glVertex3f( flameSize * ff, 0, -flameSize * ff)
##            glTexCoord2f(0.0, 1.0)
##            glVertex3f(-flameSize * ff, 0,  flameSize * ff)
##            glTexCoord2f(1.0, 1.0)
##            glVertex3f( flameSize * ff, 0,  flameSize * ff)
##            glEnd()
##            glPopMatrix()
##            glDisable(GL_TEXTURE_2D)
##          
##          glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
##
##          #self.hit[n] = True



    if self.disableFlameSFX != True:
      flameLimit = 10.0
      flameLimitHalf = round(flameLimit/2.0)
      for fretNum in range(self.strings+1):   #need to add 1 to string count to check this correctly (bass drum doesnt count as a string)
        #MFH - must include secondary drum keys here
        #if controls.getState(self.keys[fretNum]):
        if controls.getState(self.keys[fretNum]) or controls.getState(self.keys[fretNum+5]):

          if self.freestyleHitFlameCounts[fretNum] < flameLimit:
            ms = math.sin(self.time) * .25 + 1
  
            if fretNum == 0:
              x  = (self.strings / 2 - 2) * w
            else:
              x  = (self.strings / 2 +.5 - fretNum) * w
            #x  = (self.strings / 2 - fretNum) * w
  
            xlightning = (self.strings / 2 - fretNum)*2.2*w
            ff = 1 + 0.25       
            y = v + ff / 6
            glBlendFunc(GL_ONE, GL_ONE)
  
            if self.theme == 2:
              y -= 0.5
            
            #flameSize = self.flameSizes[self.scoreMultiplier - 1][fretNum]
            flameSize = self.flameSizes[self.cappedScoreMult - 1][fretNum]
            if self.theme == 0 or self.theme == 1: #THIS SETS UP GH3 COLOR, ELSE ROCKBAND(which is DEFAULT in Theme.py)
              flameColor = self.gh3flameColor
            else: #MFH - fixing crash!
              #try:
              #  flameColor = self.flameColors[self.scoreMultiplier - 1][fretNum]
              #except IndexError:
              flameColor = self.fretColors[fretNum]
            if flameColor[0] == -2:
              flameColor = self.fretColors[fretNum]
            
            ff += 1.5 #ff first time is 2.75 after this
  
            if self.freestyleHitFlameCounts[fretNum] < flameLimitHalf:
              flamecol = (flameColor[0], flameColor[1], flameColor[2])
              if self.starPowerActive:
                if self.theme == 0 or self.theme == 1: #GH3 starcolor
                  flamecol = self.spColor #(.3,.7,.9)
                else: #Default starcolor (Rockband)
                  flamecol = (.1,.1,.1)
              self.engine.draw3Dtex(self.hitflames2Drawing, coord = (x, y + .20, 0), rot = (90, 1, 0, 0),
                                    scale = (.25 + .6 * ms * ff, self.freestyleHitFlameCounts[fretNum]/6.0 + .6 * ms * ff, self.freestyleHitFlameCounts[fretNum] / 6.0 + .6 * ms * ff),
                                    vertex = (-flameSize * ff,-flameSize * ff,flameSize * ff,flameSize * ff),
                                    texcoord = (0.0,0.0,1.0,1.0), multiples = True, alpha = True, color = flamecol)
  
              flamecol = (flameColor[0], flameColor[1], flameColor[2])
              if self.starPowerActive:
                if self.theme == 0 or self.theme == 1: #GH3 starcolor
                  flamecol = self.spColor #(.3,.7,.9)
                else: #Default starcolor (Rockband)
                  flamecol = (.1,.1,.1)
              self.engine.draw3Dtex(self.hitflames2Drawing, coord = (x - .005, y + .25 + .005, 0), rot = (90, 1, 0, 0),
                                    scale = (.30 + .6 * ms * ff, (self.freestyleHitFlameCounts[fretNum] + 1) / 5.5 + .6 * ms * ff, (self.freestyleHitFlameCounts[fretNum] + 1) / 5.5 + .6 * ms * ff),
                                    vertex = (-flameSize * ff,-flameSize * ff,flameSize * ff,flameSize * ff),
                                    texcoord = (0.0,0.0,1.0,1.0), multiples = True, alpha = True, color = flamecol)
  
              flamecol = (flameColor[0], flameColor[1], flameColor[2])
              if self.starPowerActive:
                if self.theme == 0 or self.theme == 1: #GH3 starcolor
                  flamecol = self.spColor #(.3,.7,.9)
                else: #Default starcolor (Rockband)
                  #flamecol = glColor3f(.2,.2,.2)
                  flamecol = (.2,.2,.2)
              self.engine.draw3Dtex(self.hitflames2Drawing, coord = (x+.005, y +.25 +.005, 0), rot = (90, 1, 0, 0),
                                    scale = (.35 + .6 * ms * ff, (self.freestyleHitFlameCounts[fretNum] + 1) / 5.0 + .6 * ms * ff, (self.freestyleHitFlameCounts[fretNum] + 1) / 5.0 + .6 * ms * ff),
                                    vertex = (-flameSize * ff,-flameSize * ff,flameSize * ff,flameSize * ff),
                                    texcoord = (0.0,0.0,1.0,1.0), multiples = True, alpha = True, color = flamecol)
  
              flamecol = (flameColor[0], flameColor[1], flameColor[2])
              if self.starPowerActive:
                if self.theme == 0 or self.theme == 1: #GH3 starcolor
                  flamecol = self.spColor #(.3,.7,.9)
                else: #Default starcolor (Rockband)
                  flamecol = (.3,.3,.3)
              self.engine.draw3Dtex(self.hitflames2Drawing, coord = (x, y +.25 +.005, 0), rot = (90, 1, 0, 0),
                                    scale = (.40 + .6 * ms * ff, (self.freestyleHitFlameCounts[fretNum] + 1)/ 4.7 + .6 * ms * ff, (self.freestyleHitFlameCounts[fretNum] + 1) / 4.7 + .6 * ms * ff),
                                    vertex = (-flameSize * ff,-flameSize * ff,flameSize * ff,flameSize * ff),
                                    texcoord = (0.0,0.0,1.0,1.0), multiples = True, alpha = True, color = flamecol)
            else:
              flameColorMod0 = 0.1 * (flameLimit - self.freestyleHitFlameCounts[fretNum])
              flameColorMod1 = 0.1 * (flameLimit - self.freestyleHitFlameCounts[fretNum])
              flameColorMod2 = 0.1 * (flameLimit - self.freestyleHitFlameCounts[fretNum])
              
              flamecol = (flameColor[0] * flameColorMod0, flameColor[1] * flameColorMod1, flameColor[2] * flameColorMod2)

              #MFH - hit lightning logic is not needed for freestyle flames...

              self.engine.draw3Dtex(self.hitflames1Drawing, coord = (x, y + .35, 0), rot = (90, 1, 0, 0),
                                    scale = (.25 + .6 * ms * ff, self.freestyleHitFlameCounts[fretNum] / 3.0 + .6 * ms * ff, self.freestyleHitFlameCounts[fretNum] / 3.0 + .6 * ms * ff),
                                    vertex = (-flameSize * ff,-flameSize * ff,flameSize * ff,flameSize * ff),
                                    texcoord = (0.0,0.0,1.0,1.0), multiples = True, alpha = True, color = flamecol)

  
              flameColorMod0 = 0.1 * (flameLimit - self.freestyleHitFlameCounts[fretNum])
              flameColorMod1 = 0.1 * (flameLimit - self.freestyleHitFlameCounts[fretNum])
              flameColorMod2 = 0.1 * (flameLimit - self.freestyleHitFlameCounts[fretNum])
              
              flamecol = (flameColor[0] * flameColorMod0, flameColor[1] * flameColorMod1, flameColor[2] * flameColorMod2)      
              if self.starPowerActive:
                if self.theme == 0 or self.theme == 1: #GH3 starcolor
                  flamecol = self.spColor #(.3,.7,.9)
                else: #Default starcolor (Rockband)
                  flamecol = (.5,.5,.5)
              self.engine.draw3Dtex(self.hitflames1Drawing, coord = (x - .005, y + .40 + .005, 0), rot = (90, 1, 0, 0),
                                    scale = (.30 + .6 * ms * ff, (self.freestyleHitFlameCounts[fretNum] + 1)/ 2.5 + .6 * ms * ff, (self.freestyleHitFlameCounts[fretNum] + 1) / 2.5 + .6 * ms * ff),
                                    vertex = (-flameSize * ff,-flameSize * ff,flameSize * ff,flameSize * ff),
                                    texcoord = (0.0,0.0,1.0,1.0), multiples = True, alpha = True, color = flamecol)
  
              flameColorMod0 = 0.1 * (flameLimit - self.freestyleHitFlameCounts[fretNum])
              flameColorMod1 = 0.1 * (flameLimit - self.freestyleHitFlameCounts[fretNum])
              flameColorMod2 = 0.1 * (flameLimit - self.freestyleHitFlameCounts[fretNum])
              
              flamecol = (flameColor[0] * flameColorMod0, flameColor[1] * flameColorMod1, flameColor[2] * flameColorMod2)
              if self.starPowerActive:
                if self.theme == 0 or self.theme == 1: #GH3 starcolor
                  flamecol = self.spColor #(.3,.7,.9)
                else: #Default starcolor (Rockband)
                  flamecol = (.6,.6,.6)
              self.engine.draw3Dtex(self.hitflames1Drawing, coord = (x + .005, y + .35 + .005, 0), rot = (90, 1, 0, 0),
                                    scale = (.35 + .6 * ms * ff, (self.freestyleHitFlameCounts[fretNum] + 1) / 2.0 + .6 * ms * ff, (self.freestyleHitFlameCounts[fretNum] + 1) / 2.0 + .6 * ms * ff),
                                    vertex = (-flameSize * ff,-flameSize * ff,flameSize * ff,flameSize * ff),
                                    texcoord = (0.0,0.0,1.0,1.0), multiples = True, alpha = True, color = flamecol)              
  
              flameColorMod0 = 0.1 * (flameLimit - self.freestyleHitFlameCounts[fretNum])
              flameColorMod1 = 0.1 * (flameLimit - self.freestyleHitFlameCounts[fretNum])
              flameColorMod2 = 0.1 * (flameLimit - self.freestyleHitFlameCounts[fretNum])
              
              flamecol = (flameColor[0] * flameColorMod0, flameColor[1] * flameColorMod1, flameColor[2] * flameColorMod2)
              if self.starPowerActive:
                if self.theme == 0 or self.theme == 1: #GH3 starcolor
                  flamecol = self.spColor #(.3,.7,.9)
                else: #Default starcolor (Rockband)
                  flamecol = (.7,.7,.7)
              self.engine.draw3Dtex(self.hitflames1Drawing, coord = (x + .005, y + .35 + .005, 0), rot = (90, 1, 0, 0),
                                    scale = (.40 + .6 * ms * ff, (self.freestyleHitFlameCounts[fretNum] + 1) / 1.7 + .6 * ms * ff, (self.freestyleHitFlameCounts[fretNum] + 1) / 1.7 + .6 * ms * ff),
                                    vertex = (-flameSize * ff,-flameSize * ff,flameSize * ff,flameSize * ff),
                                    texcoord = (0.0,0.0,1.0,1.0), multiples = True, alpha = True, color = flamecol)             

            self.freestyleHitFlameCounts[fretNum] += 1
        
          else:   #MFH - flame count is done - reset it!
            self.freestyleHitFlameCounts[fretNum] = 0    #MFH



  def render(self, visibility, song, pos, controls, killswitch):

    if not self.starNotesSet == True:
      self.totalNotes = 0
      for time, event in song.track[self.player].getAllEvents():
        if not isinstance(event, Note):
          continue
        self.totalNotes += 1
      stars = []
      maxStars = []
      maxPhrase = self.totalNotes/120
      for q in range(0,maxPhrase):
        for n in range(0,10):
          stars.append(self.totalNotes/maxPhrase*(q)+n+maxPhrase/4)
        maxStars.append(self.totalNotes/maxPhrase*(q)+10+maxPhrase/4)
      i = 0
      for time, event in song.track[self.player].getAllEvents():
        if not isinstance(event, Note):
          continue
        for a in stars:
          if i == a:
            self.starNotes.append(time)
            event.star = True
        for a in maxStars:
          if i == a:
            self.maxStars.append(time)
            event.finalStar = True
        i += 1
      for time, event in song.track[self.player].getAllEvents():
        if not isinstance(event, Note):
          continue
        for q in self.starNotes:
          if time == q:
            event.star = True
        for q in self.maxStars:
          if time == q and not event.finalStar:
            event.star = True
      self.starNotesSet = True
    if not (self.coOpFailed and not self.coOpRestart):
      glEnable(GL_BLEND)
      glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
      glEnable(GL_COLOR_MATERIAL)
      if self.leftyMode:
        glScalef(-1, 1, 1)

      if self.ocount <= 1:
        self.ocount = self.ocount + .1
      else:
        self.ocount = 1

      if self.isFailing == True:
        if self.failcount <= 1 and self.failcount2 == False:
          self.failcount += .05
        elif self.failcount >= 1 and self.failcount2 == False:
          self.failcount = 1
          self.failcount2 = True
        
        if self.failcount >= 0 and self.failcount2 == True:
          self.failcount -= .05
        elif self.failcount <= 0 and self.failcount2 == True:
          self.failcount = 0
          self.failcount2 = False

      if self.isFailing == False and self.failcount > 0:
        self.failcount -= .05
        self.failcount2 = False

      if self.starPowerActive:

        if self.spcount < 1.2:
          self.spcount += .05
          self.spcount2 = 1
        elif self.spcount >=1.2:
          self.spcount = 1.2
          self.spcount2 = 0
      else:
        if self.spcount > 0:
          self.spcount -= .05
          self.spcount2 = 2
        elif self.spcount <=0:
          self.spcount = 0
          self.spcount2 = 0

      self.renderNeck(visibility, song, pos)
      self.renderIncomingNecks(visibility, song, pos) #MFH
      if self.theme == 0 or self.theme == 1 or self.theme == 2:
        self.drawTrack(self.ocount, song, pos)
        self.drawBPM(visibility, song, pos)
        self.drawSideBars(visibility, song, pos)
      else:
        self.renderTracks(visibility)
        self.renderBars(visibility, song, pos)
        
      if self.freestyleActive or self.drumFillsActive:
        self.renderOpenNotes(visibility, song, pos)
        self.renderNotes(visibility, song, pos)
        self.renderFreestyleLanes(visibility, song, pos, controls) #MFH - render the lanes on top of the notes.
        self.renderFrets(visibility, song, controls)
        
        if self.hitFlamesPresent: #MFH - only when present!
          self.renderFreestyleFlames(visibility, controls)    #MFH - freestyle hit flames
        
      else:
      
        self.renderFreestyleLanes(visibility, song, pos, controls)

    #if self.fretsUnderNotes:    #MFH
        if self.fretsUnderNotes and self.twoDnote != False:    #MFH
          self.renderFrets(visibility, song, controls)
          self.renderOpenNotes(visibility, song, pos)
          self.renderNotes(visibility, song, pos)
        else:
          self.renderOpenNotes(visibility, song, pos)
          self.renderNotes(visibility, song, pos)
          self.renderFrets(visibility, song, controls)

        if self.hitFlamesPresent: #MFH - only when present!
          self.renderFlames(visibility, song, pos, controls)    #MFH - only when freestyle inactive!
    
      if self.leftyMode:
        glScalef(-1, 1, 1)

  def getMissedNotes(self, song, pos, catchup = False):
    if not song:
      return
    if not song.readyToGo:
      return

    m1      = self.lateMargin
    m2      = self.lateMargin * 2
      
    track   = song.track[self.player]
    notes   = [(time, event) for time, event in track.getEvents(pos - m1, pos - m2) if isinstance(event, Note)]
    notes   = [(time, event) for time, event in notes if (time >= (pos - m2)) and (time <= (pos - m1))]
    notes   = [(time, event) for time, event in notes if not event.played and not event.hopod and not event.skipped]

    if catchup == True:
      for time, event in notes:
        event.skipped = True

    return sorted(notes, key=lambda x: x[1].number)        


  def getMissedNotesMFH(self, song, pos, catchup = False):
    if not song:
      return
    if not song.readyToGo:
      return

    m1      = self.lateMargin
    m2      = self.lateMargin * 2

      
    track   = song.track[self.player]
    notes   = [(time, event) for time, event in track.getEvents(pos - m2, pos - m1) if isinstance(event, Note)]   #was out of order
    
    #MFH - this additional filtration step removes sustains whose Note On event time is now outside the hitwindow.
    notes   = [(time, event) for time, event in notes if (time >= (pos - m2)) and (time <= (pos - m1))] 
    
    notes   = [(time, event) for time, event in notes if not event.played and not event.hopod and not event.skipped]

    if catchup == True:
      for time, event in notes:
        event.skipped = True

    return sorted(notes, key=lambda x: x[0])    #MFH - what the hell, this should be sorted by TIME not note number....

  def getRequiredNotes(self, song, pos):
    return self.getRequiredNotesMFH(song, pos)
#-    track   = song.track[self.player]
#-    notes = [(time, event) for time, event in track.getEvents(pos - self.lateMargin, pos + self.earlyMargin) if isinstance(event, Note)]
#-    notes = [(time, event) for time, event in notes if not event.played]
#-    notes = [(time, event) for time, event in notes if (time >= (pos - self.lateMargin)) and (time <= (pos + self.earlyMargin))]
#-    if notes:
#-      t     = min([time for time, event in notes])
#-      notes = [(time, event) for time, event in notes if time - t < 1e-3]
#-    return sorted(notes, key=lambda x: x[1].number)

  def getRequiredNotes2(self, song, pos, hopo = False):
    return self.getRequiredNotesMFH(song, pos)

#-    track   = song.track[self.player]
#-    notes = [(time, event) for time, event in track.getEvents(pos - self.lateMargin, pos + self.earlyMargin) if isinstance(event, Note)]
#-    notes = [(time, event) for time, event in notes if not (event.hopod or event.played)]
#-    notes = [(time, event) for time, event in notes if (time >= (pos - self.lateMargin)) and (time <= (pos + self.earlyMargin))]
#-    if notes:
#-      t     = min([time for time, event in notes])
#-      notes = [(time, event) for time, event in notes if time - t < 1e-3]
#-      
#-    return sorted(notes, key=lambda x: x[1].number)
    


  def getRequiredNotes3(self, song, pos, hopo = False):
    return self.getRequiredNotesMFH(song, pos)

#-    track   = song.track[self.player]
#-    notes = [(time, event) for time, event in track.getEvents(pos - self.lateMargin, pos + self.earlyMargin) if isinstance(event, Note)]
#-    notes = [(time, event) for time, event in notes if not (event.hopod or event.played or event.skipped)]
#-    notes = [(time, event) for time, event in notes if (time >= (pos - self.lateMargin)) and (time <= (pos + self.earlyMargin))]
#-
#-    return sorted(notes, key=lambda x: x[1].number)

  #MFH - corrected and optimized:
  def getRequiredNotesMFH(self, song, pos):
    track   = song.track[self.player]
    notes = [(time, event) for time, event in track.getEvents(pos - self.lateMargin, pos + self.earlyMargin) if isinstance(event, Note)]
    notes = [(time, event) for time, event in notes if not (event.hopod or event.played or event.skipped)]

    #MFH - this additional filtration step removes sustains whose Note On event time is now outside the hitwindow.
    notes = [(time, event) for time, event in notes if (time >= (pos - self.lateMargin)) and (time <= (pos + self.earlyMargin))]

    return sorted(notes, key=lambda x: x[0])    #MFH - what the hell, this should be sorted by TIME not note number....


  #MFH - corrected and optimized:
  def getRequiredNotesForJurgenOnTime(self, song, pos):
    track   = song.track[self.player]
    notes = [(time, event) for time, event in track.getEvents(pos - self.lateMargin, pos + 30) if isinstance(event, Note)]
    notes = [(time, event) for time, event in notes if not (event.hopod or event.played or event.skipped)]

    return sorted(notes, key=lambda x: x[0])    #MFH - what the hell, this should be sorted by TIME not note number....

  
  def hitNote(self, time, note):
     self.pickStartPos = max(self.pickStartPos, time)
     self.playedNotes = [(time, note)]
     note.played       = True
     return True  

  def areNotesTappable(self, notes):
    if not notes:
      return
    #for time, note in notes:
    #  if note.tappable > 1:
    #    return True
    return False


  def playDrumSounds(self, controls, playBassDrumOnly = False):   #MFH - handles playing of drum sounds.  
    #Returns list of drums that were just hit (including logic for detecting a held bass pedal)
    #pass playBassDrumOnly = True (optional paramater) to only play the bass drum sound, but still
    #  return a list of drums just hit (intelligently play the bass drum if it's held down during gameplay)
    drumsJustHit = [False, False, False, False, False]

    for i in range (5):
      if controls.getState(self.keys[i]) or controls.getState(self.keys[5+i]):
        if i == 0:
          if not self.bassDrumPedalDown:  #MFH - gotta check if bass drum pedal is just held down!
            if self.engine.data.bassDrumSoundFound:
              self.engine.data.bassDrumSound.play()
            self.bassDrumPedalDown = True
            drumsJustHit[0] = True
            if self.fretboardHop < 0.04:
              self.fretboardHop = 0.04  #stump
        else:
          self.bassDrumPedalDown = False
        if i == 1:
          if self.engine.data.T1DrumSoundFound and not playBassDrumOnly:
            self.engine.data.T1DrumSound.play()
          drumsJustHit[i] = True
        if i == 2:
          if self.engine.data.T2DrumSoundFound and not playBassDrumOnly:
            self.engine.data.T2DrumSound.play()
          drumsJustHit[i] = True
        if i == 3:
          if self.engine.data.T3DrumSoundFound and not playBassDrumOnly:
            self.engine.data.T3DrumSound.play()
          drumsJustHit[i] = True
        if i == 4:   #MFH - must actually activate starpower!
          if self.engine.data.CDrumSoundFound and not playBassDrumOnly:
            self.engine.data.CDrumSound.play()
          drumsJustHit[i] = True
    
    return drumsJustHit


  #volshebnyi - handle freestyle picks here
  def freestylePick(self, song, pos, controls):
    drumsJustHit = self.playDrumSounds(controls)
    numHits = 0
    for i, drumHit in enumerate(drumsJustHit):
      if drumHit:
        numHits += 1
        if i == 4:
          if not self.bigRockEndingMarkerSeen and (self.drumFillsActive or self.drumFillWasJustActive) and self.drumFillsHits >= 4 and not self.starPowerActive:
            drumFillCymbalPos = self.freestyleStart+self.freestyleLength
            minDrumFillCymbalHitTime = drumFillCymbalPos - self.earlyMargin
            maxDrumFillCymbalHitTime = drumFillCymbalPos + self.lateMargin
            if (pos >= minDrumFillCymbalHitTime) and (pos <= maxDrumFillCymbalHitTime):
              self.freestyleSP = True
        
    
    
#-    if controls.getState(self.keys[0]):   
#-      if not self.bassDrumPedalDown:  #MFH - gotta check if bass drum pedal is just held down!
#-        numHits = 1
#-        if self.engine.data.bassDrumSoundFound:
#-          self.engine.data.bassDrumSound.play()
#-        self.bassDrumPedalDown = True
#-    for i in range (1,5):
#-      if controls.getState(self.keys[i]) or controls.getState(self.keys[4+i]):
#-        numHits += 1
#-        if i == 1:
#-          if self.engine.data.T1DrumSoundFound:
#-            self.engine.data.T1DrumSound.play()
#-        if i == 2:
#-          if self.engine.data.T2DrumSoundFound:
#-            self.engine.data.T2DrumSound.play()
#-        if i == 3:
#-          if self.engine.data.T3DrumSoundFound:
#-            self.engine.data.T3DrumSound.play()
#-        if i == 4:   #MFH - must actually activate starpower!
#-          if self.engine.data.CDrumSoundFound:
#-            self.engine.data.CDrumSound.play()
#-          if self.drumFillsActive and self.drumFillsHits >= 4 and not self.starPowerActive:
#-            drumFillCymbalPos = self.freestyleStart+self.freestyleLength
#-            minDrumFillCymbalHitTime = drumFillCymbalPos - self.earlyMargin
#-            maxDrumFillCymbalHitTime = drumFillCymbalPos + self.lateMargin
#-            if (pos >= minDrumFillCymbalHitTime) and (pos <= maxDrumFillCymbalHitTime):
#-              self.freestyleSP = True

    return numHits

  
  def startPick(self, song, pos, controls, hopo = False):
    if not song:
      return False
    if not song.readyToGo:
      return

    if self.lastFretWasBassDrum:
      if controls.getState(self.keys[1]) or controls.getState(self.keys[2]) or controls.getState(self.keys[3]) or controls.getState(self.keys[4]) or controls.getState(self.keys[6]) or controls.getState(self.keys[7]) or controls.getState(self.keys[8]) or controls.getState(self.keys[9]):
        self.lastFretWasBassDrum = False
    elif controls.getState(self.keys[0]) or controls.getState(self.keys[5]):
      self.lastFretWasBassDrum = True
    else:
      self.lastFretWasBassDrum = False
      
    #Faaa Drum sound
    if self.lastFretWasT1:
      if controls.getState(self.keys[0]) or controls.getState(self.keys[2]) or controls.getState(self.keys[3]) or controls.getState(self.keys[4]) or controls.getState(self.keys[5]) or controls.getState(self.keys[7]) or controls.getState(self.keys[8]) or controls.getState(self.keys[9]):
        self.lastFretWasT1 = False
    elif controls.getState(self.keys[1]) or controls.getState(self.keys[6]):
      self.lastFretWasT1 = True
    else:
      self.lastFretWasT1 = False

    if self.lastFretWasT2:
      if controls.getState(self.keys[0]) or controls.getState(self.keys[1]) or controls.getState(self.keys[3]) or controls.getState(self.keys[4]) or controls.getState(self.keys[5]) or controls.getState(self.keys[6]) or controls.getState(self.keys[8]) or controls.getState(self.keys[9]):
        self.lastFretWasT2 = False
    elif controls.getState(self.keys[2]) or controls.getState(self.keys[7]):
      self.lastFretWasT2 = True
    else:
      self.lastFretWasT2 = False

    if self.lastFretWasT3:
      if controls.getState(self.keys[0]) or controls.getState(self.keys[1]) or controls.getState(self.keys[2]) or controls.getState(self.keys[4]) or controls.getState(self.keys[5]) or controls.getState(self.keys[6]) or controls.getState(self.keys[7]) or controls.getState(self.keys[9]):
        self.lastFretWasT3 = False
    elif controls.getState(self.keys[3]) or controls.getState(self.keys[8]):
      self.lastFretWasT3 = True
    else:
      self.lastFretWasT3 = False		  

    if self.lastFretWasC:
      if controls.getState(self.keys[0]) or controls.getState(self.keys[1]) or controls.getState(self.keys[2]) or controls.getState(self.keys[3]) or controls.getState(self.keys[5]) or controls.getState(self.keys[6]) or controls.getState(self.keys[7]) or controls.getState(self.keys[8]):
        self.lastFretWasC = False
    elif controls.getState(self.keys[4]) or controls.getState(self.keys[9]):
      self.lastFretWasC = True
    else:
      self.lastFretWasC = False
  
    #self.matchingNotes = self.getRequiredNotes(song, pos)
    self.matchingNotes = self.getRequiredNotesMFH(song, pos)    #MFH - ignore skipped notes please!
    

    # no self.matchingNotes?
    if not self.matchingNotes:
      return False
    self.playedNotes = []
    self.pickStartPos = pos
    
    #adding bass drum hit every bass fret:
    
    for time, note in self.matchingNotes:
      for i in range(5):
        if note.number == i and (controls.getState(self.keys[i]) or controls.getState(self.keys[i+5])):
          if self.guitarSolo:
            self.currentGuitarSoloHitNotes += 1
          if i == 0 and self.fretboardHop < 0.07:
              self.fretboardHop = 0.07  #stump

          Shader.list.var["drum"][i]=Shader.list.time()
          return self.hitNote(time, note)  
        
          

    return False        
    
  def startPick2(self, song, pos, controls, hopo = False):
    res = self.startPick(song, pos, controls, hopo)
    return res

  def startPick3(self, song, pos, controls, hopo = False):
    res = self.startPick(song, pos, controls, hopo)
    return res


  def endPick(self, pos):
    self.playedNotes = []
    #for time, note in self.playedNotes:
    #  if time + note.length > pos + self.noteReleaseMargin:
    #    return False
    return True
    
  def getPickLength(self, pos):
    #if not self.playedNotes:
    return 0.0
    
    ## The pick length is limited by the played notes
    #pickLength = pos - self.pickStartPos
    #for time, note in self.playedNotes:
    #  pickLength = min(pickLength, note.length)
    #return pickLength

  def coOpRescue(self, pos):
    self.coOpRestart = True #initializes Restart Timer
    self.coOpRescueTime  = pos
    self.starPower  = 0
    Log.debug("Rescued at " + str(pos))
  
  def run(self, ticks, pos, controls):
    if not self.paused:
      self.time += ticks
    #myfingershurt: must not decrease SP if paused.
    if self.starPowerActive == True and self.paused == False:
      self.starPower -= ticks/self.starPowerDecreaseDivisor 
      if self.starPower <= 0:
        self.starPower = 0
        self.starPowerActive = False
    

    activeFrets = [(note.number - 1) for time, note in self.playedNotes]

    
    for n in range(self.strings):
      if   n == 0 and (controls.getState(self.keys[1]) or controls.getState(self.keys[6])):
            self.fretWeight[n] = 0.5  
      elif n == 1 and (controls.getState(self.keys[2]) or controls.getState(self.keys[7])):
            self.fretWeight[n] = 0.5  
      elif n == 2 and (controls.getState(self.keys[3]) or controls.getState(self.keys[8])):
            self.fretWeight[n] = 0.5  
      elif n == 3 and (controls.getState(self.keys[4]) or controls.getState(self.keys[9])):
            self.fretWeight[n] = 0.5  
      elif controls.getState(self.keys[0]) or controls.getState(self.keys[5]):
            self.fretWeight[n] = 0.5
      else:
        self.fretWeight[n] = max(self.fretWeight[n] - ticks / 64.0, 0.0)
      if n in activeFrets:
        self.fretActivity[n] = min(self.fretActivity[n] + ticks / 32.0, 1.0)
      else:
        self.fretActivity[n] = max(self.fretActivity[n] - ticks / 64.0, 0.0)
      if -1 in activeFrets:
        self.fretActivity[n] = min(self.fretActivity[n] + ticks / 24.0, 0.6)

    # glorandwarf: moved the update bpm code - was after the for statement below
    # update bpm
    #if self.currentBpm != self.targetBpm:
    #  diff = self.targetBpm - self.currentBpm
    #  if (round((diff * .03), 4) != 0):
    #    self.currentBpm = round(self.currentBpm + (diff * .03), 4)
    #  else:
    #    self.currentBpm = self.targetBpm
    #  self.setBPM(self.currentBpm) # glorandwarf: was setDynamicBPM(self.currentBpm)

    for time, note in self.playedNotes:
      if pos > time + note.length:
        return False

    return True
