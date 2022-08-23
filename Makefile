default:
	@echo "Usage:"
	@echo "$$ make clean|build|upload|release|install"
clean:
	@rm -rf build dist VERSION *.egg-info
build:
	python setup.py bdist_wheel
	find ./dist/ -name "*py3*.whl" -exec python -m remake_pyconly_wheel {} dist \;
upload:
	twine upload ./dist/*-py3*.whl -r som
release:
	make clean
	make build
	make upload
install:
	python setup.py install
uninstall:
	python setup.py uninstall
build-tag:
	# make build-tag -e tag=###
	git checkout ${tag}
	make build
docker-image:
	docker build -t icersong/box-server .
run:
	unset CONFIG_MODE && python -m box_server
run-dev:
	set CONFIG_MODE=develop && python -m box_server
run-with-gunicon:
	gunicorn -c conf/gunicorn-conf.py box_server.site:app
run-dev-with-gunicon:
	gunicorn -c conf/gunicorn-conf-develop.py box_server.site:app
run-mqtt-client:
	set FLASK_APP=box_server.site && python -m box_server.mqtt
build-docker-base:
	docker build -f Dockerfile.base --tag icersong/gunicorn .
build-docker-base-tag:
	docker build -f Dockerfile.base --tag icersong/gunicorn:20.0.4-python3.9.1-alpine3.13-`date "+%Y%m%d%H%M"` .
build-docker-app:
	docker build -f Dockerfile.app --tag icersong/box-server .
build-docker-app-tag:
	docker build -f Dockerfile.app --tag icersong/box-server:`date "+%Y%m%d%H%M"` .
docker-prune:
	docker system prune -f
docker-initdb:
	docker run --rm icersong/box-server python -m box_server initdb
docker-run-daemon:
	docker run -d --name box-server --restart=always -p 7777:80 \
	-v /srv/box-server:/usr/local/box-server \
	-v /srv/box-server/var/local/box_server:/var/local/box_server \
	-v /srv/box-server/var/log:/var/log \
	icersong/box-server
test-local:
	python -m tests.test_blueprint_smartbox -b
test-server:
	python -m tests.test_blueprint_smartbox -b --url-root http://smart-factory.cn
