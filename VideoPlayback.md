
# Introduction #

Beginning with FoFiX 4.0.0, video playback has been internalized with a custom Theora module. For the non-technical, this means that old .avi will no longer play and must be converted to Theora (.ogv). The names and locations for videos have also changed. This guide intends to summarize the conversion process and naming conventions.


---


# Using ffmpeg2theora #

We've chosen [ffmpeg2theora](http://v2v.cc/~j/ffmpeg2theora/) as the officially supported converter for its ease of use and platform support. All installation instructions and binary downloads for each platform can be found on the [ffmpeg2theora](http://v2v.cc/~j/ffmpeg2theora/download.html) download page.


## Command Line Example ##
The following is a command line example that will produce very good results on any platform.

```
ffmpeg2theora -v 10 -V 2000 --soft-target --optimize --two-pass input.avi
```


## Windows GUI Frontend ##

Windows users who want to use a GUI rather than the command prompt should find [Theora Converter .NET](http://sourceforge.net/projects/theoraconverter) acceptable.


---


# Video Names and Locations #
_The following instructions are subject to change. If in doubt, take a look at the source code and log files to aid in troubleshooting._
## Theme Background Videos ##
Theme background videos should be named _"default.ogv"_ and placed in the theme's _backgrounds_ folder:
```
path/to/fofix/data/themes/Theme-Name/backgrounds/default.ogv
```
## Song Specific Videos ##
Song videos should be named _"background.ogv"_ and placed in the specific song's folder:
```
path/to/songs/Artist-Song/background.ogv
```