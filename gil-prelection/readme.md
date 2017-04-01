# commands
export PATH=$PATH:$HOME/pypy-stm-2.5.1-linux64/bin:/opt/jython/bin
./draw.sh python2 threads.py 1
./draw.sh python2 threads.py 4

./draw.sh python2 process.py 1
./draw.sh python2 process_correct.py 1
./draw.sh python2 process_correct.py 4
./draw.sh python2 pool.py 4

./draw.sh /opt/jython/bin/jython threads.py 4
./draw.sh ipy threads.py 4

./draw.sh pypy threads.py 1
./draw.sh pypy threads.py 4
./draw.sh pypy-stm threads.py 4

./make.sh
./draw.sh python2 threads_cython.py 1
./draw.sh python2 threads_cython.py 4

