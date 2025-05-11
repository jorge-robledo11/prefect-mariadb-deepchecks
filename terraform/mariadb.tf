terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {}

# (Opcional) si usas conversión automática:
resource "null_resource" "convert_parquet" {
  provisioner "local-exec" {
    command = <<EOC
python3 - <<EOF
import pandas as pd
df = pd.read_parquet("data/dataset.parquet")
df.to_csv("data/dataset.csv", index=False)
EOF
    EOC
  }
  triggers = { parquet_hash = filesha256("data/dataset.parquet") }
}

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

  mounts {
    type   = "bind"
    source = "${abspath(path.module)}/data"
    target = "/docker-entrypoint-initdb.d"
  }

  restart        = "always"
  remove_volumes = true

  # garantiza que primero convierta el Parquet
  depends_on = [null_resource.convert_parquet]
}
