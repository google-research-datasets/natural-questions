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
import nq_eval as ev
import tensorflow as tf


class EvalUtilsTest(tf.test.TestCase):
  """Testing codes for eval_utils"""

  def _get_nq_label(self, long_span, short_span_list, eid=0):
    return util.NQLabel(example_id=eid, long_answer_span=long_span,
                        short_answer_span_list=short_span_list,
                        long_score=0, short_score=0,
                        yes_no_answer='none')

  def _get_nq_label_with_yes_no(self, long_span, yes_no_answer, eid=0):
    assert yes_no_answer != 'none'
    return util.NQLabel(example_id=eid, long_answer_span=long_span,
                        short_answer_span_list=[],
                        long_score=0, short_score=0,
                        yes_no_answer=yes_no_answer)

  def _get_span(self, start, end):
    return util.Span(-1, -1, start, end)

  def testLongStat(self):
    """Test instance level long answer f1."""
    # Test cases when there is no long answer.
    gold_label_spans = [(0, 10), (-1, -1), (-1, -1), (-1, -1), (-1, -1)]
    gold_label_list = [
        self._get_nq_label(self._get_span(a, b), [])
        for a, b in gold_label_spans
    ]
    pred_label = self._get_nq_label(self._get_span(0, 10), [])
    gold_has_answer, pred_has_answer, is_correct, _ = ev.score_long_answer(
        gold_label_list, pred_label)

    self.assertEqual(gold_has_answer, False)
    self.assertEqual(pred_has_answer, True)
    self.assertEqual(is_correct, False)

    # Test cases when there is a long answer.
    gold_label_spans = [(0, 10), (0, 9), (-1, -1), (-1, -1), (-1, -1)]
    gold_label_list = [
        self._get_nq_label(self._get_span(a, b), [])
        for a, b in gold_label_spans
    ]

    pred_label = self._get_nq_label(self._get_span(0, 10), [])
    gold_has_answer, pred_has_answer, is_correct, _ = ev.score_long_answer(
        gold_label_list, pred_label)
    self.assertEqual(gold_has_answer, True)
    self.assertEqual(pred_has_answer, True)
    self.assertEqual(is_correct, True)

  def testShortStat(self):
    """Test instance level short answer f1."""
    long_span = self._get_span(0, 10)

    # Test case when there is no gold short answer.
    gold_label_spans_1 = [(1, 3), (5, 6)]
    gold_label_spans_2 = [(-1, -1)]
    gold_label_spans_3 = [(-1, -1)]
    gold_label_spans_4 = [(-1, -1)]
    gold_label_spans_5 = [(-1, -1)]

    gold_label_list = []

    for spans in [
        gold_label_spans_1, gold_label_spans_2, gold_label_spans_3,
        gold_label_spans_4, gold_label_spans_5
    ]:
      gold_label_list.append(
          self._get_nq_label(long_span,
                             [self._get_span(a, b) for a, b in spans]))

    pred_label = self._get_nq_label(
        long_span, [self._get_span(a, b) for a, b in gold_label_spans_1])

    gold_has_answer, pred_has_answer, is_correct, _ = ev.score_short_answer(
        gold_label_list, pred_label)
    self.assertEqual(gold_has_answer, False)
    self.assertEqual(pred_has_answer, True)
    self.assertEqual(is_correct, False)

    # Test case when there is gold short answer.
    gold_label_spans_1 = [(1, 3), (5, 6)]
    gold_label_spans_2 = [(1, 3), (5, 6)]
    gold_label_spans_3 = [(-1, -1)]
    gold_label_spans_4 = [(-1, -1)]
    gold_label_spans_5 = [(-1, -1)]

    gold_label_list = []

    for spans in [
        gold_label_spans_1, gold_label_spans_2, gold_label_spans_3,
        gold_label_spans_4, gold_label_spans_5
    ]:
      gold_label_list.append(
          self._get_nq_label(long_span,
                             [self._get_span(a, b) for a, b in spans]))

    pred_label = self._get_nq_label(
        long_span, [self._get_span(a, b) for a, b in gold_label_spans_1])

    gold_has_answer, pred_has_answer, is_correct, _ = ev.score_short_answer(
        gold_label_list, pred_label)
    self.assertEqual(gold_has_answer, True)
    self.assertEqual(pred_has_answer, True)
    self.assertEqual(is_correct, True)

    # Test case for not exactly match.
    pred_label = self._get_nq_label(long_span, [self._get_span(1, 3)])
    gold_has_answer, pred_has_answer, is_correct, _ = ev.score_short_answer(
        gold_label_list, pred_label)
    self.assertEqual(gold_has_answer, True)
    self.assertEqual(pred_has_answer, True)
    self.assertEqual(is_correct, False)

    # Test case when there is a yes/no answer

    gold_label_spans_2 = [(1, 3), (5, 6)]
    gold_label_spans_3 = [(-1, -1)]
    gold_label_spans_4 = [(-1, -1)]
    gold_label_spans_5 = [(-1, -1)]

    # first annotation is yes/no
    gold_label_list = [self._get_nq_label_with_yes_no(long_span, 'yes')]

    for spans in [
        gold_label_spans_2, gold_label_spans_3, gold_label_spans_4,
        gold_label_spans_5
    ]:
      gold_label_list.append(
          self._get_nq_label(long_span,
                             [self._get_span(a, b) for a, b in spans]))

    pred_label = self._get_nq_label_with_yes_no(long_span, 'yes')

    gold_has_answer, pred_has_answer, is_correct, _ = ev.score_short_answer(
        gold_label_list, pred_label)
    self.assertEqual(gold_has_answer, True)
    self.assertEqual(pred_has_answer, True)
    self.assertEqual(is_correct, True)

    pred_label = self._get_nq_label_with_yes_no(long_span, 'no')

    gold_has_answer, pred_has_answer, is_correct, _ = ev.score_short_answer(
        gold_label_list, pred_label)
    self.assertEqual(gold_has_answer, True)
    self.assertEqual(pred_has_answer, True)
    self.assertEqual(is_correct, False)

  def testPrCurve(self):
    """Test instance level short answer f1."""

    # has_gold, has_pred, is_correct, score
    answer_stats = [[True, True, True, 1.0],
                    [False, True, False, 10.0]]

    answer_stats.sort(key=lambda x: x[-1], reverse=True)

    ((_, best_precision, best_recall, _),
     target_pr_scores_list) = ev.compute_pr_curves(
         answer_stats, targets=[0.5, 0.75, 0.9])

    self.assertEqual(best_precision, 0.5)
    self.assertEqual(best_recall, 1.0)

    self.assertEqual(target_pr_scores_list[0][0], 0.5)
    self.assertEqual(target_pr_scores_list[0][1], 1.0)  # recall@0.5

    self.assertEqual(target_pr_scores_list[1][0], 0.75)
    self.assertEqual(target_pr_scores_list[1][1], 0.0)  # recall@0.5

    self.assertEqual(target_pr_scores_list[2][0], 0.9)
    self.assertEqual(target_pr_scores_list[2][1], 0.0)  # recall@0.5


if __name__ == '__main__':
  tf.test.main()
