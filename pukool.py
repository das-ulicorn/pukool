#!/usr/bin/python
# coding: ascii
#
# This file is part of pukool.
# (c) 2007 Ulrich M. Schwarz
# For license details, see COPYING.
#
# $Id: pukool.py,v 1.2 2007/07/29 08:40:53 ulmi Exp $
import sys
import re

# first is type identifier, second is tried against label name,
# third is tried against hyperref anchor name.
# TODO: put this into external configuration file.
labelpatterns=(
  ("eq", "^eq:", "^equation"),
  ("sec", "^(sec|cha|part)", "(section|^part|^chapter)"),
  ("fig", "^(fig|abb):", "^figure"),
  ("tab", "^tab:", "^table"),
  ("thm", "^thm:", None)
)

# do a DFS through the aux files and collect all lines starting
# with "\newlabel"
def refresh(fnam):
  global labels
  for line in file(fnam, "r").xreadlines():
    matches = labelRE.search(line)
    if matches:
      labels += [matches.groups()]
#      print "match   : %s" % (`matches.groups()`,)
    else:
      matches = inputRE.search(line)
      if matches:
        refresh(matches.group(1))

# take a string and remove all commands and braces.
# this avoids problems with spurious braces and formatting commands.
def sanitize(lbl):
  lbl=re.sub(r'\\[a-zA-Z@]+\s*',"",lbl)
  lbl=re.sub(r'{|}|\(|\)',"",lbl)
  return lbl

def pukool(spec):
  # it's cheap to check if the number is right:
  spec[1]=sanitize(spec[1])
  for label in labels:
    if (spec[1]==sanitize(label[1])): # TODO: normalize label upon read.
      # the number is right.
      # what patterns apply?
      for (kind, labelre, anchorre) in labelpatterns:
        if (kind==spec[0]):
          # this rule applies to this kind of ref.
          if (labelre and re.match(labelre, label[0])) \
             or (label[4] and anchorre \
                 and re.match(anchorre, label[4])):
            
            print "%s" % label[0];
  print "" # mark end of output.

labelRE=re.compile(r'''
  ^\s*
  \\newlabel{(.*?)} # match 1 is label name
  {                 # strip outer braces.
  {(.*?)}{(.*?)}# these are always present: number and page.
  (?:{(.*?)}{(.*?)}{(.*?)})?# these are from hyperref.
  # no, we cannot just kleene over the arguments, since we need the match data.
  }# 
''', re.VERBOSE)

inputRE=re.compile(r'''
^\s*\\@input{(.*?)}
''', re.VERBOSE)

# startup.
if (len(sys.argv) < 2):
  print '''
  This is pukool $Revision: 1.2 $
  
  USAGE: pukool.py mainfile.aux
  
  Send pairs of kind and number into stdin.
  You'll receive a list of matching labels (usually one),
  separated by newlines. To exit, send a blank line.
  
  Example:
  $ ./pukool.py main.aux
  eq 1.3.2
  eq:concurrency
  
  pukool looks at naming conventions for labels (eq:... for equations etc.)
  and at hyperref information if present to determine the kind.
  
  Supported kinds:
 ''',
  for (kind, _,__) in labelpatterns:
    print "%s " % (kind,),
  sys.exit(1)
mainfile = sys.argv[len(sys.argv)-1]
labels=[]
refresh(mainfile)
action = sys.stdin.readline().split()
while (len(action)):
  #  print "Eingabe:>%s<" % action[0]
  if len(action)!=2:
    pass
  else:
    pukool(action)
  action = sys.stdin.readline().split()

#$Id: pukool.py,v 1.2 2007/07/29 08:40:53 ulmi Exp $
