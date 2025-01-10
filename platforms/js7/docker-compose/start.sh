docker compose --env-file ./.env.sample -f docker-compose.agent.yaml up -d
docker compose --env-file ./.env.sample -f docker-compose.controller.yaml up -d
docker compose --env-file ./.env.sample -f docker-compose.js7-cockpit.yaml up -d