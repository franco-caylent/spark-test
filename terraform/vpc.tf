module "tamr_vpc" {
    source = "git::git@github.com:franco-caylent/terraform-aws-networking.git?ref=feature/mvp"
    vpc_cidr_block        = "10.0.0.0/16"
    application_subnet_cidr_block = "10.0.0.0/24"
    compute_subnet_cidr_block = "10.0.1.0/24"
    data_subnet_cidr_blocks = ["10.0.2.0/24", "10.0.3.0/24"]
    load_balancing_subnets_cidr_blocks = ["10.0.4.0/24", "10.0.5.0/24"]
    public_subnets_cidr_blocks = ["10.0.6.0/24", "10.0.7.0/24"]
    ingress_cidr_blocks   = ["0.0.0.0/0"]
    availability_zones    = ["us-west-1a","us-west-1b"]
    create_public_subnets = true
    enable_nat_gateway    = true
    create_load_balancing_subnets = true
    tags = {
        "application": "tamr",
        "Terraform": "true"
        "Name": "tmp-franco"
    }
}
