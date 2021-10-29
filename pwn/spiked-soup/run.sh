#!/bin/bash

set -o xtrace

echo "Enter the amount of bytes in your ELF, a newline, then your ELF: "
read count

temp="$(mktemp)"
function cleanup {
  echo "Removing temporary file"
  rm -v "${temp}"
}
trap cleanup EXIT

head -c "${count}" > "${temp}"

timeout --foreground 30 spike -l "${temp}"
