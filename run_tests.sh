#!/bin/bash

set -e

run_test() {

  local filename="$1"
  local searchdir="${2:-"tests"}"
  $(python -m unittest discover -p "$filename" "$searchdir")

}


while true;
  do
    case "$1" in

      -h|--help)

        cat <<"BLOCK"
Run all the tests for PyPerf. Optionall, choose one or more groups to run.

run_tests.sh [group [group [group ...]]]

Groups:

  all:                All test groups.
  profile:            Profiler tests.
  wsgi:               API tests.
  transport:          All transport tests (requires all tranport services).
  transport-amqp:     AMQP transport tests (requires ampq and guest account).
  executor:           Run the Executor tests.
BLOCK

        exit 1
        shift;;

      all)

        run_test "*"
        break;;

      profile)

        run_test "test_basic_profile.py"
        shift;;

      wsgi)

        run_test "test_wsgi_app.py"
        shift;;

      transport)

        run_test "*" "tests/transports"
        shift;;

      transport-amqp)

        run_test "test_amqp.py" "tests/transports"
        shift;;

      executor)

        run_test "test_executor.py"
        shift;;

      *)

        if [[ "$1" == "" ]]; then
          break
        fi

        echo "Unrecognized option ($1)." 1>&2
        shift;;

      --)
        shift
        break;;
    esac
  done
