#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gimpfu import *
import os
"""=========================================================="""
##  Copyright 25 Feb 2018  @Doyousketch2  <doyousketch2@yahoo.com>
##  GNU GPL v3 - http://www.gnu.org/licenses/gpl-3.0.html
"""=========================================================="""
##  Place script in directory that suits your OS:
##
##  /home/yourname/.gimp-2.8/plug-ins
##  /usr/share/gimp/2.0/plug-ins
##  ~/Library/Application/Support/GIMP/2.8/plug-ins
##
##  C:\Users\yourname\.gimp-2.8\plug-ins
##  C:\Program Files\GIMP 2\share\gimp\2.0\plug-ins
##  C:\Documents and Settings\yourname\.gimp-2.8\plug-ins
##
##  If needed, set file permissions to allow script execution
##  chmod +x eawb.py
"""=========================================================="""

def split( img, draw, w, h, pad, subdir ):
  ## group entire procedure within one undo command
  pdb .gimp_image_undo_group_start( img )

  sourcename  = pdb .gimp_image_get_filename(img)
  basedir  = os .path .dirname(sourcename)
  subdirname  = os .path .join(basedir, subdir)

  if not os .path .isdir(subdirname):
    os .mkdir(subdirname)

  j = 1
  y = 0
  while (y +h <= pdb .gimp_image_height(img)):

    subsub  = os .path .join(subdirname, str(j))
    if not os .path .isdir(subsub):
      os .mkdir(subsub)

    i = 1
    x = 0
    while (x +w <= pdb .gimp_image_width(img)):

      pdb .gimp_image_select_rectangle( img, CHANNEL_OP_REPLACE, x, y, w, h )
      pdb .gimp_edit_cut( draw )

      newimage  = pdb .gimp_edit_paste_as_new()
      drawable  = pdb .gimp_image_active_drawable(newimage)

      filename  = str(j) +'_' +str(i) +'.png'
      fullpath  = os .path .join(subsub, filename)

      pdb .file_png_save_defaults(newimage, drawable, fullpath, filename)
      x  = x +w +pad
      i += 1
    y  = y +h +pad
    j += 1

  ##  close up undo group, then refresh display
  pdb .gimp_image_undo_group_end( img )
  pdb .gimp_displays_flush()


register (
        "tile_splitter",  ##  commandline
        "Splits tiles",   ##  blurb
        "Tell it tile size, & padding between pixels, then split em",  ##  help

        "Doyousketch2",   ##  author
        "GNU GPL v3",     ##  copyright
        "25 Feb 2018",    ##  date

        "<Image>/Filters/Map/Tile Splitter...",  ##  menu location
        "RGB*",           ##  image types
        [ ## type, "var",  "gui label", default, (min, max, step)

          (PF_SLIDER, "w", "Tile Width", 64, (2, 128, 2) ),
          (PF_SLIDER, "h", "Tile Height", 64, (2, 128, 2) ),
          (PF_SLIDER, "pad", "Padding between tiles", 2, (0, 20, 1) ),
          (PF_STRING, "subdir", "Subdir", "output"),

        ],               ##  parameters
        [],              ##  results
        split )   ##  name of function

main()

