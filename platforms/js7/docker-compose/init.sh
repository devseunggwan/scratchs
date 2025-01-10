mkdir js7-agent-primary
mkdir js7-controller-primary
mkdir js7-joc-primary-config
mkdir js7-joc-primary-logs
mkdir db_data

docker compose --env-file ./.env.sample -f docker-compose.yaml up -d

cp -f hibernate.cfg.xml js7-joc-primary-config/
docker-compose exec js7-joc-primary /bin/bash -c /opt/sos-berlin.com/js7/joc/install/joc_install_tables.sh

docker-compose restart js7-joc-primary