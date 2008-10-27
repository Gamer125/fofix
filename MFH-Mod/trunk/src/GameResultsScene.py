#####################################################################
# -*- coding: iso-8859-1 -*-                                        #
#                                                                   #
# Frets on Fire                                                     #
# Copyright (C) 2006 Sami Ky�stil�                                  #
#               2008 Alarian                                        #
#               2008 myfingershurt                                  #
#               2008 Glorandwarf                                    #
#               2008 ShiekOdaSandz                                  #
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

from Scene import SceneServer, SceneClient
from Menu import Menu
import Player
import Dialogs
import Song
import Data
import Theme
from Audio import Sound
from Language import _

import pygame
import math
import random

from OpenGL.GL import *
import Config
import Version

#myfingershurt: needed for multi-OS file fetching
import os
import Log


class GameResultsScene:
  pass

class GameResultsSceneServer(GameResultsScene, SceneServer):
  pass

class GameResultsSceneClient(GameResultsScene, SceneClient):
  def createClient(self, libraryName, songName, players = 1): #players = None
    Log.debug("GameResultsSceneClient class init...")
    self.libraryName     = libraryName
    self.songName        = songName
    self.stars           = [0 for i in players]
    self.accuracy        = [0 for i in players]
    self.counter         = 0
    self.showHighscores  = False
    self.highscoreIndex  = [-1 for i in players]
    self.taunt           = None
    self.uploadingScores = [False for p in players]
    self.highScoreResult = [None for p in players]
    self.resultNum       = 0
    self.uploadResult    = None
    self.nextScene       = None
    self.offset          = None
    self.pauseScroll     = None
    self.scorePart       = None
    self.scoreDifficulty = None
    self.playerList      = players
    self.spinnyDisabled   = True#NO SPINNY!!!    

    #myfingershurt: reordering so default is Change Song.
    items = [
      (_("Continue"),       self.changeSong),
      (_("Replay"),            self.replay),
      (_("Quit"), self.quit),
    ]
    self.menu = Menu(self.engine, items, onCancel = self.quit, pos = (.2, .5))
      
    self.engine.resource.load(self, "song", lambda: Song.loadSong(self.engine, songName, library = self.libraryName, notesOnly = True, part = [player.part for player in self.playerList]), onLoad = self.songLoaded)

    #Get theme
    themename = self.engine.data.themeLabel
    #now theme determination logic is only in data.py:
    self.theme = self.engine.data.theme
      
    self.starScoring = self.engine.config.get("game", "star_scoring")#MFH
    self.Congratphrase = self.engine.config.get("game", "congrats")#blazingamer

    self.resultCheerLoop = self.engine.config.get("game", "result_cheer_loop")#MFH
    self.cheerLoopDelay = self.engine.config.get("game", "cheer_loop_delay")#MFH
    self.cheerLoopCounter = self.cheerLoopDelay   #MFH - starts out ready to cheer
      
    #MFH
    self.hopoStyle        = self.engine.config.get("game", "hopo_style")
    if self.hopoStyle == 0:
      self.hopoStyle = _("None")
    elif self.hopoStyle == 1:
      self.hopoStyle = _("RF-Mod")
    elif self.hopoStyle == 2:
      self.hopoStyle = _("GH2 Strict")
    elif self.hopoStyle == 3:
      self.hopoStyle = _("GH2 Sloppy")
    elif self.hopoStyle == 4:
      self.hopoStyle = _("GH2")
    self.hitWindow = self.engine.config.get("game", "hit_window")  #this should be global, not retrieved every BPM change.
    if self.hitWindow == 0:
      self.hitWindow = _("Wide")
    elif self.hitWindow == 1:
      self.hitWindow = _("Standard")
    elif self.hitWindow == 2:
      self.hitWindow = _("Tight")
    elif self.hitWindow == 3:
      self.hitWindow = _("Hot Pants Tight")
    elif self.hitWindow == 4:
      self.hitWindow = _("Tight Like a Tiger")


    self.engine.loadImgDrawing(self, "background", os.path.join("themes",themename,"gameresults.png"))

    phrase = random.choice(Theme.resultsPhrase.split("_"))
    if phrase == "None":
      i = random.randint(0,5)
      if i == 0:
        phrase = _("Relax, it was an excellent show.")
      elif i == 1:
        phrase = _("Truly Amazing!")
      elif i == 2:
        phrase = _("Thanks for playing!")
      elif i == 3:
        phrase = _("One more song can't hurt, can it?")
      elif i == 4:
        phrase = _("What an amazing performance!")
      else:
        phrase = _("That's how it's done!")
    Dialogs.showLoadingScreen(self.engine, lambda: self.song, text = phrase)
    
  
  def handleWorldChartRanking(self, resultTemp):   #MFH
    self.highScoreResult[self.resultNum] = self.uploadResult
    self.resultNum += 1
  
  def keyPressed(self, key, unicode):
    ret = SceneClient.keyPressed(self, key, unicode)

    c = self.controls.keyPressed(key)
    if self.song and (c in [Player.KEY1, Player.KEY2, Player.CANCEL, Player.ACTION1, Player.ACTION2, Player.DRUM1A, Player.DRUM4A] or key == pygame.K_RETURN):
      for i,player in enumerate(self.playerList):
      
        scores = self.song.info.getHighscores(player.difficulty, part = player.part)
        if not scores or player.score > scores[-1][0] or len(scores) < 5:
          if player.cheating:
            Dialogs.showMessage(self.engine, _("No highscores for cheaters!"))
          elif player.score == 0: #trinidude4
            Dialogs.showMessage(self.engine, _("No highscore")) #trinidude4
          else:
            #alarian name = Dialogs.getText(self.engine, _("%d points is a new high score! Player " + str(i+1) + " enter your name") % player.score, player.name)
            name = Dialogs.getText(self.engine, _("%d points is a new high score! Enter your name") % player.score, player.name)
            if name:
              player.name = name

            #myfingershurt: don't separate chords for drum part totals:
            if player.part.text == "Drums":
              notesTotal = len([1 for time, event in self.song.track[i].getAllEvents() if isinstance(event, Song.Note)])
            else:
              notesTotal = len(set(time for time, event in self.song.track[i].getAllEvents() if isinstance(event, Song.Note)))
              
            modOptions1 = self.engine.config.getModOptions1(player.twoChord, 0)
            modOptions2 = self.engine.config.getModOptions2()
            scoreExt = (player.notesHit, notesTotal, player.longestStreak, Version.branchVersion(), modOptions1, modOptions2)
            self.highscoreIndex[i] = self.song.info.addHighscore(player.difficulty, player.score, self.stars[i], player.name, part = player.part, scoreExt = scoreExt)
            self.song.info.save()
          
            if self.engine.config.get("game", "uploadscores") and not player.cheating:
              self.uploadingScores[i] = True
              # evilynux - New url starting 20080902
              fn = lambda: self.song.info.uploadHighscores(self.engine.config.get("game", "uploadurl_w67_starpower"), self.song.getHash(), part = player.part)
              
              #self.engine.resource.load(self, "uploadResult", fn)
              self.engine.resource.load(self, "uploadResult", fn, onLoad = self.handleWorldChartRanking)  #MFH

      if len(self.playerList) > 1 and self.playerList[0].part == self.playerList[1].part and self.playerList[0].difficulty == self.playerList[1].difficulty and self.highscoreIndex[0] != -1 and self.highscoreIndex[1] != -1 and self.highscoreIndex[1] <= self.highscoreIndex[0]:
        self.highscoreIndex[0] += 1
      
      if self.song.info.count:
        count = int(self.song.info.count)
      else:
        count = 0
      count += 1
      self.song.info.count = "%d" % count
      self.song.info.save()
      self.showHighscores = True
      self.engine.view.pushLayer(self.menu)
      return True
    return ret

  def hidden(self):
    SceneClient.hidden(self)
    if self.nextScene:
      self.nextScene()
    
  def quit(self):
    self.background = None
    self.song = None
    self.engine.view.popLayer(self.menu)
    self.session.world.finishGame()
    
  def replay(self):
    self.background = None
    self.song = None
    self.engine.view.popLayer(self.menu)
    self.session.world.deleteScene(self)
    self.nextScene = lambda: self.session.world.createScene("GuitarScene", libraryName = self.libraryName, songName = self.songName, Players = len(self.playerList))
  
  def changeSong(self):
    self.background = None
    self.song = None
    self.engine.view.popLayer(self.menu)
    self.session.world.deleteScene(self)
    self.nextScene = lambda: self.session.world.createScene("SongChoosingScene")
   
  def songLoaded(self, song):
    for i,player in enumerate(self.playerList):
      song.difficulty[i] = player.difficulty

      notes = player.totalStreakNotes
      if notes:# ShiekOdaSandz: Determines the number of stars received at the end of the song; I modified Coffee's settings
        f = float(player.notesHit) / notes
        #self.stars[i]    = int(5.0   * (f + .05))
        self.stars[i] = player.stars
        self.accuracy[i] = 100.0 * f
        self.hits=player.notesHit
        self.totalnotes=notes
        
        taunt = None

        if self.Congratphrase:
          if player.score == 0 or player.cheating == True:
            taunt = os.path.join("sounds","jurgen1.ogg")
          elif self.accuracy[i] == 100.0:    #MFH - this will only play when you 100% a song
            taunt = random.choice([os.path.join("sounds","100pct1.ogg"), os.path.join("sounds","100pct2.ogg"), os.path.join("sounds","100pct3.ogg")])
          elif self.accuracy[i] >= 99.0:    #MFH - these 3 sounds will only play when you get > 99.0%
            taunt = random.choice([os.path.join("sounds","99pct1.ogg"), os.path.join("sounds","99pct2.ogg"), os.path.join("sounds","99pct3.ogg")])

          elif self.stars[i] in [0, 1]:
            taunt = random.choice([os.path.join("sounds","jurgen2.ogg"), os.path.join("sounds","jurgen3.ogg"), os.path.join("sounds","jurgen4.ogg"), os.path.join("sounds","jurgen5.ogg")])
          elif self.stars[i] == 5:
            taunt = random.choice([os.path.join("sounds","perfect1.ogg"), os.path.join("sounds","perfect2.ogg"), os.path.join("sounds","perfect3.ogg")])

      if taunt:
        try:
          self.engine.resource.load(self, "taunt", lambda: Sound(self.engine.resource.fileName(taunt)))
        except IOError:
          taunt = None

  def nextHighScore(self):
    if self.scoreDifficulty == None:
      self.scoreDifficulty = self.player.difficulty
    if self.scorePart == None:
      self.scorePart = self.player.part
      return
    
    found = 0  
    for part in self.song.info.parts:
      for difficulty in self.song.info.difficulties:
        if found == 1:
          self.scoreDifficulty = difficulty
          self.scorePart = part
          return
        
        if self.scoreDifficulty == difficulty and self.scorePart == part:
          found = 1

    self.scoreDifficulty = self.song.info.difficulties[0]
    self.scorePart = self.song.info.parts[0]
        
  def run(self, ticks):
    SceneClient.run(self, ticks)
    self.time    += ticks / 50.0
    self.counter += ticks

    if self.offset != None:
      self.offset -= ticks / 20000.0
    if self.pauseScroll != None:
      self.pauseScroll += ticks / 20000.0
      
    if self.counter > 5000 and self.taunt:
      #self.taunt.setVolume(self.engine.config.get("audio", "guitarvol"))
      self.taunt.setVolume(self.engine.config.get("audio", "SFX_volume"))  #MFH - sound effect level
      self.taunt.play()
      self.taunt = None

    #MFH - add counter here to play another crowd cheer before the one playing ends for an endless cheering loop
    if self.engine.data.cheerSoundFound > 0 and self.resultCheerLoop > 0:
      if self.resultCheerLoop == 2 or (self.resultCheerLoop == 1 and self.engine.data.cheerSoundFound == 2):
        self.cheerLoopCounter += 1
        if self.cheerLoopCounter >= self.cheerLoopDelay:
          self.cheerLoopCounter = 0
          self.engine.data.crowdSound.play()
    
  def anim(self, start, ticks):
    return min(1.0, float(max(start, self.counter)) / ticks)

  def render(self, visibility, topMost):
    self.engine.view.setViewport(1,0)
    SceneClient.render(self, visibility, topMost)
    
    bigFont = self.engine.data.bigFont
    font    = self.engine.data.font

    v = ((1 - visibility) ** 2)
    
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_COLOR_MATERIAL)

    self.engine.view.setOrthogonalProjection(normalize = True)
    try:
      t = self.time / 100
      w, h, = self.engine.view.geometry[2:4]
      r = .5
      if self.background:
        imgwidth = self.background.width1()
        wfactor = 640.000/imgwidth
        self.background.transform.reset()
        #self.background.transform.scale(1,-1)
        self.background.transform.scale(wfactor,-wfactor)
        self.background.transform.translate(w/2,h/2)
        self.background.draw()
      
      if self.showHighscores:
        for j,player in enumerate(self.playerList):
          #self.engine.view.setViewportHalf(len(self.playerList),j)
          scale = 0.0017
          endScroll = -.14
        
          if self.pauseScroll != None:
            self.offset = 0.0

          if self.pauseScroll > 0.5:
            self.pauseScroll = None
          if self.offset == None:
            self.offset = 0
            self.pauseScroll = 0
            self.nextHighScore()

          
          # evilynux - highscore
          if self.song is not None:
            text = _("%s High Scores for %s") % (self.scorePart, Dialogs.removeSongOrderPrefixFromName(self.song.info.name))
          else:
            text = _("%s High Scores") % self.scorePart
          w, h = font.getStringSize(text)

          Theme.setBaseColor(1 - v)
          font.render(text, (.5 - w / 2, .01 - v + self.offset))

          text = _("Difficulty: %s") % (self.scoreDifficulty)
          w, h = font.getStringSize(text)
          Theme.setBaseColor(1 - v)
          font.render(text, (.5 - w / 2, .01 - v + h + self.offset))
        
          x = .01
          y = .16 + v
          
        if self.song:
          i = -1
          for i, scores in enumerate(self.song.info.getHighscores(self.scoreDifficulty, part = self.scorePart)):
            score, stars, name, scores_ext = scores
            notesHit, notesTotal, noteStreak, modVersion, modOptions1, modOptions2 = scores_ext
            if stars == 6:
              stars = 5
              perfect = 1
            else:
              perfect = 0
            for j,player in enumerate(self.playerList):
              if (self.time % 10.0) < 5.0 and i == self.highscoreIndex[j] and self.scoreDifficulty == player.difficulty and self.scorePart == player.part:
                Theme.setSelectedColor(1 - v)
                break
              else:
                Theme.setBaseColor(1 - v)
            font.render("%d." % (i + 1), (x, y + self.offset),    scale = scale)
            if notesTotal != 0:
              score = "%s %.1f%%" % (score, (float(notesHit) / notesTotal) * 100.0)
            if noteStreak != 0:
              score = "%s (%d)" % (score, noteStreak)
            font.render(unicode(score), (x + .05, y + self.offset),   scale = scale)
            options = ""
            w2, h2 = font.getStringSize(options, scale = scale / 2)
            font.render(unicode(options), (.6 - w2, y + self.offset),   scale = scale / 2)
            # evilynux - Fixed star size following Font render bugfix
            if perfect == 1 and self.theme == 2:
              glColor3f(1, 1, 0) #racer: perfect is now gold for rock band
            font.render(unicode(Data.STAR2 * stars + Data.STAR1 * (5 - stars)), (x + .6, y + self.offset), scale = scale * 1.8)
            if perfect == 1 and self.theme < 2:
              glColor3f(0, 1, 0) #racer: perfect is green for any non-RB theme
            font.render(unicode(Data.STAR2 * stars + Data.STAR1 * (5 - stars)), (x + .6, y + self.offset), scale = scale * 1.8)
            for j,player in enumerate(self.playerList):
              if (self.time % 10.0) < 5.0 and i == self.highscoreIndex[j] and self.scoreDifficulty == player.difficulty and self.scorePart == player.part:
                Theme.setSelectedColor(1 - v)
                break
              else:
                Theme.setBaseColor(1 - v)
            font.render(name, (x + .8, y + self.offset), scale = scale)
            y += h
            endScroll -= .07
            
          if self.offset < endScroll or i == -1:
            self.offset = .8
            self.nextHighScore()
            endScroll = -0.14
          
        for j,player in enumerate(self.playerList): #MFH 
          if self.uploadingScores[j]:
            sScale = 0.001
            sW, sH = font.getStringSize("A", scale = sScale)
            sYPos = .7 - ( (sH * 1.25) * j)
            Theme.setBaseColor(1 - v)
            if self.highScoreResult[j] is None:
              upScoreText = _("Uploading Scores...")
              font.render("P%d (%s) %s" % (j+1, player.name, upScoreText), (.05, sYPos + v), scale = sScale)
            else:
              result = str(self.highScoreResult[j]).split(";")
              if len(result) > 0:
                upScoreText1 = _("Scores uploaded!")
                if result[0] == "True":
                  #MFH - display rank if it was successful
                  if len(result) > 1:
                    #font.render(_("Scores uploaded! ...your highscore ranks #" + result[1] + " on the world starpower chart!" ), (.05, .7 + v), scale = 0.001)
                    upScoreText2 = _("your highscore ranks")
                    upScoreText3 = _("on the world starpower chart!")
                    font.render("P%d (%s) %s %s  ...%s #%d %s" % (j+1, player.name, player.part.text, upScoreText1, upScoreText2, int(result[1]), upScoreText3), (.05, sYPos + v), scale = sScale)
                  else:
                    upScoreText2 = _("unknown rank.")
                    font.render("P%d (%s) %s %s  ... %s" % (j+1, player.name, player.part.text, upScoreText1, upScoreText2), (.05, sYPos + v), scale = sScale)
                else:
                  upScoreText2 = _("no new highscore.")
                  #font.render(_("Score upload failed!  World charts may be down."), (.05, .7 + v), scale = 0.001)
                  font.render("P%d (%s) %s %s  ...%s" % (j+1, player.name, player.part.text, upScoreText1, upScoreText2), (.05, sYPos + v), scale = sScale)
              else:
                upScoreText1 = _("Score upload failed!  World charts may be down.")
                font.render("P%d (%s) %s %s" % (j+1, player.name, player.part.text, upScoreText1), (.05, sYPos + v), scale = sScale)
        
        return
        



      #initial scoring - skipped after names entered
      Theme.setBaseColor(1 - v)
      if self.playerList[0].cheating:
        text = _("%s Cheated!") % Dialogs.removeSongOrderPrefixFromName(self.song.info.name)
      else:
        text = _("%s Finished!") % Dialogs.removeSongOrderPrefixFromName(self.song.info.name)
        w, h = font.getStringSize(text)
        Dialogs.wrapText(font, (.05, .045 - v), text)
        text = "%d/" % self.hits
        text2 = _("%d notes hit") % self.totalnotes
        text = text + text2
        w, h = font.getStringSize(text)
        Dialogs.wrapText(font, (.5 - w / 2, .54 - v - h), text)

      #MFH - TODO - add HOPO system & hit window display to this screen
      settingsScale = 0.0012
      settingsText = "HOPOs: %s, Hit Window: %s" % (self.hopoStyle, self.hitWindow)
      w, h = font.getStringSize(settingsText, settingsScale)
      font.render(settingsText, (.5 - w/2, 0.0), scale = settingsScale)
        
      for j,player in enumerate(self.playerList):
        if self.playerList[j].cheating:
          self.stars[j] = 0
          self.accuracy[j] = 0.0
    
        self.engine.view.setViewportHalf(len(self.playerList),j)
        text = "%d" % (player.score * self.anim(1000, 2000))
        w, h = bigFont.getStringSize(text)
        bigFont.render(text, (.5 - w / 2, .11 + v + (1.0 - self.anim(0, 1000) ** 3)), scale = 0.0025)
      
        if self.counter > 1000:
          scale = 0.0017
          if self.stars[j] == 6 and self.theme == 2: #racer: gold perfect for RB
            glColor3f(1, 1, 0)  
            text = (Data.STAR2 * (self.stars[j] - 1))
          elif self.stars[j] == 6 and self.theme < 2: #racer: green perfect for non-RB
            glColor3f(0, 1, 0)  
            text = (Data.STAR2 * (self.stars[j] - 1))
          else:
            text = (Data.STAR2 * self.stars[j] + Data.STAR1 * (5 - self.stars[j]))

          w, h = bigFont.getStringSize(Data.STAR1, scale = scale)
          x = .5 - w * len(text) / 2
          for i, ch in enumerate(text):
            bigFont.render(ch, (x + 100 * (1.0 - self.anim(1000 + i * 200, 1000 + (i + 1) * 200)) ** 2, .35 + v), scale = scale)
            x += w
      
        if self.counter > 2500:
          Theme.setBaseColor(1 - v)
          text = _("Accuracy: %.1f%%") % self.accuracy[j]
          w, h = font.getStringSize(text)
          font.render(text, (.5 - w / 2, .55 + v))
          text = _("Longest note streak: %d") % player.longestStreak
          w, h = font.getStringSize(text)
          font.render(text, (.5 - w / 2, .55 + h + v))
          if player.twoChord > 0:
            text = _("Part: %s on %s (2 chord)") % (player.part, player.difficulty)
          else:
            text = _("Part: %s on %s") % (player.part, player.difficulty)
          w, h = font.getStringSize(text)
          font.render(text, (.5 - w / 2, .55 + (2 * h)+ v))
      self.engine.view.setViewport(1,0)
    finally:
      self.engine.view.setViewport(1,0)
      self.engine.view.resetProjection()
