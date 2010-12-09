# Makefile for Dionex Funkload Tests
.PHONY: clean all start stop restart status
.PHONY:	test credential_test bench credential_bench
.PHONY:	start_monitor stop_monitor restart_monitor
.PHONY:	start_credential stop_credential restart_credential

CREDCTL := bin/fl-credential-ctl credentials.conf
MONCTL := bin/fl-monitor-ctl monitor.conf
MONCTL_CARVING := bin/fl-monitor-ctl monitor-carving.conf
MONCTL_CHOPPING := bin/fl-monitor-ctl monitor-chopping.conf
MONCTL_PARING := bin/fl-monitor-ctl monitor-paring.conf
MONCTL_WAKIZASHI := bin/fl-monitor-ctl monitor-wakizashi.conf


ifdef URL
# FunkLoad options
	FLOPS = -u $(URL)
else
	FLOPS = --accept-invalid-links -vv
endif

all: test

mklogs:
	mkdir -p logs

# testing
qa_test: mklogs
	bin/fl-run-test test_QA.py --simple-fetch -vd $(FLOPS)

qa_test_auth: mklogs
	bin/fl-run-test test_QAauth.py -vd $(FLOPS)

qa_test_full: mklogs
	bin/fl-run-test test_QAfull.py -vd $(FLOPS)

prod_test: mklogs
	bin/fl-run-test test_Prod.py -vd $(FLOPS)

# benching
qa_bench: mklogs
	#$(MONCTL) restart
	-bin/fl-run-bench test_QA.py QA.test_loads
	#-bin/fl-build-report --html -o reports logs/qa-bench.xml
	#$(MONCTL) stop

qa_bench_auth: mklogs
	#$(MONCTL) restart
	-bin/fl-run-bench test_QAauth.py QAauth.test_loads
	#-bin/fl-build-report --html -o reports logs/qa-bench.xml
	#$(MONCTL) stop

qa_bench_full: mklogs
	#$(MONCTL) restart
	-bin/fl-run-bench --accept-invalid-links -D 5400 test_QAfull.py QA.test_loads
	#-bin/fl-build-report --html -o reports logs/qa-bench.xml
	#$(MONCTL) stop

prod_bench: mklogs
	#$(MONCTL) restart
	-bin/fl-run-bench test_Prod.py Prod.test_loads
	-bin/fl-build-report --html -o reports logs/prod-bench.xml
	#$(MONCTL) stop

# monitor ctl
start_monitor:
	$(MONCTL) start

stop_monitor:
	-$(MONCTL) stop

start_monitor_carving:
	$(MONCTL_CARVING) start

stop_monitor_carving:
	-$(MONCTL_CARVING) stop

start_monitor_chopping:
	$(MONCTL_CHOPPING) start

stop_monitor_chopping:
	-$(MONCTL_CHOPPING) stop

start_monitor_paring:
	$(MONCTL_PARING) start

stop_monitor_paring:
	-$(MONCTL_PARING) stop

start_monitor_wakizashi:
	$(MONCTL_WAKIZASHI) start

stop_monitor_wakizashi:
	-$(MONCTL_WAKIZASHI) stop

# credential ctl
start_credential:
	$(CREDCTL) start

stop_credential:
	-$(CREDCTL) stop

restart_credential:
	$(CREDCTL) restart

# misc
status:
	$(MONCTL) status;
	$(CREDCTL) status;

stop: stop_monitor stop_credential

start: start_monitor start_credential

restart: restart_monitor restart_credential

buildout:
	python ./bootstrap.py -d -v 1.4.4
	./bin/buildout

clean:
	-find . "(" -name "*~" -or  -name ".#*" ")" -print0 | xargs -0 rm -f
