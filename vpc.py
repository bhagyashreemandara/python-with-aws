import boto3

def list_vpcs(session):
    ec2 = session.client("ec2")
    response = ec2.describe_vpcs()
    vpcs = response.get("Vpcs", [])

    if not vpcs:
        print("No VPCs found in this region.")
    else:
        print("VPCs:")
        for vpc in vpcs:
            tags = vpc.get("Tags", [])
            name_tag = next((t["Value"] for t in tags if t["Key"] == "Name"), "N/A")
            print(f"  VPC ID: {vpc['VpcId']}, CIDR: {vpc['CidrBlock']}, Name: {name_tag}")

def create_vpc(session):
    ec2 = session.client("ec2")

    # Get input from user
    cidr_block = input("Enter CIDR block for new VPC (e.g., 10.0.0.0/16): ")
    tag_name = input("Enter Name tag for the VPC: ")

    # Create VPC
    response = ec2.create_vpc(CidrBlock=cidr_block)
    vpc_id = response["Vpc"]["VpcId"]

    # Add tag
    ec2.create_tags(
        Resources=[vpc_id],
        Tags=[{"Key": "Name", "Value": tag_name}]
    )

    print(f"✅ Created VPC {vpc_id} with CIDR {cidr_block} and Name {tag_name}")
    return vpc_id

def main():
    # Take region as input
    region = input("Enter AWS region (e.g., ap-south-1, us-east-1): ")

    # Create a session using profile
    session = boto3.Session(profile_name="myprofile", region_name=region)

    # First list existing VPCs
    print("\n--- Existing VPCs ---")
    list_vpcs(session)

    # Ask if user wants to create new VPC
    choice = input("\nDo you want to create a new VPC? (yes/no): ").strip().lower()
    if choice == "yes":
        create_vpc(session)

        # List again
        print("\n--- VPCs after creation ---")
        list_vpcs(session)

if __name__ == "__main__":
    main()

