# K-CRIS MCP Server

An **MCP (Model Context Protocol) server** that connects to the [Korea Disease Control and Prevention Agency (KDCA) Clinical Research DB](https://www.data.go.kr/data/3033869/openapi.do) OpenAPI on the Korean government data portal.  
For more information on the Clinical Research Information Service (CRIS), see the [CRIS introduction](https://cris.nih.go.kr/cris/info/introduce.do).

## Features

| Tool | Description |
|------|-------------|
| `kcris_list_studies` | **List** clinical studies by search term and pagination (CRIS ID, title, study type, etc.) |
| `kcris_get_study` | **Detail** view of a study by CRIS registration number (e.g. KCT0002243): study info, participating sites, funding, sponsor, arms, primary outcomes, etc. |

## Requirements

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

## Installation

### 1. Clone and enter the project

```bash
git clone https://github.com/your-username/kcris-mcp-server.git
cd kcris-mcp-server
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

With `uv`:

```bash
uv pip install -r requirements.txt
```

To run the local package:

```bash
pip install -e .
# or with uv
uv pip install -e .
```

### 3. Environment variables

```bash
cp .env.example .env
```

Edit `.env` and set:

- `DATA_GO_KR_SERVICE_KEY`: Your API key from the [Korean government data portal](https://www.data.go.kr/) (apply for [KDCA Clinical Research DB](https://www.data.go.kr/data/3033869/openapi.do), then get the key from “My Page”).

## Usage

### Run the server locally

After installing dependencies:

```bash
uv run kcris-mcp-server
```

Or, if the package is installed:

```bash
python -m kcris_mcp_server
```

### Claude Desktop integration

Add the following to your Claude Desktop config:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

In Claude Desktop: **Settings → Developer → Edit Config**.

#### Option 1: Python directly

```json
{
  "mcpServers": {
    "kcris": {
      "command": "python",
      "args": ["-m", "kcris_mcp_server"],
      "cwd": "/path/to/kcris-mcp-server",
      "env": {
        "DATA_GO_KR_SERVICE_KEY": "your-service-key-here"
      }
    }
  }
}
```

> Run `pip install -r requirements.txt` and `pip install -e .` first.

#### Option 2: uv (recommended)

```json
{
  "mcpServers": {
    "kcris": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/kcris-mcp-server",
        "run",
        "kcris-mcp-server"
      ],
      "env": {
        "DATA_GO_KR_SERVICE_KEY": "your-service-key-here"
      }
    }
  }
}
```

> **Note**: In Claude Desktop (GUI), `uv` may not be on PATH. Use the **full path** to `uv` in `command` (e.g. `/Users/username/.local/bin/uv`). Run `which uv` in a terminal to get the path.

#### Option 3: uvx (local project)

```json
{
  "mcpServers": {
    "kcris": {
      "command": "/path/to/uvx",
      "args": ["--from", "/path/to/kcris-mcp-server", "kcris-mcp-server"],
      "env": {
        "DATA_GO_KR_SERVICE_KEY": "your-service-key-here"
      }
    }
  }
}
```

- Restart Claude Desktop completely after changing the config.

### Example prompts for Claude

| Goal | Example prompt |
|------|----------------|
| Search by condition/keyword | "Search for diabetes clinical studies", "Show 10 recruiting heart disease trials" |
| Study detail | "Get details for KCT0002243", "CRIS ID KCT0001234: sites and sponsor" |
| Pagination | "Search diabetes and show page 2" |

Example flow:

- **User**: Search for 10 diabetes clinical studies.
- **Response**: Calls `kcris_list_studies(srch_word="당뇨", num_of_rows=10, page_no=1)` and summarizes the results.

- **User**: Tell me about study KCT0002243.
- **Response**: Calls `kcris_get_study(cris_number="KCT0002243")` and summarizes title, recruitment status, sites, arms, etc.

---

## API reference

- **Base URL**: `http://apis.data.go.kr/1352159/crisinfodataview`
- **List**: `GET .../list` — `serviceKey`, `resultType=json`, `srchWord`, `numOfRows` (1–50), `pageNo`
- **Detail**: `GET .../detail` — `serviceKey`, `resultType=json`, `crisNumber` (CRIS registration number)

## License

This project is licensed under the MIT License.
