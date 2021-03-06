#####################################################################
# -*- coding: iso-8859-1 -*-                                        #
#                                                                   #
# Frets on Fire                                                     #
# Copyright (C) 2006 Sami Ky�stil�                                  #
#               2008 myfingershurt                                  #
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

import midi
import Log
import Audio
import Config
import os
import re
import shutil
import Config
import sha
import binascii
import Cerealizer
import urllib
import Version
import Theme
import copy
from Language import _

DEFAULT_LIBRARY         = "songs"

EXP_DIF     = 0
HAR_DIF     = 1
MED_DIF     = 2
EAS_DIF     = 3

#MFH - special text-event tracks for the separated text-event list variable
TK_SCRIPT = 0         #script.txt events
TK_SECTIONS = 1       #Section events
TK_GUITAR_SOLOS = 2   #Guitar Solo start/stop events
TK_LYRICS = 3         #RB MIDI Lyric events
TK_UNUSED_TEXT = 4    #Unused / other text events

#code for adding tracks, inside song.py:
#self.song.eventTracks[TK_SCRIPT].addEvent(self.abs_time(), event)  #MFH - add an event to the script.txt track
#self.song.eventTracks[TK_SECTIONS].addEvent(self.abs_time(), event)  #MFH - add an event to the sections track
#self.song.eventTracks[TK_GUITAR_SOLOS].addEvent(self.abs_time(), event)  #MFH - add an event to the guitar solos track
#self.song.eventTracks[TK_LYRICS].addEvent(self.abs_time(), event)  #MFH - add an event to the lyrics track
#self.song.eventTracks[TK_UNUSED_TEXT].addEvent(self.abs_time(), event)  #MFH - add an event to the unused text track

#code for accessing track objects, outside song.py:
#self.song.eventTracks[Song.TK_SCRIPT]
#self.song.eventTracks[Song.TK_SECTIONS]
#self.song.eventTracks[Song.TK_GUITAR_SOLOS]
#self.song.eventTracks[Song.TK_LYRICS]
#self.song.eventTracks[Song.TK_UNUSED_TEXT]


FOF_TYPE                = 0
GH1_TYPE                = 1
GH2_TYPE                = 2

GUITAR_PART             = 0
RHYTHM_PART             = 1
BASS_PART               = 2
LEAD_PART               = 3
DRUM_PART               = 4

class Part:
  def __init__(self, id, text):
    self.id   = id
    self.text = text
    Log.debug("Part class init (song.py)...")
    
  def __str__(self):
    return self.text

  def __repr__(self):
    return self.text

parts = {
  GUITAR_PART: Part(GUITAR_PART, "Guitar"),
  RHYTHM_PART: Part(RHYTHM_PART, "Rhythm Guitar"),
  BASS_PART:   Part(BASS_PART,   "Bass Guitar"),
  LEAD_PART:   Part(LEAD_PART,   "Lead Guitar"),
  DRUM_PART:   Part(DRUM_PART,   "Drums"),
}

class Difficulty:
  def __init__(self, id, text):
    self.id   = id
    self.text = text
    Log.debug("Difficulty class init (song.py)...")

    
  def __str__(self):
    return self.text

  def __repr__(self):
    return self.text

difficulties = {
  EAS_DIF: Difficulty(EAS_DIF, "Easy"),
  MED_DIF: Difficulty(MED_DIF, "Medium"),
  HAR_DIF: Difficulty(HAR_DIF, "Hard"),
  EXP_DIF: Difficulty(EXP_DIF, "Expert"),
}

defaultSections = ["Start","1/4","1/2","3/4"]





class SongInfo(object):
  def __init__(self, infoFileName):
    self.songName      = os.path.basename(os.path.dirname(infoFileName))
    self.fileName      = infoFileName
    self.info          = Config.MyConfigParser()
    self._difficulties = None
    self._parts        = None

    self.locked = False

    #MFH - want to read valid sections from the MIDI in for practice mode selection here:
    self._sections = None
    

    self.name = _("NoName")
    

    try:
      self.info.read(infoFileName)
    except:
      pass
    
    Log.debug("SongInfo class init (song.py): " + self.name)

    # Read highscores and verify their hashes.
    # There ain't no security like security throught obscurity :)
    self.highScores = {}
    
    scores = self._get("scores", str, "")
    scores_ext = self._get("scores_ext", str, "")
    if scores:
      scores = Cerealizer.loads(binascii.unhexlify(scores))
      if scores_ext:
        scores_ext = Cerealizer.loads(binascii.unhexlify(scores_ext))
      for difficulty in scores.keys():
        try:
          difficulty = difficulties[difficulty]
        except KeyError:
          continue
        for i, base_scores in enumerate(scores[difficulty.id]):
          score, stars, name, hash = base_scores
          if scores_ext != "":
            #Someone may have mixed extended and non extended
            try:
              hash_ext, stars2, notesHit, notesTotal, noteStreak, modVersion, modOptions1, modOptions2 =  scores_ext[difficulty.id][i]
              scoreExt = (notesHit, notesTotal, noteStreak, modVersion, modOptions1, modOptions2)
            except:
              hash_ext = 0
              scoreExt = (0, 0, 0 , "RF-mod", "Default", "Default")
          if self.getScoreHash(difficulty, score, stars, name) == hash:
            if scores_ext != "" and hash == hash_ext:
              self.addHighscore(difficulty, score, stars, name, part = parts[GUITAR_PART], scoreExt = scoreExt)
            else:
              self.addHighscore(difficulty, score, stars, name, part = parts[GUITAR_PART])
          else:
            Log.warn("Weak hack attempt detected. Better luck next time.")

    self.highScoresRhythm = {}
    
    scores = self._get("scores_rhythm", str, "")
    scores_ext = self._get("scores_rhythm_ext", str, "")
    if scores:
      scores = Cerealizer.loads(binascii.unhexlify(scores))
      if scores_ext:
        scores_ext = Cerealizer.loads(binascii.unhexlify(scores_ext))
      for difficulty in scores.keys():
        try:
          difficulty = difficulties[difficulty]
        except KeyError:
          continue
        #for score, stars, name, hash in scores[difficulty.id]:
        #  if self.getScoreHash(difficulty, score, stars, name) == hash:
        #    self.addHighscore(difficulty, score, stars, name, part = parts[RHYTHM_PART])
        #  else:
        #    Log.warn("Weak hack attempt detected. Better luck next time.")
        for i, base_scores in enumerate(scores[difficulty.id]):
          score, stars, name, hash = base_scores
          if scores_ext != "":
            #Someone may have mixed extended and non extended
            try:
              hash_ext, stars2, notesHit, notesTotal, noteStreak, modVersion, modOptions1, modOptions2 =  scores_ext[difficulty.id][i]
              scoreExt = (notesHit, notesTotal, noteStreak, modVersion, modOptions1, modOptions2)
            except:
              hash_ext = 0
              scoreExt = (0, 0, 0 , "RF-mod", "Default", "Default")
          if self.getScoreHash(difficulty, score, stars, name) == hash:
            if scores_ext != "" and hash == hash_ext:
              self.addHighscore(difficulty, score, stars, name, part = parts[RHYTHM_PART], scoreExt = scoreExt)
            else:
              self.addHighscore(difficulty, score, stars, name, part = parts[RHYTHM_PART])
          else:
            Log.warn("Weak hack attempt detected. Better luck next time.")

    self.highScoresBass = {}
    
    scores = self._get("scores_bass", str, "")
    scores_ext = self._get("scores_bass_ext", str, "")
    if scores:
      scores = Cerealizer.loads(binascii.unhexlify(scores))
      if scores_ext:
        scores_ext = Cerealizer.loads(binascii.unhexlify(scores_ext))
      for difficulty in scores.keys():
        try:
          difficulty = difficulties[difficulty]
        except KeyError:
          continue
        #for score, stars, name, hash in scores[difficulty.id]:
        #  if self.getScoreHash(difficulty, score, stars, name) == hash:
        #    self.addHighscore(difficulty, score, stars, name, part = parts[BASS_PART])
        #  else:
        #    Log.warn("Weak hack attempt detected. Better luck next time.")
        for i, base_scores in enumerate(scores[difficulty.id]):
          score, stars, name, hash = base_scores
          if scores_ext != "":
            #Someone may have mixed extended and non extended
            try:
              hash_ext, stars2, notesHit, notesTotal, noteStreak, modVersion, modOptions1, modOptions2 =  scores_ext[difficulty.id][i]
              scoreExt = (notesHit, notesTotal, noteStreak, modVersion, modOptions1, modOptions2)
            except:
              hash_ext = 0
              scoreExt = (0, 0, 0 , "RF-mod", "Default", "Default")
          if self.getScoreHash(difficulty, score, stars, name) == hash:
            if scores_ext != "" and hash == hash_ext:
              self.addHighscore(difficulty, score, stars, name, part = parts[BASS_PART], scoreExt = scoreExt)
            else:
              self.addHighscore(difficulty, score, stars, name, part = parts[BASS_PART])
          else:
            Log.warn("Weak hack attempt detected. Better luck next time.")

    self.highScoresLead = {}
    
    scores = self._get("scores_lead", str, "")
    scores_ext = self._get("scores_lead_ext", str, "")
    if scores:
      scores = Cerealizer.loads(binascii.unhexlify(scores))
      if scores_ext:
        scores_ext = Cerealizer.loads(binascii.unhexlify(scores_ext))
      for difficulty in scores.keys():
        try:
          difficulty = difficulties[difficulty]
        except KeyError:
          continue
        #for score, stars, name, hash in scores[difficulty.id]:
        #  if self.getScoreHash(difficulty, score, stars, name) == hash:
        #    self.addHighscore(difficulty, score, stars, name, part = parts[LEAD_PART])
        #  else:
        #    Log.warn("Weak hack attempt detected. Better luck next time.")            
        for i, base_scores in enumerate(scores[difficulty.id]):
          score, stars, name, hash = base_scores
          if scores_ext != "":
            #Someone may have mixed extended and non extended
            try:
              hash_ext, stars2, notesHit, notesTotal, noteStreak, modVersion, modOptions1, modOptions2 =  scores_ext[difficulty.id][i]
              scoreExt = (notesHit, notesTotal, noteStreak, modVersion, modOptions1, modOptions2)
            except:
              hash_ext = 0
              scoreExt = (0, 0, 0 , "RF-mod", "Default", "Default")
          if self.getScoreHash(difficulty, score, stars, name) == hash:
            if scores_ext != "" and hash == hash_ext:
              self.addHighscore(difficulty, score, stars, name, part = parts[LEAD_PART], scoreExt = scoreExt)
            else:
              self.addHighscore(difficulty, score, stars, name, part = parts[LEAD_PART])
          else:
            Log.warn("Weak hack attempt detected. Better luck next time.")

    #myfingershurt: drums :)
    self.highScoresDrum = {}
    
    scores = self._get("scores_drum", str, "")
    scores_ext = self._get("scores_drum_ext", str, "")
    if scores:
      scores = Cerealizer.loads(binascii.unhexlify(scores))
      if scores_ext:
        scores_ext = Cerealizer.loads(binascii.unhexlify(scores_ext))
      for difficulty in scores.keys():
        try:
          difficulty = difficulties[difficulty]
        except KeyError:
          continue
        #for score, stars, name, hash in scores[difficulty.id]:
        #  if self.getScoreHash(difficulty, score, stars, name) == hash:
        #    self.addHighscore(difficulty, score, stars, name, part = parts[DRUM_PART])
        #  else:
        #    Log.warn("Weak hack attempt detected. Better luck next time.")         
        for i, base_scores in enumerate(scores[difficulty.id]):
          score, stars, name, hash = base_scores
          if scores_ext != "":
            #Someone may have mixed extended and non extended
            try:
              hash_ext, stars2, notesHit, notesTotal, noteStreak, modVersion, modOptions1, modOptions2 =  scores_ext[difficulty.id][i]
              scoreExt = (notesHit, notesTotal, noteStreak, modVersion, modOptions1, modOptions2)
            except:
              hash_ext = 0
              scoreExt = (0, 0, 0 , "RF-mod", "Default", "Default")
          if self.getScoreHash(difficulty, score, stars, name) == hash:
            if scores_ext != "" and hash == hash_ext:
              self.addHighscore(difficulty, score, stars, name, part = parts[DRUM_PART], scoreExt = scoreExt)
            else:
              self.addHighscore(difficulty, score, stars, name, part = parts[DRUM_PART])
          else:
            Log.warn("Weak hack attempt detected. Better luck next time.")
            
  def _set(self, attr, value):
    if not self.info.has_section("song"):
      self.info.add_section("song")
    if type(value) == unicode:
      value = value.encode(Config.encoding)
    else:
      value = str(value)
    self.info.set("song", attr, value)
    
  def getObfuscatedScores(self, part = parts[GUITAR_PART]):
    s = {}
    if part == parts[GUITAR_PART]:
      highScores = self.highScores
    elif part == parts[RHYTHM_PART]:
      highScores = self.highScoresRhythm
    elif part == parts[BASS_PART]:
      highScores = self.highScoresBass
    elif part == parts[LEAD_PART]:
      highScores = self.highScoresLead
    elif part == parts[DRUM_PART]:
      highScores = self.highScoresDrum
    else:
      highScores = self.highScores
      
    for difficulty in highScores.keys():
      s[difficulty.id] = [(score, stars, name, self.getScoreHash(difficulty, score, stars, name)) for score, stars, name, scores_ext in highScores[difficulty]]
    return binascii.hexlify(Cerealizer.dumps(s))

  def getObfuscatedScoresExt(self, part = parts[GUITAR_PART]):
    s = {}
    if part == parts[GUITAR_PART]:
      highScores = self.highScores
    elif part == parts[RHYTHM_PART]:
      highScores = self.highScoresRhythm
    elif part == parts[BASS_PART]:
      highScores = self.highScoresBass
    elif part == parts[LEAD_PART]:
      highScores = self.highScoresLead
    elif part == parts[DRUM_PART]:
      highScores = self.highScoresDrum
    else:
      highScores = self.highScores
      
    for difficulty in highScores.keys():
      s[difficulty.id] = [(self.getScoreHash(difficulty, score, stars, name), stars) + scores_ext for score, stars, name, scores_ext in highScores[difficulty]]
    return binascii.hexlify(Cerealizer.dumps(s))

  def save(self):
    if self.highScores != {}:
      self._set("scores",        self.getObfuscatedScores(part = parts[GUITAR_PART]))
      self._set("scores_ext",    self.getObfuscatedScoresExt(part = parts[GUITAR_PART]))
    if self.highScoresRhythm != {}:
      self._set("scores_rhythm", self.getObfuscatedScores(part = parts[RHYTHM_PART]))
      self._set("scores_rhythm_ext", self.getObfuscatedScoresExt(part = parts[RHYTHM_PART]))
    if self.highScoresBass != {}:
      self._set("scores_bass",   self.getObfuscatedScores(part = parts[BASS_PART]))
      self._set("scores_bass_ext",   self.getObfuscatedScoresExt(part = parts[BASS_PART]))
    if self.highScoresLead != {}:
      self._set("scores_lead",   self.getObfuscatedScores(part = parts[LEAD_PART]))
      self._set("scores_lead_ext",   self.getObfuscatedScoresExt(part = parts[LEAD_PART]))
    #myfingershurt: drums :)
    if self.highScoresDrum != {}:
      self._set("scores_drum", self.getObfuscatedScores(part = parts[DRUM_PART]))
      self._set("scores_drum_ext", self.getObfuscatedScoresExt(part = parts[DRUM_PART]))
    
    f = open(self.fileName, "w")
    self.info.write(f)
    f.close()
    
  def _get(self, attr, type = None, default = ""):
    try:
      v = self.info.get("song", attr)
    except:
      v = default
    if v is not None and type:
      v = type(v)
    return v

  def getDifficulties(self):
    # Tutorials only have the medium difficulty
    if self.tutorial:
      return [difficulties[HAR_DIF]]

    if self._difficulties is not None:
      return self._difficulties

    # See which difficulties are available
    try:
      noteFileName = os.path.join(os.path.dirname(self.fileName), "notes.mid")
      Log.debug("Retrieving difficulties from: " + noteFileName)
      info = MidiInfoReaderNoSections()
      midiIn = midi.MidiInFile(info, noteFileName)
      try:
        midiIn.read()
      except MidiInfoReaderNoSections.Done:
        pass
      info.difficulties.sort(lambda a, b: cmp(b.id, a.id))
      self._difficulties = info.difficulties
    except:
      self._difficulties = difficulties.values()
    return self._difficulties

  def getParts(self):
    if self._parts is not None:
      return self._parts

    # See which parts are available
    try:
      noteFileName = os.path.join(os.path.dirname(self.fileName), "notes.mid")
      Log.debug("Retrieving parts from: " + noteFileName)
      info = MidiPartsReader()

      midiIn = midi.MidiInFile(info, noteFileName)
      try:
        midiIn.read()
      except MidiPartsReader.Done:
        pass
      if info.parts == []:
        part = parts[GUITAR_PART]
        info.parts.append(part)
      info.parts.sort(lambda b, a: cmp(b.id, a.id))
      self._parts = info.parts
    except:
      self._parts = parts.values()
    return self._parts

  def getName(self):
    return self._get("name")

  def setName(self, value):
    self._set("name", value)

  def getArtist(self):
    return self._get("artist")

  def getYear(self):
    return self._get("year")

  def getLoading(self):
    return self._get("loading_phrase")

  def getCassetteColor(self):
    c = self._get("cassettecolor")
    if c:
      return Theme.hexToColor(c)
  
  def setCassetteColor(self, color):
    self._set("cassettecolor", Theme.colorToHex(color))
  
  def setArtist(self, value):
    self._set("artist", value)

  def setYear(self, value):
    self._set("year", value)

  def setLoading(self, value):
    self._set("loading_phrase", value)
    
  def getScoreHash(self, difficulty, score, stars, name):
    return sha.sha("%d%d%d%s" % (difficulty.id, score, stars, name)).hexdigest()
    
  def getDelay(self):
    return self._get("delay", int, 0)
    
  def setDelay(self, value):
    return self._set("delay", value)

  def getFrets(self):
    return self._get("frets")

  def setFrets(self, value):
    self._set("frets", value)
    
  def getVersion(self):
    return self._get("version")

  def setVersion(self, value):
    self._set("version", value)

  def getTags(self):
    return self._get("tags")

  def setTags(self, value):
    self._set("tags", value)

  def getHopo(self):
    return self._get("hopo")

  def setHopo(self, value):
    self._set("hopo", value)

  def getCount(self):
    return self._get("count")

  def setCount(self, value):
    self._set("count", value)

  def getEighthNoteHopo(self):
    return self._get("eighthnote_hopo")

  def setEighthNoteHopo(self, value):
    self._set("eighthnote_hopo", value)

  def getLyrics(self):
    return self._get("lyrics")

  def setLyrics(self, value):
    self._set("lyrics", value)    
        

  def getHighscoresWithPartString(self, difficulty, part = str(parts[GUITAR_PART]) ):
    if part == str(parts[GUITAR_PART]):
      highScores = self.highScores
    elif part == str(parts[RHYTHM_PART]):
      highScores = self.highScoresRhythm
    elif part == str(parts[BASS_PART]):
      highScores = self.highScoresBass
    elif part == str(parts[LEAD_PART]):
      highScores = self.highScoresLead
    #myfingershurt: drums :)
    elif part == str(parts[DRUM_PART]):
      highScores = self.highScoresDrum
    else:
      highScores = self.highScores
      
    try:
      return highScores[difficulty]
    except KeyError:
      return []


  def getHighscores(self, difficulty, part = parts[GUITAR_PART]):
    if part == parts[GUITAR_PART]:
      highScores = self.highScores
    elif part == parts[RHYTHM_PART]:
      highScores = self.highScoresRhythm
    elif part == parts[BASS_PART]:
      highScores = self.highScoresBass
    elif part == parts[LEAD_PART]:
      highScores = self.highScoresLead
    #myfingershurt: drums :)
    elif part == parts[DRUM_PART]:
      highScores = self.highScoresDrum
    else:
      highScores = self.highScores
      
    try:
      return highScores[difficulty]
    except KeyError:
      return []
      
  def uploadHighscores(self, url, songHash, part = parts[GUITAR_PART]):
    try:
      d = {
        "songName": self.songName,
        "songHash": songHash,
        "scores":   self.getObfuscatedScores(part = part),
        "scores_ext": self.getObfuscatedScoresExt(part = part),
        "version":  Version.version(),
        "songPart": part
      }
      data = urllib.urlopen(url + "?" + urllib.urlencode(d)).read()
      Log.debug("Score upload result: %s" % data)
      #return data == "True"
      return data   #MFH - want to return the actual result data.
    except Exception, e:
      Log.error("Score upload error: %s" % e)
      return False
    return True
  
  def addHighscore(self, difficulty, score, stars, name, part = parts[GUITAR_PART], scoreExt = (0, 0, 0, "RF-mod", "Default", "Default")):
    if part == parts[GUITAR_PART]:
      highScores = self.highScores
    elif part == parts[RHYTHM_PART]:
      highScores = self.highScoresRhythm
    elif part == parts[BASS_PART]:
      highScores = self.highScoresBass
    elif part == parts[LEAD_PART]:
      highScores = self.highScoresLead
    #myfingershurt: drums :)
    elif part == parts[DRUM_PART]:
      highScores = self.highScoresDrum
    else:
      highScores = self.highScores

    if not difficulty in highScores:
      highScores[difficulty] = []
    highScores[difficulty].append((score, stars, name, scoreExt))
    highScores[difficulty].sort(lambda a, b: {True: -1, False: 1}[a[0] > b[0]])
    highScores[difficulty] = highScores[difficulty][:5]
    for i, scores in enumerate(highScores[difficulty]):
      _score, _stars, _name, _scores_ext = scores
      if _score == score and _stars == stars and _name == name:
        return i
    return -1

  def isTutorial(self):
    return self._get("tutorial", int, 0) == 1

  def findTag(self, find, value = None):
    for tag in self.tags.split(','):
      temp = tag.split('=')
      if find == temp[0]:
        if value == None:
          return True
        elif len(temp) == 2 and value == temp[1]:
          return True

    return False
      

  def getSections(self):    #MFH
    if self._sections is not None:
      return self._sections
    # See which sections are available
    try:
      noteFileName = os.path.join(os.path.dirname(self.fileName), "notes.mid")
      Log.debug("Retrieving sections from: " + noteFileName)
      info = MidiInfoReader()
      midiIn = midi.MidiInFile(info, noteFileName)
      try:
        midiIn.read()
      except MidiInfoReader.Done:
        pass
      self._sections = info.sections
      if len(self._sections) <= 1:
        self._sections = info.noteCountSections
        self._sections.insert(0,["0:00 -> Start", 0.0])
        Log.warn("Song.py: Using auto-generated note count sections...")
        Log.debug("Practice sections: " + str(self._sections))
            
      else:
        self._sections.insert(0,["0:00 -> Start", 0.0])
        Log.debug("Practice sections: " + str(self._sections))
    except Exception, e:
      Log.warn("Song.py: Unable to retrieve section names for practice mode selection: %s" % e)
      self._sections = None
    return self._sections


    #coolguy567's unlock system
  def getUnlockID(self):
    return self._get("unlock_id")
    
  def getUnlockRequire(self):
    return self._get("unlock_require")
  
  def getUnlockText(self):
    return self._get("unlock_text", default = _("This song is locked."))
  
  # This takes True or False, not the value in the ini
  def setCompleted(self, value):
    if value:
      self._set("unlock_completed", len(self.name) * len(self.artist) + 1)
    else:
      self._set("unlock_completed", 0)
    
  # This returns True or False, not the value in the ini
  def getCompleted(self):
    iniValue = self._get("unlock_completed", int, default = 0)
    if iniValue == len(self.name) * len(self.artist) + 1: # yay, security through obscurity!
      return True
    else:
      return False
  
  def setLocked(self, value):
    self.locked = value
  
  # WARNING this will only work on a SongInfo loaded via getAvailableSongs
  # (yeah, I know)
  def getLocked(self):
    return self.locked

    
  name          = property(getName, setName)
  artist        = property(getArtist, setArtist)
  year          = property(getYear, setYear)
  loading       = property(getLoading, setLoading)
  delay         = property(getDelay, setDelay)
  tutorial      = property(isTutorial)
  difficulties  = property(getDifficulties)
  cassetteColor = property(getCassetteColor, setCassetteColor)
  #New RF-mod Items
  parts         = property(getParts)
  frets         = property(getFrets, setFrets)
  version       = property(getVersion, setVersion)
  tags          = property(getTags, setTags)
  hopo          = property(getHopo, setHopo)
  count         = property(getCount, setCount)
  lyrics        = property(getLyrics, setLyrics)
  EighthNoteHopo = property(getEighthNoteHopo, setEighthNoteHopo)
  #May no longer be necessary
  folder        = False
  
  completed     = property(getCompleted, setCompleted)
  sections      = property(getSections)   #MFH

class LibraryInfo(object):
  def __init__(self, libraryName, infoFileName):
    self.libraryName   = libraryName
    self.fileName      = infoFileName
    self.info          = Config.MyConfigParser()
    self.songCount     = 0

    self.artist = None

    Log.debug("LibraryInfo class init (song.py)...")
    

    try:
      self.info.read(infoFileName)
    except:
      pass

    # Set a default name
    if not self.name:
      self.name = os.path.basename(os.path.dirname(self.fileName))
    if Config.get("performance", "disable_libcount") == True:
      return
    # Count the available songs
    libraryRoot = os.path.dirname(self.fileName)
    for name in os.listdir(libraryRoot):
      if not os.path.isdir(os.path.join(libraryRoot, name)) or name.startswith("."):
      #if not os.path.isdir(os.path.join(libraryRoot, name)):
        continue
      if os.path.isfile(os.path.join(libraryRoot, name, "notes.mid")):
        self.songCount += 1

  def _set(self, attr, value):
    if not self.info.has_section("library"):
      self.info.add_section("library")
    if type(value) == unicode:
      value = value.encode(Config.encoding)
    else:
      value = str(value)
    self.info.set("library", attr, value)
    
  def save(self):
    f = open(self.fileName, "w")
    self.info.write(f)
    f.close()
    
  def _get(self, attr, type = None, default = ""):
    try:
      v = self.info.get("library", attr)
    except:
      v = default
    if v is not None and type:
      v = type(v)
    return v

  def getName(self):
    return self._get("name")

  def setName(self, value):
    self._set("name", value)

  def getColor(self):
    c = self._get("color")
    if c:
      return Theme.hexToColor(c)
  
  def setColor(self, color):
    self._set("color", Theme.colorToHex(color))
        
  name          = property(getName, setName)
  color         = property(getColor, setColor)




class BlankSpaceInfo(object): #MFH
  #def __init__(self, config, section):
  def __init__(self, nameToDisplay = ""):
    #self.info    = config
    #self.section = section
    self.nameToDisplay = nameToDisplay

    Log.debug("BlankSpaceInfo class init (song.py)...")

    self.artist = None    #MFH - prevents search errors

  def _set(self, attr, value):
    if type(value) == unicode:
      value = value.encode(Config.encoding)
    else:
      value = str(value)
    self.info.set(self.section, attr, value)
    
  def _get(self, attr, type = None, default = ""):
    try:
      v = self.info.get(self.section, attr)
    except:
      v = default
    if v is not None and type:
      v = type(v)
    return v

  def getName(self):
    #return self._get("name")
    return self.nameToDisplay

  def setName(self, value):
    self._set("name", value)

  def getColor(self):
    c = self._get("color")
    if c:
      return Theme.hexToColor(c)
  
  def setColor(self, color):
    self._set("color", Theme.colorToHex(color))

  def getUnlockID(self):
    return ""

         
  name          = property(getName, setName)
  color         = property(getColor, setColor)



class CareerResetterInfo(object): #MFH
  #def __init__(self, config, section):
  def __init__(self):
    #self.info    = config
    #self.section = section

    Log.debug("CareerResetterInfo class init (song.py)...")

    self.artist = None    #MFH - prevents search errors

  def _set(self, attr, value):
    if type(value) == unicode:
      value = value.encode(Config.encoding)
    else:
      value = str(value)
    self.info.set(self.section, attr, value)
    
  def _get(self, attr, type = None, default = ""):
    try:
      v = self.info.get(self.section, attr)
    except:
      v = default
    if v is not None and type:
      v = type(v)
    return v

  def getName(self):
    #return self._get("name")
    return _("Reset Career")

  def setName(self, value):
    self._set("name", value)

  def getColor(self):
    c = self._get("color")
    if c:
      return Theme.hexToColor(c)
  
  def setColor(self, color):
    self._set("color", Theme.colorToHex(color))
         
  name          = property(getName, setName)
  color         = property(getColor, setColor)


#coolguy567's unlock system
class TitleInfo(object):
  def __init__(self, config, section):
    self.info    = config
    self.section = section

    Log.debug("TitleInfo class init (song.py)...")

    self.artist = None    #MFH - prevents search errors

  def _set(self, attr, value):
    if type(value) == unicode:
      value = value.encode(Config.encoding)
    else:
      value = str(value)
    self.info.set(self.section, attr, value)
    
  def _get(self, attr, type = None, default = ""):
    try:
      v = self.info.get(self.section, attr)
    except:
      v = default
    if v is not None and type:
      v = type(v)
    return v

  def getName(self):
    return self._get("name")

  def setName(self, value):
    self._set("name", value)

  def getColor(self):
    c = self._get("color")
    if c:
      return Theme.hexToColor(c)
  
  def setColor(self, color):
    self._set("color", Theme.colorToHex(color))
        
  def getUnlockID(self):
    return self._get("unlock_id")
        
  name          = property(getName, setName)
  color         = property(getColor, setColor)




class Event:
  def __init__(self, length):
    self.length = length

class Note(Event):
  def __init__(self, number, length, special = False, tappable = 0, star = False, finalStar = False):
    Event.__init__(self, length)
    self.number   = number
    self.played   = False
    self.special  = special
    self.tappable = tappable
    #RF-mod
    self.hopod   = False
    self.skipped = False
    self.flameCount = 0
    self.star = star
    self.finalStar = finalStar
    self.noteBpm = 0.0
    
    
  def __repr__(self):
    return "<#%d>" % self.number

class Bars(Event):
  def __init__(self, barType):
    Event.__init__(self, barType)
    self.barType   = barType #0 half-beat, 1 beat, 2 measure
    self.soundPlayed = False
    
  def __repr__(self):
    return "<#%d>" % self.barType

class Tempo(Event):
  def __init__(self, bpm):
    Event.__init__(self, 0)
    self.bpm = bpm
    
  def __repr__(self):
    return "<%d bpm>" % self.bpm

class TextEvent(Event):
  def __init__(self, text, length):
    Event.__init__(self, length)
    self.text = text

  def __repr__(self):
    return "<%s>" % self.text

class PictureEvent(Event):
  def __init__(self, fileName, length):
    Event.__init__(self, length)
    self.fileName = fileName
    
class Track:
  granularity = 50
  
  def __init__(self, engine):
    self.events = []
    self.allEvents = []
    self.marked = False

    Log.debug("Track class init (song.py)...")

    self.chordFudge = 1

    self.hopoTick = engine.config.get("coffee", "moreHopo")

  def __getitem__(self, index):
    #if isinstance(index, slice):
    #    return [x**2 for x in index]
    #else:
    #    return index**2
    #return index**2
    return self.allEvents[index]

  def __len__(self):
    return len(self.allEvents)

  def addEvent(self, time, event):
    for t in range(int(time / self.granularity), int((time + event.length) / self.granularity) + 1):
      if len(self.events) < t + 1:
        n = t + 1 - len(self.events)
        n *= 8
        self.events = self.events + [[] for n in range(n)]
      self.events[t].append((time - (t * self.granularity), event))
    self.allEvents.append((time, event))

  def removeEvent(self, time, event):
    for t in range(int(time / self.granularity), int((time + event.length) / self.granularity) + 1):
      e = (time - (t * self.granularity), event)
      if t < len(self.events) and e in self.events[t]:
        self.events[t].remove(e)
    if (time, event) in self.allEvents:
      self.allEvents.remove((time, event))

  def getEvents(self, startTime, endTime):
    t1, t2 = [int(x) for x in [startTime / self.granularity, endTime / self.granularity]]
    if t1 > t2:
      t1, t2 = t2, t1

    events = []
    for t in range(max(t1, 0), min(len(self.events), t2)):
      for diff, event in self.events[t]:
        time = (self.granularity * t) + diff
        if not (time, event) in events:
          events.append((time, event))
    return events

  def getAllEvents(self):
    return self.allEvents

  def reset(self):
    for eventList in self.events:
      for time, event in eventList:
        if isinstance(event, Note):
          event.played = False
          event.hopod = False
          event.skipped = False
          event.flameCount = 0

  #myfingershurt: this function may be commented out, but is left in for
  #old INI file compatibility reasons
  #def markTappable(self):
    # Determine which notes are tappable. The rules are:
    #  1. Not the first note of the track
    #  2. Previous note not the same as this one
    #  3. Previous note not a chord
    #  4. Previous note ends at most 161 ticks before this one starts
    #bpm             = None
    #ticksPerBeat    = 480
    #tickThreshold   = 161
    #prevNotes       = []
    #currentNotes    = []
    #currentTicks    = 0.0
    #prevTicks       = 0.0
    #epsilon         = 1e-3

    #def beatsToTicks(time):
      #return (time * bpm * ticksPerBeat) / 60000.0

    #if not self.allEvents:
      #return

    #for time, event in self.allEvents + [self.allEvents[-1]]:
      #if isinstance(event, Tempo):
        #bpm = event.bpm
      #elif isinstance(event, Note):
        # All notes are initially not tappable
        #event.tappable = 0
        #ticks = beatsToTicks(time)
        
        # Part of chord?
        #if ticks < currentTicks + epsilon:
          #currentNotes.append(event)
          #continue

        # Previous note not a chord?
        #if len(prevNotes) == 1:
          # Previous note ended recently enough?
          #prevEndTicks = prevTicks + beatsToTicks(prevNotes[0].length)
          #if currentTicks - prevEndTicks <= tickThreshold:
            #for note in currentNotes:
              # Are any current notes the same as the previous one?
              #if note.number == prevNotes[0].number:
                #break
            #else:
              # If all the notes are different, mark the current notes tappable
              #for note in currentNotes:
                #note.tappable = 2

        # Set the current notes as the previous notes
        #prevNotes    = currentNotes
        #prevTicks    = currentTicks
        #currentNotes = [event]
        #currentTicks = ticks
#---------------------

  def markHopoRF(self, EighthNH):
    lastTick = 0
    lastTime  = 0
    lastEvent = Note
    
    tickDelta = 0
    noteDelta = 0

    #dtb file says 170 ticks
    hopoDelta = 170
    if str(EighthNH) == "1":
        hopoDelta = 250
    else:
        hopoDelta = 170
    self.chordFudge = 10

    if self.hopoTick == 0:
      ticksPerBeat = 960
    elif self.hopoTick == 1:
      ticksPerBeat = 480
    else:
      ticksPerBeat = 240
    hopoNotes = []
    chordNotes = []
    sameNotes = []
    bpmNotes = []
    firstTime = 1

    #If already processed abort   
    if self.marked == True:
      return
    
    for time, event in self.allEvents:
      if isinstance(event, Tempo):
        bpmNotes.append([time, event])
        continue
      if not isinstance(event, Note):
        continue
      
      while bpmNotes and time >= bpmNotes[0][0]:
        #Adjust to new BPM
        #bpm = bpmNotes[0][1].bpm
        bpmTime, bpmEvent = bpmNotes.pop(0)
        bpm = bpmEvent.bpm

      tick = (time * bpm * ticksPerBeat) / 60000.0
      lastTick = (lastTime * bpm * ticksPerBeat) / 60000.0
      
      #skip first note
      if firstTime == 1:
        event.tappable = -3
        lastEvent = event
        lastTime  = time
        firstTime = 0
        continue

      tickDelta = tick - lastTick        
      noteDelta = event.number - lastEvent.number

      #previous note and current note HOPOable      
      if tickDelta <= hopoDelta:
        #Add both notes to HOPO list even if duplicate.  Will come out in processing
        if (not hopoNotes) or not (hopoNotes[-1][0] == lastTime and hopoNotes[-1][1] == lastEvent):
          #special case for first marker note.  Change it to a HOPO start
          if not hopoNotes and lastEvent.tappable == -3:
            lastEvent.tappable = 1
          #this may be incorrect if a bpm event happened inbetween this note and last note
          hopoNotes.append([lastTime, bpmEvent])
          hopoNotes.append([lastTime, lastEvent])

        hopoNotes.append([bpmTime, bpmEvent])
        hopoNotes.append([time, event])
        
      #HOPO Over        
      if tickDelta > hopoDelta:
        if hopoNotes != []:
          #If the last event is the last HOPO note, mark it as a HOPO end
          if lastEvent.tappable != -1 and hopoNotes[-1][1] == lastEvent:
            if lastEvent.tappable >= 0:
              lastEvent.tappable = 3
            else:
              lastEvent.tappable = -1

      #This is the same note as before
      elif noteDelta == 0:
        #Add both notes to bad list even if duplicate.  Will come out in processing
        sameNotes.append(lastEvent)
        sameNotes.append(event)
        lastEvent.tappable = -2
        event.tappable = -2
            
      #This is a chord
      elif tickDelta < self.chordFudge:
        #Add both notes to bad list even if duplicate.  Will come out in processing
        if len(chordNotes) != 0 and chordNotes[-1] != lastEvent:
          chordNotes.append(lastEvent)
        chordNotes.append(event)
        lastEvent.tappable = -1
        event.tappable = -1
        
      lastEvent = event
      lastTime = time
    else:
      #Add last note to HOPO list if applicable
      if noteDelta != 0 and tickDelta > 1.5 and tickDelta < hopoDelta and isinstance(event, Note):
        hopoNotes.append([time, bpmEvent])
        hopoNotes.append([time, event])

    firstTime = 1
    note = None

    for note in list(chordNotes):
      #chord notes -1
      note.tappable = -1   

    for note in list(sameNotes):
      #same note in string -2
      note.tappable = -2

    bpmNotes = []
    
    for time, note in list(hopoNotes):
      if isinstance(note, Tempo):
        bpmNotes.append([time, note])
        continue
      if not isinstance(note, Note):
        continue
      while bpmNotes and time >= bpmNotes[0][0]:
        #Adjust to new BPM
        #bpm = bpmNotes[0][1].bpm
        bpmTime, bpmEvent = bpmNotes.pop(0)
        bpm = bpmEvent.bpm

      if firstTime == 1:
        if note.tappable >= 0:
          note.tappable = 1
        lastEvent = note
        firstTime = 0
        continue


#need to recompute (or carry forward) BPM at this time
      tick = (time * bpm * ticksPerBeat) / 60000.0
      lastTick = (lastTime * bpm * ticksPerBeat) / 60000.0
      tickDelta = tick - lastTick

      #current Note Invalid
      if note.tappable < 0:
        #If current note is invalid for HOPO, and previous note was start of a HOPO section, then previous note not HOPO
        if lastEvent.tappable == 1:
          lastEvent.tappable = 0
        #If current note is beginning of a same note sequence, it's valid for END of HOPO only
        elif lastEvent.tappable > 0:
          lastEvent.tappable = 3
      #current note valid
      elif note.tappable >= 0:
        #String of same notes can be followed by HOPO
        if note.tappable == 3:
          #This is the end of a valid HOPO section
          if lastEvent.tappable == 1 or lastEvent.tappable == 2:
            lastEvent = note
            lastTime = time
            continue
          if lastEvent.tappable == -2:
            #If its the same note again it's invalid
            if lastEvent.number == note.number:
              note.tappable = -2
            else:
              lastEvent.tappable = 1
          elif lastEvent.tappable == 0:
            lastEvent.tappable = 1
          #If last note was invalid or end of HOPO section, and current note is end, it is really not HOPO
          elif lastEvent.tappable != 2 and lastEvent.tappable != 1:
            note.tappable = 0
          #If last event was invalid or end of HOPO section, current note is start of HOPO
          else:
            note.tappable = 1
        elif note.tappable == 2:
          if lastEvent.tappable == -2:
            note.tappable = 1
          elif lastEvent.tappable == -1:
            note.tappable = 0
        elif note.tappable == 1:
          if lastEvent.tappable == 2:
            note.tappable = 0
        else:
          if lastEvent.tappable == -2:
            if tickDelta <= hopoDelta:
              lastEvent.tappable = 1
              
          if lastEvent.tappable != 2 and lastEvent.tappable != 1:
            note.tappable = 1
          else:
            if note.tappable == 1:
              note.tappable = 1
            else:
              note.tappable = 2
      lastEvent = note
      lastTime = time
    else:
      if note != None:
        #Handle last note
        #If it is the start of a HOPO, it's not really a HOPO
        if note.tappable == 1:
          note.tappable = 0
        #If it is the middle of a HOPO, it's really the end of a HOPO
        elif note.tappable == 2:
          note.tappable = 3      
    self.marked = True

    for time, event in self.allEvents:
      if isinstance(event, Tempo):
        bpmNotes.append([time, event])
        continue
      if not isinstance(event, Note):
        continue



#---------------------
  def markHopoGH2(self, EighthNH, HoposAfterChords):
    lastTick = 0
    lastTime  = 0
    lastEvent = Note
    
    tickDelta = 0
    noteDelta = 0

    #dtb file says 170 ticks
    hopoDelta = 170
    if str(EighthNH) == "1":
        hopoDelta = 250
    else:
        hopoDelta = 170

    #chordFudge = 10
    self.chordFudge = 1   #MFH - there should be no chord fudge.

    if self.hopoTick == 0:    #HOPO frequency
      ticksPerBeat = 960
    elif self.hopoTick == 1:
      ticksPerBeat = 480
    else:
      ticksPerBeat = 240
    hopoNotes = []

    #myfingershurt:
    tickDeltaBeforeLast = 0     #3 notes in the past
    lastTickDelta = 0   #2 notes in the past

    
    bpmNotes = []
    firstTime = 1

    #If already processed abort   
    if self.marked == True:
      return
    
    for time, event in self.allEvents:
      if isinstance(event, Tempo):
        bpmNotes.append([time, event])
        continue
      if not isinstance(event, Note):
        continue
      
      while bpmNotes and time >= bpmNotes[0][0]:
        #Adjust to new BPM
        #bpm = bpmNotes[0][1].bpm
        bpmTime, bpmEvent = bpmNotes.pop(0)
        bpm = bpmEvent.bpm

      tick = (time * bpm * ticksPerBeat) / 60000.0
      lastTick = (lastTime * bpm * ticksPerBeat) / 60000.0


     
      #skip first note
      if firstTime == 1:
        event.tappable = -3
        lastEvent = event
        lastTime  = time
        eventBeforeLast = lastEvent
        timeBeforeLast = lastTime
        eventBeforeEventBeforeLast = eventBeforeLast
        timeBeforeTimeBeforeLast = timeBeforeLast
        firstTime = 0
        continue

      #tickDeltaBeforeTickDeltaBeforeLast = tickDeltaBeforeLast    #4 notes in the past
      tickDeltaBeforeLast = lastTickDelta     #3 notes in the past
      lastTickDelta = tickDelta   #2 notes in the past
      
      tickDelta = tick - lastTick        
      noteDelta = event.number - lastEvent.number

      #myfingershurt: This initial sweep drops any notes within the timing 
      # threshold into the hopoNotes array (which would be more aptly named,
      #  the "potentialHopoNotes" array).  Another loop down below 
      #   further refines the HOPO determinations...

      #previous note and current note HOPOable      
      if tickDelta <= hopoDelta:
        #Add both notes to HOPO list even if duplicate.  Will come out in processing
        if (not hopoNotes) or not (hopoNotes[-1][0] == lastTime and hopoNotes[-1][1] == lastEvent):
          #special case for first marker note.  Change it to a HOPO start
          if not hopoNotes and lastEvent.tappable == -3:
            lastEvent.tappable = 1
          #this may be incorrect if a bpm event happened inbetween this note and last note
          hopoNotes.append([lastTime, bpmEvent])
          hopoNotes.append([lastTime, lastEvent])

        hopoNotes.append([bpmTime, bpmEvent])
        hopoNotes.append([time, event])




        
      #HOPO definitely over - time since last note too great.
      if tickDelta > hopoDelta:
        if hopoNotes != []:
          #If the last event is the last HOPO note, mark it as a HOPO end
          if lastEvent.tappable != -1 and hopoNotes[-1][1] == lastEvent:
            if lastEvent.tappable >= 0:
              lastEvent.tappable = 3
            else:
              lastEvent.tappable = -1






    #note pattern:
      # R R R R R
      # Y       Y
    #should be
      # 1 3-2-2-4
    #first pass:
      #actual: if first RY considered "same note" as next R:
      #-4 0-2-2
       #if last RY considered "same note" as prev R:
      #-4 0-2-2-2
      #actual: if first RY not considered "same note" as next R:
      #-4 0-2-2
    

      #This is the same note as before
      elif noteDelta == 0:
        #Add both notes to bad list even if duplicate.  Will come out in processing
        #myfingershurt: to fix same-note HOPO bug.
        if HoposAfterChords:
          if lastEvent.tappable != -4:   #if the last note was not a chord,
            if eventBeforeLast.tappable == -4 and lastTickDelta <= hopoDelta:  #and if the event before last was a chord, don't remark the last one.
              event.tappable = -5
            else:
              event.tappable = -2
            #myfingershurt: yeah, mark the last one.  
            lastEvent.tappable = -2
        else:
          event.tappable = -2
          lastEvent.tappable = -2







            
      #This is a chord
      #myfingershurt: both this note and the last note are listed at the same time
      #to allow after-chord HOPOs, we need a separate identification for "chord" notes
      #and also might need to track the "last" chord notes in a separate array
      elif tickDelta < self.chordFudge:
        #Add both notes to bad list even if duplicate.  Will come out in processing
        #myfingershurt:
        if HoposAfterChords:
          if eventBeforeLast.tappable == -2 and lastTickDelta <= hopoDelta:
            if eventBeforeEventBeforeLast.tappable >= 0 and tickDeltaBeforeLast <= hopoDelta:
              eventBeforeLast.tappable = -5   #special case that needs to be caught
            if lastEvent.tappable == -2:    #catch case where event before last event was marked as the same note
              if eventBeforeEventBeforeLast.tappable >= 0 and tickDeltaBeforeLast <= hopoDelta:
                eventBeforeLast.tappable = 0
          lastEvent.tappable = -4
          event.tappable = -4
        #keep track of chords as they are found
        else:
          lastEvent.tappable = -1
          event.tappable = -1

        


        
      #myfingershurt: to really check marking, need to track 3 notes into the past. 
      eventBeforeEventBeforeLast = eventBeforeLast
      timeBeforeTimeBeforeLast = timeBeforeLast
      eventBeforeLast = lastEvent
      timeBeforeLast = lastTime
      lastEvent = event
      lastTime = time

    else:
      #Add last note to HOPO list if applicable
      #myfingershurt:
      if noteDelta != 0 and tickDelta > self.chordFudge and tickDelta < hopoDelta and isinstance(event, Note):
        hopoNotes.append([time, bpmEvent])
        hopoNotes.append([time, event])

      #myfingershurt marker: (next - FOR loop)----

    #myfingershurt: comments - updated marking system
    #--at this point, the initial note marking sweep has taken place.  Here is further marking of hopoNotes.
    #the .tappable property has special meanings:
    # -5 = This note is the same as the last note, which was a HOPO, and the next note is a chord.
    #       or, this note is the same as the last note, which was a HOPO, so no matter what it shouldn't be tappable.
    # -4 = This note is part of a chord
    # -3 = This is the very first note in a song
    # -2 = This note is part of a string of "same notes"
    # -1 = This note is too far away from the last note to be tappable.
    #  0 = This note is nowhere near another note and must be strummed (also default value)
    #  1 = This note is the first in a string of HOPOs - this note must be strummed to initiate the HOPOs following it!
    #  2 = This note is in the midst of HOPOs
    #  3 = This note is the final of a string of HOPOs


    firstTime = 1
    note = None

    tickDeltaBeforeTickDeltaBeforeLast = 0    #4 notes in the past
    tickDeltaBeforeLast = 0     #3 notes in the past
    lastTickDelta = 0   #2 notes in the past

    bpmNotes = []
    
    for time, note in list(hopoNotes):
      if isinstance(note, Tempo):
        bpmNotes.append([time, note])
        continue
      if not isinstance(note, Note):
        continue
      while bpmNotes and time >= bpmNotes[0][0]:
        #Adjust to new BPM
        #bpm = bpmNotes[0][1].bpm
        bpmTime, bpmEvent = bpmNotes.pop(0)
        bpm = bpmEvent.bpm

      if firstTime == 1:
        if note.tappable >= 0:
          note.tappable = 1
        lastEvent = note
        lastTime = time
        firstTime = 0
        eventBeforeLast = lastEvent
        eventBeforeEventBeforeLast = eventBeforeLast
        eventBeforeEventBeforeEventBeforeLast = eventBeforeLast
        continue




      #need to recompute (or carry forward) BPM at this time

      tickDeltaBeforeTickDeltaBeforeLast = tickDeltaBeforeLast    #4 notes in the past
      tickDeltaBeforeLast = lastTickDelta     #3 notes in the past
      lastTickDelta = tickDelta   #2 notes in the past


      tick = (time * bpm * ticksPerBeat) / 60000.0
      lastTick = (lastTime * bpm * ticksPerBeat) / 60000.0
      tickDelta = tick - lastTick



      #current Note Invalid for HOPO----------
      if note.tappable < 0:

    #test note pattern:
      # R   R     R R R R
      # Y Y Y Y Y     Y
    #first pass:
      #-4-2-4-2-5-2-2-4 
    #second pass:
      # 1 3 1 3 1 3-2-4 

        #myfingershurt:
        #If current note is beginning of a same note sequence, it's valid for END of HOPO only
        #need to alter this to not screw up single-same-note-before chords:
        #elif lastEvent.tappable == 2 and note.tappable == -2:
        if (lastEvent.tappable == 1 or lastEvent.tappable == 2) and note.tappable == -2:
          note.tappable = 3
        #If current note is invalid for HOPO, and previous note was start of a HOPO section, then previous note not HOPO
        elif lastEvent.tappable == 1:
          lastEvent.tappable = 0


        #and let's not forget the special case when two same-note-sequences on different frets are in sequence:
        elif lastEvent.tappable == -2 and note.tappable == -2 and lastEvent.number != note.number:
          lastEvent.tappable = 1
          note.tappable = 3
        #special case where the new -5 note is followed by a string same notes on a different fret:
        elif lastEvent.tappable == -5 and note.tappable == -2:
          lastEvent.tappable = 1
          note.tappable = 3
        
        #special case where last note was a chord, and this note is counted as the same note as the last in the chord
        elif lastEvent.tappable == -4 and note.tappable == -2:
          thisNoteShouldStillBeAHopo = True
          #determine the highest note in the chord:
          topChordNote = lastEvent.number    
          if eventBeforeLast.number > topChordNote:
            topChordNote = eventBeforeLast.number
          numChordNotes = 2
          #now to determine how many notes were in that chord:
          if tickDeltaBeforeLast < self.chordFudge:  #is there a 3rd note in the same chord?
            if eventBeforeEventBeforeLast.number > topChordNote:
              topChordNote = eventBeforeEventBeforeLast.number
            numChordNotes = 3
            if tickDeltaBeforeTickDeltaBeforeLast < self.chordFudge:  #is there a 4th note in the same chord?
              if eventBeforeEventBeforeEventBeforeLast.number > topChordNote:
                topChordNote = eventBeforeEventBeforeEventBeforeLast.number
              numChordNotes = 4
          if topChordNote == note.number:   #only if the note number matches the top chord note do we outlaw the HOPO.
            thisNoteShouldStillBeAHopo = False
          if thisNoteShouldStillBeAHopo:
            #here, need to go back and mark all notes in this chord as tappable = 1 not just the last one.
            #chord max of 4 frets (5 is just ridiculous) - so if "lastEvent" is the 4th, must go back and change 3rd, 2nd, and 1st
            lastEvent.tappable = 1
            eventBeforeLast.tappable = 1    #at least 2 notes in chord
            if numChordNotes >= 3:  #is there a 3rd note in the same chord?
              eventBeforeEventBeforeLast.tappable = 1
              if numChordNotes == 4:  #is there a 4th note in the same chord?
                eventBeforeEventBeforeEventBeforeLast.tappable = 1
            note.tappable = 3

        #If current note is invalid for HOPO, and previous note was a HOPO section, then previous note is end of HOPO
        elif lastEvent.tappable > 0:
          lastEvent.tappable = 3
      #current note valid
      elif note.tappable >= 0:
        #String of same notes can be followed by HOPO
        if note.tappable == 3:

          #myfingershurt: the new after-chord HOPO special logic needs to also be applied here
          if lastEvent.tappable == -5:  #special case, still can be HOPO start
            lastEvent.tappable = 1
          if lastEvent.tappable == -4:  #chord
            thisNoteShouldStillBeAHopo = True
            #determine the highest note in the chord:
            topChordNote = lastEvent.number    
            if eventBeforeLast.number > topChordNote:
              topChordNote = eventBeforeLast.number
            numChordNotes = 2
            #now to determine how many notes were in that chord:
            if tickDeltaBeforeLast < self.chordFudge:  #is there a 3rd note in the same chord?
              if eventBeforeEventBeforeLast.number > topChordNote:
                topChordNote = eventBeforeEventBeforeLast.number
              numChordNotes = 3
              if tickDeltaBeforeTickDeltaBeforeLast < self.chordFudge:  #is there a 4th note in the same chord?
                if eventBeforeEventBeforeEventBeforeLast.number > topChordNote:
                  topChordNote = eventBeforeEventBeforeEventBeforeLast.number
                numChordNotes = 4
            if topChordNote == note.number:   #only if the note number matches the top chord note do we outlaw the HOPO.
              thisNoteShouldStillBeAHopo = False
            if thisNoteShouldStillBeAHopo:
              #here, need to go back and mark all notes in this chord as tappable = 1 not just the last one.
              #chord max of 4 frets (5 is just ridiculous) - so if "lastEvent" is the 4th, must go back and change 3rd, 2nd, and 1st
              lastEvent.tappable = 1
              eventBeforeLast.tappable = 1    #at least 2 notes in chord
              if numChordNotes >= 3:  #is there a 3rd note in the same chord?
                eventBeforeEventBeforeLast.tappable = 1
                if numChordNotes == 4:  #is there a 4th note in the same chord?
                  eventBeforeEventBeforeEventBeforeLast.tappable = 1
            else:
              note.tappable = -1

          #This is the end of a valid HOPO section
          if lastEvent.tappable == 1 or lastEvent.tappable == 2:
            eventBeforeEventBeforeEventBeforeLast = eventBeforeLast
            #timeBeforeTimeBeforeTimeBeforeLast = timeBeforeLast
            eventBeforeEventBeforeLast = eventBeforeLast
            #timeBeforeTimeBeforeLast = timeBeforeLast
            eventBeforeLast = lastEvent
            #timeBeforeLast = lastTime
            lastEvent = note
            lastTime = time
            continue
          if lastEvent.tappable == -2:
            #If its the same note again it's invalid
            if lastEvent.number == note.number:
              note.tappable = -2
            else:
              lastEvent.tappable = 1
          elif lastEvent.tappable == 0:
            lastEvent.tappable = 1
          #If last note was invalid or end of HOPO section, and current note is end, it is really not HOPO
          elif lastEvent.tappable != 2 and lastEvent.tappable != 1:
            note.tappable = 0
          #If last event was invalid or end of HOPO section, current note is start of HOPO
          else:
            note.tappable = 1
        elif note.tappable == 2:
          if lastEvent.tappable == -2:
            note.tappable = 1
          elif lastEvent.tappable == -1:
            note.tappable = 0
          elif lastEvent.tappable == 3:
            lastEvent.tappable = 2



        elif note.tappable == 1:
          if lastEvent.tappable == 2:
            note.tappable = 0



        #myfingershurt: default case, tappable=0
        else:
          if lastEvent.tappable == -5:  #special case, still can be HOPO start
            lastEvent.tappable = 1
          if lastEvent.tappable == -4:  #chord
            thisNoteShouldStillBeAHopo = True
            #determine the highest note in the chord:
            topChordNote = lastEvent.number    
            if eventBeforeLast.number > topChordNote:
              topChordNote = eventBeforeLast.number
            numChordNotes = 2
            #now to determine how many notes were in that chord:
            if tickDeltaBeforeLast < self.chordFudge:  #is there a 3rd note in the same chord?
              if eventBeforeEventBeforeLast.number > topChordNote:
                topChordNote = eventBeforeEventBeforeLast.number
              numChordNotes = 3
              if tickDeltaBeforeTickDeltaBeforeLast < self.chordFudge:  #is there a 4th note in the same chord?
                if eventBeforeEventBeforeEventBeforeLast.number > topChordNote:
                  topChordNote = eventBeforeEventBeforeEventBeforeLast.number
                numChordNotes = 4
            if topChordNote == note.number:   #only if the note number matches the top chord note do we outlaw the HOPO.
              thisNoteShouldStillBeAHopo = False
            if thisNoteShouldStillBeAHopo:
              #here, need to go back and mark all notes in this chord as tappable = 1 not just the last one.
              #chord max of 4 frets (5 is just ridiculous) - so if "lastEvent" is the 4th, must go back and change 3rd, 2nd, and 1st
              lastEvent.tappable = 1
              eventBeforeLast.tappable = 1    #at least 2 notes in chord
              if numChordNotes >= 3:  #is there a 3rd note in the same chord?
                eventBeforeEventBeforeLast.tappable = 1
                if numChordNotes == 4:  #is there a 4th note in the same chord?
                  eventBeforeEventBeforeEventBeforeLast.tappable = 1
            else:
              note.tappable = -1

          if lastEvent.tappable == -2 and tickDelta <= hopoDelta:  #same note
            lastEvent.tappable = 1
          if lastEvent.tappable == 3 and tickDelta <= hopoDelta:   #supposedly last of a HOPO
            lastEvent.tappable = 2
          
          if lastEvent.tappable != 2 and lastEvent.tappable != 1:
            note.tappable = 1
          else:
            if note.tappable == 1:
              note.tappable = 1
            else:
              note.tappable = 2
      

      #myfingershurt: to really check marking, need to track 4 notes into the past.
      eventBeforeEventBeforeEventBeforeLast = eventBeforeLast
      eventBeforeEventBeforeLast = eventBeforeLast
      eventBeforeLast = lastEvent
      lastEvent = note
      lastTime = time
    else:
      if note != None:
        #Handle last note
        #If it is the start of a HOPO, it's not really a HOPO
        if note.tappable == 1:
          note.tappable = 0
        #If it is the middle of a HOPO, it's really the end of a HOPO
        elif note.tappable == 2:
          #myfingershurt: here, need to check if the last note is a HOPO after chord and is being merged into the chord (which happens if too close to end of song)
          if tickDelta < self.chordFudge:
            note.tappable = -4
          else:
            note.tappable = 3      

    self.marked = True

  def markBars(self):
    tempoTime = []
    tempoBpm = []

    #get all the bpm changes and their times
    for time, event in self.allEvents:
      if isinstance(event, Tempo):
        tempoTime.append(time)
        tempoBpm.append(event.bpm)
        endBpm = event.bpm
        continue
      if isinstance(event, Note):
        endTime = time + event.length + 30000
        continue
    tempoTime.append(endTime)
    tempoBpm.append(endBpm)

    #calculate and add the measures/beats/half-beats
    passes = 0  
    limit = len(tempoTime)
    time = tempoTime[0]
    THnote = 256.0 #256th note
    drawBar = True
    i = 0
    while i < (limit - 1):
      msTotal = tempoTime[i+1] - time
      if msTotal == 0:
        i += 1
        continue
      tempbpm = tempoBpm[i]
      nbars = (msTotal * (tempbpm / (240.0 / THnote) )) / 1000.0 
      inc = msTotal / nbars

      while time < tempoTime[i+1]:
        if drawBar == True:
          if (passes % (THnote / 1.0) == 0.0): #256/1
            event = Bars(2) #measure
            self.addEvent(time, event)
          elif (passes % (THnote / 4.0) == 0.0): #256/4
            event = Bars(1) #beat
            self.addEvent(time, event)
          elif (passes % (THnote / 8.0) == 0.0): #256/8
            event = Bars(0) #half-beat
            self.addEvent(time, event)
          
          passes = passes + 1
          
        time = time + inc
        drawBar = True

      if time > tempoTime[i+1]:
        time = time - inc
        drawBar = False
        
      i += 1

    #add the last measure/beat/half-beat
    if time == tempoTime[i]:
      if (passes % (THnote / 1.0) == 0.0): #256/1
        event = Bars(2) #measure
        self.addEvent(time, event)
      elif (passes % (THnote / 4.0) == 0.0): #256/4
        event = Bars(1) #beat
        self.addEvent(time, event)
      elif (passes % (THnote / 8.0) == 0.0): #256/8
        event = Bars(0) #half-beat
        self.addEvent(time, event)



class Song(object):
  def __init__(self, engine, infoFileName, songTrackName, guitarTrackName, rhythmTrackName, noteFileName, scriptFileName = None, partlist = [parts[GUITAR_PART]], drumTrackName = None):
    self.engine        = engine
    
    Log.debug("Song class init (song.py)...")
    
    self.info         = SongInfo(infoFileName)
    self.tracks       = [[Track(self.engine) for t in range(len(difficulties))] for i in range(len(partlist))]
    self.difficulty   = [difficulties[EXP_DIF] for i in partlist]
    self._playing     = False
    self.start        = 0.0
    self.noteFileName = noteFileName
    
    self.bpm          = None
    
    self.period       = 0
    self.parts        = partlist
    self.delay        = self.engine.config.get("audio", "delay")
    self.delay        += self.info.delay
    self.missVolume   = self.engine.config.get("audio", "miss_volume")

    self.hasMidiLyrics = False

    #MFH - add a separate variable to house the special text event tracks:
    #MFH - special text-event tracks for the separated text-event list variable
    #TK_SCRIPT = 0         #script.txt events
    #TK_SECTIONS = 1       #Section events
    #TK_GUITAR_SOLOS = 2   #Guitar Solo start/stop events
    #TK_LYRICS = 3         #RB MIDI Lyric events
    #TK_UNUSED_TEXT = 4    #Unused / other text events
    self.eventTracks       = [Track(self.engine) for t in range(0,5)]    #MFH - should result in eventTracks[0] through [4]

    # load the tracks
    if songTrackName:
      self.music       = Audio.Music(songTrackName)

    self.guitarTrack = None
    self.rhythmTrack = None
    
    #myfingershurt:
    self.drumTrack = None
    #if songTrackName:
    #  drumTrackName = songTrackName.replace("song.ogg","drums.ogg")

    try:
      if guitarTrackName:
        self.guitarTrack = Audio.StreamingSound(self.engine, self.engine.audio.getChannel(1), guitarTrackName)
    except Exception, e:
      Log.warn("Unable to load guitar track: %s" % e)

    try:
      if rhythmTrackName:
        self.rhythmTrack = Audio.StreamingSound(self.engine, self.engine.audio.getChannel(2), rhythmTrackName)
    except Exception, e:
      Log.warn("Unable to load rhythm track: %s" % e)

    
    try:
      if drumTrackName:
        self.drumTrack = Audio.StreamingSound(self.engine, self.engine.audio.getChannel(3), drumTrackName)
    except Exception, e:
      Log.warn("Unable to load drum track: %s" % e)



    # load the notes   
    if noteFileName:
      Log.debug("Retrieving notes from: " + noteFileName)
      midiIn = midi.MidiInFile(MidiReader(self), noteFileName)
      midiIn.read()
      
    # load the script
    if scriptFileName and os.path.isfile(scriptFileName):
      scriptReader = ScriptReader(self, open(scriptFileName))
      scriptReader.read()

  #myfingershurt: new function to re-retrieve the a/v delay setting so it can be changed in-game:
  def refreshAudioDelay(self):  
    self.delay        = self.engine.config.get("audio", "delay")
    self.delay        += self.info.delay

  #myfingershurt: new function to refresh the miss volume after a pause
  def refreshMissVolume(self):  
    self.missVolume   = self.engine.config.get("audio", "miss_volume")

  

  def getHash(self):
    h = sha.new()
    f = open(self.noteFileName, "rb")
    bs = 1024
    while True:
      data = f.read(bs)
      if not data: break
      h.update(data)
    return h.hexdigest()
  
  def setBpm(self, bpm):
    self.bpm    = bpm
    self.period = 60000.0 / self.bpm

  def save(self):
    self.info.save()
    f = open(self.noteFileName + ".tmp", "wb")
    midiOut = MidiWriter(self, midi.MidiOutFile(f))
    midiOut.write()
    f.close()

    # Rename the output file after it has been succesfully written
    shutil.move(self.noteFileName + ".tmp", self.noteFileName)

  def play(self, start = 0.0):
    self.start = start
    self.music.play(0, start / 1000.0)
    #RF-mod No longer needed?
    self.music.setVolume(1.0)
    if self.guitarTrack:
      assert start == 0.0
      self.guitarTrack.play()
    if self.rhythmTrack:
      assert start == 0.0
      self.rhythmTrack.play()
    #myfingershurt
    if self.drumTrack:
      assert start == 0.0
      self.drumTrack.play()
    self._playing = True

  def pause(self):
    self.music.pause()
    self.engine.audio.pause()

  def unpause(self):
    self.music.unpause()
    self.engine.audio.unpause()

  def setInstrumentVolume(self, volume, part):
    if part == parts[GUITAR_PART]:
      self.setGuitarVolume(volume)
    elif part == parts[BASS_PART]:
      self.setRhythmVolume(volume)
    elif part == parts[RHYTHM_PART]:
      self.setRhythmVolume(volume)
    elif part == parts[DRUM_PART]:
      self.setDrumVolume(volume)
    else:
      self.setRhythmVolume(volume)
      
  def setGuitarVolume(self, volume):
    if self.guitarTrack:
      if volume == 0:
        self.guitarTrack.setVolume(self.missVolume)
      else:
        self.guitarTrack.setVolume(volume)
    #This is only used if there is no guitar.ogg to lower the volume of song.ogg instead of muting this track
    else:
      if volume == 0:
        self.music.setVolume(self.missVolume * 1.5)
      else:
        self.music.setVolume(volume)

  def setRhythmVolume(self, volume):
    if self.rhythmTrack:
      if volume == 0:
        self.rhythmTrack.setVolume(self.missVolume)
      else:
        self.rhythmTrack.setVolume(volume)
  
  def setDrumVolume(self, volume):
    if self.drumTrack:
      if volume == 0:
        self.drumTrack.setVolume(self.missVolume)
      else:
        self.drumTrack.setVolume(volume)

  def setBackgroundVolume(self, volume):
    self.music.setVolume(volume)
  
  def setAllTrackVolumes(self, volume):
    self.setBackgroundVolume(volume)
    self.setDrumVolume(volume)
    self.setRhythmVolume(volume)
    self.setGuitarVolume(volume)
  
  def stop(self):
    for tracks in self.tracks:
      for track in tracks:
        track.reset()
      
    self.music.stop()
    self.music.rewind()
    if self.guitarTrack:
      self.guitarTrack.stop()
    if self.rhythmTrack:
      self.rhythmTrack.stop()
    if self.drumTrack:
      self.drumTrack.stop()
    self._playing = False

  def fadeout(self, time):
    for tracks in self.tracks:
      for track in tracks:
        track.reset()
    
    self.music.fadeout(time)
    if self.guitarTrack:
      self.guitarTrack.fadeout(time)
    if self.rhythmTrack:
      self.rhythmTrack.fadeout(time)
    if self.drumTrack:
      self.drumTrack.fadeout(time)
    self._playing = False

  def getPosition(self):
    if not self._playing:
      pos = 0.0
    else:
      pos = self.music.getPosition()
    if pos < 0.0:
      pos = 0.0
    return pos + self.start - self.delay

  def isPlaying(self):
    return self._playing and self.music.isPlaying()

  def getBeat(self):
    return self.getPosition() / self.period

  def update(self, ticks):
    pass

  def getTrack(self):
    return [self.tracks[i][self.difficulty[i].id] for i in range(len(self.difficulty))]

  track = property(getTrack)

noteMap = {     # difficulty, note
  0x60: (EXP_DIF, 0),
  0x61: (EXP_DIF, 1),
  0x62: (EXP_DIF, 2),
  0x63: (EXP_DIF, 3),
  0x64: (EXP_DIF, 4),
  0x54: (HAR_DIF, 0),
  0x55: (HAR_DIF, 1),
  0x56: (HAR_DIF, 2),
  0x57: (HAR_DIF, 3),
  0x58: (HAR_DIF, 4),
  0x48: (MED_DIF, 0),
  0x49: (MED_DIF, 1),
  0x4a: (MED_DIF, 2),
  0x4b: (MED_DIF, 3),
  0x4c: (MED_DIF, 4),
  0x3c: (EAS_DIF, 0),
  0x3d: (EAS_DIF, 1),
  0x3e: (EAS_DIF, 2),
  0x3f: (EAS_DIF, 3),
  0x40: (EAS_DIF, 4),
}

reverseNoteMap = dict([(v, k) for k, v in noteMap.items()])


class MidiWriter:
  def __init__(self, song, out):
    self.song         = song
    self.out          = out
    self.ticksPerBeat = 480
    Log.debug("MidiWriter class init (song.py)...")
    

  def midiTime(self, time):
    return int(self.song.bpm * self.ticksPerBeat * time / 60000.0)

  def write(self):
    self.out.header(division = self.ticksPerBeat)
    self.out.start_of_track()
    self.out.update_time(0)
    if self.song.bpm:
      self.out.tempo(int(60.0 * 10.0**6 / self.song.bpm))
    else:
      self.out.tempo(int(60.0 * 10.0**6 / 122.0))

    # Collect all events
    events = [zip([difficulty] * len(track.getAllEvents()), track.getAllEvents()) for difficulty, track in enumerate(self.song.tracks[0])]
    events = reduce(lambda a, b: a + b, events)
    events.sort(lambda a, b: {True: 1, False: -1}[a[1][0] > b[1][0]])
    heldNotes = []

    for difficulty, event in events:
      time, event = event
      if isinstance(event, Note):
        time = self.midiTime(time)

        # Turn off any held notes that were active before this point in time
        for note, endTime in list(heldNotes):
          if endTime <= time:
            self.out.update_time(endTime, relative = 0)
            self.out.note_off(0, note)
            heldNotes.remove((note, endTime))

        note = reverseNoteMap[(difficulty, event.number)]
        self.out.update_time(time, relative = 0)
        self.out.note_on(0, note, event.special and 127 or 100)
        heldNotes.append((note, time + self.midiTime(event.length)))
        heldNotes.sort(lambda a, b: {True: 1, False: -1}[a[1] > b[1]])

    # Turn off any remaining notes
    for note, endTime in heldNotes:
      self.out.update_time(endTime, relative = 0)
      self.out.note_off(0, note)
      
    self.out.update_time(0)
    self.out.end_of_track()
    self.out.eof()
    self.out.write()

class ScriptReader:
  def __init__(self, song, scriptFile):
    self.song = song
    self.file = scriptFile
    Log.debug("ScriptReader class init (song.py)...")
    

  def read(self):
    for line in self.file:
      if line.startswith("#") or line.isspace(): continue
      time, length, type, data = re.split("[\t ]+", line.strip(), 3)
      time   = float(time)
      length = float(length)

      if type == "text":
        event = TextEvent(data, length)
      elif type == "pic":
        event = PictureEvent(data, length)
      else:
        continue

      self.song.eventTracks[TK_SCRIPT].addEvent(time, event)  #MFH - add an event to the script.txt track

      #for track in self.song.tracks:
      #  for t in track:
      #    t.addEvent(time, event)

class MidiReader(midi.MidiOutStream):
  def __init__(self, song):
    midi.MidiOutStream.__init__(self)
    self.song = song
    self.heldNotes = {}
    self.velocity  = {}
    self.ticksPerBeat = 480
    self.tempoMarkers = []
    self.partTrack = 0
    self.partnumber = -1
    Log.debug("MidiReader class init (song.py)...")
    
    self.readTextAndLyricEvents = Config.get("game","rock_band_events")
    self.guitarSoloIndex = 0
    self.guitarSoloActive = False
    self.guitarSoloSectionMarkers = False

  def addEvent(self, track, event, time = None):
    if self.partnumber == -1:
      #Looks like notes have started appearing before any part information. Lets assume its part0
      self.partnumber = self.song.parts[0]
    
    if (self.partnumber == None) and isinstance(event, Note):
      return True

    if time is None:
      time = self.abs_time()
    assert time >= 0
    
    if track is None:
      for t in self.song.tracks:
        for s in t:
          s.addEvent(time, event)
    else:
      
      tracklist = [i for i,j in enumerate(self.song.parts) if self.partnumber == j]
      for i in tracklist:
        #Each track needs it's own copy of the event, otherwise they'll interfere
        eventcopy = copy.deepcopy(event)
        if track < len(self.song.tracks[i]):
          self.song.tracks[i][track].addEvent(time, eventcopy)

  def abs_time(self):
    def ticksToBeats(ticks, bpm):
      return (60000.0 * ticks) / (bpm * self.ticksPerBeat)
      
    if self.song.bpm:
      currentTime = midi.MidiOutStream.abs_time(self)

      scaledTime      = 0.0
      tempoMarkerTime = 0.0
      currentBpm      = self.song.bpm
      for i, marker in enumerate(self.tempoMarkers):
        time, bpm = marker
        if time > currentTime:
          break
        scaledTime += ticksToBeats(time - tempoMarkerTime, currentBpm)
        tempoMarkerTime, currentBpm = time, bpm
      return scaledTime + ticksToBeats(currentTime - tempoMarkerTime, currentBpm)
    return 0.0

  def header(self, format, nTracks, division):
    self.ticksPerBeat = division
    if nTracks == 2:
      self.partTrack = 1
    
  def tempo(self, value):
    bpm = 60.0 * 10.0**6 / value
    self.tempoMarkers.append((midi.MidiOutStream.abs_time(self), bpm))
    if not self.song.bpm:
      self.song.setBpm(bpm)
    self.addEvent(None, Tempo(bpm))

  def sequence_name(self, text):
    #if self.get_current_track() == 0:
    self.partnumber = None
      
    if (text == "PART GUITAR" or text == "T1 GEMS" or text == "Click" or text == "MIDI out") and parts[GUITAR_PART] in self.song.parts:
      self.partnumber = parts[GUITAR_PART]
    elif text == "PART RHYTHM" and parts[RHYTHM_PART] in self.song.parts:
      self.partnumber = parts[RHYTHM_PART]
    elif text == "PART BASS" and parts[BASS_PART] in self.song.parts:
      self.partnumber = parts[BASS_PART]
    elif text == "PART GUITAR COOP" and parts[LEAD_PART] in self.song.parts:
      self.partnumber = parts[LEAD_PART]
    elif text == "PART DRUM" and parts[DRUM_PART] in self.song.parts:
      self.partnumber = parts[DRUM_PART]
    #for rock band unaltered rip compatibility
    elif text == "PART DRUMS" and parts[DRUM_PART] in self.song.parts:
      self.partnumber = parts[DRUM_PART]
    elif self.get_current_track() <= 1 and parts [GUITAR_PART] in self.song.parts:
      #Oh dear, the track wasn't recognised, lets just assume it was the guitar part
      self.partnumber = parts[GUITAR_PART]

    self.guitarSoloIndex = 0
    self.guitarSoloActive = False

      
  def note_on(self, channel, note, velocity):
    if self.partnumber == None:
      return
    self.velocity[note] = velocity
    self.heldNotes[(self.get_current_track(), channel, note)] = self.abs_time()

  def note_off(self, channel, note, velocity):
    if self.partnumber == None:
      return
    try:
      startTime = self.heldNotes[(self.get_current_track(), channel, note)]
      endTime   = self.abs_time()
      del self.heldNotes[(self.get_current_track(), channel, note)]
      if note in noteMap:
        track, number = noteMap[note]
        self.addEvent(track, Note(number, endTime - startTime, special = self.velocity[note] == 127), time = startTime)
      else:
        #Log.warn("MIDI note 0x%x at %d does not map to any game note." % (note, self.abs_time()))
        pass
    except KeyError:
      Log.warn("MIDI note 0x%x on channel %d ending at %d was never started." % (note, channel, self.abs_time()))

  
  #MFH - OK - this needs to be optimized.
  #There should be a separate "Sections" track, and a separate "Lyrics" track created for their respective events
  #Then another separate "Text Events" track to put all the unused events, so they don't bog down the game when it looks through / filters / sorts these track event lists
  
  
  #myfingershurt: adding MIDI text event access
  #these events happen on their own track, and are processed after the note tracks.
  #just mark the guitar solo sections ahead of time 
  #and then write an iteration routine to go through whatever track / difficulty is being played in GuitarScene 
  #to find these markers and count the notes and add a new text event containing each solo's note count
  def text(self, text):
    if text.find("GNMIDI") < 0:   #to filter out the midi class illegal usage / trial timeout messages
      #Log.debug(str(self.abs_time()) + "-MIDI Text: " + text)
      if self.readTextAndLyricEvents > 0:
        unusedEvent = None
        event = None
        gSoloEvent = False
        #also convert all underscores to spaces so it look better
        text = text.replace("_"," ")
        if text.lower().find("section") >= 0:
          self.guitarSoloSectionMarkers = True      #GH1 dont use section markers... GH2+ do
          #strip unnecessary text / chars:
          text = text.replace("section","")
          text = text.replace("[","")
          text = text.replace("]","")
          #also convert "gtr" to "Guitar"
          text = text.replace("gtr","Guitar")
          #event = TextEvent("SEC: " + text, 250.0)
          event = TextEvent(text, 250.0)
          if text.lower().find("solo") >= 0 and text.lower().find("drum") < 0 and text.lower().find("outro") < 0 and text.lower().find("organ") < 0 and text.lower().find("synth") < 0 and text.lower().find("bass") < 0 and text.lower().find("harmonica") < 0:
            gSoloEvent = True
            gSolo = True
          elif text.lower().find("guitar") >= 0 and text.lower().find("lead") >= 0:    #Foreplay Long Time "[section_gtr_lead_1]"
            gSoloEvent = True
            gSolo = True
          elif text.lower().find("guitar") >= 0 and text.lower().find("line") >= 0:   #support for REM Orange Crush style solos
            gSoloEvent = True
            gSolo = True
          elif text.lower().find("guitar") >= 0 and text.lower().find("ostinato") >= 0:   #support for Pleasure solos "[section gtr_ostinato]"
            gSoloEvent = True
            gSolo = True
          else: #this is the cue to end solos...
            gSoloEvent = True
            gSolo = False
        elif text.lower().find("solo") >= 0 and text.find("[") < 0 and text.lower().find("drum") < 0 and text.lower().find("map") < 0 and text.lower().find("play") < 0 and not self.guitarSoloSectionMarkers:
          #event = TextEvent("SEC: " + text, 250.0)
          event = TextEvent(text, 250.0)
          gSoloEvent = True
          if text.lower().find("off") >= 0:
            gSolo = False
          else:
            gSolo = True
        elif (text.lower().find("verse") >= 0 or text.lower().find("chorus") >= 0) and text.find("[") < 0 and not self.guitarSoloSectionMarkers:   #this is an alternate GH1-style solo end marker
          #event = TextEvent("SEC: " + text, 250.0)
          event = TextEvent(text, 250.0)
          gSoloEvent = True
          gSolo = False
        elif text.lower().find("gtr") >= 0 and text.lower().find("off") >= 0 and text.find("[") < 0 and not self.guitarSoloSectionMarkers:   #this is an alternate GH1-style solo end marker
          #also convert "gtr" to "Guitar"
          text = text.replace("gtr","Guitar")
          #event = TextEvent("SEC: " + text, 100.0)
          event = TextEvent(text, 100.0)
          gSoloEvent = True
          gSolo = False
        else:  #unused text event
          #unusedEvent = TextEvent("TXT: " + text, 100.0)
          unusedEvent = TextEvent(text, 100.0)
        #now, check for guitar solo status change:
        soloSlop = 150.0   
        if gSoloEvent:
          if gSolo:
            if not self.guitarSoloActive:
              self.guitarSoloActive = True
              #soloEvent = TextEvent("GSOLO" + str(self.guitarSoloIndex) + " ON", 250.0)
              soloEvent = TextEvent("GSOLO ON", 250.0)
              Log.debug("GSOLO ON event " + event.text + " found at time " + str(self.abs_time()) )
              self.song.eventTracks[TK_GUITAR_SOLOS].addEvent(self.abs_time(), soloEvent)  #MFH - add an event to the guitar solos track
              #for track in self.song.tracks:
              #  for t in track:
              #    t.addEvent(self.abs_time()-soloSlop, soloEvent)
              #self.guitarSoloNoteCount = [0,0,0,0]
              #self.guitarSoloStartTime = self.abs_time()
          else: #this is the cue to end solos...
            if self.guitarSoloActive:
              #soloEvent = TextEvent("GSOLO" + str(self.guitarSoloIndex) + " OFF", 250.0)
              #MFH - here, check to make sure we're not ending a guitar solo that has just started!!
              curTime = self.abs_time()
              if self.song.eventTracks[TK_GUITAR_SOLOS][-1][0] < curTime:
                self.guitarSoloActive = False
                soloEvent = TextEvent("GSOLO OFF", 250.0)
                Log.debug("GSOLO OFF event " + event.text + " found at time " + str(curTime) )
                self.guitarSoloIndex += 1
                self.song.eventTracks[TK_GUITAR_SOLOS].addEvent(curTime, soloEvent)  #MFH - add an event to the guitar solos track
                #for track in self.song.tracks:
                #  for t in track:
                #    t.addEvent(self.abs_time()+soloSlop, soloEvent)

    
        if event:
          curTime = self.abs_time()
          if len(self.song.eventTracks[TK_SECTIONS]) <= 1:
            self.song.eventTracks[TK_SECTIONS].addEvent(curTime, event)  #MFH - add an event to the sections track
          elif len(self.song.eventTracks[TK_SECTIONS]) > 1:    #ensure it exists first
            if self.song.eventTracks[TK_SECTIONS][-1][0] < curTime: #ensure we're not adding two consecutive sections to the same location!
              self.song.eventTracks[TK_SECTIONS].addEvent(curTime, event)  #MFH - add an event to the sections track
        elif unusedEvent:
          self.song.eventTracks[TK_UNUSED_TEXT].addEvent(self.abs_time(), unusedEvent)  #MFH - add an event to the unused text track
        
        #for track in self.song.tracks:
        #  for t in track:
        #    t.addEvent(self.abs_time(), event)

        


  #myfingershurt: adding MIDI lyric event access
  def lyric(self, text):
    if text.find("GNMIDI") < 0:   #to filter out the midi class illegal usage / trial timeout messages
      #Log.debug(str(self.abs_time()) + "-MIDI Lyric: " + text)
      if self.readTextAndLyricEvents > 0:
        #event = TextEvent("LYR: " + text, 400.0)
        event = TextEvent(text, 400.0)
        self.song.hasMidiLyrics = True
        self.song.eventTracks[TK_LYRICS].addEvent(self.abs_time(), event)  #MFH - add an event to the lyrics track
        #for track in self.song.tracks:
        #  for t in track:
        #    t.addEvent(self.abs_time(), event)

  
  
class MidiInfoReaderNoSections(midi.MidiOutStream):
  # We exit via this exception so that we don't need to read the whole file in
  class Done: pass
  
  def __init__(self):
    midi.MidiOutStream.__init__(self)
    self.difficulties = []
    Log.debug("MidiInfoReaderNoSections class init (song.py)...")

    #MFH: practice section support:
    self.ticksPerBeat = 480
    self.sections = []
    self.tempoMarkers = []
    self.guitarSoloSectionMarkers = False
    self.bpm = None

  def note_on(self, channel, note, velocity):
    try:
      track, number = noteMap[note]
      diff = difficulties[track]
      if not diff in self.difficulties:
        self.difficulties.append(diff)
        #ASSUMES ALL parts (lead, rhythm, bass) have same difficulties of guitar part!
        if len(self.difficulties) == len(difficulties):
           raise Done
    except KeyError:
      pass




class MidiInfoReader(midi.MidiOutStream):
  # We exit via this exception so that we don't need to read the whole file in
  class Done: pass
  
  def __init__(self):
    midi.MidiOutStream.__init__(self)
    self.difficulties = []
    Log.debug("MidiInfoReader class init (song.py)...")

    #MFH: practice section support:
    self.ticksPerBeat = 480
    self.sections = []
    self.tempoMarkers = []
    self.guitarSoloSectionMarkers = False
    self.bpm = None

    self.noteCountSections = []
    self.nextSectionMinute = 0.25
    

  def note_on(self, channel, note, velocity):
    pos = midi.MidiOutStream.abs_time(self)
    if (pos / 60000) >= self.nextSectionMinute:
      text = "%d:%02d -> " % (pos / 60000, (pos % 60000) / 1000) + "Section " + str(round(self.nextSectionMinute,2))
      self.nextSectionMinute += 0.25
      Log.debug("Found default practice section: " + str(pos) + " - " + text)
      self.noteCountSections.append([text,pos])

    try:
      track, number = noteMap[note]
      diff = difficulties[track]
      if not diff in self.difficulties:
        self.difficulties.append(diff)
    except KeyError:
      pass

  def lyric(self, text):  #filter lyric events
    if text.find("GNMIDI") < 0:   #to filter out the midi class illegal usage / trial timeout messages
      #Log.debug(str(self.abs_time()) + "-MIDI Lyric: " + text)
      text = ""

  #MFH - adding text event / section retrieval here 
  #also must prevent "Done" flag setting so can read whole MIDI file, all text events
  def text(self, text):
    if text.find("GNMIDI") < 0:   #to filter out the midi class illegal usage / trial timeout messages
      pos = midi.MidiOutStream.abs_time(self)
      #Log.debug("Found MidiInfoReader text event: " + text)
      #if self.readTextAndLyricEvents > 0:
      text = text.replace("_"," ")
      if text.lower().find("section") >= 0:
        if not self.guitarSoloSectionMarkers:
          self.guitarSoloSectionMarkers = True      #GH1 dont use section markers... GH2+ do
          self.sections = []  #reset sections
        #strip unnecessary text / chars:
        text = text.replace("section","")
        text = text.replace("[","")
        text = text.replace("]","")
        #also convert "gtr" to "Guitar"
        text = text.replace("gtr","Guitar")
        Log.debug("Found practice section: " + str(pos) + " - " + text)

        text = "%d:%02d -> " % (pos / 60000, (pos % 60000) / 1000) + text
        self.sections.append([text,pos])
        
        
      elif text.lower().find("solo") >= 0 and text.find("[") < 0 and text.lower().find("drum") < 0 and text.lower().find("map") < 0 and text.lower().find("play") < 0 and not self.guitarSoloSectionMarkers:
        Log.debug("Found practice section: " + str(pos) + " - " + text)
        text = "%d:%02d -> " % (pos / 60000, (pos % 60000) / 1000) + text
        self.sections.append([text,pos])
      elif text.lower().find("verse") >= 0 and text.find("[") < 0 and not self.guitarSoloSectionMarkers:   #this is an alternate GH1-style solo end marker
        Log.debug("Found practice section: " + str(pos) + " - " + text)
        text = "%d:%02d -> " % (pos / 60000, (pos % 60000) / 1000) + text
        self.sections.append([text,pos])
      elif text.lower().find("gtr") >= 0 and text.lower().find("off") >= 0 and text.find("[") < 0 and not self.guitarSoloSectionMarkers:   #this is an alternate GH1-style solo end marker
        #also convert "gtr" to "Guitar"
        text = text.replace("gtr","Guitar")
        Log.debug("Found practice section: " + str(pos) + " - " + text)
        text = "%d:%02d -> " % (pos / 60000, (pos % 60000) / 1000) + text
        self.sections.append([text,pos])
      elif not self.guitarSoloSectionMarkers:   #General GH1-style sections.  Messy but effective.
        Log.debug("Found practice section: " + str(pos) + " - " + text)
        text = "%d:%02d -> " % (pos / 60000, (pos % 60000) / 1000) + text
        self.sections.append([text,pos])
        
      else:  #unused text event
        text = ""





class SongQueue:
  def __init__(self):
    self.songName = []
    self.library = []
    self.players = []
    self.difficulty1 = []
    self.difficulty2 = []
    self.part1 = []
    self.part2 = []     
    Log.debug("SongQueue class init (song.py)...")
        
  def addSong(self, songName, library, players, difficulty1, difficulty2, part1, part2):
    self.songName.append(songName)
    self.library.append(library)
    self.players.append(players)
    self.difficulty1.append(difficulty1)
    self.difficulty2.append(difficulty2)
    self.part1.append(part1)
    self.part2.append(part2)
  
  def nextSong(self, counter): #should be called getSong now, but don't know how to refactor in python
    nextSong = [self.songName[counter], self.library[counter], self.players[counter], 
                self.difficulty1[counter], self.difficulty2[counter], 
                self.part1[counter], self.part2[counter]]
    return nextSong
  
  def load(self, engine, loadfile):        
    path = os.path.abspath(engine.resource.loadfile("queues", loadame))
    self = pickle.load("%s%s" %path %loadfile)
  
  def save(self, engine, fileName):
    if not fileName:
        return False
    path = os.path.abspath(engine.resource.fileName("queues", fileName))
    if os.path.isdir(path):
        return False
    savefile = open(("%(p)s%(f)s.que") % {"p" : path, "f": fileName}, "w")
    pickle.dump(self, savefile)
    savefile.close
    return True
  
  def reset(self):
    self.songName = []
    self.library = []
    self.players = []
    self.difficulty1 = []
    self.difficulty2 = []
    self.part1 = []
    self.part2 = [] 



class MidiPartsReader(midi.MidiOutStream):
  # We exit via this exception so that we don't need to read the whole file in
  class Done: pass
  
  def __init__(self):
    midi.MidiOutStream.__init__(self)
    self.parts = []
    Log.debug("MidiPartsReader class init (song.py)...")
    
  def sequence_name(self, text):

    if text == "PART GUITAR" or text == "T1 GEMS" or text == "Click":
      if not parts[GUITAR_PART] in self.parts:
        part = parts[GUITAR_PART]
        self.parts.append(part)

    if text == "PART RHYTHM":
      if not parts[RHYTHM_PART] in self.parts:
        part = parts[RHYTHM_PART]
        self.parts.append(part)        
     
    if text == "PART BASS":
      if not parts[BASS_PART] in self.parts:
        part = parts[BASS_PART]
        self.parts.append(part)

    if text == "PART GUITAR COOP":
      if not parts[LEAD_PART] in self.parts:
        part = parts[LEAD_PART]
        self.parts.append(part)

    #myfingershurt: drums, rock band rip compatible :)
    if text == "PART DRUM" or text == "PART DRUMS":
      if not parts[DRUM_PART] in self.parts:
        part = parts[DRUM_PART]
        self.parts.append(part)


def loadSong(engine, name, library = DEFAULT_LIBRARY, seekable = False, playbackOnly = False, notesOnly = False, part = [parts[GUITAR_PART]], practiceMode = False):

  Log.debug("loadSong function call (song.py)...")


  #RF-mod (not needed?)
  guitarFile = engine.resource.fileName(library, name, "guitar.ogg")
  songFile   = engine.resource.fileName(library, name, "song.ogg")
  rhythmFile = engine.resource.fileName(library, name, "rhythm.ogg")
  noteFile   = engine.resource.fileName(library, name, "notes.mid", writable = True)
  infoFile   = engine.resource.fileName(library, name, "song.ini", writable = True)
  scriptFile = engine.resource.fileName(library, name, "script.txt")
  previewFile = engine.resource.fileName(library, name, "preview.ogg")
  #myfingershurt:
  drumFile = engine.resource.fileName(library, name, "drums.ogg")


  if seekable:
    if os.path.isfile(guitarFile) and os.path.isfile(songFile):
      # TODO: perform mixing here
      songFile   = guitarFile
      guitarFile = None
      rhythmFile = ""
    else:
      songFile   = guitarFile
      guitarFile = None
      rhythmFile = ""
      
  if not os.path.isfile(songFile):
    songFile   = guitarFile
    guitarFile = None
  
  if not os.path.isfile(rhythmFile):
    rhythmFile = None
    #if os.path.isfile(alternteRhythmFile):    #support for bass.ogg
      #rhythmFile = alternateRhythmFile

  if not os.path.isfile(drumFile):
    drumFile = None
 

  if practiceMode:    #single track practice mode only!
    if part[0] == parts[GUITAR_PART] and guitarFile != None:
      songFile = guitarFile
    elif part[0] == parts[BASS_PART] and rhythmFile != None:
      songFile = rhythmFile
    elif part[0] == parts[DRUM_PART] and drumFile != None:
      songFile = drumFile
    guitarFile = None
    rhythmFile = None
    drumFile = None      
    
      



  if playbackOnly:
    noteFile = None
    if os.path.isfile(previewFile):
      songFile = previewFile
      guitarFile = None
      rhythmFile = None
      drumFile = None
      
  if notesOnly:
    songFile = None
    guitarFile = None
    rhythmFile = None
    previewFile = None
    drumFile = None

  if songFile != None and guitarFile != None:
    #check for the same file
    songStat = os.stat(songFile)
    guitarStat = os.stat(guitarFile)
    #Simply checking file size, no md5
    if songStat.st_size == guitarStat.st_size:
      guitarFile = None
  
  song       = Song(engine, infoFile, songFile, guitarFile, rhythmFile, noteFile, scriptFile, part, drumFile)
  return song

def loadSongInfo(engine, name, library = DEFAULT_LIBRARY):
  #RF-mod (not needed?)
  infoFile   = engine.resource.fileName(library, name, "song.ini", writable = True)
  return SongInfo(infoFile)
  
def createSong(engine, name, guitarTrackName, backgroundTrackName, rhythmTrackName = None, library = DEFAULT_LIBRARY):
  #RF-mod (not needed?)
  path = os.path.abspath(engine.resource.fileName(library, name, writable = True))
  os.makedirs(path)
  
  guitarFile = engine.resource.fileName(library, name, "guitar.ogg", writable = True)
  songFile   = engine.resource.fileName(library, name, "song.ogg",   writable = True)
  noteFile   = engine.resource.fileName(library, name, "notes.mid",  writable = True)
  infoFile   = engine.resource.fileName(library, name, "song.ini",   writable = True)
  
  shutil.copy(guitarTrackName, guitarFile)
  
  if backgroundTrackName:
    shutil.copy(backgroundTrackName, songFile)
  else:
    songFile   = guitarFile
    guitarFile = None

  if rhythmTrackName:
    rhythmFile = engine.resource.fileName(library, name, "rhythm.ogg", writable = True)
    shutil.copy(rhythmTrackName, rhythmFile)
  else:
    rhythmFile = None
    
  f = open(noteFile, "wb")
  m = midi.MidiOutFile(f)
  m.header()
  m.start_of_track()
  m.update_time(0)
  m.end_of_track()
  m.eof()
  m.write()
  f.close()

  song = Song(engine, infoFile, songFile, guitarFile, rhythmFile, noteFile)
  song.info.name = name
  song.save()
  
  return song

def getDefaultLibrary(engine):
  return LibraryInfo(DEFAULT_LIBRARY, engine.resource.fileName(DEFAULT_LIBRARY, "library.ini"))

def getAvailableLibraries(engine, library = DEFAULT_LIBRARY):
  Log.debug("Song.getAvailableLibraries function call...library = " + str(library) )
  # Search for libraries in both the read-write and read-only directories
  songRoots    = [engine.resource.fileName(library),
                  engine.resource.fileName(library, writable = True)]
  libraries    = []
  libraryRoots = []

  for songRoot in set(songRoots):
    if (os.path.exists(songRoot) == False):
      return libraries
    for libraryRoot in os.listdir(songRoot):
      libraryRoot = os.path.join(songRoot, libraryRoot)
      if not os.path.isdir(libraryRoot):
        continue
      if os.path.isfile(os.path.join(libraryRoot, "notes.mid")):
        continue
      libName = library + os.path.join(libraryRoot.replace(songRoot, ""))
      
      libraries.append(LibraryInfo(libName, os.path.join(libraryRoot, "library.ini")))
      #Log.debug("Library added: " + str(libraries) )
      continue # why were these here? we must filter out empty libraries - coolguy567
                #MFH - I'll tell you why -- so that empty ("tiered" / organizational) folders are displayed, granting access to songs in subfolders...
      
      dirs = os.listdir(libraryRoot)
      for name in dirs:
        if os.path.isfile(os.path.join(libraryRoot, name, "song.ini")):
          if not libraryRoot in libraryRoots:
            libName = library + os.path.join(libraryRoot.replace(songRoot, ""))
            libraries.append(LibraryInfo(libName, os.path.join(libraryRoot, "library.ini")))
            #Log.debug("Library added: " + str(libraries) )
            libraryRoots.append(libraryRoot)

  libraries.sort(lambda a, b: cmp(a.name.lower(), b.name.lower()))
  return libraries

def getAvailableSongs(engine, library = DEFAULT_LIBRARY, includeTutorials = False):
  order = engine.config.get("game", "sort_order")
  tut = engine.config.get("game", "tut")
  
  if tut:
    includeTutorials = True

  #MFH - Career Mode determination:
  gameMode1p = engine.config.get("player0","mode_1p")
  if gameMode1p == 2:
    careerMode = True
  else:
    careerMode = False

  # Search for songs in both the read-write and read-only directories
  if library == None:
    return []
  songRoots = [engine.resource.fileName(library), engine.resource.fileName(library, writable = True)]
  names = []
  for songRoot in songRoots:
    if (os.path.exists(songRoot) == False):
      return []
    for name in os.listdir(songRoot):
      if not os.path.isfile(os.path.join(songRoot, name, "notes.mid")):
        continue
      if not os.path.isfile(os.path.join(songRoot, name, "song.ini")) or name.startswith("."):
      #if not os.path.isfile(os.path.join(songRoot, name, "song.ini")):
        continue
      if not name in names:
        names.append(name)

  songs = [SongInfo(engine.resource.fileName(library, name, "song.ini", writable = True)) for name in names]
  if not includeTutorials:
    songs = [song for song in songs if not song.tutorial]
  songs = [song for song in songs if not song.artist == '=FOLDER=']

  #coolguy567's unlock system
  if careerMode:
    for song in songs:
      if song.getUnlockRequire() != "":
        song.setLocked(False)
        for song2 in songs:
          if song.getUnlockRequire() == song2.getUnlockID() and not song2.completed:
            song.setLocked(True)
      else:
        song.setLocked(False)


  if order == 1:
    songs.sort(lambda a, b: cmp(a.artist.lower(), b.artist.lower()))
  elif order == 2:
    songs.sort(lambda a, b: cmp(int(b.count+str(0)), int(a.count+str(0))))
  else:
    songs.sort(lambda a, b: cmp(a.name.lower(), b.name.lower()))
  return songs


  #coolguy567's unlock system
def getAvailableTitles(engine, library = DEFAULT_LIBRARY):
  if library == None:
    return []
  
  path = os.path.join(engine.resource.fileName(library, writable = True), "titles.ini")
  if not os.path.isfile(path):
    return []
  
  config = Config.MyConfigParser()
  titles = []
  try:
    config.read(path)
    sections = config.get("titles", "sections")
    
    for section in sections.split():
      titles.append(TitleInfo(config, section))
    
    titles.append(BlankSpaceInfo(_("End of Career")))
    
  except:
    Log.debug("titles.ini could not be read (song.py)")
    return []
  
  return titles
  
def getAvailableSongsAndTitles(engine, library = DEFAULT_LIBRARY, includeTutorials = False):
  if library == None:
    return []

  #MFH - Career Mode determination:
  gameMode1p = engine.config.get("player0","mode_1p")
  if gameMode1p == 2:
    careerMode = True
    quickPlayMode = False
  else:
    careerMode = False
    if gameMode1p == 0:
      quickPlayMode = True
    else:
      quickPlayMode = False
      
  quickPlayCareerTiers = engine.config.get("game", "quickplay_career_tiers")
  if quickPlayMode and not quickPlayCareerTiers:
    titles = []
  else:
    titles = getAvailableTitles(engine, library)

  items = getAvailableSongs(engine, library, includeTutorials) + titles
  items.sort(lambda a, b: compareSongsAndTitles(engine, a, b))

  if careerMode and titles != []:
    items.append(BlankSpaceInfo())
    items.append(CareerResetterInfo())
  return items
  
def compareSongsAndTitles(engine, a, b):

  #MFH - want to push all non-career songs in a folder below all titles and career songs
  
  #When an unlock_id does not exist in song.ini, a blank string "" value is returned.
  #Can check for this to determine that this song should be below any titles or non-None unlock_id's

  #>>> def numeric_compare(x, y):
  #>>>    if x>y:
  #>>>       return 1
  #>>>    elif x==y:
  #>>>       return 0
  #>>>    else: # x<y
  #>>>       return -1

  #MFH - Career Mode determination:
  gameMode1p = engine.config.get("player0","mode_1p")
  if gameMode1p == 2:
    careerMode = True
    quickPlayMode = False
  else:
    careerMode = False
    if gameMode1p == 0:
      quickPlayMode = True
    else:
      quickPlayMode = False
      
  quickPlayCareerTiers = engine.config.get("game", "quickplay_career_tiers")
  if quickPlayMode and not quickPlayCareerTiers:
    order = engine.config.get("game", "sort_order")
    if order == 1:
      return cmp(a.artist.lower(), b.artist.lower())
    elif order == 2:
      return cmp(int(b.count+str(0)), int(a.count+str(0)))
    else:
      return cmp(a.name.lower(), b.name.lower())
  else:
    #Log.debug("Unlock IDs found, a=" + str(a.getUnlockID()) + ", b=" + str(b.getUnlockID()) )
    if a.getUnlockID() == "" and b.getUnlockID() != "":   #MFH - a is a bonus song, b is involved in career mode
      return 1
    elif b.getUnlockID() == "" and a.getUnlockID() != "":   #MFH - b is a bonus song, a is involved in career mode - this is fine.
      return -1
    elif a.getUnlockID() == "" and b.getUnlockID() == "":   #MFH - a and b are both bonus songs; apply sorting logic.
      #MFH: catch BlankSpaceInfo ("end of career") marker, ensure it goes to the top of the bonus songlist
      if isinstance(a, SongInfo) and isinstance(b, BlankSpaceInfo):   #a is a bonus song, b is a blank space (end of career marker)
        return 1
      elif isinstance(a, BlankSpaceInfo) and isinstance(b, SongInfo):   #a is a blank space, b is a bonus song (end of career marker) - this is fine.
        return -1
      else: #both bonus songs, apply sort order:
        order = engine.config.get("game", "sort_order")
        if order == 1:
          return cmp(a.artist.lower(), b.artist.lower())
        elif order == 2:
          return cmp(int(b.count+str(0)), int(a.count+str(0)))
        else:
          return cmp(a.name.lower(), b.name.lower())
    #original career sorting logic:
    elif a.getUnlockID() != b.getUnlockID():    #MFH - if returned unlock IDs are different, sort by unlock ID (this roughly sorts the tiers and shoves "bonus" songs to the top)
      return cmp(a.getUnlockID(), b.getUnlockID())
    elif isinstance(a, TitleInfo) and isinstance(b, TitleInfo):
      return 0
    elif isinstance(a, TitleInfo) and isinstance(b, SongInfo):
      return -1
    elif isinstance(a, SongInfo) and isinstance(b, TitleInfo):
      return 1
    else:   #MFH - This is where career songs are sorted within tiers -- we want to force sorting by "name" only:
      return cmp(a.name.lower(), b.name.lower())    #MFH - force sort by name for career songs
