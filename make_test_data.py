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
"""Utility to generate sample predictions from the gold annotations.

Example usage:

make_test_data --gold_path=<path-to-gold-data> --output=test.json

The logic to generate fake scores is as follows:

1. True answers are dropped at the rate (1 - desired_recall)
2. Scores are assigned uniformly at random in the range [0, 2].
3. If generate_false_positives is true, then long answers consisting of the
   first token are added for null documents, with scores in the range [0,1].
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import random
from absl import app
from absl import flags

import eval_utils as util

flags.DEFINE_string('gold_path', None, 'Path to gold data.')
flags.DEFINE_string('output_path', None, 'Path to write JSON.')
flags.DEFINE_integer('num_threads', 10, 'Number of threads for reading.')
flags.DEFINE_float('desired_recall', 1.0,
                   'Desired maximum recall of predictions.')
flags.DEFINE_bool('generate_false_positives', False,
                  'Whether or not to generate false positives for null docs.')

FLAGS = flags.FLAGS


def main(_):
  nq_gold_dict = util.read_annotation(FLAGS.gold_path,
                                      n_threads=FLAGS.num_threads)

  def label_to_pred(labels):
    """Convert a list of gold human annotations to a perfect prediction."""
    gold_has_short_answer = util.gold_has_short_answer(labels)

    gold_has_long_answer = util.gold_has_long_answer(labels)

    # We did not put `long_answer` and `yes_no_answer`, and they should be
    # considered as null when loading from data.

    pred = {
        'example_id': labels[0].example_id,
        'short_answers': [],
        'short_answers_score': random.random(),
        'long_answer_score': random.random()
    }

    keep_answer = random.random() <= FLAGS.desired_recall
    for label in labels:
      if gold_has_short_answer and keep_answer:
        pred['short_answers_score'] *= 2
        if not util.is_null_span_list(label.short_answer_span_list):
          pred['short_answers'] = (
              [{'start_token': span.start_token_idx,
                'end_token': span.end_token_idx,
                'start_byte': span.start_byte,
                'end_byte': span.end_byte}
               for span in label.short_answer_span_list])
          pred['yes_no_answer'] = 'none'
        elif label.yes_no_answer != 'none':
          pred['short_answers'] = []
          pred['yes_no_answer'] = label.yes_no_answer

      if (gold_has_long_answer and not label.long_answer_span.is_null_span() and
          keep_answer):
        pred['long_answer'] = {
            'start_token': label.long_answer_span.start_token_idx,
            'end_token': label.long_answer_span.end_token_idx,
            'start_byte': label.long_answer_span.start_byte,
            'end_byte': label.long_answer_span.end_byte
        }
        pred['long_answer_score'] *= 2

    if FLAGS.generate_false_positives:
      if not gold_has_short_answer:
        pred['short_answers'] = [
            {'start_token': 0, 'end_token': 1,
             'start_byte': -1, 'end_byte': -1}]

      if not gold_has_long_answer:
        pred['long_answer_start_token'] = 0
        pred['long_answer_end_token'] = 1

    return pred

  predictions = []
  for _, labels in nq_gold_dict.iteritems():
    predictions.append(label_to_pred(labels))

  with open(FLAGS.output_path, 'w') as f:
    json.dump({'predictions': predictions}, f)

if __name__ == '__main__':
  flags.mark_flag_as_required('gold_path')
  flags.mark_flag_as_required('output_path')

  app.run(main)
