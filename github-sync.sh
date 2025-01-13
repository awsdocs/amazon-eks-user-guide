#!/bin/bash

set -e  # Exit on any error

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

# Check if both remotes exist
if ! git remote | grep -q "^origin$"; then
    print_error "Remote 'origin' not found"
fi

if ! git remote | grep -q "^github$"; then
    print_error "Remote 'github' not found"
fi

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
    print_warning "You have uncommitted changes. Please commit or stash them before syncing."
    exit 1
fi

# Store current branch
current_branch=$(git symbolic-ref --short HEAD)

print_status "Fetching from github remote..."
if ! git fetch github; then
    print_error "Failed to fetch from github remote"
fi

print_status "Attempting to merge github/mainline..."
if ! git merge github/mainline --no-edit; then
    print_error "Merge failed. Please resolve conflicts and try again"
fi

print_status "Pushing changes to github..."
if ! git push github; then
    print_error "Failed to push to github remote"
fi

# If we got here, everything worked
print_status "Successfully synced mainline branch between remotes!"

# Optional: Return to original branch if we weren't on mainline
if [ "$current_branch" != "mainline" ]; then
    print_status "Returning to branch '$current_branch'..."
    git checkout "$current_branch"
fi

