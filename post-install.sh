#!/bin/bash
echo "running post-install script"

# Web Explorer tool setup
# Copy files from .strategic-claude-basic/tools/web_explorer to project root

TOOL_DIR=".strategic-claude-basic/tools/web_explorer"

echo "Setting up web_explorer tool..."

# Copy scripts directory
cp -r "${TOOL_DIR}/root_scripts" scripts
chmod +x scripts/*.sh
echo "  - Copied scripts/"

# Copy configuration files
cp "${TOOL_DIR}/root_dot_gitignore" .gitignore
echo "  - Copied .gitignore"

cp "${TOOL_DIR}/root_dot_mcp_dot_json" .mcp.json
echo "  - Copied .mcp.json"

cp "${TOOL_DIR}/root_example_dot_env" example.env
echo "  - Copied example.env"

cp "${TOOL_DIR}/root_justfile" justfile
echo "  - Copied justfile"

echo "web_explorer tool setup complete!"
