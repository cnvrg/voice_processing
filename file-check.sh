#!/bin/bash

# Set the token patterns you want to search for
TOKEN_PATTERN_1="^[A-Za-z0-9+/]{44}=="
TOKEN_PATTERN_2="^[A-Za-z0-9+/]{28}="

# Get the commit hashes in reverse chronological order
COMMITS=$(git rev-list --all)

# Loop through each commit
for COMMIT in $COMMITS; do
    echo "Checking commit: $COMMIT"

    # Get the list of files changed in the commit
    FILES=$(git diff-tree --no-commit-id --name-only -r $COMMIT)

    # Loop through each changed file
    for FILE in $FILES; do
        # Check if the file contains either token pattern as a whole word
        if grep -q -w -E "$TOKEN_PATTERN_1|$TOKEN_PATTERN_2" "$FILE"; then
            echo "Token pattern found in file: $FILE"
        fi
    done

    echo
done
