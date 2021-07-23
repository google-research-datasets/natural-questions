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
"""Web frontend for browsing Google's Natural Questions.

Example usage:

pip install absl-py
pip install jinja2
pip install tornado
pip install wsgiref

python nq_browser --nq_jsonl=nq-train-sample.jsonl.gz
python nq_browser --nq_jsonl=nq-dev-sample.jsonl.gz --dataset=dev --port=8081
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import base64
import gzip
import json
import os

import wsgiref.simple_server

from absl import app
from absl import flags

import jinja2
import numpy as np
import tornado.web
import tornado.wsgi


FLAGS = flags.FLAGS

flags.DEFINE_string('nq_jsonl', None,
                    'Path to jsonlines file containing Natural Questions.')
flags.DEFINE_boolean('gzipped', True, 'Whether the jsonlines are gzipped.')
flags.DEFINE_enum('dataset', 'train', ['train', 'dev'],
                  'Whether this is training data or dev data.')
flags.DEFINE_integer('port', 8080, 'Port to listen on.')
flags.DEFINE_integer('max_examples', 200,
                     'Max number of examples to load in the browser.')
flags.DEFINE_enum('mode', 'all_examples',
                  ['all_examples', 'long_answers', 'short_answers'],
                  'Subset of examples to show.')


class LongAnswerCandidate(object):
  """Representation of long answer candidate."""

  def __init__(self, contents, index, is_answer, contains_answer):
    self.contents = contents
    self.index = index
    self.is_answer = is_answer
    self.contains_answer = contains_answer
    if is_answer:
      self.style = 'is_answer'
    elif contains_answer:
      self.style = 'contains_answer'
    else:
      self.style = 'not_answer'


class Example(object):
  """Example representation."""

  def __init__(self, json_example):
    self.json_example = json_example

    # Whole example info.
    self.url = json_example['document_url']
    self.title = json_example.get('document_title', 'Wikipedia')
    self.example_id = base64.urlsafe_b64encode(
        str(self.json_example['example_id']).encode('utf-8'))
    self.document_html = self.json_example['document_html'].encode('utf-8')
    self.document_tokens = self.json_example['document_tokens']
    self.question_text = json_example['question_text']

    if FLAGS.dataset == 'train':
      if len(json_example['annotations']) != 1:
        raise ValueError(
            'Train set json_examples should have a single annotation.')
      annotation = json_example['annotations'][0]
      self.has_long_answer = annotation['long_answer']['start_byte'] >= 0
      self.has_short_answer = annotation[
          'short_answers'] or annotation['yes_no_answer'] != 'NONE'

    elif FLAGS.dataset == 'dev':
      if len(json_example['annotations']) != 5:
        raise ValueError('Dev set json_examples should have five annotations.')
      self.has_long_answer = sum([
          annotation['long_answer']['start_byte'] >= 0
          for annotation in json_example['annotations']
      ]) >= 2
      self.has_short_answer = sum([
          bool(annotation['short_answers']) or
          annotation['yes_no_answer'] != 'NONE'
          for annotation in json_example['annotations']
      ]) >= 2

    self.long_answers = [
        a['long_answer']
        for a in json_example['annotations']
        if a['long_answer']['start_byte'] >= 0 and self.has_long_answer
    ]
    self.short_answers = [
        a['short_answers']
        for a in json_example['annotations']
        if a['short_answers'] and self.has_short_answer
    ]
    self.yes_no_answers = [
        a['yes_no_answer']
        for a in json_example['annotations']
        if a['yes_no_answer'] != 'NONE' and self.has_short_answer
    ]

    if self.has_long_answer:
      long_answer_bounds = [
          (la['start_byte'], la['end_byte']) for la in self.long_answers
      ]
      long_answer_counts = [
          long_answer_bounds.count(la) for la in long_answer_bounds
      ]
      long_answer = self.long_answers[np.argmax(long_answer_counts)]
      self.long_answer_text = self.render_long_answer(long_answer)

    else:
      self.long_answer_text = ''

    if self.has_short_answer:
      short_answers_ids = [[
          (s['start_byte'], s['end_byte']) for s in a
      ] for a in self.short_answers] + [a for a in self.yes_no_answers]
      short_answers_counts = [
          short_answers_ids.count(a) for a in short_answers_ids
      ]

      self.short_answers_texts = [
          ', '.join([
              self.render_span(s['start_byte'], s['end_byte'])
              for s in short_answer
          ])
          for short_answer in self.short_answers
      ]

      self.short_answers_texts += self.yes_no_answers
      self.short_answers_text = self.short_answers_texts[np.argmax(
          short_answers_counts)]
      self.short_answers_texts = set(self.short_answers_texts)

    else:
      self.short_answers_texts = []
      self.short_answers_text = ''

    self.candidates = self.get_candidates(
        self.json_example['long_answer_candidates'])

    self.candidates_with_answer = [
        i for i, c in enumerate(self.candidates) if c.contains_answer
    ]

  def render_long_answer(self, long_answer):
    """Wrap table rows and list items, and render the long answer.

    Args:
      long_answer: Long answer dictionary.

    Returns:
      String representation of the long answer span.
    """

    if long_answer['end_token'] - long_answer['start_token'] > 500:
      return 'Large long answer'

    html_tag = self.document_tokens[long_answer['end_token'] - 1]['token']
    if html_tag == '</Table>' and self.render_span(
        long_answer['start_byte'], long_answer['end_byte']).count('<TR>') > 30:
      return 'Large table long answer'

    elif html_tag == '</Tr>':
      return '<TABLE>{}</TABLE>'.format(
          self.render_span(long_answer['start_byte'], long_answer['end_byte']))

    elif html_tag in ['</Li>', '</Dd>', '</Dd>']:
      return '<Ul>{}</Ul>'.format(
          self.render_span(long_answer['start_byte'], long_answer['end_byte']))

    else:
      return self.render_span(long_answer['start_byte'],
                              long_answer['end_byte'])

  def render_span(self, start, end):
    return self.document_html[start:end].decode()

  def get_candidates(self, json_candidates):
    """Returns a list of `LongAnswerCandidate` objects for top level candidates.

    Args:
      json_candidates: List of Json records representing candidates.

    Returns:
      List of `LongAnswerCandidate` objects.
    """
    candidates = []
    top_level_candidates = [c for c in json_candidates if c['top_level']]
    for candidate in top_level_candidates:
      tokenized_contents = ' '.join([
          t['token'] for t in self.json_example['document_tokens']
          [candidate['start_token']:candidate['end_token']]
      ])

      start = candidate['start_byte']
      end = candidate['end_byte']
      is_answer = self.has_long_answer and np.any(
          [(start == ans['start_byte']) and (end == ans['end_byte'])
           for ans in self.long_answers])
      contains_answer = self.has_long_answer and np.any(
          [(start <= ans['start_byte']) and (end >= ans['end_byte'])
           for ans in self.long_answers])

      candidates.append(
          LongAnswerCandidate(tokenized_contents, len(candidates), is_answer,
                              contains_answer))

    return candidates


def has_long_answer(json_example):
  for annotation in json_example['annotations']:
    if annotation['long_answer']['start_byte'] >= 0:
      return True
  return False


def has_short_answer(json_example):
  for annotation in json_example['annotations']:
    if annotation['short_answers']:
      return True
  return False


def load_examples(fileobj):
  """Reads jsonlines containing NQ examples.

  Args:
    fileobj: File object containing NQ examples.

  Returns:
    Dictionary mapping example id to `Example` object.
  """

  def _load(examples, f):
    """Read serialized json from `f`, create examples, and add to `examples`."""

    for l in f:
      json_example = json.loads(l)
      if FLAGS.mode == 'long_answers' and not has_long_answer(json_example):
        continue

      elif FLAGS.mode == 'short_answers' and not has_short_answer(json_example):
        continue

      example = Example(json_example)
      examples[example.example_id] = example

      if len(examples) == FLAGS.max_examples:
        break

  examples = {}
  if FLAGS.gzipped:
    _load(examples, gzip.GzipFile(fileobj=fileobj))
  else:
    _load(examples, fileobj)

  return examples


class MainHandler(tornado.web.RequestHandler):
  """Displays an overview table of the loaded NQ examples."""

  def initialize(self, jinja2_env, examples):
    self.env = jinja2_env
    self.tmpl = self.env.get_template('index.html')
    self.examples = examples

  def get(self):
    res = self.tmpl.render(
        dataset=FLAGS.dataset.capitalize(), examples=self.examples.values())
    self.write(res)


class HtmlHandler(tornado.web.RequestHandler):
  """Displays the html field contained in a NQ example."""

  def initialize(self, examples):
    self.examples = examples

  def get(self):
    example_id = str(self.get_argument('example_id'))
    self.write(self.examples[example_id].document_html)


class FeaturesHandler(tornado.web.RequestHandler):
  """Displays a detailed view of the features extracted from a NQ example."""

  def initialize(self, jinja2_env, examples):
    self.env = jinja2_env
    self.tmpl = self.env.get_template('features.html')
    self.examples = examples

  def get(self):
    example_id = str(self.get_argument('example_id'))
    res = self.tmpl.render(
        dataset=FLAGS.dataset.capitalize(), example=self.examples[example_id])
    self.write(res)


class NqServer(object):
  """Serves all different tools."""

  def __init__(self, web_path, examples):
    """
    """
    tmpl_path = web_path + '/templates'
    static_path = web_path + '/static'
    jinja2_env = jinja2.Environment(loader=jinja2.FileSystemLoader(tmpl_path))

    self.application = tornado.wsgi.WSGIApplication([
        (r'/', MainHandler, {
            'jinja2_env': jinja2_env,
            'examples': examples
        }),
        (r'/html', HtmlHandler, {
            'examples': examples
        }),
        (r'/features', FeaturesHandler, {
            'jinja2_env': jinja2_env,
            'examples': examples
        }),
        (r'/static/(.*)', tornado.web.StaticFileHandler, {
            'path': static_path
        }),
    ])

  def serve(self):
    """Main entry point for the NqSever."""
    server = wsgiref.simple_server.make_server('', FLAGS.port, self.application)
    server.serve_forever()


def main(unused_argv):
  with open(FLAGS.nq_jsonl) as fileobj:
    examples = load_examples(fileobj)

  web_path = os.path.dirname(os.path.realpath(__file__))
  NqServer(web_path, examples).serve()


if __name__ == '__main__':
  app.run(main)
