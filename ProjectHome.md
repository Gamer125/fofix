![http://imgur.com/XHlSl.png](http://imgur.com/XHlSl.png)<br>
(Frets on Fire X)<br>
<br>
<a href='Hidden comment: 
_Love FoFiX? Want to make a difference? Support your freeware developers today!_
[http://code.google.com/p/fofix/wiki/Donations http://i35.tinypic.com/2zsmwk2.jpg]
'></a><br>
<br>
<h3>The latest source code is <a href='https://github.com/fofix/fofix'>on GitHub</a>.</h3>

<h3>Downloads of the latest stable version (3.121) are in the sidebar and <a href='http://code.google.com/p/fofix/downloads/list'>on the Downloads tab</a>.</h3>

<h3>Downloads of the latest unstable version (4.0.0 alpha 1) are <a href='http://code.google.com/p/fofix/downloads/list'>on the Downloads tab</a>.</h3>

<h3>Visit our IRC channel: <code>#fofix</code> on OFTC (<a href='http://chat.mibbit.com/#fofix@OFTC'>web interface</a>)</h3>

<hr />

<h2>News</h2>
<h4>November 27, 2010</h4>
<b>Version 4.0.0 alpha 1 released</b>

The first alpha of what will eventually become FoFiX 4.0.0 has been released. There is a lot of work still remaining to be done, but this alpha will let you preview and check out what has been done so far.<br>
<br>
The main new things are the MegaLight v4 theme, Theora video playback, the beginning of a faster OpenGL binding, and improved theme customizability (including a new custom rockmeter mechanism and the return of the original FoF's stage.ini).<br>
<br>
Download: <a href='http://code.google.com/p/fofix/downloads/detail?name=fofix-4.0.0alpha1.tar.bz2&can=2&q='>source code</a> or <a href='http://code.google.com/p/fofix/downloads/detail?name=fofix-4.0.0alpha1-win32.7z&can=2&q='>Windows binary</a>

Have fun, and don't forget to <a href='http://chat.mibbit.com/#fofix@OFTC'>stop by our IRC channel</a> (<code>#fofix</code> on OFTC) to give us your thoughts, questions, and comments or otherwise have a friendly chat with us about FoFiX.<br>
<br>
--stump<br>
<br>
<hr />
<h4>September 17, 2010</h4>
<b>Development progress update</b>

While just from looking at this page it may look like not much has been going on, a lot has been.  Here are some things that probably should have had news items written about them when they happened:<br>
<br>
<ul><li>We switched from Subversion to Git.  The Git repository is hosted <a href='http://github.com/stump/fofix'>on GitHub</a>.<br>
</li><li>We opened up our project IRC channel, <code>#fofix</code> on OFTC.  Hanging out there is a good idea if you're interested in following FoFiX's continued development or if you think you might want to contribute.  (You can also access the channel <a href='http://chat.mibbit.com/#fofix@OFTC'>via Mibbit, right in your browser</a>.)<br>
</li><li>We cut support for Python 2.4.  We will no longer be held back from taking advantage of newer Python features that can improve the code by having to maintain compatibility with 2.4.<br>
</li><li>We merged a development branch (cmgl) that greatly speeds up rendering.  It uses native code, so some compilation is now necessary to run from source.  We're likely to move more things to native code in the future, so expect the build system to become much more fleshed out (and FoFiX to get faster) as this is done.<br>
</li><li>We have two new developers: weirdpeople and fuzion.</li></ul>

The release of 4.0 is still quite a long way away; we probably won't even hit beta in the near future.  But once we do a little bit more, we might make an alpha for preview purposes.<br>
<br>
If you really want to see what's going on, you can <a href='http://github.com/stump/fofix/blob/master/doc/RunningFromSource.mkd#readme'>set yourself up to run the latest code from Git</a>, but be aware that it's likely to be a bit unstable.<br>
<br>
<hr />

<h4>December 6, 2009</h4>
<b>Update for v3.120 - we're calling it v3.121!</b>
(FoFiX v3.121 Final: <a href='https://code.google.com/p/fofix/source/detail?r=1988'>r1988</a>)<br>
<br>
While development on the 4.0 side of things is going strong, we decided that the speed increases we've come across were worth bringing back to the 3.x line as well. With that in mind, here's v3.121! v3.121 will give you increased performance and a more precise and helpful error logging system. (Trust us, this is good.)<br>
<br>
Download links are (as always) right here on the front page - check the <b>Featured Downloads</b> sidebar to your right, or click the Downloads tab up top for more options.<br>
<br>
Windows and GNU/Linux downloads are available now - Mac downloads will follow shortly!<br>
<br>
<b>Python 2.4 Users</b>: Make sure you try the Python 2.6 version! We're planning to cut support for Python 2.4 soon, so you'll want to make sure everything works right before then! This version should help take care of a good number of the speed issues we've had. To those of you who are running Python 2.4 from sources, you should also get around to updating your setup to run FoFiX from Python 2.6.<br>
<br>
GNU/Linux players: Download the source archive and follow the instructions on our <a href='RunningUnderGNULinux.md'>RunningUnderGNULinux</a> wiki page.<br>
<br>
-akedrou<br>
<br>
<h4>Older news can be found in the <a href='OldNews.md'>OldNews</a> wiki page</h4>

<hr />

<h2>About</h2>
A multi-OS rhythm game, written in Python, similar to Guitar Hero or Rock Band.  Play guitar, bass or drums along with your favorite songs on your computer using either your keyboard or instruments.  You can use your Guitar Hero or Rock Band instrument controllers.<br>
<br>
Separated audio tracks will mute when you fail to hit or sustain the required notes correctly to simulate a real concert-playing experience.<br>
<br>
<h3>Simplified list of features</h3>
<ul><li>Completely Customizable Graphics (standard .PNG format)<br>
</li><li>Completely Customizable Sound Effects & Menu Music (standard .OGG format)<br>
</li><li>Completely Customizable Fretboard Point Of View (POV)<br>
</li><li>Completely Customizable Menus and Layouts<br>
</li><li>2D or 3D Notes & Frets<br>
</li><li>3D Note Texturing<br>
</li><li>Unlimited Themes<br>
</li><li>Unlimited Necks<br>
</li><li>Graphical Neck Selection<br>
</li><li>Up to 4 players in a variety of different multiplayer game modes<br>
</li><li>Random Stages, Stage Rotation (slideshow) and basic Animated Stages<br>
</li><li>Support for separated song, guitar, bass and drum audio tracks<br>
</li><li>Guitar playable & separated track support<br>
</li><li>Lead Guitar & Rhythm Guitar playable track support<br>
</li><li>Bass Guitar playable & separated track support<br>
</li><li>Bass Groove 5x, 6x, 10x, and 12x multiplier support<br>
</li><li>Playable Drums and Vocals!<br>
</li><li>Starpower/Overdrive<br>
</li><li>Big Rock Endings<br>
</li><li>Drum Fills to activate starpower / overdrive<br>
</li><li>Native MIDI instrument input / controller support<br>
</li><li>Pitch-bending whammy DSP effect<br>
</li><li>Songlist metadata caching for faster subsequent load times<br>
</li><li>Both digital and analog Killswitch effects (Pseudo whammy bar support)<br>
</li><li>AI support (We call him Jurgen; he rules us all)<br>
</li><li>Support for Guitar Solos, Bass Solos, and Drum Solos<br>
</li><li>Practice mode: single-track, full-speed, selectable start position / section<br>
</li><li>Slowdown mode: single or multiple tracks, 3/4, 1/2 or 1/4 speed<br>
</li><li>Includes four tutorial songs to get you started<br>
</li><li>Customizable HO/POs (including chord pull-offs) and Note Hit Window<br>
</li><li>In-Game Status Display<br>
</li><li>In-Game Star Score Display (continuous partial star fillup available)<br>
</li><li><a href='http://www.wembley1967.com/chart/'>World high score chart</a> with optional score uploading