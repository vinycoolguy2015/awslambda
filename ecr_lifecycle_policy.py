mport boto3
from botocore.exceptions import ClientError

def list_ecr_repos_with_lifecycle(region="ap-southeast-1"):
    ecr = boto3.client("ecr", region_name=region)
    repos_with_policy = []

    # Paginate through all repos
    paginator = ecr.get_paginator("describe_repositories")
    for page in paginator.paginate():
        for repo in page["repositories"]:
            repo_name = repo["repositoryName"]
            try:
                # Try fetching lifecycle policy
                response = ecr.get_lifecycle_policy(repositoryName=repo_name)
                if "lifecyclePolicyText" in response:
                    repos_with_policy.append(repo_name)
            except ClientError as e:
                if e.response["Error"]["Code"] == "LifecyclePolicyNotFoundException":
                    # Repo does not have a lifecycle policy
                    continue
                else:
                    print(f"Error fetching policy for {repo_name}: {e}")
    
    return repos_with_policy


if __name__ == "__main__":
    region = "ap-southeast-1"  # Change as needed
    repos = list_ecr_repos_with_lifecycle(region)
    if repos:
        print("Repositories with lifecycle policies:")
        for r in repos:
            print(f" - {r}")
    else:
        print("No repositories with lifecycle policies found.")
