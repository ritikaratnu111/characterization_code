#!/bin/bash
vesyla -o out *.m
manas -o out -t json out/filegen
cp ./out/filegen/sim_vsim/* .
