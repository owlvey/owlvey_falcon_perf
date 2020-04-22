set PYTHONPATH=.

rem python -m unittest specs.test_A001.TargetTest.test_load
rem locust -H http://192.168.0.14:45001 --csv=A001 -f performance/test_A001_load.py --no-web -c 50 -r 5 --run-time 10m --stop-timeout 60  --only-summary


python  -m unittest specs.test_A002.TargetTest.test_restore

echo "start test ========================================"

set mydate=%date:~10,4%_%date:~7,2%_%date:~4,2%

set mytime=%time:~0,2%_%time:~3,2%_%time:~6,2%

locust -H http://192.168.0.14:45001 --csv="A002_%mydate%_%mytime%" -f performance/test_A002_load.py --no-web -c 10 -r 2 --run-time 10m --stop-timeout 30  --only-summary

