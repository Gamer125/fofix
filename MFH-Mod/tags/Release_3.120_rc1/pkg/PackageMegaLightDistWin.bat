cd ..
copy fofix.ini fofix.bak
copy pkg\fofix.fresh.ini fofix.ini
"C:\Program Files\WinRAR\winrar" u -dh -s -m5 -tl -ibck -x@pkg\filesToExclude.lst pkg\FoFiX-Full-Win32.rar @pkg\Dist-MegaLight.lst
copy fofix.bak fofix.ini
del fofix.bak
