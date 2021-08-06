variable "name_prefix" {
  type        = string
  description = "A prefix to add to the names of all created resources."
  default     = "tamr-config-test"
}

variable "ingress_cidr_blocks" {
  type        = list(string)
  description = "List of CIDR blocks from which ingress to ElasticSearch domain, Tamr VM, Tamr Postgres instance are allowed (i.e. VPN CIDR)"
  default     = ["0.0.0.0/0"]
}
/*
variable "vpc_id" {
  type        = string
  description = "VPC ID of deployment"
  default = "vpc-0055bc68852d4f6d6"
}

variable "subnet_id" {
  type        = string
  description = "Subnet ID for ElasticSearch domain, Tamr VM, EMR cluster"
  default = "subnet-0cf41113ab180544c"
}
*/