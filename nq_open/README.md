# NQ-Open

--------------------------------------------------------------------------------
**On 2020/09/22 the canonical EfficientQA dev set was updated to account for an
error.**

**If you are using NQ-open.efficientqa.dev.jsonl, please change to
NQ-open.efficientqa.dev.1.1.jsonl.**

--------------------------------------------------------------------------------

The NQ-Open task, introduced by
[Lee et.al. 2019](https://www.aclweb.org/anthology/P19-1612/), is an open domain
question answering benchmark that is derived from
[Natural Questions](https://ai.google.com/research/NaturalQuestions).
The goal is to predict an English answer string for an input English question.
All questions can be answered using the contents of English Wikipedia.

The NQ-Open task is currently being used to evaluate submissions to the
[EfficientQA competition](https://efficientqa.github.io/),
which is part of the
[NeurIPS 2020 competition track](https://neurips.cc/Conferences/2020/CompetitionTrack).

There are three data splits in this repository. All have been created from
Natural Questions data using
[this conversion script](https://github.com/google-research/language/blob/master/language/orqa/preprocessing/convert_to_nq_open.py).
To date, most works have reported results on the Original Dev set. However, we
have also created an EfficientQA Dev split to be IID with the EfficientQA
test set. The EfficientQA test set will be released at the end of the
EfficientQA competition.

| Split               | Size   | Filename                          |
|---------------------|--------|-----------------------------------|
| Train               | 87,925 | NQ-open.train.jsonl               |
| Original Dev        | 3,610  | NQ-open.dev.jsonl                 |
| EfficientQA Dev     | 1,800 | NQ-open.efficientqa.dev.1.1.jsonl  |
| EfficientQA Test    | 1,800 | NA                                 |

All of the Natural Questions data is released under the
[CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/) license.


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


