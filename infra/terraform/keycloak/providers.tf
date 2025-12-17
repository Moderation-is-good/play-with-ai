terraform {
  required_version = ">= 1.5.0"
  required_providers {
    keycloak = {
      source  = "mrparkers/keycloak"
      version = "~> 4.1"
    }
  }
}

provider "keycloak" {
  client_id     = var.kc_admin_client_id
  client_secret = var.kc_admin_client_secret
  url           = var.kc_url
  realm         = "master"
  tls_insecure_skip_verify = false
}
