mkdir js7-agent-primary
mkdir js7-controller-primary
mkdir js7-joc-primary-config
mkdir js7-joc-primary-logs
mkdir db_data

docker network create js7

docker compose --env-file ./.env.sample -f docker-compose.agent.yaml up -d
docker compose --env-file ./.env.sample -f docker-compose.controller.yaml up -d
docker compose --env-file ./.env.sample -f docker-compose.js7-cockpit.yaml up -d

cp -f hibernate.cfg.xml js7-joc-primary-config/
docker-compose exec js7-joc-primary /bin/sh -c /opt/sos-berlin.com/js7/joc/install/joc_install_tables.sh