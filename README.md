Gedit Grails Bundle 
====================

This Bundle aims to augment the default editor for the Gnome Desktop Environment
to improve its efficiency specifically as a tool for Groovy/Grails development.

Features
--------

- Syntax Highlighting
- Various autoCompletion tools
- Command Line helpers and scripts
- Themes

Installation
------------

- Install script included (only tested in Ubuntu 10.04)
- Manually install plugins and styles by placing in ~/.gnome2/gedit file 

History
-------

12/29/09 - 
  updating install script to automatically insert plugins and snippets as 
  described above. choose autoComplete plugin over word completion because it 
  doesn't conflict with the snippets plugin. still trying to find where to put 
  grails tags now. Currently it is a mystery they and won't show up inside of 
  gedit. considering getting rid of them and focusing on improving snippets.

12/30/09 - 
  improving by small degrees the groovy.lang file for groovy syntax highlighting.

01/06/10 - 
  updating snippets - add/re-adding couple plugins - slightly modded oblivion 
  color scheme. Should do "sudo apt-get install ack-grep" if you want to have a 
  faster find in files plugin.

03/16/10 - 
  updating snippets - clones of html and js snippets for use in gsp's, and java 
  snippets for use in groovy files. found the ctrl+space helper for snippet 
  suggestions.
  
09/13/10 - 
  updating g:tags, and install script for them. adding gred script from Marco - 
  http://mycodesnippets.com/2010/05/15/edit-grails-files-with-gedit-and-gred-on-linux/
  will still need to manuallyadd export EDITOR="/usr/bin/gedit" to your ~/.bashrc 
  file. 
  added zen-coding-plugin and inherited it's licence as well. modified to not
  conflict with snap-open plugin 
  
10/10/10 - 
  add groovy++ (.gpp) to get groovy syntax highlighting too.

27/10/10
  add classbrowser plugin with groovy support
