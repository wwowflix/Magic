param(
  [string]$Tag = "1.1.0",
  [string]$DockerUser = "wwowdocker"
)

docker build -t magic:$Tag .
docker tag magic:$Tag $DockerUser/magic:$Tag
docker tag magic:$Tag $DockerUser/magic:latest
docker push $DockerUser/magic:$Tag
docker push $DockerUser/magic:latest
