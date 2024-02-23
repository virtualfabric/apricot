#! /bin/sh
# shellcheck disable=SC2086
# shellcheck disable=SC2089

# Required arguments
if [ -z "${BACKEND}" ]; then
    echo "BACKEND environment variable is not set"
    exit 1
fi

if [ -z "${CLIENT_ID}" ]; then
    echo "CLIENT_ID environment variable is not set"
    exit 1
fi

if [ -z "${CLIENT_SECRET}" ]; then
    echo "CLIENT_SECRET environment variable is not set"
    exit 1
fi

if [ -z "${DOMAIN}" ]; then
    echo "DOMAIN environment variable is not set"
    exit 1
fi

if [ -z "${REDIS_HOST}" ]; then
    echo "REDIS_HOST environment variable is not set"
    exit 1
fi

if [ -z "${UID_ATTRIBUTE}" ]; then
    echo "UID_ATTRIBUTE environment variable is not set"
    exit 1
fi

# Arguments with defaults
if [ -z "${PORT}" ]; then
    echo "PORT environment variable is not set: using default of 1389"
    PORT="1389"
fi

if [ -z "${REDIS_PORT}" ]; then
    echo "REDIS_PORT environment variable is not set: using default of 6379"
    REDIS_PORT="6379"
fi

# Optional arguments
EXTRA_OPTS=""
if [ -n "${ENTRA_TENANT_ID}" ]; then
    EXTRA_OPTS="${EXTRA_OPTS} --entra-tenant-id $ENTRA_TENANT_ID"
fi

# Run the server
hatch run python run.py \
    --backend "$BACKEND" \
    --client-id "$CLIENT_ID" \
    --client-secret "$CLIENT_SECRET"  \
    --domain "$DOMAIN" \
    --port "${PORT}" \
    --uid-attribute "${UID_ATTRIBUTE}" \
    --redis-host "${REDIS_HOST}" \
    --redis-port "${REDIS_PORT}" \
    $EXTRA_OPTS
