#!/usr/bin/env bash

function previous_date {
    NUM=$1
    D="$(/bin/date +%Y%m%d --date="$NUM day")"
    echo "$D"
}

function main {
    ENV_KEY=$1
    ENV_CREDS=$2
    ENV_DRIVE=$3
    EMA_DIR=$4
    source $ENV_KEY
    source $ENV_CREDS
    source $ENV_DRIVE
    $HOME/.local/bin/pipenv run python \
        "${EMA_DIR}/scripts/download.py" \
        --conf "${EMA_DIR}/config.yaml" \
        --startdate "$(previous_date -31)" \
        --enddate "$(previous_date -1)" \
        --output "drive:ema/data"
}

main $1 $2 $3 $4
