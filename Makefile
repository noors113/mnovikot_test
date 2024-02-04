help:
	@echo 'Available commands:                                                '
	@echo '                                                                   '
	@echo 'Usage:                                                             '
	@echo ' make lint                              		   		  lint project'
	@echo ' make test                              		   		  test project'

lint:
	isort .
	black .
test:
	pytest tests/