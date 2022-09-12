# This is the PyMTL wrapper for the corresponding Verilog RTL model RegIncVRTL.

from pymtl3 import *
from pymtl3.stdlib import stream
from pymtl3.passes.backends.verilog import *


class RegIncRTL( VerilogPlaceholder, Component ):

  # Constructor

  def construct( s ):
    # If translated into Verilog, we use the explicit name

    s.set_metadata( VerilogTranslationPass.explicit_module_name, 'RegIncRTL' )

    # Interface
    s.recv = stream.ifcs.RecvIfcRTL( Bits32 )
    s.send = stream.ifcs.SendIfcRTL( Bits32 )


RegInc = RegIncRTL
