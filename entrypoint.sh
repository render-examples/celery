#!/usr/bin/env bash
set -euo pipefail

# Démarrer RabbitMQ en mode détaché (daemon)
rabbitmq-server -detached

# Attendre que rabbitmq soit prêt (loop vérification)
timeout=60
count=0
until rabbitmqctl status >/dev/null 2>&1; do
  sleep 1
  count=$((count+1))
  if [ "$count" -ge "$timeout" ]; then
    echo "RabbitMQ n'a pas démarré après ${timeout}s" >&2
    tail -n 200 /var/log/rabbitmq/*.log || true
    exit 1
  fi
done

echo "RabbitMQ démarré — lancement de Flower"

# Lancer Flower (sur le port 5555 dans le conteneur)
# Broker pointe sur localhost puisque RabbitMQ tourne dans le même conteneur
exec flower --broker=amqp://admin:admin@localhost:5672// --port=5555
