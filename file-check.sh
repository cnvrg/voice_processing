#!/bin/bash

# Set the token pattern you want to search for
TOKEN_PATTERN=r'\b[A-Za-z0-9]{32}\b'

# Get the commit hashes in reverse chronological order
COMMITS=$(git rev-list --all)

# Loop through each commit
for COMMIT in $COMMITS; do
    echo "Checking commit: $COMMIT"

    # Get the list of files changed in the commit
    FILES=$(git diff-tree --no-commit-id --name-only -r $COMMIT)

        # Check if the file exists before searching for the token pattern
	if [ -f "$FILE" ]; then
		# Check if the file contains the token pattern
		if grep -q "$TOKEN_PATTERN" "$FILE"; then
			echo "Token pattern found in file: $FILE"
		fi
	fi

    echo
done
