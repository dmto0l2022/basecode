echo ">>>>>>> container_application_1 <<<<<<<<"
podman logs --since 10m container_application_1
podman logs --since 10m container_fastapi_data_1
podman logs --since 10m container_fastapi_about_1
podman logs --since 10m container_mariadb
podman logs --since 10m container_redis_1
