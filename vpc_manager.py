from flask import Flask, render_template, request, redirect, url_for, session, flash
import boto3

app = Flask(__name__)
app.secret_key = "supersecretkey123"  # Needed for session and flash messages

# ------------------ AWS Session Management ------------------
def create_session(access_key, secret_key, region):
    """Create boto3 session with given credentials"""
    return boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region
    )

def get_ec2_client():
    """Return EC2 client if logged in"""
    if "aws_session" in session:
        return session["aws_session"].client("ec2")
    else:
        return None

# ------------------ VPC Operations ------------------
def list_vpcs(region):
    ec2 = session["aws_session"].client("ec2", region_name=region)
    response = ec2.describe_vpcs()
    vpcs = []
    for vpc in response.get("Vpcs", []):
        tags = vpc.get("Tags", [])
        name_tag = next((t["Value"] for t in tags if t["Key"] == "Name"), "N/A")
        vpcs.append({
            "VpcId": vpc["VpcId"],
            "CidrBlock": vpc["CidrBlock"],
            "Name": name_tag
        })
    return vpcs

def create_vpc(region, cidr_block, tag_name):
    ec2 = session["aws_session"].client("ec2", region_name=region)
    response = ec2.create_vpc(CidrBlock=cidr_block)
    vpc_id = response["Vpc"]["VpcId"]
    ec2.create_tags(Resources=[vpc_id], Tags=[{"Key": "Name", "Value": tag_name}])
    return vpc_id

def delete_vpc(region, vpc_id):
    ec2 = session["aws_session"].client("ec2", region_name=region)
    ec2.delete_vpc(VpcId=vpc_id)
    return vpc_id

def create_subnet(region, vpc_id, cidr_block):
    ec2 = session["aws_session"].client("ec2", region_name=region)
    response = ec2.create_subnet(VpcId=vpc_id, CidrBlock=cidr_block)
    subnet_id = response["Subnet"]["SubnetId"]
    return subnet_id

# ------------------ Routes ------------------
@app.route("/", methods=["GET", "POST"])
def login():
    """AWS login page"""
    if request.method == "POST":
        access_key = request.form.get("access_key")
        secret_key = request.form.get("secret_key")
        region = request.form.get("region")
        try:
            session["aws_session"] = create_session(access_key, secret_key, region)
            session["region"] = region
            flash("✅ Logged in successfully!", "success")
            return redirect(url_for("dashboard"))
        except Exception as e:
            flash(f"❌ Login failed: {str(e)}", "danger")
    return render_template("login.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "aws_session" not in session:
        return redirect(url_for("login"))

    region = session.get("region", "")
    vpcs = list_vpcs(region)

    # Handle form submissions
    if request.method == "POST":
        if "create_vpc" in request.form:
            cidr = request.form.get("cidr")
            tag = request.form.get("tag")
            try:
                vpc_id = create_vpc(region, cidr, tag)
                flash(f"✅ Created VPC {vpc_id}", "success")
                vpcs = list_vpcs(region)
            except Exception as e:
                flash(f"❌ Error creating VPC: {str(e)}", "danger")

        elif "delete_vpc" in request.form:
            vpc_id = request.form.get("vpc_id")
            try:
                delete_vpc(region, vpc_id)
                flash(f"🗑️ Deleted VPC {vpc_id}", "success")
                vpcs = list_vpcs(region)
            except Exception as e:
                flash(f"❌ Error deleting VPC: {str(e)}", "danger")

        elif "create_subnet" in request.form:
            vpc_id = request.form.get("vpc_id")
            subnet_cidr = request.form.get("subnet_cidr")
            try:
                subnet_id = create_subnet(region, vpc_id, subnet_cidr)
                flash(f"✅ Created Subnet {subnet_id} in VPC {vpc_id}", "success")
            except Exception

