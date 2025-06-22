# Do it once in the beginning
# gcloud auth login
# gcloud config set project "nebula-prime-13736"


gcloud functions deploy api \
  --runtime python312 \
  --trigger-http \
  --allow-unauthenticated \
  --entry-point handler \
  --region us-central1 \
  --timeout=360 \
  --memory 768MB \
  --max-instances 20
