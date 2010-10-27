""" Groovy language parser for gedit's class browser plugin """

# Robert Zakrzewski (zakrzewski.robert@gmail.com)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, 
# Boston, MA 02111-1307, USA.

import gtk
import gobject
import re

import pango
import options
from parserinterface import ClassParserInterface
import imagelibrary

#---------------------------------------------------------------------------
# Regular expressions definitions
EXP = r".*?"                                # anything, but *not greedy*
EXP += "(?: +)"                             # default (public) visibility
EXP += "(\w+)[ \t]+(\w+)(\(.*\))"           # function declaration
EXP += " *\{$"                              # the tail
RE_PUB_METHOD = re.compile(EXP)

EXP = r".*?"                                # anything, but *not greedy*
EXP += "(?:(public|private|protected) +)"   # visibility, must be given
EXP += "(\w+)[ \t]+(\w+)(\(.*\))"           # function declaration
EXP += " *\{$"                              # the tail
RE_METHOD = re.compile(EXP)

EXP = r".*?"                # anything, but *not greedy*
EXP += "def +(\w+)(\(.*\))" # method by def declaration
EXP += " *\{$"              # the tail
RE_DEF_METHOD = re.compile(EXP)

EXP = r".*?"            # anything, but *not greedy*
EXP += "def +(\w+)"     # closure declaration
EXP += " *= *\{$"       # the tail
RE_CLOSURE = re.compile(EXP)

RE_CLASS = re.compile(r".*class +(\w+)(?: +extends +(\w+))? *\{$")

RE_PACKAGE = re.compile(r".*package +((?:(?:((?![0-9_])[a-zA-Z0-9_]+)\.?)+)(?<!\.))")
        
#---------------------------------------------------------------------------
# Helper classes
class Token:
    """ Represents any tree node with information about groovy elements """
    def __init__(self, tp):
        self.type = tp
        self.name = None
        self.params = None
        self.retvaluetype = None
        self.visibility = None

        self.uri = None
        self.start = None
        self.end = None

        self.parent = None
        self.children = [] # a list of nested tokens

    def append(self, child):
        """ Append child node to this node """
        child.parent = self
        self.children.append(child)
        
    def __str__(self):
        return str(self.type) + " " + str(self.name)


#---------------------------------------------------------------------------
class _DummyToken:
    """ Represents dummy/fake node of the tree. Dummy nodes are not loeded into the tree """
    def __init__(self):
        self.parent = None
        self.children = [] # a list of nested tokens
        
    def append(self, child):
        """ append child node to this dummy node. Childs do not render too """
        child.parent = self
        self.children.append(child)
        
        
#---------------------------------------------------------------------------        
class GroovyParser( ClassParserInterface ):
    """ This class provides Groovy files parsing """
    def __init__(self):
        self.initializedExpandAll = False
        self.verbose = False

    def getTokenFromChunk(self, chunk):
        if self.verbose: print "CHUNK: %s " % chunk
        # third step: perform regular expression to get a token
        match = re.match(RE_METHOD, chunk)
        if match:
            t = Token("function")
            if self.verbose: print "METHOD: %s" % str(match.groups())
            t.visibility, retVal, t.name, t.params = match.groups()
            return t
        
        match = re.match(RE_PUB_METHOD, chunk)
        if match:
            t = Token("function")
            if self.verbose: print "METHOD: %s" % str(match.groups())
            retVal, t.name, t.params = match.groups()
            return t
        
        match = re.match(RE_DEF_METHOD, chunk)
        if match:
            t = Token("function")
            if self.verbose: print "CLOSURE: %s" % str(match.groups())
            t.visibility = "public"
            t.name, t.params = match.groups()
            return t
                
        match = re.match(RE_CLOSURE, chunk)
        if match:
            t = Token("member")
            if self.verbose: print "CLOSURE: %s" % str(match.groups())
            t.name = match.group(1)
            return t
                    
        match = re.match(RE_CLASS,chunk)
        if match:
            if self.verbose: print "CLASS: %s" % str(match.groups())
            t = Token("class")
            t.name, t.params = match.groups()
            return t
        
        return None

    def getTokenBackwards(self, string, position ):
        """ Iterate a string backwards from a given position to get token.""" 
        
        # first step: get chunk where definition must be located
        # get substring up to a key character
        i = position
        while i > 0:
            i-=1
            if string[i] in ";}{/": # "/" is for comment endings
                break
        
        # remove dirt
        chunk = string[i:position+1].strip()
        chunk = chunk.replace("\n"," ")
        chunk = chunk.replace("\r"," ")
        chunk = chunk.replace("\t"," ")
        
        return self.getTokenFromChunk(chunk)
        
        
    def parse(self, doc):
        # on first parse set autoexpandable setting
        if not self.initializedExpandAll:
			if options.singleton():
				options.singleton().autocollapse = False
			# the next calls should behave inline with user's settings
			self.initializedExpandAll = True
        text = doc.get_text(*doc.get_bounds())
        # create top level node that is required by tree
        root = Token("root")
        parent = self.__get_toplevel_package(root, text, doc.get_uri())
        self.__get_tokens(parent, text, doc.get_uri())
        self.__browsermodel = gtk.TreeStore(gobject.TYPE_PYOBJECT)
        for child in root.children: self.__appendTokenToBrowser(child,None)
        return self.__browsermodel
        
    def cellrenderer(self, column, ctr, model, it):
        """ Render the browser cell according to the token it represents. """
        tok = model.get_value(it,0)
        name = tok.name
        colour = options.singleton().colours[ "function" ]
        if tok.type == "class":
            name = "class "+tok.name
            colour = options.singleton().colours[ "class" ]
        if self.verbose: print "RENDERING CELL NAME=%s" % str(name)
        ctr.set_property("text", name)
        ctr.set_property("foreground-gdk", colour)

    def pixbufrenderer(self, column, crp, model, it):
        tok = model.get_value(it,0)
        if tok.type == "class":
            icon = "class"
        else:
            if tok.visibility == "private": icon = "method_priv"
            elif tok.visibility == "protected": icon = "method_prot"
            else: icon = "method"
        crp.set_property("pixbuf",imagelibrary.pixbufs[icon])
            
    def get_tag_position(self, model, path):
        tok = model.get_value( model.get_iter(path), 0 )
        try: return tok.uri, tok.start+1
        except: pass

    def __appendTokenToBrowser(self, token, parentit ):
        if token.__class__ == _DummyToken: return
        it = self.__browsermodel.append(parentit,(token,))
        token.path = self.__browsermodel.get_path(it)
        for child in token.children:
            self.__appendTokenToBrowser(child, it)

    def __get_toplevel_package(self, parent, string, uri):
        linecount = -1
        for line in string.splitlines():
            if self.verbose: print "PACKAGE CHUNK: %s" % line
            linecount += 1
            lstrip = line.lstrip()
            if len(lstrip) == 0:
                # skip empty lines
                continue
            match = re.match(RE_PACKAGE, string)
            if match:
                if self.verbose: print "PACKAGE: %s" % str(match.groups())
                t = Token("namespace")
                # get first group from the match
                t.name = match.group(1)
                if self.verbose: print "PACKAGE NAME=%s" % t.name
                t.uri = uri
                t.start = linecount
                if parent:
                    parent.append(t)
                return t
            else:
                break
        return parent
                
    def __get_tokens(self, parent, string, uri):
        firstParent = parent
        ident = 0
        
        if self.verbose: print "-"*80
        
        line = 0 # count lines
        commentStarted = False
        onelineComment = False
        multilineComment = False
        # search for starting bracket
        stringLen = len(string)
        for i in range(len(string)-1):
        
            c = string[i]
            
            # handle comments: oneline and multiline
            if onelineComment:
                if c == "\n":
                    # end of oneline comment
                    onelineComment = False
                    line += 1
                continue
            elif multilineComment:
                if c == "\n":
                    # increment line number but do not stop comment section
                    line += 1
                    continue
                elif c == "*" and i < stringLen - 1 and string[i+1] == "/":
                    # end of multiline comment
                    multilineComment = False
                else:
                    # skip to the end of comment
                    continue
                    
            
            if c == "{": #------------------------------------------------------
            
                # get a token from the chunk of code preceding the bracket
                token = self.getTokenBackwards( string, i )
                
                if token:
                    # assign line number and uri to the token
                    token.uri = uri
                    token.start = line
                    
                else:
                    # dummy token for empty brackets. Will not get added to tree.
                    token = _DummyToken()
                    
                # append the token to the tree
                parent.append(token)
                parent = token

                ident += 1
                
                commentStarted = False
                
            elif c == "}": #----------------------------------------------------
                ident -= 1
                if parent != firstParent:
                    parent.end = line
                    parent = parent.parent
                    
                commentStarted = False
                
            elif c == "/": #----------------------------------------------------
                if commentStarted:
                    onelineComment = True
                    commentStarted = False
                else:
                    commentStarted = True
            elif c == "*":
                if commentStarted:
                    multilineComment = True
                    commentStarted = False
            elif c == "\n":
                line += 1
                
                commentStarted = False
            else:
				commentStarted = False
                
        return firstParent
        


