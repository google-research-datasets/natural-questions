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
r"""Script to apply `text_utils.simplify_nq_data` to all examples in a split.

We have provided the processed training set at the link below.

https://storage.cloud.google.com/natural_questions/v1.0-simplified/simplified-nq-train.jsonl.gz

The test set, used by NQ's competition website, is only provided in the original
NQ format. If you wish to use the simplified format, then you should call
`text_utils.simplify_nq_data` in your submitted system.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import glob
import gzip
import json
import os
import time

from absl import app
from absl import flags

import text_utils as text_utils

FLAGS = flags.FLAGS

flags.DEFINE_string(
    "data_dir", None, "Path to directory containing original NQ"
    "files, matching the pattern `nq-<split>-??.jsonl.gz`.")


def main(_):
  """Runs `text_utils.simplify_nq_example` over all shards of a split.

  Prints simplified examples to a single gzipped file in the same directory
  as the input shards.
  """
  split = os.path.basename(FLAGS.data_dir)
  outpath = os.path.join(FLAGS.data_dir,
                         "simplified-nq-{}.jsonl.gz".format(split))
  with gzip.open(outpath, "wb") as fout:
    num_processed = 0
    start = time.time()
    for inpath in glob.glob(os.path.join(FLAGS.data_dir, "nq-*-??.jsonl.gz")):
      print("Processing {}".format(inpath))
      with gzip.open(inpath, "rb") as fin:
        for l in fin:
          utf8_in = l.decode("utf8", "strict")
          utf8_out = json.dumps(
              text_utils.simplify_nq_example(json.loads(utf8_in))) + u"\n"
          fout.write(utf8_out.encode("utf8"))
          num_processed += 1
          if not num_processed % 100:
            print("Processed {} examples in {}.".format(num_processed,
                                                        time.time() - start))


if __name__ == "__main__":
  app.run(main)
