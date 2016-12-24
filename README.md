# greensnow_cli
An unofficial Greensnow python client.


```
usage: greensnow_cli.py [-h] [-i inputfile] [-d request_delay]
                        [--regex_match regex_match] [--raw_data raw_data]

Simple unofficial Greensnow Python client.

optional arguments:
  -h, --help            show this help message and exit
  -i inputfile, --inputfile inputfile
                        File to check IPs.
  -d request_delay, --delay request_delay
                        Delay between two requests.
  --regex_match regex_match
                        The regex must match before being treat.
  --raw_data raw_data   Direct ips input instead of input file. Ignore if
                        inputfile is set.
```

### Example 1 :

##### Command :
```
python greensnow_cli.py -i examples/file1.txt --regex_match "^.* Ban.*$"
```

##### Output :
```
|        IP       |   State   | Country |
|  182.131.125.7  |  WARNING  |    CN   |
|  218.86.97.236  |  WARNING  |    CN   |
|  110.38.217.161 |  WARNING  |    PK   |
|  182.71.120.158 |  WARNING  |    IN   |
```

### Example 2 :

##### Command :
```
python greensnow_cli.py -i examples/file2.txt
```

##### Output :
```
|        IP       |   State   | Country |
| 210.180.221.136 |  WARNING  |    KR   |
|  182.131.125.7  |  WARNING  |    CN   |
|  218.86.97.236  |  WARNING  |    CN   |
|  110.38.217.161 |  WARNING  |    PK   |
|  182.71.120.158 |  WARNING  |    IN   |
|  182.71.120.159 |     OK    |    IN   |
```


### Example 3 :

##### Command :
```
python greensnow_cli.py --raw_data "182.131.125.7,110.38.217.161,182.71.120.158"
```

##### Output :
```
|        IP       |   State   | Country |
|  182.131.125.7  |  WARNING  |    CN   |
|  110.38.217.161 |  WARNING  |    PK   |
|  182.71.120.158 |  WARNING  |    IN   |
```
