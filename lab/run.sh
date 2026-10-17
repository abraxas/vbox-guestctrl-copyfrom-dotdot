#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

export COMPOSE_PROJECT_NAME="${COMPOSE_PROJECT_NAME:-vbox-guestctrl-copyfrom-dotdot}"
export PYTHONUNBUFFERED=1
export COMPOSE_PROGRESS="${COMPOSE_PROGRESS:-plain}"
export COMPOSE_ANSI="${COMPOSE_ANSI:-never}"

LABEL="vbox-guestctrl-copyfrom-dotdot"
WITNESS="VBOX-GUESTCTRL-COPYFROM-DOTDOT-WITNESS"

chmod +x poc.py

down() {
  echo "== docker compose down -v =="
  docker compose -p "${COMPOSE_PROJECT_NAME}" down -v --remove-orphans || true
}

fail_setup() {
  local reason="$1"
  echo "FAIL ${LABEL} ${reason} ${WITNESS}" | tee poc-last-run.txt
  docker compose -p "${COMPOSE_PROJECT_NAME}" logs --no-color --tail=80 || true
  exit 1
}

trap down EXIT

echo "== docker compose down (clean) =="
down

echo "== docker compose up --build =="
up_ok=0
for attempt in $(seq 1 8); do
  if docker compose -p "${COMPOSE_PROJECT_NAME}" up --build -d; then
    up_ok=1
    break
  fi
  echo "compose-up-retry attempt=${attempt}"
  sleep 8
  down
done
if [[ "${up_ok}" != 1 ]]; then
  fail_setup "compose-up-failed"
fi

echo "== wait gadget =="
ok=0
for i in $(seq 1 60); do
  if docker compose -p "${COMPOSE_PROJECT_NAME}" exec -T gadget python3 -c 'print("pong")' \
      >/dev/null 2>&1; then
    ok=1
    echo "gadget-ready attempt=${i}"
    break
  fi
  echo "gadget-wait attempt=${i}"
  sleep 1
done
if [[ "${ok}" != 1 ]]; then
  fail_setup "gadget-not-ready"
fi

echo "== poc.py (in-container source harness) =="
set +e
docker compose -p "${COMPOSE_PROJECT_NAME}" exec -T gadget python3 /lab/poc.py \
  | tee poc-last-run.txt
rc=${PIPESTATUS[0]}
set -e

if ! tail -n1 poc-last-run.txt 2>/dev/null | grep -qE '^(SUCCESS|FAIL) '; then
  echo "FAIL ${LABEL} poc-exit=${rc} ${WITNESS}" >> poc-last-run.txt
  rc=1
fi

exit "${rc}"
