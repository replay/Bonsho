#!/bin/bash

function run_test_cmd {
  CMD=${1}
  ${CMD}
  if [ ${?} != 0 ]
  then
    echo "error in ${CMD}"
    exit 1
  fi
}

run_test_cmd "flake8 ."
run_test_cmd "nosetests"
