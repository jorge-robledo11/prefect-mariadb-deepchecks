variable "mysql_root_password" {
  description = "Password del root de MariaDB"
  type        = string
}

variable "mysql_database" {
  description = "Nombre de la base de datos a crear"
  type        = string
}

variable "port_internal" {
  description = "Puerto interno de MariaDB dentro del contenedor"
  type        = number
}

variable "port_external" {
  description = "Puerto externo de MariaDB en el host"
  type        = number
}
