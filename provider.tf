provider "github" {
  app_auth {
    id              = "1201094"  
    installation_id = "63770249" 
    pem_file        = var.GH_APP_TOKEN
  }
  owner = "myTestOrg0" 
}
