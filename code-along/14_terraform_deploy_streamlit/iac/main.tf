resource "azurerm_resource_group" "rgweb" {
  name     = "terror-webapp-resources"
  location = "swedencentral"
}


resource "azurerm_storage_account" "terror_data_storage" {
  name                     = "leterrorletrroename"
  resource_group_name      = azurerm_resource_group.rgweb.name
  location                 = azurerm_resource_group.rgweb.location
  account_tier             = "Standard"
  account_replication_type = "GRS" # Geo-Redundant Storage (good for data)
}

resource "azurerm_container_registry" "acr" {
  name                = "acrterror"
  resource_group_name = azurerm_resource_group.rgweb.name
  location            = azurerm_resource_group.rgweb.location
  sku                 = "Basic"
  admin_enabled       = true
}

resource "azurerm_service_plan" "aspweb" {
  name                = "asp"
  resource_group_name = azurerm_resource_group.rgweb.name
  location            = azurerm_resource_group.rgweb.location
  os_type             = "Linux"
  sku_name            = "S1"
}

resource "azurerm_linux_web_app" "alwawebb" {
  name                = "alwaeencore"
  resource_group_name = azurerm_resource_group.rgweb.name
  location            = azurerm_resource_group.rgweb.location
  service_plan_id     = azurerm_service_plan.aspweb.id

  site_config {
    application_stack {
      docker_image_name   = "acrterror.azurecr.io/terradashboard:latest"
      docker_registry_url = "https://acrterror.azurecr.io"
    }
  }
  # app_settings = {
  #   # Note: We use the account's primary access key for DuckDB connection
  #   "AZURE_STORAGE_ACCOUNT_NAME" = azurerm_storage_account.terror_data_storage.name
  #   "AZURE_STORAGE_ACCOUNT_KEY"  = azurerm_storage_account.terror_data_storage.primary_access_key
  # }
}
