# Deploy locally

```
git clone https://github.com/ksonda/global-river-runner.git
cd deploy/local
wget https://www.sciencebase.gov/catalog/file/get/614a8864d34e0df5fb97572d?name=merit_plus.sql.gz
docker-compose up -d
```

pygeoapi should be accessible at localhost:5050. The database may take up to an hour to load depending on your hardware.
