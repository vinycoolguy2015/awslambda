#!/bin/bash

# List all Lambda functions
FUNCTIONS=$(aws lambda list-functions --query "Functions[].FunctionName" --output text)

# Iterate over each function
for FUNCTION in $FUNCTIONS; do
  echo $FUNCTION
  # Define the specific qualifiers to check
  QUALIFIERS=("TM-FSS-MANAGED" "\$LATEST" "provisioned")

  # Check Provisioned Concurrency for each specific qualifier
  for QUALIFIER in "${QUALIFIERS[@]}"; do
    # Get provisioned concurrency config
    RESPONSE=$(aws lambda get-provisioned-concurrency-config --function-name "$FUNCTION" --qualifier "$QUALIFIER" 2>/dev/null)

    # Check if the response contains RequestedProvisionedConcurrentExecutions
    if [ $? -eq 0 ]; then
      REQUESTED=$(echo "$RESPONSE" | jq -r '.RequestedProvisionedConcurrentExecutions // 0')
      
      # Check if RequestedProvisionedConcurrentExecutions > 0
      if [ "$REQUESTED" -gt 0 ]; then
        echo "Function: $FUNCTION, Qualifier: $QUALIFIER, RequestedProvisionedConcurrentExecutions: $REQUESTED"
      fi
    fi
  done
done
