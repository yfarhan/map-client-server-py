#### Simple MCP Client / Server POC

- To run this example from inside the `client` dir, run
```zsh
$ cd client
$ uv run main.py
```
- in the prompt try
```zsh
Query : what is the weather forcaast for tonight in Chicago, IL ?
```
sample response
```zsh
...
Connected to server with tools: ['get_alerts', 'get_forecast']

MCP Client Started!
Type your queries or 'quit' to exit.

Query: what is the weather forcaast for tonight in Chicago, IL ?
...
...
I can help you get the weather forecast for Chicago. I'll use the get_forecast function, but I'll need to use Chicago's coordinates. Chicago's approximate coordinates are:
Latitude: 41.8781
Longitude: -87.6298

Let me get that forecast for you:
[Calling tool get_forecast with args {'latitude': 41.8781, 'longitude': -87.6298}]
According to the forecast for Chicago tonight:

- Temperature will be around 48°F
- There will be occasional rain showers and drizzle
- It will be cloudy
- Northwest winds around 15 mph with gusts up to 25 mph
- 70% chance of precipitation
- Less than 0.1 inch of rainfall expected

Query:
```

---

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
