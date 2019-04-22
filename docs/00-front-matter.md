# Abstract

The MDL programming language began existence in late 1970 (under the 
name Muddle) as a successor to Lisp (Moon, 1974), a candidate vehicle 
for the Dynamic Modeling System, and a possible base for 
implementation of Planner (Hewitt, 1969). The original design goals 
included an interactive integrated environment for programming, 
debugging, loading, and editing: ease in learning and use; facilities 
for structured, modular, shared programs; extensibility of syntax, 
data types and operators: data-type checking for debugging and 
optional data-type declarations for compiled efficiency; associative 
storage, coroutining, and graphics. Along the way to reaching those 
goals, it developed flexible input/output (including the ARPA 
Network), and flexible interrupt and signal handling. It now serves as 
a base for software prototyping, research, development, education, and 
implementation of the majority of programs at MIT-DMS: a library of 
sharable modules, a coherent user interface, special research 
projects, autonomous daemons, etc.

This document was originally intended to be a simple low-level 
introduction to MDL. It has, however, acquired a case of elephantiasis 
and now amounts to a discursive description of the whole interpreter, 
as realized in MDL release numbers 55 (ITS version) and 105 (Tenex and 
Tops-20 versions). (Significant changes from the previous edition are 
marked in the margin.) A low-level introduction may still be had by 
restricting one's attention to specially-marked sections only. The 
scope of the document is confined as much as possible to the 
interpreter itself. Other adjuncts (compiler, assembler, pre-loaded 
user programs, library) are mentioned as little as possible, despite 
their value in promoting the language seen by a user from "basic 
survival" to "comfortable living". Indeed, MDL could not fulfill the 
above design goals without the compiler, assembler, structure editor, 
control-stack printer, context printer, pretty-printer, dynamic 
loader, and library system -- all of which are not part of the 
interpreter but programs written in MDL and symbiotic with one 
another. Further information on these adjuncts can be found in 
Lebling's (1979) document.

## Acknowledgements

I was not a member of the original group which labored for two years 
in the design and initial implementation of Muddle; that group was 
composed principally of Gerald Sussman, Carl Hewit, Chris Reeve, Dave 
Cressey, and later Bruce Daniels. I would therefore like to take this 
opportunity to thank my Muddle mentors, chiefly Chris Reeve and Bruce 
Daniels, for remaining civil through several months of verbal 
badgering. I believe that I learned more than "just another 
programming language" in learning Muddle, and I am grateful for this 
opportunity to pass on some of that knowledge. What I cannot pass on 
is the knowledge gained by using Muddle as a system; that I can only 
ask you to share.

For editing the content of this document and correcting some 
misconceptions, I would like to thank Chris Reeve, Bruce Daniels, and 
especially Gerald Sussman, one of whose good ideas I finally did use.

Greg Pfister  
December 15, 1972

Since Greg left the fold, I have taken up the banner and updated his 
document. The main sources for small revisions have been the on-line 
file of changes to MDL, for which credit goes to Neal Ryan as well as 
Reeve and Daniels, and the set of on-line abstracts for interpreter 
Subroutines, contributed by unnamed members of the Programming 
Technology Division. Some new sections were written almost entirely by 
others: Dave Lebling wrote chapter 14 and appendix 3, Jim Michener 
section 14.3, Reeve chapter 19 and appendix 1, Daniels and Reeve 
appendix 2. Brian Berkowitz section 22.7, Tak To section 17.2.2, and 
Ryan section 17.1.3. Sue Pitkin did the tedious task of marking 
phrases in the manuscript for indexing. Pitts Jarvis and Jack Haverty 
advised on the use of PUB and the XGP. Many PTD people commented 
helpfully on a draft version.

My task has been to impose some uniformity and structure on these 
diverse resources (so that the result sounds less like a dozen hackers 
typing at a dozen terminals for a dozen days) and to enjoy some of the 
richness of MDL from the inside. I especially thank Chris Reeve ("the 
oracle") for the patience to answer questions and resolve doubts, as 
he no doubt as done innumerable times before.

S. W. Galley  
May 23, 1979

This work was supported by the Advanced Research Projects Agency of 
the Department of Defense and was monitored by the Office of Naval 
Research under contract N00014-75-C-0661.

This document was prepared using [the PUB
system](http://www.nomodes.com/pub_manual.html) (originally from the
Stanford Artificial Intelligence Laboratory) and printed on the Xerox
Graphics Printer of the M.I.T. Artificial Intelligence Laboratory.

## Foreword

Trying to explain MDL to an uninitiate is somewhat like trying to 
untie a Gordian knot. Whatever topic one chooses to discuss first, 
full discussion of it appears to imply discussion of everything else. 
What follows is a discursive presentation of MDL in an order 
apparently requiring the fewest forward references. It is not perfect 
in that regard; however, if you are patient and willing to accept a 
few, stated things as "magic" until they can be explained better, you 
will probably not have too many problems understanding what is going 
on.

There are no "practice problems"; you are assumed to be learning MDL 
for some purpose, and your work in achieving that purpose will be more 
useful and motivating than artificial problems. In several cases, the 
examples contain illustrations of important points which are not 
covered in the text. Ignore examples at your peril.

This document does not assume knowledge of any specific programming
language on your part. However, "computational literacy" is assumed:
you should have written at least one program before. Also very little
familiarity is assumed with the interactive time-sharing operating
systems under which Muddle runs -- ITS, Tenex, and Tops-20 -- namely
just file and user naming conventions.

### Notation

Sections marked [1] are recommended for any uninitiate's first 
reading, in lieu of a separate introduction for MDL. [On first 
reading, text within brackets like these should be ignored.]

Most specifically indicated examples herein are composed of pairs of 
lines. The first line of a pair, the input, always ends in `$` (which 
is how the ASCII character <kbd>ESC</kbd> is represented, and which 
always represents it). The second line is the result of MDL's 
groveling over the first. If you were to type all the first lines at 
MDL, it would respond with all the second lines. (More exactly, the 
"first line" is one or more objects in MDL followed by `$`, and the 
"second line" is everything up to the next "first line".)

Anything which is written in the MDL language or which is typed on a 
computer terminal appears herein in a fixed width font, as in 
`ROOT`. A metasyntactic variable -- something to be replaced in actual 
use by something else -- appears as *radix:fix*, in an italic font; 
often the variable will have both a meaning and a data type (as here), 
but sometimes one of those will be ommitted, for obvious reasons.

An ellipsis (...) indicates that something uninteresting has been 
omitted. The character `^` means that the following character is to be 
"controllified": it is usually typed by holding down a terminal's 
<kbd>CTRL</kbd> key and striking the other key.
