terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = "~>4.47"
    }
  }
  required_version ="~> 1.12"
}

provider "azurerm" {
  features{
  
  }
}