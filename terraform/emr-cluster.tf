module "emr-logs-bucket" {
  source      = "git::git@github.com:Datatamer/terraform-aws-s3.git?ref=1.0.0"
  bucket_name = "franco-logs"
  read_write_actions = [
    "s3:HeadBucket",
    "s3:PutObject",
  ]
  read_write_paths = [""] # r/w policy permitting specified rw actions on entire bucket
}

# Set up root directory bucket
module "emr-rootdir-bucket" {
  source           = "git::git@github.com:Datatamer/terraform-aws-s3.git?ref=1.0.0"
  bucket_name      = "franco-root"
  read_write_paths = [""] # r/w policy permitting default rw actions on entire bucket
}

# Create new EC2 key pair
/*resource "tls_private_key" "emr_private_key" {
  algorithm = "RSA"
}

module "emr_key_pair" {
  source     = "terraform-aws-modules/key-pair/aws"
  version    = "1.0.0"
  key_name   = "spark-test-emr-key"
  public_key = tls_private_key.emr_private_key.public_key_openssh
}*/

resource "aws_s3_bucket_object" "sample_bootstrap_script" {
  bucket                 = module.emr-rootdir-bucket.bucket_name
  key                    = "bootstrap-actions/install_dependencies.sh"
  source                 = "./install_dependencies.sh"
  server_side_encryption = "AES256"
}

# EMR Static Spark cluster
module "emr-spark" {
  # source = "git::git@github.com:Datatamer/terraform-aws-emr.git?ref=5.0.0"
  #source = "git::git@github.com:franco-caylent/terraform-aws-emr.git?ref=feature/isolatedEmr"
  source = "git@github.com:Datatamer/terraform-aws-emr.git?ref=5.2.0"
  # Configurations
  create_static_cluster = true
  release_label         = "emr-5.29.0" # spark 2.4.4
  applications          = ["Spark", "ganglia"]
  emr_config_file_path  = "./emr.json"
  additional_tags       = {}
  bootstrap_actions     = [
    {
      name = "install_dependencies",
      path = "s3://${module.emr-rootdir-bucket.bucket_name}/bootstrap-actions/install_dependencies.sh"
      args = []
    }
  ]
  # Networking
  subnet_id  = module.tamr_vpc.compute_subnet_id
  vpc_id     = module.tamr_vpc.vpc_id
  tamr_cidrs = []
  tamr_sgs   = []

  # External resource references
  bucket_name_for_root_directory = module.emr-rootdir-bucket.bucket_name
  bucket_name_for_logs           = module.emr-logs-bucket.bucket_name
  s3_policy_arns                 = [module.emr-logs-bucket.rw_policy_arn, module.emr-rootdir-bucket.rw_policy_arn]
  bucket_path_to_logs            = "logs/spark-test-cluster/"
  key_pair_name                  = "tamr-vm-test"

  # Names
  cluster_name                  = "Franco Test Cluster"
  emr_service_role_name         = "spark-test-service-role"
  emr_ec2_role_name             = "spark-test-ec2-role"
  emr_ec2_instance_profile_name = "spark-test-instance-profile"
  emr_service_iam_policy_name   = "spark-test-service-policy"
  emr_ec2_iam_policy_name       = "spark-test-ec2-policy"
  master_instance_fleet_name    = "Spark-Test-MasterInstanceFleet"
  core_instance_fleet_name      = "Spark-Test-CoreInstanceFleet"
  emr_managed_master_sg_name    = "Spark-Test-EMR-Spark-Master"
  emr_managed_core_sg_name      = "Spark-Test-EMR-Spark-Core"
  emr_additional_master_sg_name = "Spark-Test-EMR-Spark-Additional-Master"
  emr_additional_core_sg_name   = "Spark-Test-EMR-Spark-Additional-Core"
  emr_service_access_sg_name    = "Spark-Test-EMR-Spark-Service-Access"

  # Scale
  master_instance_on_demand_count = 1
  core_instance_on_demand_count   = 2
  master_instance_type            = "m4.large"
  core_instance_type              = "r5.xlarge"
  master_ebs_size                 = 50
  core_ebs_size                   = 50
  depends_on = [
    module.tamr_vpc
  ]
}