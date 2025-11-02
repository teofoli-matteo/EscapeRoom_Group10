## I. Author
**Teofoli Matteo**  
Contributions: `Player`, `Game Engine`, `Logger`, `Lobby`, `SOC Room`, and `Final Gate Room`.\
**Nwaoyibo Chiamaka**  
Contributions: `Game`, `Vault Corridor`, and `Malware Room`, 
**Kong Phil**  
Contributions: `Game`, `Base Room`, `DNS Closet Room` and `Malware Room`.

## II. Implemented Components
### 1) `Player` – Token Inventory Manager
**File:** `engine/player.py`
Handles the player’s token inventory.
#### Features
- Adds collected tokens with `add_token(key, value)`
- Displays current tokens with `show_inventory()`
- Keeps track of all discovered evidence during the game

### 2) `Game` – Core Game Engine
**File:** `engine/game.py`
#### Features
- Command-line interpreter `(look, move, inspect, use, inventory, etc.)`
- Error handling.
- Save and load system using JSON files.
- Initialization of each room.
- Initialization of the player and logger.
- Interactive **command-line loop** `run()` -> the main game loop

### 3) `Logger` – Game Transcript Recorder
**File:** `engine/logger.py`
Handles all transcript and event logging for the game.
#### Features
- Prints logs to the console
- Stores all messages internally
- Saves transcripts to a file at the end of a session

### 4) `Lobby` – Entry Room
**File:** `rooms/lobby.py`
Serves as the central hub.
#### Description
- Provides the player with the available destinations.
- Represents the narrative introduction of the game.

### 5) `SOC Triage Room` – Log Analysis Challenge
**File:** `rooms/soc_triage.py`
#### Logic
- Parses the log file line-by-line.
- Extracts IP addresses from failed SSH login attempts.
- Groups them by `/24` subnet and counts occurrences.
- Finds the subnet and IP with the most failures.
- Generates a token based on: `token = last_octet_of_top_IP + total_failures`

### 6) `Vault Corridor Room` - Vault Dump Analysis 
**File:** `rooms/vault_corridor_room.py`
#### Logic
- Precompiled a regex pattern that captures SAFE{a-b-c}
- parsed the vault_dump.txt file to find all safe code candidates
- Validates safe codes with checksum verification

### 7) `DNS Closet Room` - Base64 Decode Challenge
**File:** `rooms/dns_closet_room.py`
#### Logic
- Parse a `key-value` file.
- Deal with stray newlines and missing padding.
- Decode value as Base64 and log the decoded hint text.

### 8) `Malware Lab Room` - Process Tree Forensics
**File:** `rooms/malware_room.py`
#### Logic
- Load the process tree from `proc_tree.jsonl`
- Build an adjacency children map `children[ppid] -> list[pid]`
- Run DFS first, then BFS, to find a path from the starting PID to any process running `curl` or `scp`.
- Log the path and terminal PID.

### III. Team Work
In order to work efficiently, we decided to create a **Discord** group. The purpose of this group is to discuss problems and solutions, but also to distribute tasks to each member and ensure follow-up for successful collaboration.
At the same time, we decided to use **GitHub** for the code so that it would be easy for each member to follow progress and also to be able to push each other's progress.\
Given that this project is being built by members with different levels of coding experience and backgrounds, we have decided to divide the project into several parts. Each instruction is accompanied by detailed implementation instructions so that group members don't get lost in their implementation. To ensure the project progresses smoothly, we try to maintain fluid communication via Discord about any advances (if there have been any). When implementations require more knowledge, we meet in class to collaborate effectively, provide clear explanations, and code together in order to make progress.
