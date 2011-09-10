# -*- coding: utf-8 -*-
# See LICENSE.txt for licensing terms
#$HeadURL: https://rst2pdf.googlecode.com/svn/tags/0.16/rst2pdf/nodehandlers.py $
#$LastChangedDate: 2009-12-05 01:09:59 -0300 (Sat, 05 Dec 2009) $
#$LastChangedRevision: 1588 $

# Import all node handler modules here.
# The act of importing them wires them in.

import genelements
import genpdftext

#sphinxnodes needs these
from genpdftext import NodeHandler, FontHandler, HandleEmphasis

# createpdf needs this
nodehandlers = NodeHandler()
