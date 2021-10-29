#!/bin/sh
socat -dd TCP4-LISTEN:7007,fork,reuseaddr EXEC:'./start.sh',pty,echo=0,rawer,iexten=0
