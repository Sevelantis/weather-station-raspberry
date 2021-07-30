build:
	docker-compose up -d --build && docker ps

up:
	docker-compose up -d && docker ps

clean:
	docker rmi -f $(shell docker images -aq) ;
	docker rm -f $(shell docker ps -aq) ;
	docker ps -a ;
	docker images -a