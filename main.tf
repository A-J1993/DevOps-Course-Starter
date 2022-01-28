terraform {
 required_providers {
 azurerm = {
 source = "hashicorp/azurerm"
 version = ">= 2.49"
 }
 }
     backend "azurerm" {
        resource_group_name  = "CreditSuisse2_Ali-JohnMirsepassi_ProjectExercise"
        storage_account_name = "tfstate1304206509"
        container_name       = "tfstate"
        key                  = "terraform.tfstate"
    }
}
provider "azurerm" {
 features {}
}
data "azurerm_resource_group" "main" {
 name = "CreditSuisse2_Ali-JohnMirsepassi_ProjectExercise"
}

resource "azurerm_app_service_plan" "main" {
 name = "terraformed-asp"
 location = data.azurerm_resource_group.main.location
 resource_group_name = data.azurerm_resource_group.main.name
 kind = "Linux"
 reserved = true
 sku {
 tier = "Basic"
 size = "B1"
 }
}
resource "azurerm_app_service" "main" {
 name = "ajm-tf-based-app"
 location = data.azurerm_resource_group.main.location
 resource_group_name = data.azurerm_resource_group.main.name
 app_service_plan_id = azurerm_app_service_plan.main.id
 site_config {
 app_command_line = ""
 linux_fx_version = "DOCKER|aj1993/my-image-prod:latest"
 }
 app_settings = {
 "SECRET_KEY" = var.SECRET_KEY
 "DOCKER_REGISTRY_SERVER_URL" = "https://index.docker.io"
 "MONGO_CLIENT" = "mongodb://${azurerm_cosmosdb_account.main.name}:${azurerm_cosmosdb_account.main.primary_key}@${azurerm_cosmosdb_account.main.name}.mongo.cosmos.azure.com:10255/DefaultDatabase?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000"
 
 "DB_NAME"= var.DB_NAME
 
 "CLIENT_ID"= var.CLIENT_ID
 "CLIENT_SECRET"= var.CLIENT_SECRET
 
 "OAUTHLIB_INSECURE_TRANSPORT"=1
 
 "USER_ID"= var.USER_ID
 "REDIRECT_URI"="https://ajm-tf-based-app.azurewebsites.net/login/callback"
 
 }
}


resource "azurerm_cosmosdb_account" "main" {
  name                = "ajm-tfex-cosmosdb-account" 
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  capabilities { name = "EnableServerless" }
  capabilities { name = "EnableMongo" }
  offer_type          = "Standard"
  kind                = "MongoDB"

  mongo_server_version = "4.0"
  

  consistency_policy {
    consistency_level       = "BoundedStaleness"
    max_interval_in_seconds = 300
    max_staleness_prefix    = 100000
  }

  geo_location {
    location          = data.azurerm_resource_group.main.location
    failover_priority = 0
  }
}
  


resource "azurerm_cosmosdb_mongo_database" "ajm-cosmos" {
 name                = "ajm-cosmos"
 resource_group_name = "CreditSuisse2_Ali-JohnMirsepassi_ProjectExercise"
 account_name        = azurerm_cosmosdb_account.main.name
 #lifecycle { prevent_destroy = true }
}
