#!/bin/zsh

# Session name
SESH="workspace"

# Check if the tmux session already exists
tmux has-session -t $SESH 2>/dev/null

# If the session does not exist, create it
if [ $? != 0 ]; then
    echo "No tmux session found. Creating a new session named '$SESH'."
    cd $(pwd)/$1
    # Create a new session with the first window named "editor"
    tmux new-session -d -s $SESH -n "editor" "nvim ."

    # Create the second window named "helper"
    tmux new-window -t $SESH -n "helper"

    # Split the "editor" window vertically (side-by-side panes)
    tmux split-window -h -t $SESH\:editor
fi

tmux attach-session -t $SESH

