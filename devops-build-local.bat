pushd "./containers/locust"

docker-compose build

popd

docker tag registry/performance localhost:48700/registry/performance
docker push localhost:48700/registry/performance

pushd "./containers/wrk"

docker-compose build

popd