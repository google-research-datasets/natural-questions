# Natural Questions

Natural Questions (NQ) contains real user questions issued to Google search, and
answers found from Wikipedia by annotators.
NQ is designed for the training and evaluation of automatic question answering
systems.

Please see
[http://ai.google.com/research/NaturalQuestions](http://ai.google.com/research/NaturalQuestions)
to get the data and view the leaderboard.
For more details on the design and content of the dataset, please see
the paper
[Natural Questions: a Benchmark for Question Answering Research](https://ai.google/research/pubs/pub47761).
To help you get started on this task we have provided some
[baseline systems](https://github.com/google-research/language/tree/master/language/question_answering)
that can be branched.


# Data Description
NQ contains 307,372 training examples, 7,830 examples for development, and we
withold a further 7,842 examples for testing. In the paper, we demonstrate a
human upper bound of 87% F1 on the long answer selection task, and 76% on the
short answer selection task.

To run on the hidden test set, you will have to upload a Docker image containing
your system to the
[NQ competition site](http://ai.google.com/research/NaturalQuestions/competition).
Instructions on building the Docker image are given [here](competition.md).


## Data Format
Each example in the original NQ format contains the rendered HTML of an entire
Wikipedia page, as well as a tokenized representation of the text on the page.

This section will go on to define the full NQ data format, but we recognize
that most users will only want a version of the data in which the text has
already been extracted. We have supplied a
[simplified version of the training set](https://storage.cloud.google.com/natural_questions/v1.0-simplified/simplified-nq-train.jsonl.gz)
and we have also supplied a `simplify_nq_example` function
in [data_utils.py](data_utils.py) which maps from the original format to the
simplified format. Only the original format is provided by our
[competition site](https://ai.google.com/research/NaturalQuestions/competition).
If you use the simplified data, you should call `simplify_nq_example` on each
example seen during evaluation and you should provide predictions using the
`start_token` and `end_token` offsets that correspond to the whitespace
separated tokens in the document text.

As well as recognizing predictions according to token offsets, the evaluation
script also recognizes predictions as byte offsets into the original HTML. This
allows users to define their own text extraction and tokenization schemes.

To help you explore the data, this repository also contains a simple
[data browser](nq_browser.py) that you can run on your own machine, and modify
as you see fit. We also have provided extra preprocessing utilities and
tensorflow dataset code in
[the repository containing the baseline systems presented in our paper](https://github.com/google-research/language/tree/master/language/question_answering).
The rest of this section describes the data format thouroughly in reference to
a [toy example](toy_example.md).

Each example contains a single question, a tokenized representation of the question,
a timestamped Wikipedia URL, and the HTML representation of that Wikipedia page.

```json
"question_text": "who founded google",
"question_tokens": ["who", "founded", "google"],
"document_url": "http://www.wikipedia.org/Google",
"document_html": "<html><body><h1>Google</h1><p>Google was founded in 1998 by ..."
```

We release the raw HTML, since this is what was seen by our annotators, and we
would like to support approaches that make use of the document structure.
However, we expect most initial efforts will prefer to use a tokenized
representation of the page.

```json
"document_tokens":[
  { "token": "<h1>", "start_byte": 12, "end_byte": 16, "html_token": true },
  { "token": "Google", "start_byte": 16, "end_byte": 22, "html_token": false },
  { "token": "inc", "start_byte": 23, "end_byte": 26, "html_token": false },
  { "token": ".", "start_byte": 26, "end_byte": 27, "html_token": false },
  { "token": "</h1>", "start_byte": 27, "end_byte": 32, "html_token": true },
  { "token": "<p>", "start_byte": 32, "end_byte": 35, "html_token": true },
  { "token": "Google", "start_byte": 35, "end_byte": 41, "html_token": false },
  { "token": "was", "start_byte": 42, "end_byte": 45, "html_token": false },
  { "token": "founded", "start_byte": 46, "end_byte": 53, "html_token": false },
  { "Token": "in", "start_byte": 54, "end_byte": 56, "html_token": false },
  { "token": "1998", "start_byte": 57, "end_byte": 61, "html_token": false },
  { "token": "by", "start_byte": 62, "end_byte": 64, "html_token": false },
```

Each token is either a word or a HTML tag that defines a heading, paragraph,
table, or list. HTML tags are marked as such using the boolean field `html_token`.
Each token also has an inclusive `start_byte` and exclusive `end_byte` that
identifies the token's position within the example's UTF-8 indexed HTML string.

### Long Answer Candidates
The first task in Natural Questions is to identify the *smallest* HTML bounding
box that contains all of the information required to infer the answer to a
question.
These long answers can be paragraphs, lists, list items, tables, or table rows.
While the candidates can be inferred directly from the HTML or token sequence, we
also include a list of long answer candidates for convenience.
Each candidate is defined in terms of offsets into both the HTML and the
document tokens.
As with all other annotations, start offsets are inclusive and end offsets are
exclusive.

```json
"long_answer_candidates": [
  { "start_byte": 32, "end_byte": 106, "start_token": 5, "end_token": 22, "top_level": true },
  { "start_byte": 65, "end_byte": 102, "start_token": 13, "end_token": 21, "top_level": false },
```

In this example, you can see that the second long answer candidate is contained
within the first. We do not disallow nested long answer candidates, we just ask
annotators to find the *smallest candidate containing all of the information
required to infer the answer to the question*. However, we do observe that 95%
of all long answers (including all paragraph answers) are not nested below any
other candidates.
Since we believe that some users may want to start by only considering
non-overlapping candidates, we include a boolean flag `top_level` that
identifies whether a candidate is nested below another (`top_level = False`) or
not (`top_level = True`). Please be aware that this flag is only included for
convenience and it is not related to the task definition in any way.
For more information about the distribution of long answer types, please
see the data statistics section below.

### Annotations
The NQ training data has a single annotation with each example and the evaluation
data has five. Each annotation defines a "long_answer" span, a list of
`short_answers`, and a `yes_no_answer`.  If the annotator has marked a long
answer, then the long answer dictionary identifies this long answer using byte
offsets, token offsets, and an index into the list of long answer candidates. If
the annotator has marked that no long answer is available, all of the fields in
the long answer dictionary are set to -1.

```json
"annotations": [{
  "long_answer": { "start_byte": 32, "end_byte": 106, "start_token": 5, "end_token": 22, "candidate_index": 0 },
  "short_answers": [
    {"start_byte": 73, "end_byte": 78, "start_token": 15, "end_token": 16},
    {"start_byte": 87, "end_byte": 92, "start_token": 18, "end_token": 19}
  ],
  "yes_no_answer": "NONE"
}]
```

Each of the short answers is also identified using both byte offsets and token
indices. There is no limit to the number of short answers. There is also often
no short answer, since some questions such as "describe google's founding" do
not have a succinct extractive answer. When this is the case, the long answer is
given but the "short_answers" list is empty.

Finally, if no short answer is given, it is possible that there is a
`yes_no_answer` for questions such as "did larry co-found google". The values
for this field `YES`, or `NO` if a yes/no answer is given. The default value is
`NONE` when no yes/no answer is given. For statistics on long answers, short
answers, and yes/no answers, please see the data statistics section below.

### Data Statistics
The NQ training data contains 307,373 examples. 152,148 have a long answer
and 110,724 have a short answer. Short answers can be sets of spans in the document
(106,926), or yes or no (3,798). Long answers are HTML bounding boxes, and the
distribution of NQ long answer types is as follows:

| HTML tags | Percent of long answers |
|-----------|-------------------------|
| `<P>`     | 72.9%                   |
| `<Table>` | 19.0%                   |
| `<Tr>`    | 1.5%                    |
| `<Ul>`, `<Ol>`, `<Dl>` | 3.2%       |
| `<Li>`, `<Dd>`, `<Dt>` | 3.4%       |

While we allow any paragraph, table, or list element to be a long answer,
we find that 95% of the long answers are not contained by any other
long answer candidate. We mark these `top level` candidates in the data,
as described above.

Short answers may contain more than one span, if the question is asking
for a list of answers (e.g. who made it to stage 3 in american ninja warrior season 9).
However, almost all short answers (90%) only contain a single span of text.
All short answers are contained by the long answer given in the same annotation.

# Prediction Format
Please see the [evaluation script](nq_eval.py) for a description of the prediction
format that your model should output.

# Contact us
If you have a technical question regarding the dataset, code or publication, please
create an issue in this repository. This is the fastest way to reach us.

If you would like to share feedback or report concerns, please email us at <natural-questions@google.com>.
