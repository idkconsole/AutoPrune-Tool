# Auto Prune Bot

A Discord bot that automatically prunes members based on role changes.

## Features

- Automatically prunes members based on their role changes.
- Configurable to enable or disable wall role logic.
- Uses intensity-logger for logging.

## Requirements

- Python 3.8+
- `discord.py==1.7.3`
- `intensity-logger==0.1.2`

## Installation

1. Clone the repository or download the script files.
2. Navigate to the project directory.
3. Install the required packages:

```sh
pip install -r requirements.txt
```

## Configuration
Edit the `main.py` file to set the following variables:

`token`: Your Discord bot token.
`target_server_id`: The ID of the target server.
`wall_role_id`: The ID of the wall role.
`is_wall_role_enabled`: Set to True to enable wall role logic, False to disable.
`prune_reason`: The reason for pruning members.
