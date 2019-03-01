|WARNING: Once you have created your Docker image and uploaded it to the NQ competition site, you must  grant our service account read access. Otherwise your Docker images will be private and we won't be able to run them. |
| :--- |
| 1. Go to the storage tab in the gcloud console. |
| 2. Locate the artifacts bucket. It should have a name like `artifacts.<project-name >.appspot.com` |
| 3. Click the dropdown for the bucket and select "Edit Bucket Permissions". |
| 4. Grant Storage Object Viewer permissions to the following user: `mljam-compute@mljam-205019.iam.gserviceaccount.com` |

# Building a Docker Image for the Natural Questions Competition
First, make sure that you have set up a profile as instructed on the
[Natural Questions competition site](http://ai.google.com/research/NaturalQuestions/competition).

You must submit your model as a Docker image. You are allowed to use whatever
software dependencies you want, but those dependencies must be included in your
Docker image. Let's say your model is a Tensorflow model. For this, you can use
the official tensorflow Docker container as the base container image:

```dockerfile
FROM tensorflow/tensorflow:latest
ADD nq_model /nq_model/
```

The first line of this Dockerfile says to use the official Tensorflow Docker
image as the starting point of the image. The second line says to add the
contents of a directory called `nq_model` to a folder called
`/nq_model` inside the image. Read the Docker manual for more details
on how to use Dockerfiles.

The folder `/nq_model` is expected to contain a script called
`submission.sh`. The NQ test set is in a number of gzipped jsonl files
with exactly the same format as the released development set. During
evaluation, the `/nq_model/submission.sh` script contained in
your Docker image will be called with an argument `input_path` that
matches the files containing the test set. Another argument `output_path`
tells your code where to write predictions for each of the input examples.
For a complete description of the prediction format, please see the
[evaluation script](nq_eval.py).

Below, we give an example `submission.sh` that works with the
[`nq_export_scorer.py`](https://github.com/google-research/language/tree/master/language/question_answering/experiments/nq_export_scorer.py)
 executable released along with the NQ baselines.

```shell
#!/bin/bash
#
# submission.sh: The script to be launched in the Docker image.
#
# Usage: submission.sh <input_path> <output_path>
#   input_path: File pattern (e.g. <input dir>/nq-test-??.jsonl.gz).
#   output_path: Path to JSON file containing predictions (e.g. predictions.json).
#
# Sample usage:
#   submission.sh input_path output_path

INPUT_PATH=$1
OUTPUT_PATH=$2

# YOUR CODE HERE!
#
# For example, to run the baseline system from:
#  https://github.com/google-research/language/tree/master/language/question_answering/experiments/nq_export_scorer.py)

python -m language.question_answering.experiments.nq_export_scorer
  --input_data_pattern=${INPUT_PATH} \
  --output_path=${OUTPUT_PATH} \
  --context_export_dir=<path_to_exported_long_answer_model_within_docker_image> \
  --entity_export_dir=<path_to_exported_short_answer_model_within_docker_image>
```

When you upload your Docker image to the
[NQ competition site](http://ai.google.com/research/NaturalQuestions/competition),
`/nq_model/submission.sh` will be called with `input_path` and
`output_path` arguments that point to the test data input, and the output
file that will be fed to the evaluation script, respectively.

Remember that each team is only allowed to make one submission per week to the
NQ leaderboard. But you are allowed to run as many times as you like on
the 200 item sample that we provide so that you can test your uploaded Docker
image.
