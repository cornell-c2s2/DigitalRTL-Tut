#=========================================================================
# RegInc_test
#=========================================================================

import pytest
import random
import struct

random.seed(0xdeadbeef)

from pymtl3 import *
from pymtl3.stdlib import stream
from pymtl3.stdlib.test_utils import mk_test_case_table, run_sim

from reginc.RegIncRTL import RegIncRTL
import numpy as np
import sys
from os.path import exists
import os

class TestHarness( Component ):

  def construct( s, RegInc ):

    s.src    = stream.SourceRTL( Bits32 )
    s.sink   = stream.SinkRTL  ( Bits32 )
    s.RegInc = RegInc

    s.RegInc.recv //= s.src.send
    s.sink.recv   //= s.RegInc.send

  def done( s ):
    return s.src.done() and s.sink.done()

  def line_trace( s ):
    return "{} > {} > {}".format(
      s.src.line_trace(), s.pipeline.line_trace(), s.sink.line_trace(),
    )

def simple(name):
  return [Bits32(0),Bits32(1),
          Bits32(1),Bits32(2)]


test_case_table = mk_test_case_table([
#                          delays  
#                          --------
  (                       "msgs                          src sink"),
  [ "simple",              simple("simple"),             0,  0],
  ])

@pytest.mark.parametrize( **test_case_table )
def test( test_params, cmdline_opts ):

  th = TestHarness( RegIncRTL() )
  
  th.set_param("top.src.construct",
    msgs=test_params.msgs[::2],
    initial_delay=test_params.src + 3,
    interval_delay=test_params.src)

  th.set_param("top.sink.construct",
    msgs=test_params.msgs[1::2],
    initial_delay=test_params.sink + 3,
    interval_delay=test_params.sink)

  run_sim( th, cmdline_opts, duts=['pipeline'] )