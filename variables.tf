
variable "location" {
 description = "The Azure location where all resources in thisdeployment should be created"
 default = "uksouth"
}
variable "SECRET_KEY" {
    default = "secret-key"
}

variable "DB_NAME" {
    default ="card_board"
}

variable "CLIENT_ID"{

}
variable "CLIENT_SECRET"{

}

variable "OAUTHLIB_INSECURE_TRANSPORT"{
    default =1
}

variable "USER_ID" {

}