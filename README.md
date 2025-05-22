#### Simple MCP Client / Server POC

1. Creating an MCP Client :

@see client/main.py
```py
# client/main.py
async def connect_to_server(self, cfg: map):
    ...
    ...
    server_params = StdioServerParameters(
        command=command,
        args=args,
        env=None
    )
    ...
    ...
    await self.mcp_client01.initialize()
```

> NOTE: to create multiple Clients we can simply loop over the config mcpservers in the config and add these instances to a hash map.

2. Processing the query :
@see client/main.py
```py
async def process_query(self, query: str) -> str:
    ...
    # getting the available tools
    response = await self.mcp_client01.list_tools()
    ...
    # Initial Claude API call
    response = self.anthropic.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        messages=messages,
        tools=available_tools
    )
```

3. Making the tool call
@see client/main.py

```py
async def process_query(self, query: str) -> str:
    ...
    # Execute tool call
    result = await self.mcp_client01.call_tool(tool_name, tool_args)
```

#### Example Config.json
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "<FULL_PATH_TO_DIR>/weather-mcp-server"
      ]
    },
    "weather": {
      "command": "node",
      "args": [
        "<FULL_PATH_TO_DIR>/weather-mcp-server/build/index.js"
      ]
    },
    "cwSSH": {
      "command": "python",
      "args": [
        "<FULL_PATH_TO_DIR>/cw-mcp-ssh-server/main.py"
      ],
      "env": {
        "SOME_API_KEY": "1234"
      }
    },
    "websearch": {
      "command": "node",
      "args": [
        "<FULL_PATH_TO_DIR>/claude-search-mcp/dist/index.js"
      ]
    }
  }
}
```
