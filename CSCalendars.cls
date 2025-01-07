%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Creodocs Calendars
% LaTeX Class
% Version 1.0 (January 5, 2025)
%
% This class originates from:
% https://www.LaTeXTemplates.com
%
% Author:
% Vel (vel@latextemplates.com)
%
% License:
% CC BY-NC-SA 4.0 (https://creativecommons.org/licenses/by-nc-sa/4.0/)
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%----------------------------------------------------------------------------------------
%	CLASS CONFIGURATION
%----------------------------------------------------------------------------------------

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{CSCalendars}[2025/01/05 Creodocs Calendars Class v1.0]

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{extarticle}} % Pass through any extra options specified to the base class
\ProcessOptions\relax % Process class options

\LoadClass{extarticle} % Load the base class

%----------------------------------------------------------------------------------------
%	REQUIRED PACKAGES AND MISC CONFIGURATIONS
%----------------------------------------------------------------------------------------

\setlength{\parindent}{0pt} % Paragraph indentation
\setlength{\parskip}{6pt} % Vertical space between paragraphs

\pagestyle{empty} % Suppress headers and footers

\usepackage{etoolbox} % Required for conditional logic

%----------------------------------------------------------------------------------------
%	MARGINS
%----------------------------------------------------------------------------------------

\usepackage[
	landscape, % Landscape paper orientation
	margin=1cm, % Equal margin on all sides
	%showframe % Uncomment to show frames around the margins for debugging purposes
]{geometry}

%----------------------------------------------------------------------------------------
%	FONTS
%----------------------------------------------------------------------------------------

\usepackage[utf8]{inputenc} % Required for inputting international characters
\usepackage[T1]{fontenc} % Output font encoding for international characters

\usepackage{palatino} % Use the Palatino font

%----------------------------------------------------------------------------------------
%	TABLES
%----------------------------------------------------------------------------------------

\setlength{\tabcolsep}{0.0075\textwidth} % Set table column padding to be proportional to text width

\usepackage{array} % Required for manipulating table columns
\renewcommand{\arraystretch}{1.25} % Increase the height of table rows

\newcolumntype{R}[1]{>{\raggedleft\arraybackslash}p{#1}} % Define a new right-aligned paragraph column type
\newcolumntype{L}[1]{>{\raggedright\arraybackslash}p{#1}} % Define a new left-aligned (no justification) paragraph column type
\newcolumntype{C}[1]{>{\centering\arraybackslash}p{#1}} % Define a new centered paragraph column type

%----------------------------------------------------------------------------------------
%	CALENDAR TABLE
%----------------------------------------------------------------------------------------

\newenvironment{calendar}{
	\begin{tabular}{| L{0.1272\textwidth} | L{0.1272\textwidth} | L{0.1272\textwidth} | L{0.1272\textwidth} | L{0.1272\textwidth} | L{0.1272\textwidth} | L{0.1272\textwidth}|} % Column alignments and widths. Widths can be precisely calculated with: ((\textwidth - (\tabcolsep * 14)) - <width of vertical rules>) / 7 (or via trial and error :)).
		\hline % Horizontal rule
		\outputdayoftheweek & \outputdayoftheweek & \outputdayoftheweek & \outputdayoftheweek & \outputdayoftheweek & \outputdayoftheweek & \outputdayoftheweek\\ % Output the days of the week, automatically determined from the setting in the template
		\hline % Horizontal rule
		\hline % Horizontal rule
}{
	\end{tabular}%
}

% NOTE Wasted 2 hours implementing the tabulararray package which makes all the table specifications much easier, but does not allow using \day where inside \day further expansions of commands are needed (such as for \ifnumequal). Basically, you can't use & and \\ inside conditional logic within \day, even if you specify expand=\day. This is the table spec code in case this becomes possible in the future:
%\begin{tblr}[expand=\day]{ % Need to expand \day which contains & characters separating cells
%	colspec={| X | X | X | X | X | X | X |}, % Column widths
%	row{1}={font=\scshape\centering}, % Styling and spacing in the first days of the week row
%	row{2-Z}={ht=2.5cm, valign=h, rowsep=6pt, font=\raggedright}, % Styling and spacing of all subsequent rows
%	hlines = {0.5pt}, % Horizontal rules
%}

%----------------------------------------------------------------------------------------
%	CALENDAR DAYS OF THE WEEK LOGIC
%----------------------------------------------------------------------------------------

\newcounter{startingdayoftheweek} % A counter for working out the current day of the week to output in the calendar table header

\newcommand{\outputdayoftheweek}{
	\ifnumgreater{\value{startingdayoftheweek}}{7}{\setcounter{startingdayoftheweek}{1}}{} % If the counter is >7, set it back to 1 to loop it back to Sunday

	\hfill % For horizontal centering
	\begingroup
		\scshape % Small caps
		\ifnumequal{\value{startingdayoftheweek}}{1}{Sunday}{}%
		\ifnumequal{\value{startingdayoftheweek}}{2}{Monday}{}%
		\ifnumequal{\value{startingdayoftheweek}}{3}{Tuesday}{}%
		\ifnumequal{\value{startingdayoftheweek}}{4}{Wednesday}{}%
		\ifnumequal{\value{startingdayoftheweek}}{5}{Thursday}{}%
		\ifnumequal{\value{startingdayoftheweek}}{6}{Friday}{}%
		\ifnumequal{\value{startingdayoftheweek}}{7}{Saturday}{}%
		\stepcounter{startingdayoftheweek}% Iterate the counter for the next day of the week
	\endgroup
	\hfill~ % For horizontal centering
}

%----------------------------------------------------------------------------------------
%	CALENDAR DAY COMMANDS
%----------------------------------------------------------------------------------------

\newcounter{startingdate} % A counter for the starting date of the month
\newcounter{currentdayofweek} % A counter for the current day of the week (used to know when to transition to a new row)
\setcounter{currentdayofweek}{1} % Always start at 1 no matter what the starting date or day of the week are

\newlength{\dayheight} % Variable holding the height of table day cells
\setlength{\dayheight}{3.25cm} % Set the default height of day cells to fit a month's worth onto a page

\newcommand{\dayheader}[1]{\vspace{2pt}{\small\textit{#1}}} % Command to output a header/section within a day with some whitespace above
\newcommand{\eventskip}{\\\vspace{3pt}} % Vertical whitespace between events within a day
\newcommand{\eventrule}{\strut\\[-0.75\baselineskip]\rule{\linewidth}{0.5pt}\\} % Command to output a separator rule within a day, the \strut is so that all content above the rule has the same vertical height (useful if times are above the rule and have only am values with no descenders)

\renewcommand{\day}[2]{ % Command for outputting a day with a date, the first parameter is for a header such as Social or Work (optional) and the second is for the day's events
	% Output the day cell contents in a parbox to ensure a fixed height for day cells in the table
	\parbox[top][\dayheight][t]{\linewidth}{%
		\vspace{2pt} % Extra vertical whitespace at the top of the day
		\raggedright % Suppress justification
		\scriptsize % Font size
		\dayheader{#1\hfill \normalsize\arabic{startingdate}} \eventskip % Output the header with the (optional) header and (non-optional) current date
		#2 % Output the day events
	}%
	\stepcounter{startingdate}% Iterate the current date
	\ifnumequal{\value{currentdayofweek}}{7}{\setcounter{currentdayofweek}{1}\\\hline}{\stepcounter{currentdayofweek}&}% Logic for whether what comes after this day is a new day (i.e. same row), or a new week (i.e. new row)
}

\newcommand{\blankday}[1]{ % Command for outputting a day without a date. The single parameter can contain content or be used for padding days, e.g. when the first of the month is on a Tuesday you need several empty cells to the left.
	% Output the day cell contents in a parbox to ensure a fixed height for day cells in the table
	\parbox[top][\dayheight][t]{\linewidth}{%
		\vspace{4pt} % Extra vertical whitespace at the top of the day
		\raggedright % Suppress justification
		\scriptsize % Font size
		#1 % Output the day events
	}%
	\ifnumequal{\value{currentdayofweek}}{7}{\setcounter{currentdayofweek}{1}\\\hline}{\stepcounter{currentdayofweek}&}% Logic for whether what comes after this day is a new day (i.e. same row), or a new week (i.e. new row)
}
