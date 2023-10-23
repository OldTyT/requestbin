#!/bin/bash

function show_error() {
    local message="${1}"; local funcname="${2}"; log_date=$(date '+%Y/%m/%d:%H:%M:%S')
    echo -e "[ERROR.${funcname} ${log_date}] ${message}" >&2
}

function show_notice() {
    local message="${1}"; local funcname="${2}"; log_date=$(date '+%Y/%m/%d:%H:%M:%S')
    echo -e "[NOTICE.${funcname} ${log_date}] ${message}"
}

function prepare() {
    apt-get update
    apt-get install gcc python python-dev python-pip musl-dev g++ libevent-dev netcat  -y
    /usr/local/bin/python -m pip install --upgrade pip
    pip install flake8 setuptools
}

function lint() {
    flake8
}

function build() {
    pip install --user -r requirements.txt
    python setup.py --verbose sdist --dist-dir /build
    mkdir /tmp/test_build
    cp /build/*.tar.gz /tmp/test_build
}

function prepare_for_test() {
    cd /tmp/test_build && tar -xf *.tar.gz && cd $(ls | grep requestbin | grep -v tar)
    python setup.py install --user
    pip freeze
    cd /tmp/test_build/$(ls /tmp/test_build | grep requestbin | grep -v tar)/build/lib && export BIN_TTL=172800 && export MAX_RAW_SIZE=10240 && python requestbin &
}

function unit_test() {
    export APP_TIMEOUT=15
    until nc -z localhost 8000; do APP_TIMEOUT=$((APP_TIMEOUT-1)); sleep 1; test $APP_TIMEOUT -eq 0 && exit 1; done # 2>/dev/null
    python /tmp/test_build/$(ls /tmp/test_build | grep requestbin | grep -v tar)/requestbin/test.py
}

show_notice "Start prepare."
prepare  || {
    show_error "Error on prepare. Exit."
    exit 1
}
show_notice "Start lint."
lint || {
    show_error "Error on lint. Exit."
    exit 1
}
show_notice "Start build."
build || {
    show_error "Error on build. Exit"
    exit 1
}
show_notice "Start prepare for test."
prepare_for_test || {
    show_error "Error on test. Exit"
    exit 1
}

show_notice "Start test."
unit_test || {
    show_error "Error on unit-test. Exit"
    exit 1
}
