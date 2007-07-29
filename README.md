# PUKOOL

Find label information by the printed output number.

How many times have you cursed equation labels because they're either
cryptic or longer than the equation itself? Curse no more, with pukool, you
can specify equations by the one thing you're most likely to have: the
equation number in the dvi or pdf file. (Well, actually, the one in the .aux
files, so beware of those "Labels may have changed" messages.)

The only thing you need to do is to adhere to the usal naming conventions:
start equation labels with eq:, section labels with sec:, figures with fig:
and tables with tab: (so pukool won't mistake figure 1 for equation 1) and
you're all set. If you use hyperref, you don't even need to do that: pukool
will look at anchor information provided by hyperref.

Some notes of warning:

* you can't get the label name if your equation doesn't actually have a
  label. (Well, duh.)
  
* if the number is not unique throughout your document, pukool will return
  all matches, because it'll be just as confused as your reader when there
  are several "figure 1"s.
  
* some packages write the numbers in an unusual way. For example, what reads
  "Theorem 1.1" in your document is written as 1.{1} if you use the ntheorem
  package. Looking up 1.1 hence won't give results. pukool tries to remove
  braces, parentheses and commands from both your number and the number in the 
  aux file.
  
* numbers undergo a certain amount of processing on their way to the aux file.
  Sure, you can number your equations with \fnsymbols, but I don't think any
  of it will survive pukools command filter. (You wouldn't like to type
  \ifmmode\mathdagger\else\textdagger\fi to look up your equation anyway.)

## INSTALLATION & REQUIREMENTS:

Make sure you have Python installed. (This is all so old, I guess it was Python 2.4 at the time?)

## USAGE: 

    pukool.py mainfile.aux
  
Send pairs of kind and number into stdin.
You'll receive a list of matching labels (usually one),
separated by newlines. To exit, send a blank line.
  
## EXAMPLE:

    $ ./pukool.py main.aux
    eq 1.3.2
    eq:concurrency
  
## TODO:

* have proper configuration file…

*  maybe have a way of rereading the aux files at runtime. OTOH, starting
  python anew is not very expensive.

