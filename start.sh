#!/bin/bash
source env/bin/activate
nohup pevy -c pevy.secret >pevy.out 2>pevy.err </dev/null &
