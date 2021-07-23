# NQ-Open

The NQ-Open task, introduced by
[Lee et.al. 2019](https://www.aclweb.org/anthology/P19-1612/), is an open domain
question answering benchmark that is derived from
[Natural Questions](https://ai.google.com/research/NaturalQuestions).
The goal is to predict an English answer string for an input English question.
All questions can be answered using the contents of English Wikipedia.

The NQ-Open task format was also used as part of the
[EfficientQA competition](https://efficientqa.github.io/) at NeurIPS 2020. Results
from the EfficientQA competition are reported in
[Min et.al. 2021](https://arxiv.org/pdf/2101.00133.pdf).

The EfficientQA competition used *different dev and test splits from the original
NQ-open task*. This repository contains both the original NQ-open data, as well
as the EfficientQA data. Users should take care to ensure they are reporting
metrics on the correct splits. All work preceeding the EfficientQA competition,
in December 2020, reports results on the NQ-open Dev split.

The different splits have all been created from Natural Questions data using
[this conversion script](https://github.com/google-research/language/blob/master/language/orqa/preprocessing/convert_to_nq_open.py).
Split statistics are given below. More details on the data format, including
the various `answer` fields present in the EfficientQA test set, are given
in the [Data Format](#data-format) section of this page.

| Split               | Size   | Filename                           |
|---------------------|--------|------------------------------------|
| Train               | 87,925 | NQ-open.train.jsonl                |
| Original Dev        | 3,610  | NQ-open.dev.jsonl                  |
| EfficientQA Dev     | 1,800  | NQ-open.efficientqa.dev.1.1.jsonl  |
| EfficientQA Test    | 1,769  | NQ-open.efficientqa.test.1.1.jsonl |

All of the Natural Questions data is released under the
[CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/) license.

## Data format
All of the data splits, apart from `NQ-open.efficientqa.test.1.1.jsonl`, contain
the following fields:

```
question: 'who signed the sugauli treaty on behalf of nepal'
answer: ['Raj Guru Gajaraj Mishra']
```

and predictions should be compared to the contents of the `answer` field
using the
[NQ-open evaluation script](https://github.com/google-research/language/blob/master/language/orqa/evaluation/evaluate_predictions.py).

### Answer fields in EfficientQA test
As part of the EfficientQA competition, predictions from the top performing
submission were sent for further evaluation. The details of this evaluation
are provided in [Min et.al. 2021](https://arxiv.org/pdf/2101.00133.pdf).

Instead of a single `answer` field, the EfficientQA test set has the following
fields containing reference answer strings.

1. `answer`: contains the answers from the original NQ annotations,
2. `def_correct_predictions`: contains predictions from top performing
submissions that were determined to be definitely correct by annotators,
3. `poss_correct_predictions`: contains preditions from top performing
submissions that were determined to be possibly correct given some interpretation
of the question.
4. `answer_and_def_correct_predictions`: contains the union of
`answer` and `def_correct_predictions`.

We include `poss_correct_predictions` in this release for completeness. However,
we *do not suggest that these are used for evaluation of any systems* since they
rarely provide a properly satisfactory answer to the question. You can evaluate
your predictions on the standard `answer` references or the expanded
`answer_and_def_correct_predictions` using the
[evaluation_code](https://github.com/google-research/language/blob/master/language/orqa/evaluation/evaluate_predictions.py)
with the appropriate `answer_field` flag.




For further discussion of the data, as well as our recommendations for robust
evaluation, please see [Min et.al. 2021](https://arxiv.org/pdf/2101.00133.pdf).
Also, please remember that almost all work to date has reported accuracy on the
original NQ-open dev set described above. Any work that uses the EfficientQA
test set should describe this choice explicitly.

Due to a bug in the post-competition labeling process, there may be small
discrepancies between results calculated using the 1,769 examples released as
part of the EfficientQA rated test data and the 1,800 examples used in the
original EfficientQA leaderboard. Refer to
[Min et.al. 2021](https://arxiv.org/pdf/2101.00133.pdf) for official
results.

## Baselines

| Method                                                                         | Original Dev | EfficientQa Dev | EfficientQa test |
|--------------------------------------------------------------------------------|--------------|-----------------|------------------|
| [TFIDF Nearest Question](https://arxiv.org/abs/2008.02637)                     | 22%          | 17%             | 16%              |
| [REALM](https://github.com/google-research/language/tree/master/language/realm)| 40%          | 36%             | 35%              |
| [T5XXL](https://efficientqa.github.io/getting_started.html)                    | 37%          | 32%             | 32%              |
| [DPR](https://efficientqa.github.io/getting_started.html)                      | 41%          | 37%             | 36%              |
| [DPR subset](https://efficientqa.github.io/getting_started.html)               | 35%          | 30%             | 30%              |

## Citation
If you use this data, please cite
[Kwiatkowski et.al. 2019](https://www.mitpressjournals.org/doi/full/10.1162/tacl_a_00276)
and [Lee et.al. 2019](https://www.aclweb.org/anthology/P19-1612/).
