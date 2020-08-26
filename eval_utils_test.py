# coding=utf-8
# Copyright 2018 The Google AI Language Team Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Testing code for tgq_eval."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import eval_utils as util

import tensorflow.compat.v1 as tf


class EvalUtilsTest(tf.test.TestCase):
  """Testing codes for eval_utils"""

  def testSpan(self):
    """Test inconsistent null spans."""
    self.assertRaises(ValueError, util.Span, -1, 1, -1, 1)
    self.assertRaises(ValueError, util.Span, -1, -1, -1, 1)
    self.assertRaises(ValueError, util.Span, -1, -1, 3, 1)

  def testNullSpan(self):
    """Test null spans."""
    self.assertTrue(util.Span(-1, -1, -1, -1).is_null_span())
    self.assertFalse(util.Span(-1, -1, 0, 1).is_null_span())

  def testSpanEqual(self):
    """Test span equals."""
    span_a = util.Span(100, 102, -1, -1)
    span_b = util.Span(100, 102, -1, -1)
    self.assertTrue(util.nonnull_span_equal(span_a, span_b))

    span_a = util.Span(-1, -1, 100, 102)
    span_b = util.Span(-1, -1, 100, 102)
    self.assertTrue(util.nonnull_span_equal(span_a, span_b))

    span_a = util.Span(100, 102, -1, -1)
    span_b = util.Span(-1, -1, 100, 102)
    self.assertFalse(util.nonnull_span_equal(span_a, span_b))

  def testSpanSetEqual(self):
    """Set span set equal."""
    span_a1 = util.Span(-1, -1, 100, 102)
    span_a2 = util.Span(-1, -1, 100, 102)
    span_b = util.Span(-1, -1, 101, 105)
    null_span = util.Span(-1, -1, -1, -1)

    self.assertTrue(util.span_set_equal([span_a1, span_b], [span_a2, span_b]))

    self.assertTrue(
        util.span_set_equal([span_a1, span_b], [span_a2, span_b, null_span]))

    self.assertFalse(
        util.span_set_equal([span_a1], [span_a2, span_b, null_span]))


if __name__ == '__main__':
  tf.test.main()
