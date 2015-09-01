song.ini is a text file in the format used by Python's [ConfigParser](http://docs.python.org/library/configparser.html) module.  Only the `[song]` section is meaningful; all of the listed values go into the `[song]` section.

For maximum compatibility between any programs that might have to deal with it, it is strongly recommended that the following constraints be observed when creating song.ini files:

  * Do not provide any other sections than `[song]`.
  * Make sure the `[song]` line is the first line in the file.
  * Do not use comments.
  * Use the equals sign syntax, not the colon syntax, to separate the key from the value.
  * Leave a space on either side of the equals sign.
  * Do not use the `%(...)s` (or similar) substitution syntax.
  * Avoid leaving blank lines or trailing whitespace.

We are aware of programs that deal with song.ini files using Python's `ConfigParser` module, GLib's `g_key_file_...()` functions, and home-grown parsers.  Obeying the suggestions above should keep all of these programs happy.

## Defined values in the song.ini file ##

FoFiX does not utilize all officially defined values.  Some are defined to standardize their use by added features of other programs that deal with FoFiX-format songs; the goal is maximum compatibility between different programs and avoidance of using the same value for radically different things.

### Values used by FoFiX ###

|_**song.ini value**_|_**Description**_|
|:-------------------|:----------------|
|artist = .38 Special|Indicates that the artist is ".38 Special"|
|icon = rb2          |Sets icon to use for song title. (Examples- rb1,rb2,rbdlc,rbtpk,gh1,gh2,gh2dlc,gh3,gh3dlc,gh80s,gha,ghm,ph1,ph2,ph3,ph4,phm)|
|name = Hold On Loosely|Indicates that the song name is "Hold On Loosely"|
|tags = cover        |Indicates that is not an original master. So it will show "As Made famous by" instead of "As performed by" at the beginning of the song.|
|diff\_guitar = (0-6)|Set the Difficulty for Guitar. (Rock Band 2 Setlists)|
|diff\_drums = (0-6) |Set the Difficulty for Drums. (Rock Band 2 Setlists)|
|diff\_bass = (0-6)  |Set the Difficulty for Bass. (Rock Band 2 Setlists)|
|diff\_band = (0-6)  |Set the Difficulty for full Band. (Rock Band 2 Setlists)|
|unlock\_id = gh80\_3|For career mode, indicates the Tier it belongs to.|
|unlock\_require = gh80\_2enc|For career mode, indicates the unlock\_id of the songs you have to complete to be able to play this song.|
|unlock\_text = Finish Tier 2 Encore To Unlock|This is a text that is displayed when the song is locked and you try to select it.|
|cassettecolor = #000000|Chooses the color of the cassette/CD|
|count = 1           |How many times played|
|scores =            |Encoded HighScores|
|scores\_ext =       |Also Encoded, contains other score info (longest note streak, etc)|
|tutorial =          |0 or 1 -- it tells the game not to display the song in the Set list if set to 1.  Also enables translation of the script.txt phrases (really, this is only for the Jurgen FoF tutorial -- and possibly other tutorials if they are made with script.txt)|
|delay =             |This setting adds some delay (in milliseconds, just like your A/V delay) so that the notes appear later.|
|frets =             |Name of the maker/converter of the song.|
|version =           |Show the version of the song.|
|year =              |Year in which the song has been published/made. Place at the end of the list.|
|genre =             |Specify the genre of music.|
|loading\_phrase =   |Should be put at the end of the file; displays a custom phrase (maybe more than 1, if separated by "_", but I haven't tested) on the loading screen, instead of the selected theme's default ones._|
|hopofreq =          |HOPO Frequency setting, since [r487](https://code.google.com/p/fofix/source/detail?r=487) this has 6 settings (0="Least", 1="Less", 2="Normal", 3="More", 4="Even More", 5="Most").  Detail on how old HOPO Frequency settings translate into this new list can be found in [issue 170](https://code.google.com/p/fofix/issues/detail?id=170).  Requires the user setting "Song HOPO Freq" be set to "Auto."|
|video = default.avi |Video file relative to song folder (any format supported by GStreamer can be used)|
|video\_start\_time = 0|Video start time in milliseconds.|
|video\_end\_time = -1|Video end time in milliseconds (**NOT** relative to specified video start time)|

### Values defined but _not implemented_ by FoFiX ###

FoFiX _does not do anything_ with these values, but other programs might use them.  If FoFiX implements the appropriate features in the future, it will use any appropriate values from here as-is, and the entry will be moved to the preceding table.

|_**song.ini value**_|_**Type**_|_**Known Users**_|_**Description**_|
|:-------------------|:---------|:----------------|:----------------|
|preview\_start\_time = |integer (milliseconds)|[Performous](http://performous.org/)|Time offset at which the song preview starts.|
|cover =             |string    |[Performous](http://performous.org/)|Filename of cover image _(note: FoFiX's behavior is to use the appropriate one of album.png and label.png for the setlist mode in use)_|
|background =        |string    |[Performous](http://performous.org/)|Filename of image to display in the background during gameplay|

If you would like to have us officially define a value for your program, we'll be more than happy to if it makes sense.  Hop into our IRC channel ([#fofix on OFTC](irc://irc.oftc.net/fofix)) and give your proposal to stump or akedrou.