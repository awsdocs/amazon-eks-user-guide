#!/bin/bash

set -e  # Exit on any error

# Configuration
GITHUB_SSH_URL="git@github.com:awsdocs/amazon-eks-user-guide.git"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper function for printing status messages
print_status() {
    echo -e "${GREEN}==>${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}Warning:${NC} $1"
}

print_error() {
    echo -e "${RED}Error:${NC} $1"
    exit 1
}

# Check if we're in a git repository
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    print_error "Not in a git repository"
fi

# Check if current branch is mainline
current_branch=$(git symbolic-ref --short HEAD)
if [ "$current_branch" != "mainline" ]; then
    print_error "Must be on 'mainline' branch to sync. Currently on '$current_branch'"
fi

# Check for origin remote
if ! git remote | grep -q "^origin$"; then
    print_error "Remote 'origin' not found"
fi

# Check for github remote, add if missing
if ! git remote | grep -q "^github$"; then
    print_status "Github remote not found. Adding it..."
    if ! git remote add github "$GITHUB_SSH_URL"; then
        print_error "Failed to add github remote"
    fi
fi

# Test GitHub authentication
print_status "Testing GitHub authentication..."
if ! git ls-remote github &>/dev/null; then
    print_error "GitHub authentication failed. Please check your SSH keys and permissions"
fi

# Check for uncommitted changes
 if ! git diff-index --quiet HEAD --; then
     print_warning "You have uncommitted changes. Please commit or stash them before syncing."
     exit 1
 fi

print_status "Fetching from github remote..."
if ! git fetch github; then
    print_error "Failed to fetch from github remote. Check your internet connection and repository permissions"
fi

print_status "Attempting to merge github/mainline..."
if ! git merge github/mainline --no-edit; then
    print_warning "Merge conflicts detected. Please:"
    echo "1. Resolve the conflicts"
    echo "2. Complete the merge with 'git commit'"
    echo "3. Run this script again to finish syncing"
    exit 1
fi

print_status "Pushing changes to github..."
if ! git push github; then
    print_error "Failed to push to github remote. Possible causes:"
    echo "- You don't have push permissions"
    echo "- The remote branch is protected"
    echo "- There are new changes on the remote that you need to pull first"
    exit 1
fi

# If we got here, everything worked
print_status "Successfully synced mainline branch between remotes!"