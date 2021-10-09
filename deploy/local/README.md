# Deploy locally

`
git clone https://github.com/ksonda/global-river-runner.git
cd deploy/local
wget https://prod-is-usgs-sb-prod-publish.s3.amazonaws.com/614a8864d34e0df5fb97572d/merit_plus.sql.gz
docker-compose up -d
`

pygeoapi should be accessible at localhost:5050
