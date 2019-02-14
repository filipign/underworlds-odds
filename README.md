## WH:U odds
Simple script for calculating chances of success/draw/failure of an attack action in Warhammer: Underworlds.

Basically, it simulate all possible combinations of dice rolls and calculate success/fail ratio, but includes many possible modifactors.

### Commands
Run script using:
```
./main.py
```

Run tests using
```
./tests.py
```

### Tests
Test coverage
```
coverage run -m unittest discover -s .
coverage report -m
```

Latest report
```
Name                 Stmts   Miss  Cover   Missing
--------------------------------------------------
characteristics.py      13      0   100%
odds.py                 76     27    64%   21-23, 28-29, 102-123, 135-138, 152-171
tests.py                83      1    99%   127
--------------------------------------------------
TOTAL                  172     28    84%
```