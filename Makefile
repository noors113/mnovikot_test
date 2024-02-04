help:
	@echo 'Available commands:                                                '
	@echo '                                                                   '
	@echo 'Usage:                                                             '
	@echo 'make lint                              		   		  lint project'
	@echo 'make test                              		   		  test project'
	@echo 'make locust							  		   		    run locust'

lint:
	isort .
	black .
test:
	pytest tests/

locust:
	locust -f locustfile.py --host=http://localhost:8000 -u 300 -r 30