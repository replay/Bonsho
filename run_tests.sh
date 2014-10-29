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
cmd="nosetests"

if [ "${1}" == "cover" ]
then
   cmd="${cmd} --with-coverage3 --cover3-html --cover3-inclusive"
fi

run_test_cmd "${cmd}"
