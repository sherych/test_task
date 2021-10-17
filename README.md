# test_task

Script scanner.py searching for all accessible and resolvable second level domain names. Then it provides summary about one of selected domains:
-
- list of IP addresses assosiated with that A record
- geolocation of IP address from public resource
- statistics of load test (latency, requests per second, response codes)
***
To launch script you need to pass aditional parameters for load testing:

    python3 scanner.py -c N -d N trusted.domain

where:
- *-c* is number of concurrent connections for load test
- *-d* is duration of load test
- *trusted.domain* is a domain that we 100% trust as one that belongs to company

Script will generate of resolved domain names:

    [1] name.domain1
    [2] name.domain2
    [3] name.domain3

Finally you can choose one of them to make a load test and gather summary about this domain name.