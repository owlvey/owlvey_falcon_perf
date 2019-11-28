#!/usr/bin/env bash


locust -H http://localhost:50001 --csv=owlvey -f level_one.py --no-web -c 100 -r 10 --run-time 2m
