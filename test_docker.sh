# Submissions to the Natural Questions leaderboard should be packaged in a
# Docker container, and submitted as outlined in
# https://ai.google.com/research/NaturalQuestions/competition/.
#
# This script can be used to test submissions locally on a small sample
# of the Natural Questions development data.

# Change the data directory to avoid re-downloading data frequently.
DATA_DIR="/tmp/natural-questions/tiny-dev"
mkdir -p "${DATA_DIR}"

# Download small data sample to test NQ submission.
if [ ! -f "${DATA_DIR}" ]; then
  gsutil cp -R "gs://bert-nq/tiny-dev/*" "${DATA_DIR}"
fi

# Remove --runtime=nvidia if you have not installed docker-nvidia locally.
IMAGE_NAME="nq-submission"
docker build --tag="${IMAGE_NAME}" .
docker run --runtime=nvidia -a stdin -a stdout -a stderr -v "${DATA_DIR}":/data \
  "${IMAGE_NAME}" bash "/nq_model/submission.sh" \
  "/data/nq-dev-sample.no-annot.jsonl.gz" \
  "/data/predictions.json"

# Install the eval code.
pip install natural-questions

# Run the evaluation.
python -m natural_questions.nq_eval \
  --gold_path="${DATA_DIR}/nq-dev-sample.jsonl.gz" \
  --predictions_path="${DATA_DIR}/predictions.json"
