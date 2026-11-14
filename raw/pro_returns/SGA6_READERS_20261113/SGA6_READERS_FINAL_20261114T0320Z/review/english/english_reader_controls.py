"""Shared single-master reader, apparatus and original-note controls."""
READER_CONTROLS = r'''
% Single annotated master; 0 diplomatic, 1 corrected with apparatus, 2 reading.
\providecommand{\SGAReaderForm}{1}
\newcommand{\SGACaptureAppState}[1]{\csname SGACapture@#1\endcsname}
\newcommand{\SGARestoreAppState}[1]{\csname SGARestore@#1\endcsname}
\newcommand{\SGAAppMark}[1]{\ifmmode{}^{[\text{\csname SGAAppNumber@#1\endcsname}]}\else\textsuperscript{[\csname SGAAppNumber@#1\endcsname]}\fi}
\long\def\var#1#2#3{\SGACaptureAppState{#3}\ifnum\SGAReaderForm=0 #1\else #2\ifnum\SGAReaderForm=1\SGAAppMark{#3}\fi\fi}
\expandafter\def\csname SGABlankPrintPage@IV\endcsname{}
\expandafter\def\csname SGABlankPrintPage@VI\endcsname{}
\expandafter\def\csname SGABlankPrintPage@X\endcsname{}
\expandafter\def\csname SGABlankPrintPage@690\endcsname{}
\expandafter\def\csname SGABlankPrintPage@rear-715\endcsname{}
\expandafter\def\csname SGABlankPrintPage@rear-716\endcsname{}
\newcommand{\SGAPrintPage}[1]{\ifcsname SGABlankPrintPage@#1\endcsname\else\ifnum\SGAReaderForm=2\ifmmode\hbox{\marginnote{\scriptsize #1}}\else\marginnote{\scriptsize #1}\fi\else\leavevmode\textsuperscript{\scriptsize[print #1]}\fi\fi}
\expandafter\def\csname SGAAuthorLabel@raisedstar\endcsname{(\textsuperscript{*})}
\expandafter\def\csname SGAAuthorLabel@unmarked\endcsname{}
\newcommand{\SGAAuthorLabel}[1]{\ifcsname SGAAuthorLabel@#1\endcsname\csname SGAAuthorLabel@#1\endcsname\else(#1)\fi}
\makeatletter
\newcommand{\SGAAuthorFootnote}[2]{\begingroup\renewcommand{\thefootnote}{#1}\def\@makefnmark{\hbox{\normalfont\SGAAuthorLabel{#1}}}\def\@makefntext##1{\parindent1em\noindent\hb@xt@1.8em{\@makefnmark\hss}##1}\footnote{#2}\endgroup}
\newcommand{\SGAAuthorFootMark}[1]{\begingroup\renewcommand{\thefootnote}{#1}\def\@makefnmark{\hbox{\normalfont\SGAAuthorLabel{#1}}}\footnotemark[\value{footnote}]\endgroup}
\newcommand{\SGAAuthorFootText}[2]{\begingroup\renewcommand{\thefootnote}{#1}\def\@makefnmark{\hbox{\normalfont\SGAAuthorLabel{#1}}}\def\@makefntext##1{\parindent1em\noindent\hb@xt@1.8em{\@makefnmark\hss}##1}\footnotetext[\value{footnote}]{#2}\endgroup}
\makeatother
'''
