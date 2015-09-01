# Old News #

#### September 22, 2009 ####
**What's that? A release?**
(FoFiX v3.120 Final: [r1881](https://code.google.com/p/fofix/source/detail?r=1881))

Yep, that's right. It's finally time to call 3.120 complete and get on with the next big thing. Check out the download links _right here on the front page under Featured Downloads_! (It's to your right - you can also click the Downloads tab up top for more options)

Grab the version for your OS. If you don't know which version to get for Windows, **try the 2.6 version first**.

**Note:** _GNU/Linux players, download the [source archive](http://fofix.googlecode.com/files/fofix-3.120.tar.gz) and follow the instructions on our [RunningUnderGNULinux](RunningUnderGNULinux.md) wiki page._ -evilynux

What's new in version 3.120? A lot! Over 170 issues were resolved by this latest version, including new Vocal support, 3 and 4-player modes, theme-customizable necks, basic character support, revamped control systems supporting more types of controllers, customizable AI difficulty, and many more enhancements and bugfixes! Check out [the list of things we've fixed for this version](http://code.google.com/p/fofix/issues/list?can=1&q=status%3Afixed%2Cverified%2Cdone+milestone%3Arelease-3.120)!

As a reminder, if you are upgrading from a beta version of FoFiX 3.120 - check your "Note Hit Window" setting in the "Mods, Cheats, and AI" menu. There is a chance it may have been set to Tightest. Most players will want Normal.

P.S. I forgot to update the credits, of all things, before packaging and so I'm making it very clear that Steven Knapman (aka knapman) provided the 3D texture used as key\_open.dae in the data folder, as well as giving a lot of very helpful input on the 3D notes coding in the run up to release. Thanks a lot, Steven! (and sorry!)

-akedrou

#### September 1st 2009 ####
**To all**: If you are upgrading from a previous version of FoFiX (including previous betas), your hit window setting will have changed. In the "Mods, Cheats, and AI" section of the Settings menu, check your "Note Hit Window". Most players will want "Normal". See [issue 956](https://code.google.com/p/fofix/issues/detail?id=956) for details.

**Windows players**: Some of you may get the [issue 959](https://code.google.com/p/fofix/issues/detail?id=959), if so delete the `POWRPROF.dll` file from your data folder.

#### August 27th 2009 ####
3.120 RC 1 (SVN [r1823](https://code.google.com/p/fofix/source/detail?r=1823)) is released for final review.

This is (hopefully) the final test release before 3.120 final, and is (predictably) a bugfix on beta 2. Neck rendering, RB Co-Op saving, high scores, translations, and setlist sorting were fixed; Detailed options menu text, "Vocals" difficulty and Jurgen vocals were added.
Check the Issues page for a [detailed list of changes](http://code.google.com/p/fofix/issues/list?can=1&q=status%3Afixed%2Cverified%2Cdone+milestone%3Arelease-3.120) since the last stable release 3.100.

**Downloads**
Downloads are here! Some computers have better performance with the older PyOpenGL 2.0.2.x builds. Choose the download that's right for your computer here!

| **OS** | **Python/PyOpenGL Version** | **Type** | **Link** |
|:-------|:----------------------------|:---------|:---------|
| Windows | Python 2.6/PyOpenGL 3.x     | Installer | [Download!](http://www.mediafire.com/download.php?ezoqmtjt0mt)|
| Windows | Python 2.6/PyOpenGL 3.x     | Archive (7zip) | [Download!](http://www.mediafire.com/download.php?nhm3zmtvclj)|
| Windows | Python 2.4/PyOpenGL 2.0.2.x | Installer | [Download!](http://www.mediafire.com/download.php?dzmzlymmwzz)|
| Windows | Python 2.4/PyOpenGL 2.0.2.x | Archive (7zip) | [Download!](http://www.mediafire.com/download.php?izoydjnjijj)|
| Mac OSX | Python 2.6/PyOpenGL 3.x     | Archive (zip) | [Download!](http://www.mediafire.com/?wmzn4242mmz) |
| Mac OSX | Python 2.5/PyOpenGL 2.0.2.x | Archive (zip) | [Download!](http://www.mediafire.com/?zi1xlz4drqg) |

**GNU/Linux**: See instructions on the [RunningUnderGNULinux](RunningUnderGNULinux.md) page.

#### June 29th 2009 ####
3.120 beta 2 (SVN [r1740](https://code.google.com/p/fofix/source/detail?r=1740)) released for testing.

Although there are some new features and settings, this is mostly a bugfix release.
So it fixes issues related to Animated Hitflames, Big Rock Endings, Cache, Drums,
Pratice Mode and Rendering. It also fixes issues appearing when pausing then
unpausing the game, Scoring issues i.e. note hits, note streaks and accuracy,
and Cache issues. Lot's of other bugs, crashes and freezes were fixed.

You may consult the [detailed list of changes](http://code.google.com/p/fofix/issues/list?can=1&q=status%3Afixed%2Cverified%2Cdone+milestone%3Arelease-3.120) since the latest stable release 3.100.

Download the package that suits you:
  * Some will get more performance out of these:
    * Full package for MS Windows with python 2.4 and pyopengl 2.0.2.x [archive](http://www.mediafire.com/?za22muyk4zc) or [installer](http://www.mediafire.com/?wqwgbmymwyz) from Mediafire
    * Full package for GNU/Linux 32bit with python 2.4 and pyopengl 2.0.1.x ¹ [from Megaupload](http://www.megaupload.com/?d=83O2W7RH)
    * Full package for GNU/Linux 64bit with python 2.4 and pyopengl 2.0.1.x ¹ ² [from Megaupload](http://www.megaupload.com/?d=D8QE6W9X)
    * Full package for MacOS X with python 2.5 and pyopengl 2.0.2.x [from Mediafire](http://www.mediafire.com/?t3zmm4ny4zm)
  * Slower to some, exact same performance for others:
    * Full package for MS Windows with python 2.6 and pyopengl 3.x [archive](http://www.mediafire.com/?efrzyzujmoy) or [installer](http://www.mediafire.com/?yohjzznn310) from Mediafire
    * Full package for GNU/Linux 32bit with python 2.5 and pyopengl 3.x [from Megaupload](http://www.megaupload.com/?d=L00LPGC1)
    * Full package for MacOS X with python 2.6 and pyopengl 3.x [from Mediafire](http://www.mediafire.com/?jymg2ewj1mm)

¹ PyOpenGL 2.0.1.x does not support shaders. Shaders support was introduced in 2.0.2.x.
Thus, to get shaders under GNU/Linux, you'll have to use the python2.5 build.

² Always crashes when starting a song? See [issue 882](https://code.google.com/p/fofix/issues/detail?id=882) and [issue 887](https://code.google.com/p/fofix/issues/detail?id=887). Please report how it works for you. That'll determine if i remove it or not.

**Note about GNU/Linux builds**: Vocals and pitchbend are disabled. I haven't yet took the time to build the required dependencies. I've postponed that to the next beta or final release instead of rushing it out the door and having it half-broken.

#### May 30th 2009 ####
Please note that we are currently in FeatureFreeze thus we are slowly moving toward a new Beta release and eventually a Final version. It's useless to ask when a new Beta will be released as no one is working full-time on this hence we can not have a strict roadmap. We are doing the best we can to bring you new features AND stability.

In the meantime, if you know how to use the code from our SVN and you know what you are doing, please help us by reporting and describing bugs in our issue tracker.

Cheers,

-Pascal (evilynux) on behalf of the FoFiX Team

#### Apr. 20th 2009 ####
3.120 beta 1 (SVN [r1352](https://code.google.com/p/fofix/source/detail?r=1352)) released for testing.
There are tons of changes, hope you'll like it ;-)

Here's a summary:
  * Added experimental shaders support¹
  * Added player profiles
  * Added controller profiles
  * Added support for GH:WT xbox360 guitar solo frets
  * Added more themeable settings
  * Added more options (e.g. enable/disable pause on lost focus)
  * Fixed various game crash or freeze (BRE, neck selection, overdrive, etc.)
  * Fixed face-off battle note streaks
  * Fixed MacOS X paths for configuration files and logs
  * Improved setlist
  * Simplified 3D rendering
  * Alot of other small and smaller fixes

¹ Requires a videocard implementing OpenGL >= 2.0 and pyopengl 3.x.

Find the detailed list of [resolved issues here](http://code.google.com/p/fofix/issues/list?can=1&q=status%3Afixed%2Cverified%2Cdone+milestone%3Arelease-3.120)

Download the package that suits you:
  * Recommended for performance:
    * Full package for GNU/Linux 32bit with python 2.4 and pyopengl 2.x [from USAupload](http://www.usaupload.net/d/nadghtggwop)
    * Full package for GNU/Linux 64bit with python 2.4 and pyopengl 2.x [from Mediafire](http://www.mediafire.com/?5bndentm8jc)
    * Full package for MacOS X with python 2.5 and pyopengl 2.x [from Mediafire](http://www.mediafire.com/?izktz2whmr0) (**Updated on april 28th**)
    * 3.100 Final to 3.120~beta1 Patch for Windows with python 2.4 and pyopengl 2.x [installer](http://www.mediafire.com/download.php?mwyjnmz5dmj) or [archive](http://www.mediafire.com/download.php?zmiojzmlccu) from Mediafire
  * Generally slower but includes shaders support:
    * Full package for GNU/Linux 32bit with python 2.5 and pyopengl 3.x [from USAupload](http://www.usaupload.net/d/meozbdkfodj)
    * Full package for GNU/Linux 64bit with python 2.5 and pyopengl 3.x [from Mediafire](http://www.mediafire.com/?yit1zkyjkit)
    * Full package for MacOS X with python 2.6 and pyopengl 3.x [from Mediafire](http://www.mediafire.com/?gwanmititzk) (**Updated on april 26th**)
    * 3.100 Final to 3.120~beta1 Patch for Windows with python 2.6 and pyopengl 3.x [installer](http://www.mediafire.com/download.php?f4yy01gjyyk) or [archive](http://www.mediafire.com/download.php?znujzymuyzh) from Mediafire

#### Feb. 21st 2009 ####
3.100 Final (SVN [r1075](https://code.google.com/p/fofix/source/detail?r=1075)) has been released (12:30am PST)
([Issues resolved since 3.030](http://code.google.com/p/fofix/issues/list?can=1&q=status%3Afixed%2Cverified%2Cdone+milestone%3Arelease-3.100)):

  * Download 3.100 Full for Windows (Archive) [from GoogleCode](http://fofix.googlecode.com/files/FoFiX-3.100-Full-Win32.rar) / [from Mediafire](http://www.mediafire.com/?nojwzlmyzjg) / [from Rapidshare](http://rapidshare.com/files/200684438/FoFiX-3.100-Full-Win32.rar)
  * Download 3.100 Full for Windows (Installer) [from Mediafire](http://www.mediafire.com/download.php?zqnwanyimzy)
  * Download 3.0xx -> 3.100 Patch for Windows (Archive) [from GoogleCode](http://fofix.googlecode.com/files/FoFiX-3.100-PatchFrom3_0xx-Win32.rar) / [from Mediafire](http://www.mediafire.com/?mmzzhvijnw0) / [from Rapidshare](http://rapidshare.com/files/200684439/FoFiX-3.100-PatchFrom3_0xx-Win32.rar)
  * Download 3.100~rc1 -> 3.100 Patch for Windows (Installer) [from Mediafire](http://www.mediafire.com/download.php?mgmzdn00y2c)
  * Download 3.100 Full for GNU/Linux 32bit [from GoogleCode](http://fofix.googlecode.com/files/FoFiX-3.100-Full-GNULinux-32bit.tar.bz2)
  * Download 3.100 Full for GNU/Linux 64bit [from GoogleCode](http://fofix.googlecode.com/files/FoFiX-3.100-Full-GNULinux-64bit.tar.bz2)
  * Download 3.100 Full for MacOS X [from GoogleCode](http://fofix.googlecode.com/files/FoFiX-3.100-Full-MacOSX-Universal.zip) / [from Mediafire](http://www.mediafire.com/?3qmrzkojb53)

#### Feb. 8th 2009 ####
3.100 Release Candidate 1 (SVN [r1017](https://code.google.com/p/fofix/source/detail?r=1017)) has been released for testing.

  * Download 3.0xx -> 3.100 RC1 Patch for Windows [from Mediafire](http://www.mediafire.com/?yent1wnmvmn) / [from Rapidshare](http://rapidshare.com/files/198617247/FoFiX-3.030_r1017-Patch-Windows_3.100RC1_.rar)
  * Download 3.100 RC1 Full for Windows [from Mediafire](http://www.mediafire.com/?uizllmvqyzo) / [from Rapidshare](http://rapidshare.com/files/198617246/FoFiX-3.030_r1017-Full-Windows_3.100RC1_.rar)
  * Download 3.100beta4 -> 3.100 RC1 Patch Installer for Windows [from Mediafire](http://www.mediafire.com/?dnyb1myyqky)
  * Download 3.100 RC1 Full for Mac [from Mediafire](http://www.mediafire.com/?y0tyytjdyyz)
  * Download 3.100 RC1 Full for GNU/Linux (32bit) [from Mediafire](http://www.mediafire.com/?ncyng1oj21n)


#### Feb. ? 2009 ####
3.100 Beta 4 (SVN [r960](https://code.google.com/p/fofix/source/detail?r=960)) has been released for testing.  This should be the last beta, 3.100 final is scheduled for release in a couple days - assuming there are no major problems with beta 4.

  * Download 3.0xx -> 3.100 beta 4 Patch for Windows [from Mediafire](http://www.mediafire.com/?mongfyqmy2i) / [from Rapidshare](http://rapidshare.com/files/195808034/FoFiX-3.030_r960-Patch-Windows_3.100beta4_.rar)
  * Download 3.0xx -> 3.100 beta 4 Patch installer for Windows [from Mediafire](http://www.mediafire.com/?zjiyyvigoht)
  * Download 3.0xx -> 3.100 beta 4 Patch for Mac [from Mediafire](http://www.mediafire.com/?ojzx2nowmwy)
  * Download 3.100 beta 4 Full for Mac [from Mediafire](http://www.mediafire.com/?n3yywbmzyyx)
  * Download 3.100 beta 4 Full for GNU/Linux (32bit) [from Mediafire](http://www.mediafire.com/?m4dlmmgctbl)

**Note to GNU/Linux users**: Sorry, i screwed up creating the binaries for beta3, no more missing glx in beta4.


#### Jan. 25th 2009 ####
3.100 Beta 3 (SVN [r862](https://code.google.com/p/fofix/source/detail?r=862)) has been released for testing.  Big Rock Endings and Drum Fills have come further since 3.100 beta 2.  Guitar picks will now repeat for menu and songlist scrolling, and lyrics will no longer show during the song countdown.

  * Download 3.0xx -> 3.100 beta 3 Patch for Windows [from Mediafire](http://www.mediafire.com/?ytkyy2jgjmg) / [from Rapidshare](http://rapidshare.com/files/189452982/FoFiX-3.030_r862-Patch-Windows_3.100beta3_.rar)
  * Download 3.100 beta 2 (from installer only) -> 3.100 beta 3 Patch Installer for Windows [from Mediafire](http://www.mediafire.com/?oqzejgukmqy)
  * Download 3.100 beta 3 Full for Mac [from Mediafire](http://www.mediafire.com/?zjygy8z732x)
  * Download 3.0xx -> 3.100 beta 3 Patch for Mac [from Mediafire](http://www.mediafire.com/?2tzgzjzdzy3)
  * Download 3.x -> 3.100 beta 3 Patch for GNU/Linux (32bit) [from Mediafire](http://www.mediafire.com/?ygydjlktjmz)
  * Download 3.100 beta 3 Full for GNU/Linux (32bit) [from Mediafire](http://www.mediafire.com/?zk11yum43a0)

#### Jan. 18th 2009 ####
3.100 Beta 2 (SVN [r812](https://code.google.com/p/fofix/source/detail?r=812)) has been released for testing.  Big Rock Endings and Drum Fills have come much further since 3.100 beta 1, as has the settings menu.  No more double-and-triple song loading cycles, either.

  * Download 3.100 beta 2 Patch for Windows [from Mediafire](http://www.mediafire.com/?yqgyngnydow) / [from Rapidshare](http://rapidshare.com/files/185779080/FoFiX-3.030_r812-Patch-Windows_3.100beta2_.rar)
  * [Download 3.100 beta 2 Patch for GNU/Linux](http://www.mediafire.com/?mxqd1xcjytv) (32bit)
  * [Download 3.100 beta 2 Full installer for Windows by js](http://www.mediafire.com/download.php?hzzmjjlmzz3)
  * [Download 3.100 beta 2 Full for Mac](http://www.mediafire.com/?t22bvymvldz)

#### Jan. 11th 2009 ####
3.100 Beta 1 (SVN [r762](https://code.google.com/p/fofix/source/detail?r=762)) has been released for testing.  Notable new features include very basic Big Rock Ending support, Drum Fills, MIDI instrument input support, whammy pitch-bending support, basic 3D note.dae texturing support, and songlist metadeta caching.

  * Download 3.100 beta 1 Patch for Windows [from Mediafire](http://www.mediafire.com/?oyzm0zzjjy2) / [from Rapidshare](http://rapidshare.com/files/183238330/FoFiX-v3.030_r762-Patch-Windows_3.100beta1_.rar)
  * [Download 3.100 beta 1 Full installer for Windows](http://www.mediafire.com/download.php?kymz3ondmrn)
  * [Download 3.100 beta 1 Full for Mac](http://www.mediafire.com/?zaxtqiynlnk)
  * [Download 3.100 beta 1 Patch for GNU/Linux (32bit)](http://www.mediafire.com/?rgxfzcmd0nj)`*`
  * [Download 3.100 beta 1 Full for GNU/Linux (32bit)](http://www.mediafire.com/?czndbnh2bjv)`*`

`*` **Note to GNU/Linux players:** MIDI instrument support and whammy pitch bending support are **not** included. Releasing a beta w/ SndObj (required for pitchbending) requires too much work for now. (--_evilynux_)

#### Jan. 7th 2009 ####

_Coming soon - 3.100 beta 1 (that's right, we're skipping from 3.030 directly to 3.100.  There will be no 3.035... entirely too much progress has been made for such a minor version increment.  -Chris)_

#### Dec. 21st 2008 ####
3.035 Beta 2 (SVN [r621](https://code.google.com/p/fofix/source/detail?r=621)) has been released for testing.
I would write more, but I have to go.  Someone else can edit this later :)
(I also appear to have obliterated the beta 1 release news... I'll have to fix this later unless someone wants to take care of that for me - I forgot to paste into the oldnews, I'm a bit rushed as I have to leave in 5 minutes)

  * [Download 3.035 beta 2 Patch for Windows](http://www.mediafire.com/?2mowhnyjklh)
  * [Download 3.035 beta 2 Patch for GNU/Linux (32bit)](http://www.mediafire.com/?x0jgmyb4jtm)
  * [Download 3.035 beta 2 Patch for GNU/Linux (64bit)](http://www.mediafire.com/?ml3yym5vwmj)
  * [Download 3.035 beta 2 Patch for MacOS X](http://www.mediafire.com/?v2zjdnoqdrl)

#### Dec. 7th 2008 ####
FoFiX has a new tutorial song, for a total of [4](http://fofix.googlecode.com/files/FoFiX-All4Tutorials.rar).  This new drum roll practice tutorial was created by venom426.

Warning: playing this tutorial song in a FoFiX revision below 548 can result in incorrect scoring due to drums allowing sustained notes.


#### Nov. 30th 2008 ####

3.035 beta 1 (SVN [r469](https://code.google.com/p/fofix/source/detail?r=469)) has been released for testing.
_Detail obliterated by chris.paiano - my bad!_

  * [Download 3.035beta1 Patch for Windows](http://www.mediafire.com/download.php?1ntnwn2ueic)
  * _Other OS download links obliterated by chris.paiano - my bad!_

#### Nov. 19th 2008 ####
Final 3.030 is finally out with [tons of changes since 3.025](http://code.google.com/p/fofix/issues/list?can=1&q=status%3Afixed%2Cverified%2Cdone+milestone%3Arelease-3.030)!
Thanks to all the players who provided valuable feedback during the beta phase.

Now head to the [download section](http://code.google.com/p/fofix/downloads/list)! ;-)

#### Nov. 14th 2008 ####
3.030 beta 2 (SVN [r355](https://code.google.com/p/fofix/source/detail?r=355)) has been released for testing.
The main reasons for this beta release is to let users test:
  * the fix for [issue 165](https://code.google.com/p/fofix/issues/detail?id=165)  (Chris does not own a guitar controller that exhibits this problem -- initial reports indicate that this problem has been solved).
  * the View thread timing changes made in [r350](https://code.google.com/p/fofix/source/detail?r=350) (Should result in major smoothness and stability improvements as well as mostly fixing[?] the double-loading screen issue).

Please post in the [FoFiX Development Thread](http://www.fretsonfire.net/forums/viewtopic.php?f=11&t=25040) if you find that 3.030 beta 2 removes the requirement for XPadder or JoyToKey for those users that currently have to use these external applications.

  * [Download 3.030beta2 Patch for Windows](http://www.mediafire.com/?mjejifdmndt)
  * [Download 3.030beta2 Patch for GNU/Linux (32bit)](http://www.mediafire.com/?nfjtn4vfn4a)
  * [Download 3.030beta2 Patch for GNU/Linux (64bit)](http://www.mediafire.com/?nbb4lduyuhi)
  * [Download 3.030beta2 Full package for MacOS X (Universal)](http://www.mediafire.com/?mhy4diigpnd)

#### Nov. 7th 2008 ####
3.030 beta 1 (SVN [r277](https://code.google.com/p/fofix/source/detail?r=277)) has been released for testing.  It's main feature is that an old, outdated dependency on Amanith and pyAmanith has been removed; the full package is lighter, less support files and libraries (saved about 1MB).

  * [Download 3.030beta1 Full package for Windows](http://www.mediafire.com/?vjjidezzw5n)
  * [Download 3.030beta1 Full package for GNU/Linux (32bit)](http://www.mediafire.com/?dahjmgxcydn)
  * [Download 3.030beta1 Full package for GNU/Linux (64bit)](http://www.mediafire.com/?glmi1n5lxvl)
  * [Download 3.030beta1 Full package for MacOS X (Universal)](http://www.mediafire.com/?icdydgzb0ej)