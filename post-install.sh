#!/bin/bash
echo "running post-install script"

# Install web search MCP tool
echo "Installing web search MCP tool..."
cd .strategic-claude-basic/tools/
python3 install_web_search_mcp.py