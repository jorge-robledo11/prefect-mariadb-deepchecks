terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {}

# El recurso null_resource "convert_parquet" se elimina.

resource "docker_image" "mariadb" {
  name         = "mariadb:latest"
  force_remove = true
}

resource "docker_container" "mariadb" {
  name  = "mariadb"
  image = docker_image.mariadb.image_id

  env = [
    "MYSQL_ROOT_PASSWORD=${var.mysql_root_password}",
    "MYSQL_DATABASE=${var.mysql_database}",
  ]

  ports {
    internal = var.port_internal
    external = var.port_external
  }

  # Primer punto de montaje: script de inicialización
  mounts {
    type      = "bind"
    source    = abspath("${path.module}/init.sh") # terraform/init.sh
    target    = "/docker-entrypoint-initdb.d/01_init_database.sh"
    read_only = true
  }

  # Segundo punto de montaje: directorio de datos CSV
  mounts {
    type      = "bind"
    source    = abspath("${path.module}/../data/raw") # proyecto_raiz/data/raw/
    target    = "/data_source"                        # init.sh usa /data_source/dataset_raw.csv
    read_only = true
  }

  restart        = "always"
  remove_volumes = true

}
