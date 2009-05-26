#####################################################################
# -*- coding: iso-8859-1 -*-                                        #
#                                                                   #
# Frets on Fire                                                     #
# Copyright (C) 2006 Sami Ky�stil�                                  #
#               2008 myfingershurt                                  #
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

from OpenGL.GL import *
import Config
import Log
import os

# read the color scheme from the config file
Config.define("theme", "background_color",  str, "#000000")
Config.define("theme", "base_color",        str, "#FFFFFF")
Config.define("theme", "selected_color",    str, "#FFBF00")

Config.define("theme", "mesh_color",        str, "#000000")#blazingamer
Config.define("theme", "hopo_color",        str, "#00AAAA")
Config.define("theme", "spot_color",        str, "#FFFFFF")
Config.define("theme", "key_color",         str, "#333333")
Config.define("theme", "key2_color",        str, "#000000")
Config.define("theme", "tracks_color",      str, "#FFFF80")
Config.define("theme", "bars_color",        str, "#FFFF80")
Config.define("theme", "glow_color",        str, "fret")

Config.define("theme", "loading_phrase",    str, None)
Config.define("theme", "results_phrase",    str, None)
Config.define("theme", "credit_song",       str, "Unknown")

Config.define("theme", "fret0_color",       str, "#22FF22")
Config.define("theme", "fret1_color",       str, "#FF2222")
Config.define("theme", "fret2_color",       str, "#FFFF22")
Config.define("theme", "fret3_color",       str, "#3333FF")
Config.define("theme", "fret4_color",       str, "#FF9933")

Config.define("theme", "flame0_1X_color",    str, "#d5ff82")
Config.define("theme", "flame1_1X_color",    str, "#ff8880")
Config.define("theme", "flame2_1X_color",    str, "#faf66b")
Config.define("theme", "flame3_1X_color",    str, "#a4f8ff")
Config.define("theme", "flame4_1X_color",    str, "#ffde8c")
Config.define("theme", "flame0_2X_color",    str, "#d5ff82")
Config.define("theme", "flame1_2X_color",    str, "#ff8880")
Config.define("theme", "flame2_2X_color",    str, "#faf66b")
Config.define("theme", "flame3_2X_color",    str, "#a4f8ff")
Config.define("theme", "flame4_2X_color",    str, "#ffde8c")
Config.define("theme", "flame0_3X_color",    str, "#d5ff82")
Config.define("theme", "flame1_3X_color",    str, "#ff8880")
Config.define("theme", "flame2_3X_color",    str, "#faf66b")
Config.define("theme", "flame3_3X_color",    str, "#a4f8ff")
Config.define("theme", "flame4_3X_color",    str, "#ffde8c")
Config.define("theme", "flame0_4X_color",    str, "#d5ff82")
Config.define("theme", "flame1_4X_color",    str, "#ff8880")
Config.define("theme", "flame2_4X_color",    str, "#faf66b")
Config.define("theme", "flame3_4X_color",    str, "#a4f8ff")
Config.define("theme", "flame4_4X_color",    str, "#ffde8c")

Config.define("theme", "flame_gh3_color",    str, "#BF6006")

Config.define("theme", "flame0_1X_size",     float, 0.075)
Config.define("theme", "flame1_1X_size",     float, 0.075)
Config.define("theme", "flame2_1X_size",     float, 0.075)
Config.define("theme", "flame3_1X_size",     float, 0.075)
Config.define("theme", "flame4_1X_size",     float, 0.075)
Config.define("theme", "flame0_2X_size",     float, 0.075)
Config.define("theme", "flame1_2X_size",     float, 0.075)
Config.define("theme", "flame2_2X_size",     float, 0.075)
Config.define("theme", "flame3_2X_size",     float, 0.075)
Config.define("theme", "flame4_2X_size",     float, 0.075)
Config.define("theme", "flame0_3X_size",     float, 0.075)
Config.define("theme", "flame1_3X_size",     float, 0.075)
Config.define("theme", "flame2_3X_size",     float, 0.075)
Config.define("theme", "flame3_3X_size",     float, 0.075)
Config.define("theme", "flame4_3X_size",     float, 0.075)
Config.define("theme", "flame0_4X_size",     float, 0.075)
Config.define("theme", "flame1_4X_size",     float, 0.075)
Config.define("theme", "flame2_4X_size",     float, 0.075)
Config.define("theme", "flame3_4X_size",     float, 0.075)
Config.define("theme", "flame4_4X_size",     float, 0.075)

Config.define("theme", "disable_song_spinny",    bool, False)
Config.define("theme", "disable_editor_spinny",  bool, False)
Config.define("theme", "disable_results_spinny", bool, False)
Config.define("theme", "disable_menu_spinny",    bool, False)

Config.define("theme", "pov_target_x",       float, None)
Config.define("theme", "pov_target_y",       float, None)
Config.define("theme", "pov_target_z",       float, None)

Config.define("theme", "pov_origin_x",       float, None)
Config.define("theme", "pov_origin_y",       float, None)
Config.define("theme", "pov_origin_z",       float, None)

#Volshebnyi - spNote and killswitch tail colors
Config.define("theme", "fretS_color",       str, "#4CB2E5")
Config.define("theme", "fretK_color",       str, "#000000")
Config.define("theme", "obar_hscale",       float, 0.7)
Config.define("theme", "obar_3dfill",       bool, False)

#blazingamer
Config.define("theme", "menu_x",       float, None)
Config.define("theme", "menu_y",       float, None)
Config.define("theme", "rbmenu",       bool, False)


Config.define("theme", "loading_x",       float, 0.5)
Config.define("theme", "loading_y",       float, 0.6)
Config.define("theme", "loading_text_color", str, "#FFFFFF")
Config.define("theme", "loading_font_scale", float, 0.0015)
Config.define("theme", "loading_right_margin", float, 1.0)
Config.define("theme", "loading_line_spacing", float, 1.0)

Config.define("theme", "twoDnote",       bool, True)
Config.define("theme", "twoDkeys",       bool, True)
Config.define("theme", "threeDspin",       bool, True)
Config.define("theme", "opencolor",       str, "#FF9933")

Config.define("theme", "songback",       bool, False)
Config.define("theme", "versiontag",       bool, False)
Config.define("theme", "rmtype",       int, None)

Config.define("theme", "shadowoffsetx", float, .0022)
Config.define("theme", "shadowoffsety", float, .0005)

Config.define("theme", "noterotdegrees",float, 0)
Config.define("theme", "noterot1",      float, 0)
Config.define("theme", "noterot2",      float, 0)
Config.define("theme", "noterot3",      float, 0)
Config.define("theme", "noterot4",      float, 0)
Config.define("theme", "noterot5",      float, 0)

#TWD
Config.define("theme", "menu_neck_choose_x", float, 0.1)
Config.define("theme", "menu_neck_choose_y", float, 0.05)

#akedrou - lobby/control activator
Config.define("theme", "control_activate_x", float, 0.645)
Config.define("theme", "control_activate_select_x", float, 0.5)
Config.define("theme", "control_activate_part_x", float, 0.41)
Config.define("theme", "control_activate_y", float, 0.18)
Config.define("theme", "control_activate_scale", float, 0.0018)
Config.define("theme", "control_activate_part_size", float, 22.000)
Config.define("theme", "control_activate_space", float, 0.045)
Config.define("theme", "control_activate_font", str, "font")
Config.define("theme", "control_description_x", float, 0.5)
Config.define("theme", "control_description_y", float, 0.13)
Config.define("theme", "control_description_scale", float, 0.002)
Config.define("theme", "control_description_font", str, "font")
Config.define("theme", "control_check_x", float, 0.16)
Config.define("theme", "control_check_y", float, 0.26)
Config.define("theme", "control_check_text_y", float, 0.61)
Config.define("theme", "control_check_part_mult", float, 2.8)
Config.define("theme", "control_check_space", float, 0.23)
Config.define("theme", "control_check_scale", float, 0.0018)
Config.define("theme", "control_check_font", str, "font")
Config.define("theme", "lobby_mode", int, 0)
Config.define("theme", "lobby_preview_x", float, 0.7)
Config.define("theme", "lobby_preview_y", float, 0.0) #worldrave
Config.define("theme", "lobby_preview_spacing", float, 0.04)
Config.define("theme", "lobby_title_x", float, 0.5)
Config.define("theme", "lobby_title_y", float, 0.07)
Config.define("theme", "lobby_title_character_x", float, 0.26)
Config.define("theme", "lobby_title_character_y", float, 0.24)
Config.define("theme", "lobby_title_scale", float, 0.0024)
Config.define("theme", "lobby_title_font", str, "loadingFont")
Config.define("theme", "lobby_avatar_x", float, 0.7)
Config.define("theme", "lobby_avatar_y", float, 0.75)
Config.define("theme", "lobby_avatar_scale", float, 1.0)
Config.define("theme", "lobby_select_x", float, 0.4)
Config.define("theme", "lobby_select_y", float, 0.32)
Config.define("theme", "lobby_select_image_x", float, 0.255)
Config.define("theme", "lobby_select_image_y", float, 0.335)
Config.define("theme", "lobby_select_scale", float, 0.0018)
Config.define("theme", "lobby_select_space", float, 0.04)
Config.define("theme", "lobby_select_font", str, "font")
Config.define("theme", "lobby_select_length", int, 5)
Config.define("theme", "lobby_title_color", str, "#FFFFFF")
Config.define("theme", "lobby_player_color", str, "#FFFFFF")
Config.define("theme", "lobby_info_color", str, "#FFFFFF")
Config.define("theme", "lobby_font_color", str, "#FFFFFF")
Config.define("theme", "lobby_select_color", str, "#FFBF00")
Config.define("theme", "lobby_disable_color", str, "#666666")
Config.define("theme", "character_create_x", float, 0.25)
Config.define("theme", "character_create_y", float, 0.15)
Config.define("theme", "character_create_help_x", float, 0.5)
Config.define("theme", "character_create_help_y", float, 0.73)
Config.define("theme", "character_create_help_scale", float, 0.0018)
Config.define("theme", "character_create_option_x", float, 0.75)
Config.define("theme", "character_create_option_font", str, "font")
Config.define("theme", "character_create_font_color", str, "#FFFFFF")
Config.define("theme", "character_create_select_color", str, "#FFBF00")
Config.define("theme", "character_create_help_color", str, "#FFFFFF")
Config.define("theme", "character_create_help_font", str, "loadingFont")
Config.define("theme", "character_create_scale", float, .0018)
Config.define("theme", "character_create_space", float, .045)

#worldrave
Config.define("theme", "setlistguidebuttonsposX", float, 0.408)
Config.define("theme", "setlistguidebuttonsposY", float, 0.0322)
Config.define("theme", "setlistguidebuttonsscaleX", float, 0.29)
Config.define("theme", "setlistguidebuttonsscaleY", float, 0.308)
Config.define("theme", "setlistpreviewbuttonposX", float, 0.5)
Config.define("theme", "setlistpreviewbuttonposY", float, 0.5)
Config.define("theme", "setlistpreviewbuttonscaleX", float, 0.5)
Config.define("theme", "setlistpreviewbuttonscaleY", float, 0.5)
Config.define("theme", "versiontagposX", float, 0.5)
Config.define("theme", "versiontagposY", float, 0.5)

#evilynux
Config.define("theme", "songlist_score_color",  str, "#93C351")
Config.define("theme", "songlistcd_score_color",  str, "#FFFFFF")
Config.define("theme", "rockmeter_score_color",  str, "#FFFFFF")
Config.define("theme", "ingame_stats_color",  str, "#FFFFFF")

#MFH
Config.define("theme", "song_cd_x",       float, None)
Config.define("theme", "song_cdscore_x",       float, None)
Config.define("theme", "song_list_x",       float, None)
Config.define("theme", "song_listscore_x",       float, None)

Config.define("theme", "song_listcd_cd_x",       float, None)
Config.define("theme", "song_listcd_cd_y",       float, None)
Config.define("theme", "song_listcd_score_x",       float, None)
Config.define("theme", "song_listcd_score_y",       float, None)
Config.define("theme", "song_listcd_list_x",       float, None)

Config.define("theme", "song_rb2_name_color",       str, "#FFFFFF")
Config.define("theme", "song_rb2_name_selected_color",       str, "#FFBF00")
Config.define("theme", "song_rb2_diff_color",       str, "#FFBF00")
Config.define("theme", "song_rb2_artist_color",       str, "#4080FF")

Config.define("theme", "pause_bkg",       str, "0.5,0.5,1.0,1.0")
Config.define("theme", "pause_text_x",       float, None)
Config.define("theme", "pause_text_y",       float, None)
Config.define("theme", "pause_text_color",  str, "#FFFFFF")
Config.define("theme", "pause_selected_color",  str, "#FFBF00")

Config.define("theme", "opt_bkg",   str, "0.5,0.5,1.0,1.0")
Config.define("theme", "opt_text_x",       float, None)
Config.define("theme", "opt_text_y",       float, None)
Config.define("theme", "opt_text_color",  str, "#FFFFFF")
Config.define("theme", "opt_selected_color",  str, "#FFBF00")


Config.define("theme", "main_menu_scale",       float, None)
Config.define("theme", "main_menu_vspacing",       float, None)
Config.define("theme", "use_solo_submenu",       bool, None)
Config.define("theme", "sub_menu_x",       float, None)
Config.define("theme", "sub_menu_y",       float, None)

Config.define("theme", "career_title_color",  str, "#000000")
Config.define("theme", "song_name_text_color",  str, "#FFFFFF")
Config.define("theme", "song_name_selected_color",  str, "#FFBF00")
Config.define("theme", "artist_text_color",  str, "#4080FF")
Config.define("theme", "artist_selected_color",  str, "#4080FF")
Config.define("theme", "library_text_color",  str, "#FFFFFF")
Config.define("theme", "library_selected_color",  str, "#FFBF00")


Config.define("theme", "fail_text_color",  str, "#FFFFFF")
Config.define("theme", "fail_completed_color",  str, "#FFFFFF")
Config.define("theme", "fail_selected_color",  str, "#FFBF00")

Config.define("theme", "result_score", str, ".5,.11,0.0025,None,None")
Config.define("theme", "result_song", str, ".05,.045,.002,None,None")
Config.define("theme", "result_song_form", int, 0)
Config.define("theme", "result_song_text", str, "%s Finished!")
Config.define("theme", "result_star", str, ".5,.4,0.15,1.1")
Config.define("theme", "result_star_type", int, 0)
Config.define("theme", "result_stats_diff", str, ".5,.55,0.002,None,None")
Config.define("theme", "result_stats_diff_text", str, "Difficulty: %s")
Config.define("theme", "result_stats_part", str, ".5,.64,0.002,None,None")
Config.define("theme", "result_stats_part_text", str, "Part: %s")
Config.define("theme", "result_stats_name", str, ".5,.73,0.002,None,None")
Config.define("theme", "result_stats_streak", str, ".5,.58,0.002,None,None")
Config.define("theme", "result_stats_streak_text", str, "Long Streak: %s")
Config.define("theme", "result_stats_accuracy", str, ".5,.61,0.002,None,None")
Config.define("theme", "result_stats_accuracy_text", str, "Accuracy: %.1f%%")
Config.define("theme", "result_stats_notes", str, ".5,.52,0.002,None,None")
Config.define("theme", "result_stats_notes_text", str, "%s Notes Hit")
Config.define("theme", "result_cheats_info", str, ".5,.3,.002")
Config.define("theme", "result_cheats_numbers", str, ".5,.35,.0015")
Config.define("theme", "result_cheats_score", str, ".75,.4,.0015")
Config.define("theme", "result_cheats_percent", str, ".45,.4,.0015")
Config.define("theme", "result_cheats_color", str, "#FFFFFF")
Config.define("theme", "result_cheats_font", str, "font")
Config.define("theme", "result_high_score_font", str, "font")
Config.define("theme", "result_menu_x", float, .5)
Config.define("theme", "result_menu_y", float, .2)

Config.define("theme", "jurgen_text_pos", str, "1,1,.00035")


#MFH - crowd cheer loop delay in theme.ini: if not exist, use value from settings. Otherwise, use theme.ini value.
Config.define("theme", "crowd_loop_delay",  int, None)

#MFH - for instrument / difficulty / practice section submenu positioning
Config.define("theme", "song_select_submenu_x",  float, None)
Config.define("theme", "song_select_submenu_y",  float, None)

#MFH - for scaling song info during countdown
Config.define("theme", "song_info_display_scale",  float, 0.0020)

#Worldrave - for song info display positioning
Config.define("theme", "song_info_display_X",  float, 0.05)
Config.define("theme", "song_info_display_Y",  float, 0.05)
Config.define("theme", "neck_length",    float, 9.0)

#MFH - option for Rock Band 2 theme.ini - only show # of stars you are working on
Config.define("theme", "display_all_grey_stars",  bool, True)
Config.define("theme", "small_1x_mult", bool, True)

#MFH - y offset = lines, x offset = spaces
Config.define("theme", "song_select_submenu_offset_lines",  int, 2)
Config.define("theme", "song_select_submenu_offset_spaces",  int, 2)

#Qstick - hopo indicator position and color
Config.define("theme", "hopo_indicator_x",       float, None)
Config.define("theme", "hopo_indicator_y",       float, None)
Config.define("theme", "hopo_indicator_active_color",   str, "#FFFFFF")
Config.define("theme", "hopo_indicator_inactive_color",   str, "#666666")

#stump - parameters for continuous fillup of stars
Config.define("theme", "star_fillup_center_x", int, None)
Config.define("theme", "star_fillup_center_y", int, None)
Config.define("theme", "star_fillup_in_radius", int, None)
Config.define("theme", "star_fillup_out_radius", int, None)
Config.define("theme", "star_fillup_color", str, None)

#Qstick - Misc
Config.define("theme", "song_list_display",       int, None)
Config.define("theme", "neck_width",    float, 3.0)

#Qstick - Results Screen

#RACER:
Config.define("theme", "fail_bkg",       str, "0.5,0.5,1.0,1.0")
Config.define("theme", "fail_text_x",       float, None)
Config.define("theme", "fail_text_y",       float, None)
Config.define("theme", "fail_songname_x",  float, 0.5)
Config.define("theme", "fail_songname_y",  float, 0.35)

submenuX = {}
submenuY = {}
submenuV = {}

backgroundColor = None
baseColor       = None
selectedColor   = None
fretColors      = None
gh3flameColor   = None

hopoColor       = None
spotColor       = None
keyColor        = None
key2Color       = None
tracksColor     = None
barsColor       = None
glowColor       = None

flameColors     = None
flameSizes      = None
loadingPhrase   = None
resultsPhrase   = None
startingPhrase  = None

spinnySongDisabled = None
spinnyEditorDisabled = None
spinnyResultsDisabled = None
spinnyMenuDisabled = None

creditSong = None
povTargetX = None
povTargetY = None
povTargetZ = None
povOriginX = None
povOriginY = None
povOriginZ = None

#Blazingamer
menuX = None
menuY = None
menuRB = None
loadingX = None
loadingY = None
loadingColor = None
loadingFScale = None
loadingRMargin = None
loadingLSpacing = None
twoDnote = None
twoDkeys = None
threeDspin = None
opencolor = None
meshColor = None
songback = None
versiontag = None
rmtype = None
shadowoffsetx = None
shadowoffsety = None

#evilynux
songlist_score_colorVar = None
songlistcd_score_colorVar = None
rockmeter_score_colorVar = None
ingame_stats_colorVar = None

#akedrou - lobby/control setup
controlActivateX = None
controlActivateSelectX = None
controlActivatePartX = None
controlActivateY = None
controlActivateScale = None
controlActivatePartSize = None
controlActivateSpace = None
controlActivateFont = None
controlDescriptionY = None
controlDescriptionX = None
controlDescriptionScale = None
controlDescriptionFont = None
controlCheckX = None
controlCheckY = None
controlCheckTextY = None
controlCheckPartMult = None
controlCheckSpace = None
controlCheckScale = None
controlCheckFont  = None
lobbyMode = None
lobbyPreviewX = None
lobbyPreviewY = None #worldrave
lobbyPreviewSpacing = None
lobbyTitleX = None
lobbyTitleY = None
lobbyTitleCharacterX = None
lobbyTitleCharacterY = None
lobbyTitleScale = None
lobbyTitleFont = None
lobbyAvatarX = None
lobbyAvatarY = None
lobbyAvatarScale = None
lobbySelectX = None
lobbySelectY = None
lobbySelectImageX = None
lobbySelectImageY = None
lobbySelectScale = None
lobbySelectSpace = None
lobbySelectFont = None
lobbySelectLength = None
lobbyTitleColor = None
lobbyInfoColor = None
lobbyFontColor = None
lobbyPlayerColor = None
lobbySelectColor = None
lobbyDisableColor = None
characterCreateX = None
characterCreateY = None
characterCreateOptionX = None
characterCreateFontColor = None
characterCreateSelectColor = None
characterCreateHelpColor = None
characterCreateHelpX = None
characterCreateHelpY = None
characterCreateHelpScale = None
characterCreateOptionFont = None
characterCreateHelpFont = None
characterCreateScale = None
characterCreateSpace = None

#worldrave 
setlistguidebuttonsposX = None
setlistguidebuttonsposY = None
setlistguidebuttonsscaleX = None
setlistguidebuttonsscaleY = None
setlistpreviewbuttonposX = None
setlistpreviewbuttonposY = None
setlistpreviewbuttonscaleY = None
setlistpreviewbuttonscaleY = None

#MFH:
song_cd_Xpos = None         #Songlist in CD mode: horizontal position of CDs/cases
song_cdscore_Xpos = None    #Songlist in CD mode: horizontal position of score info
song_list_Xpos = None       #Songlist in List mode: horizontal position of song names/artists
song_listscore_Xpos = None  #Songlist in List mode: horizontal position of score info

song_listcd_cd_Xpos = None
song_listcd_cd_Ypos = None
song_listcd_score_Xpos = None
song_listcd_score_Ypos = None
song_listcd_list_Xpos = None

pause_bkg_pos = [None]*4
pause_text_xPos = None
pause_text_yPos = None

opt_bkg_size = [None]*4
opt_text_xPos = None
opt_text_yPos = None

main_menu_scaleVar = None
main_menu_vspacingVar = None
use_solo_submenu = None
sub_menu_xVar = None
sub_menu_yVar = None

career_title_colorVar = None
opt_text_colorVar = None
opt_selected_colorVar = None
song_name_text_colorVar = None
song_name_selected_colorVar = None
artist_text_colorVar = None
artist_selected_colorVar = None
library_text_colorVar = None
library_selected_colorVar = None

song_rb2_name_colorVar = None
song_rb2_name_selected_colorVar = None
song_rb2_diff_colorVar = None
song_rb2_artist_colorVar = None

pause_text_colorVar = None
pause_selected_colorVar = None
fail_completed_colorVar = None
fail_text_colorVar = None
fail_selected_colorVar = None

#MFH - crowd cheer loop delay in theme.ini: if not exist, use value from settings. Otherwise, use theme.ini value.
crowdLoopDelay = None

#MFH - for instrument / difficulty / practice section submenu positioning
songSelectSubmenuX = None
songSelectSubmenuY = None

#TWD - for neck chooser text positionning
neck_prompt_x = None
neck_prompt_y = None

#MFH - for scaling song info during countdown
songInfoDisplayScale = None

#Worldrave - for position of song info display during countdown
songInfoDisplayX = None
songInfoDisplayY = None
versiontagposX = None
versiontagposY = None
neckLength = None

#MFH - y offset = lines, x offset = spaces
songSelectSubmenuOffsetLines = None
songSelectSubmenuOffsetSpaces = None

#MFH - option for Rock Band 2 theme.ini - only show # of stars you are working on
displayAllGreyStars = None
smallMult = None

#Qstick - hopo indicator position and color
hopoIndicatorX = None
hopoIndicatorY = None
hopoIndicatorActiveColor = None
hopoIndicatorInactiveColor = None

#stump - parameters for continuous fillup of stars
starFillupCenterX = None
starFillupCenterY = None
starFillupInRadius = None
starFillupOutRadius = None
starFillupColor = None

#Qstick - misc
songListDisplay = None
neckWidth = None

result_score = [None] * 5
result_star = [None] * 4
result_song = [None] * 5
result_song_form = None
result_song_text = None
result_stats_part = [None] * 5
result_stats_part_text = None
result_stats_name = [None] * 5
result_stats_diff = [None] * 5
result_stats_diff_text = None
result_stats_accuracy = [None] * 5
result_stats_accuracy_text = None
result_stats_streak = [None] * 5
result_stats_streak_text = None
result_stats_notes = [None] * 5
result_stats_notes_text = None
#akedrou
result_cheats_info = [None] * 3
result_cheats_numbers = [None] * 3
result_cheats_score = [None] * 3
result_cheats_percent = [None] * 3
result_cheats_color = None
result_cheats_font  = None
result_high_score_font = None
result_menu_x = None
result_menu_y = None
result_star_type = None

jurgTextPos = [None] * 3


#Racer:
#fail_bkg_xPos = None
#fail_bkg_yPos = None
fail_bkg_pos = [None]*4
fail_text_xPos = None
fail_text_yPos = None



def hexToColor(color):
  if color[0] == "#":
    color = color[1:]
    if len(color) == 3:
      return (int(color[0], 16) / 15.0, int(color[1], 16) / 15.0, int(color[2], 16) / 15.0)
    return (int(color[0:2], 16) / 255.0, int(color[2:4], 16) / 255.0, int(color[4:6], 16) / 255.0)
  elif color.lower() == "off":
    return (-1, -1, -1)
  elif color.lower() == "fret":
    return (-2, -2, -2)
  return (0, 0, 0)

def hexToColorResults(color):
  color = color.strip()
  if color[0] == "#":
    color = color[1:]
    if len(color) == 3:
      return (int(color[0], 16) / 15.0, int(color[1], 16) / 15.0, int(color[2], 16) / 15.0)
    return (int(color[0:2], 16) / 255.0, int(color[2:4], 16) / 255.0, int(color[4:6], 16) / 255.0)
  return baseColor
    
def colorToHex(color):
  return "#" + ("".join(["%02x" % int(c * 255) for c in color]))

def setSelectedColor(alpha = 1.0):
  glColor4f(*(selectedColor + (alpha,)))

def setBaseColor(alpha = 1.0):
  glColor4f(*(baseColor + (alpha,)))
  


def open(config, themepath = None):
  # Read in theme.ini specific variables
  
  setupColors(config)
  setupFrets(config)
  setupFlameColors(config)
  setupFlameSizes(config)
  setupSpinny(config)
  setupPOV(config)
  setupMisc(config)
  setupMenu(config)
  setupLobby(config) #akedrou
  setupSonglist(config) #MFH
  setupPauseNOpt(config) #MFH
  setupTWOD(config)
  setupFail(config) #racer
  setupEvilynux(config)
  setupRockmeter(config)
  setupNeckChooser(config)
  setupHopoIndicator(config)
  setupResults(config)
  setupSubmenus(config, themepath)
  

def setupNeckChooser(config):
  global neck_prompt_x, neck_prompt_y
  
  neck_prompt_x = config.get("theme", "menu_neck_choose_x")
  neck_prompt_y = config.get("theme", "menu_neck_choose_y")


def setupColors(config):
  global backgroundColor, baseColor, selectedColor
  global hopoColor, spotColor, meshColor
  global keyColor, key2Color
  global tracksColor, barsColor, glowColor
  
  backgroundColor = hexToColor(config.get("theme", "background_color"))  
  baseColor = hexToColor(config.get("theme", "base_color"))
  selectedColor = hexToColor(config.get("theme", "selected_color"))
  meshColor = hexToColor(config.get("theme", "mesh_color"))
  hopoColor = hexToColor(config.get("theme", "hopo_color"))
  spotColor = hexToColor(config.get("theme", "spot_color"))
  keyColor = hexToColor(config.get("theme", "key_color"))
  key2Color = hexToColor(config.get("theme", "key2_color"))
  tracksColor = hexToColor(config.get("theme", "tracks_color"))
  barsColor = hexToColor(config.get("theme", "bars_color"))
  glowColor = hexToColor(config.get("theme", "glow_color"))
 
def setupFrets(config):
  global fretColors
    
  if fretColors == None:
    fretColors = [hexToColor(config.get("theme", "fret%d_color" % i)) for i in range(5)]
    fretColors.append(hexToColor(config.get("theme", "fretS_color"))) #Volshebnyi - spNote color
    fretColors.append(hexToColor(config.get("theme", "fretK_color"))) #Volshebnyi - killswitch tail color
  else:
    fretColors[0] = hexToColor(config.get("theme", "fret0_color"))
    fretColors[1] = hexToColor(config.get("theme", "fret1_color"))
    fretColors[2] = hexToColor(config.get("theme", "fret2_color"))
    fretColors[3] = hexToColor(config.get("theme", "fret3_color"))
    fretColors[4] = hexToColor(config.get("theme", "fret4_color"))
    fretColors[5] = hexToColor(config.get("theme", "fretS_color"))
    fretColors[6] = hexToColor(config.get("theme", "fretK_color"))

def setupFlameColors(config):
  global flameColors
  global gh3flameColor

  temp = config.get("theme", "flame_gh3_color")
  gh3flameColor = hexToColor(temp)
  if flameColors == None:
    flameColors = [[hexToColor(config.get("theme", "flame%d_1X_color" % i)) for i in range(5)]]
    flameColors.append([hexToColor(config.get("theme", "flame%d_2X_color" % i)) for i in range(5)])
    flameColors.append([hexToColor(config.get("theme", "flame%d_3X_color" % i)) for i in range(5)])
    flameColors.append([hexToColor(config.get("theme", "flame%d_4X_color" % i)) for i in range(5)])
  else:
    flameColors[0][0] = hexToColor(config.get("theme", "flame0_1X_color"))
    flameColors[0][1] = hexToColor(config.get("theme", "flame1_1X_color"))
    flameColors[0][2] = hexToColor(config.get("theme", "flame2_1X_color"))
    flameColors[0][3] = hexToColor(config.get("theme", "flame3_1X_color"))
    flameColors[0][4] = hexToColor(config.get("theme", "flame4_1X_color"))
    flameColors[1][0] = hexToColor(config.get("theme", "flame0_2X_color"))
    flameColors[1][1] = hexToColor(config.get("theme", "flame1_2X_color"))
    flameColors[1][2] = hexToColor(config.get("theme", "flame2_2X_color"))
    flameColors[1][3] = hexToColor(config.get("theme", "flame3_2X_color"))
    flameColors[1][4] = hexToColor(config.get("theme", "flame4_2X_color"))
    flameColors[2][0] = hexToColor(config.get("theme", "flame0_3X_color"))
    flameColors[2][1] = hexToColor(config.get("theme", "flame1_3X_color"))
    flameColors[2][2] = hexToColor(config.get("theme", "flame2_3X_color")) 
    flameColors[2][3] = hexToColor(config.get("theme", "flame3_3X_color"))
    flameColors[2][4] = hexToColor(config.get("theme", "flame4_3X_color"))
    flameColors[3][0] = hexToColor(config.get("theme", "flame0_4X_color"))
    flameColors[3][1] = hexToColor(config.get("theme", "flame1_4X_color"))
    flameColors[3][2] = hexToColor(config.get("theme", "flame2_4X_color"))
    flameColors[3][3] = hexToColor(config.get("theme", "flame3_4X_color"))
    flameColors[3][4] = hexToColor(config.get("theme", "flame4_4X_color"))

        
def setupFlameSizes(config):
  global flameSizes

  if flameSizes == None:
    flameSizes = [[config.get("theme", "flame%d_1X_size" % i) for i in range(5)]]
    flameSizes.append([config.get("theme", "flame%d_2X_size" % i) for i in range(5)])
    flameSizes.append([config.get("theme", "flame%d_3X_size" % i) for i in range(5)])
    flameSizes.append([config.get("theme", "flame%d_4X_size" % i) for i in range(5)])
  else:
    flameSizes[0][0] = config.get("theme", "flame0_1X_size")
    flameSizes[0][1] = config.get("theme", "flame1_1X_size")
    flameSizes[0][2] = config.get("theme", "flame2_1X_size")
    flameSizes[0][3] = config.get("theme", "flame3_1X_size")
    flameSizes[0][4] = config.get("theme", "flame4_1X_size")
    flameSizes[1][0] = config.get("theme", "flame0_2X_size")
    flameSizes[1][1] = config.get("theme", "flame1_2X_size")
    flameSizes[1][2] = config.get("theme", "flame2_2X_size")
    flameSizes[1][3] = config.get("theme", "flame3_2X_size")
    flameSizes[1][4] = config.get("theme", "flame4_2X_size")
    flameSizes[2][0] = config.get("theme", "flame0_3X_size")
    flameSizes[2][1] = config.get("theme", "flame1_3X_size")
    flameSizes[2][2] = config.get("theme", "flame2_3X_size") 
    flameSizes[2][3] = config.get("theme", "flame3_3X_size")
    flameSizes[2][4] = config.get("theme", "flame4_3X_size")
    flameSizes[3][0] = config.get("theme", "flame0_4X_size")
    flameSizes[3][1] = config.get("theme", "flame1_4X_size")
    flameSizes[3][2] = config.get("theme", "flame2_4X_size")
    flameSizes[3][3] = config.get("theme", "flame3_4X_size")
    flameSizes[3][4] = config.get("theme", "flame4_4X_size")

def setupSpinny(config):
  global spinnySongDisabled, spinnyEditorDisabled, spinnyResultsDisabled, spinnyMenuDisabled

  spinnySongDisabled = config.get("theme", "disable_song_spinny")
  spinnyEditorDisabled = config.get("theme", "disable_editor_spinny")
  spinnyResultsDisabled = config.get("theme", "disable_results_spinny")
  spinnyMenuDisabled = config.get("theme", "disable_menu_spinny")
  
def setupPOV(config):
  global povTargetX, povTargetY, povTargetZ
  global povOriginX, povOriginY, povOriginZ
  
  povTargetX = config.get("theme", "pov_target_x")  
  povTargetY = config.get("theme", "pov_target_y")
  povTargetZ = config.get("theme", "pov_target_z")
  povOriginX = config.get("theme", "pov_origin_x")
  povOriginY = config.get("theme", "pov_origin_y")
  povOriginZ = config.get("theme", "pov_origin_z")

def setupMisc(config):
  global loadingPhrase, resultsPhrase
  global creditSong
  global crowdLoopDelay
  global songInfoDisplayScale
  global songInfoDisplayX
  global songInfoDisplayY
  global displayAllGreyStars, smallMult
  global starFillupCenterX
  global starFillupCenterY
  global starFillupInRadius
  global starFillupOutRadius
  global starFillupColor
  global songListDisplay
  global jurgTextPos
  global oBarHScale
  global oBar3dFill
  global neckWidth
  global neckLength

  loadingPhrase = config.get("theme", "loading_phrase")
  resultsPhrase = config.get("theme", "results_phrase")
  creditSong = config.get("theme", "credit_song")
  crowdLoopDelay = config.get("theme", "crowd_loop_delay")
  songInfoDisplayScale = config.get("theme", "song_info_display_scale")
  songInfoDisplayX = config.get("theme", "song_info_display_X")
  songInfoDisplayY = config.get("theme", "song_info_display_Y")
  displayAllGreyStars = config.get("theme", "display_all_grey_stars")
  smallMult = config.get("theme", "small_1x_mult")
  starFillupCenterX = config.get("theme", "star_fillup_center_x")
  starFillupCenterY = config.get("theme", "star_fillup_center_y")
  starFillupInRadius = config.get("theme", "star_fillup_in_radius")
  starFillupOutRadius = config.get("theme", "star_fillup_out_radius")
  starFillupColor = config.get("theme", "star_fillup_color")
  songListDisplay = config.get("theme", "song_list_display")
  jurgTextPos = config.get("theme", "jurgen_text_pos").split(",")
  oBarHScale = config.get("theme", "obar_hscale")
  oBar3dFill = config.get("theme", "obar_3dfill")
  neckWidth = config.get("theme", "neck_width")
  neckLength = config.get("theme", "neck_length")
#MFH:
def setupSonglist(config):
  global song_cd_Xpos, song_cdscore_Xpos, song_list_Xpos, song_listscore_Xpos
  global song_listcd_cd_Xpos, song_listcd_cd_Ypos, song_listcd_score_Xpos, song_listcd_score_Ypos, song_listcd_list_Xpos

  global setlistguidebuttonsposX, setlistguidebuttonsposY, setlistguidebuttonsscaleX, setlistguidebuttonsscaleY
  global setlistpreviewbuttonposX, setlistpreviewbuttonposY, setlistpreviewbuttonscaleX, setlistpreviewbuttonscaleY
  global career_title_colorVar, opt_text_colorVar, opt_selected_colorVar
  global song_name_text_colorVar, song_name_selected_colorVar
  global artist_text_colorVar, artist_selected_colorVar
  global library_text_colorVar, library_selected_colorVar
  global pause_text_colorVar, pause_selected_colorVar
  global fail_text_colorVar, fail_selected_colorVar, fail_completed_colorVar
  global songSelectSubmenuX, songSelectSubmenuY
  global songSelectSubmenuOffsetLines, songSelectSubmenuOffsetSpaces
  global versiontagposX, versiontagposY
  
  global song_rb2_name_colorVar, song_rb2_name_selected_colorVar, song_rb2_diff_colorVar, song_rb2_artist_colorVar

  setlistguidebuttonsposX = config.get("theme", "setlistguidebuttonsposX")
  setlistguidebuttonsposY = config.get("theme", "setlistguidebuttonsposY")
  setlistguidebuttonsscaleX = config.get("theme", "setlistguidebuttonsscaleX")
  setlistguidebuttonsscaleY = config.get("theme", "setlistguidebuttonsscaleY")
  setlistpreviewbuttonposX = config.get("theme", "setlistpreviewbuttonposX")
  setlistpreviewbuttonposY = config.get("theme", "setlistpreviewbuttonposY")
  setlistpreviewbuttonscaleX = config.get("theme", "setlistpreviewbuttonscaleX")
  setlistpreviewbuttonscaleY = config.get("theme", "setlistpreviewbuttonscaleY")
  versiontagposX = config.get("theme", "versiontagposX")
  versiontagposY = config.get("theme", "versiontagposY")
  songSelectSubmenuOffsetLines = config.get("theme", "song_select_submenu_offset_lines")
  songSelectSubmenuOffsetSpaces = config.get("theme", "song_select_submenu_offset_spaces")
  songSelectSubmenuX = config.get("theme", "song_select_submenu_x")
  songSelectSubmenuY = config.get("theme", "song_select_submenu_y")
  song_cd_Xpos = config.get("theme", "song_cd_x")
  song_listcd_cd_Xpos = config.get("theme", "song_listcd_cd_x")
  song_listcd_cd_Ypos = config.get("theme", "song_listcd_cd_y")
  song_listcd_score_Xpos = config.get("theme", "song_listcd_score_x")
  song_listcd_score_Ypos = config.get("theme", "song_listcd_score_y")
  song_listcd_list_Xpos = config.get("theme", "song_listcd_list_x")
  song_cdscore_Xpos = config.get("theme", "song_cdscore_x")
  song_list_Xpos = config.get("theme", "song_list_x")
  song_listscore_Xpos = config.get("theme", "song_listscore_x")
  career_title_colorVar = config.get("theme", "career_title_color")
  opt_text_colorVar = config.get("theme", "opt_text_color")
  opt_selected_colorVar = config.get("theme", "opt_selected_color")
  song_name_text_colorVar = config.get("theme", "song_name_text_color")
  song_name_selected_colorVar = config.get("theme", "song_name_selected_color")
  artist_text_colorVar = config.get("theme", "artist_text_color")
  artist_selected_colorVar = config.get("theme", "artist_selected_color")
  library_text_colorVar = config.get("theme", "library_text_color")
  library_selected_colorVar = config.get("theme", "library_selected_color")
  pause_text_colorVar = config.get("theme", "pause_text_color")
  pause_selected_colorVar = config.get("theme", "pause_selected_color")
  fail_completed_colorVar = config.get("theme", "fail_completed_color")
  fail_text_colorVar = config.get("theme", "fail_text_color")
  fail_selected_colorVar = config.get("theme", "fail_selected_color")
  
  song_rb2_name_colorVar = config.get("theme", "song_rb2_name_color")
  song_rb2_name_selected_colorVar = config.get("theme", "song_rb2_name_selected_color")
  song_rb2_diff_colorVar = config.get("theme", "song_rb2_diff_color")
  song_rb2_artist_colorVar = config.get("theme", "song_rb2_artist_color")

  
def setupPauseNOpt(config):
  global pause_bkg_pos, pause_text_xPos, pause_text_yPos
  global opt_bkg_size, opt_text_xPos, opt_text_yPos

  pause_bkg_pos = config.get("theme", "pause_bkg").split(",")
  pause_text_xPos = config.get("theme", "pause_text_x")
  pause_text_yPos = config.get("theme", "pause_text_y")
  opt_bkg_size = config.get("theme", "opt_bkg").split(",")
  opt_text_xPos = config.get("theme", "opt_text_x")
  opt_text_yPos = config.get("theme", "opt_text_y")
  
def setupMenu(config):
  global menuX, menuY, menuRB
  global loadingX, loadingY, loadingColor, loadingFScale, loadingRMargin, loadingLSpacing
  global main_menu_scaleVar, main_menu_vspacingVar, use_solo_submenu, sub_menu_xVar, sub_menu_yVar
  global songback, versiontag, shadowoffsetx, shadowoffsety
  
  menuX = config.get("theme", "menu_x")
  menuY = config.get("theme", "menu_y")
  menuRB = config.get("theme", "rbmenu")
  loadingX = config.get("theme", "loading_x")
  loadingY = config.get("theme", "loading_y")
  loadingColor = hexToColor(config.get("theme", "loading_text_color"))
  loadingFScale = config.get("theme", "loading_font_scale")
  loadingRMargin = config.get("theme", "loading_right_margin")
  loadingLSpacing = config.get ("theme", "loading_line_spacing")
  main_menu_scaleVar = config.get("theme", "main_menu_scale")
  main_menu_vspacingVar = config.get("theme", "main_menu_vspacing")
  use_solo_submenu = config.get("theme", "use_solo_submenu")
  sub_menu_xVar = config.get("theme", "sub_menu_x")
  sub_menu_yVar = config.get("theme", "sub_menu_y")
  songback = config.get("theme", "songback")
  versiontag = config.get("theme", "versiontag")
  shadowoffsetx = config.get("theme", "shadowoffsetx")
  shadowoffsety = config.get("theme", "shadowoffsety")

def setupLobby(config):
  global controlActivateX, controlActivateY, controlActivateScale, controlActivateFont, controlCheckTextY
  global controlActivateSelectX, controlActivatePartX, controlActivateSpace, controlActivatePartSize
  global controlDescriptionX, controlDescriptionY, controlDescriptionScale, controlDescriptionFont, controlCheckSpace
  global controlCheckX, controlCheckY, controlCheckScale, controlCheckPartMult, controlCheckFont, lobbyPreviewX
  global lobbyTitleX, lobbyTitleY, lobbyTitleScale, lobbyTitleCharacterX, lobbyTitleCharacterY, lobbySelectScale
  global lobbySelectImageX, lobbySelectImageY, lobbySelectSpace, characterCreateHelpY, lobbyPreviewY
  global lobbyTitleFont, lobbySelectX, lobbySelectY, lobbySelectFont, characterCreateX, characterCreateY
  global characterCreateOptionX, characterCreateScale, characterCreateSpace, characterCreateHelpFont
  global characterCreateOptionFont, characterCreateHelpX, characterCreateHelpScale
  global characterCreateFontColor, characterCreateSelectColor, characterCreateHelpColor
  global lobbyFontColor, lobbySelectColor, lobbyDisableColor, lobbyTitleColor, lobbyInfoColor, lobbyPlayerColor
  global lobbySelectLength, lobbyMode, lobbyPreviewSpacing, lobbyAvatarX, lobbyAvatarY, lobbyAvatarScale
  
  controlActivateX = config.get("theme", "control_activate_x")
  controlActivateSelectX = config.get("theme", "control_activate_select_x")
  controlActivatePartX = config.get("theme", "control_activate_part_x")
  controlActivateY = config.get("theme", "control_activate_y")
  controlActivateScale = config.get("theme", "control_activate_scale")
  controlActivateSpace = config.get("theme", "control_activate_space")
  controlActivatePartSize = config.get("theme", "control_activate_part_size")
  controlActivateFont = config.get("theme", "control_activate_font")
  controlDescriptionX = config.get("theme", "control_description_x")
  controlDescriptionY = config.get("theme", "control_description_y")
  controlDescriptionScale = config.get("theme", "control_description_scale")
  controlDescriptionFont = config.get("theme", "control_description_font")
  controlCheckX = config.get("theme", "control_check_x")
  controlCheckY = config.get("theme", "control_check_y")
  controlCheckTextY = config.get("theme", "control_check_text_y")
  controlCheckPartMult = config.get("theme", "control_check_part_mult")
  controlCheckScale = config.get("theme", "control_check_scale")
  controlCheckSpace = config.get("theme", "control_check_space")
  controlCheckFont  = config.get("theme", "control_check_font")
  lobbyMode = config.get("theme", "lobby_mode")
  lobbyPreviewX = config.get("theme", "lobby_preview_x")
  lobbyPreviewY = config.get("theme", "lobby_preview_y")
  lobbyPreviewSpacing = config.get("theme", "lobby_preview_spacing")
  lobbyTitleX = config.get("theme", "lobby_title_x")
  lobbyTitleY = config.get("theme", "lobby_title_y")
  lobbyTitleCharacterX = config.get("theme", "lobby_title_character_x")
  lobbyTitleCharacterY = config.get("theme", "lobby_title_character_y")
  lobbyTitleScale = config.get("theme", "lobby_title_scale")
  lobbyTitleFont = config.get("theme", "lobby_title_font")
  lobbyAvatarX = config.get("theme", "lobby_avatar_x")
  lobbyAvatarY = config.get("theme", "lobby_avatar_y")
  lobbyAvatarScale = config.get("theme", "lobby_avatar_scale")
  lobbySelectX = config.get("theme", "lobby_select_x")
  lobbySelectY = config.get("theme", "lobby_select_y")
  lobbySelectImageX = config.get("theme", "lobby_select_image_x")
  lobbySelectImageY = config.get("theme", "lobby_select_image_y")
  lobbySelectScale = config.get("theme", "lobby_select_scale")
  lobbySelectSpace = config.get("theme", "lobby_select_space")
  lobbySelectFont = config.get("theme", "lobby_select_font")
  lobbySelectLength = config.get("theme", "lobby_select_length")
  lobbyTitleColor = hexToColor(config.get("theme", "lobby_title_color"))
  lobbyInfoColor = hexToColor(config.get("theme", "lobby_info_color"))
  lobbyFontColor = hexToColor(config.get("theme", "lobby_font_color"))
  lobbyPlayerColor = hexToColor(config.get("theme", "lobby_player_color"))
  lobbySelectColor = hexToColor(config.get("theme", "lobby_select_color"))
  lobbyDisableColor = hexToColor(config.get("theme", "lobby_disable_color"))
  characterCreateX = config.get("theme", "character_create_x")
  characterCreateY = config.get("theme", "character_create_y")
  characterCreateOptionX = config.get("theme", "character_create_option_x")
  characterCreateFontColor = hexToColor(config.get("theme", "character_create_font_color"))
  characterCreateSelectColor = hexToColor(config.get("theme", "character_create_select_color"))
  characterCreateHelpColor = hexToColor(config.get("theme", "character_create_help_color"))
  characterCreateHelpX = config.get("theme", "character_create_help_x")
  characterCreateHelpY = config.get("theme", "character_create_help_y")
  characterCreateHelpScale = config.get("theme", "character_create_help_scale")
  characterCreateOptionFont = config.get("theme", "character_create_option_font")
  characterCreateHelpFont = config.get("theme", "character_create_help_font")
  characterCreateScale = config.get("theme", "character_create_scale")
  characterCreateSpace = config.get("theme", "character_create_space")

def setupTWOD(config):
  global twoDnote, twoDkeys, threeDspin, opencolor
  global noterotdegrees, noterot
  
  twoDnote = config.get("theme", "twoDnote")
  twoDkeys = config.get("theme", "twoDkeys")
  threeDspin = config.get("theme", "threeDspin")
  opencolor = hexToColor(config.get("theme", "opencolor"))
  noterotdegrees = config.get("theme", "noterotdegrees")
  noterot = tuple(config.get("theme", "noterot"+str(i+1)) for i in range(5))


#racer:
def setupFail(config):
  global fail_bkg_pos, fail_text_xPos, fail_text_yPos, fail_songname_xPos, fail_songname_yPos

  fail_bkg_pos = config.get("theme", "fail_bkg").split(",")
  fail_text_xPos = config.get("theme", "fail_text_x")
  fail_text_yPos = config.get("theme", "fail_text_y")
  fail_songname_xPos = config.get("theme", "fail_songname_x") 
  fail_songname_yPos = config.get("theme", "fail_songname_y") 

def setupRockmeter(config):
  global rmtype

  rmtype = config.get("theme", "rmtype")

def setupEvilynux(config):
  global songlist_score_colorVar, songlistcd_score_colorVar, rockmeter_score_colorVar, ingame_stats_colorVar

  songlist_score_colorVar = config.get("theme", "songlist_score_color")
  songlistcd_score_colorVar = config.get("theme", "songlistcd_score_color")
  rockmeter_score_colorVar = config.get("theme", "rockmeter_score_color")
  ingame_stats_colorVar = config.get("theme", "ingame_stats_color")

    
def setupHopoIndicator(config):
  global hopoIndicatorX, hopoIndicatorY
  global hopoIndicatorActiveColor, hopoIndicatorInactiveColor
  
  hopoIndicatorX = config.get("theme", "hopo_indicator_x")
  hopoIndicatorY = config.get("theme", "hopo_indicator_y")  
  hopoIndicatorActiveColor = hexToColor(config.get("theme", "hopo_indicator_active_color"))
  hopoIndicatorInactiveColor = hexToColor(config.get("theme", "hopo_indicator_inactive_color"))
  
def setupResults(config):
  global result_score, result_star, result_song, result_song_text, result_song_form, result_stats_part, result_stats_diff
  global result_stats_diff_text, result_stats_part_text, result_stats_streak_text, result_stats_accuracy_text
  global result_stats_accuracy, result_stats_streak, result_stats_notes, result_stats_notes_text
  global result_cheats_info, result_cheats_numbers, result_cheats_percent, result_cheats_score, result_cheats_color
  global result_menu_x, result_menu_y, result_star_type, result_stats_name, result_cheats_font, result_high_score_font
  
  result_score = config.get("theme", "result_score").split(",")
  result_star = config.get("theme", "result_star").split(",")
  result_song = config.get("theme", "result_song").split(",")
  result_song_form = config.get("theme", "result_song_form")
  result_song_text = config.get("theme", "result_song_text").strip()
  result_stats_part = config.get("theme", "result_stats_part").split(",")
  result_stats_part_text = config.get("theme", "result_stats_part_text").strip()
  result_stats_name = config.get("theme", "result_stats_name").split(",")
  result_stats_diff = config.get("theme", "result_stats_diff").split(",")
  result_stats_diff_text = config.get("theme", "result_stats_diff_text").strip()
  result_stats_accuracy = config.get("theme", "result_stats_accuracy").split(",")
  result_stats_accuracy_text = config.get("theme", "result_stats_accuracy_text").strip()
  result_stats_streak = config.get("theme", "result_stats_streak").split(",")
  result_stats_streak_text = config.get("theme", "result_stats_streak_text").strip()
  result_stats_notes = config.get("theme", "result_stats_notes").split(",")
  result_stats_notes_text = config.get("theme", "result_stats_notes_text").strip()
  result_cheats_info = config.get("theme", "result_cheats_info").split(",")
  result_cheats_numbers = config.get("theme", "result_cheats_numbers").split(",")
  result_cheats_percent = config.get("theme", "result_cheats_percent").split(",")
  result_cheats_score   = config.get("theme", "result_cheats_score").split(",")
  result_cheats_color   = config.get("theme", "result_cheats_color")
  result_cheats_font    = config.get("theme", "result_cheats_font")
  result_high_score_font = config.get("theme", "result_high_score_font")
  result_menu_x         = config.get("theme", "result_menu_x")
  result_menu_y         = config.get("theme", "result_menu_y")
  result_star_type      = config.get("theme", "result_star_type")

def setupSubmenus(config, themepath = None):
  if not themepath:
    return
  global submenuScale, submenuX, submenuY, submenuVSpace
  allfiles = os.listdir(themepath)
  submenuScale = {}
  submenuX = {}
  submenuY = {}
  submenuVSpace = {}
  listmenu = []
  for name in allfiles:
    if os.path.splitext(name)[1] == ".png":
      if name.find("text") > -1:
        found = os.path.splitext(name)[0]
        if found == "maintext":
          continue
        Config.define("theme", found, str, None)
        submenuScale[found] = None
        submenuX[found] = None
        submenuY[found] = None
        submenuVSpace[found] = None
        listmenu.append(found)
  for i in listmenu:
    if i == "maintext":
      continue
    try:
      submenuX[i] = config.get("theme", i).split(",")[0].strip()
    except IndexError:
      submenuX[i] = None
    try:
      submenuY[i] = config.get("theme", i).split(",")[1].strip()
    except IndexError:
      submenuY[i] = None
    try:
      submenuScale[i] = config.get("theme", i).split(",")[2].strip()
    except IndexError:
      submenuScale[i] = None
    try:
      submenuVSpace[i] = config.get("theme", i).split(",")[3].strip()
    except IndexError:
      submenuVSpace[i] = None
  
