# Crelate MCP Server

Model Context Protocol (MCP) server for the Crelate ATS/CRM API. Enables Claude Code and other MCP clients to interact with Crelate recruiting and staffing workflows.

**GitHub:** https://github.com/mrchevyceleb/crelate-mcp

## Quick Start

```bash
# Clone the repository
git clone https://github.com/mrchevyceleb/crelate-mcp.git
cd crelate-mcp

# Install dependencies
uv venv
uv pip install mcp httpx python-dotenv

# Configure your API key
cp .env.example .env
# Edit .env and add your CRELATE_API_KEY

# Add to Claude Code (see Configuration section below)
```

## Features

### Core CRUD Operations
- **Contacts**: List, get, create, update contacts
- **Candidates**: List, get, create candidates
- **Jobs**: List, get, create job positions
- **Companies**: List, get, create companies
- **Notes**: Create notes and attach to records
- **Tasks**: Create tasks and attach to records

### Comprehensive Reporting & Analytics (33 tools)
- **Activity Reports**: Track interactions, touchpoints, and engagement history
- **Pipeline Reports**: Analyze candidate flow through job pipelines
- **Placement Reports**: Track successful hires and metrics
- **Source Tracking**: Identify where candidates and contacts originated
- **User Activity**: Monitor team productivity and activity
- **Financial Reports**: Track invoicing and payment data
- **Aggregate Metrics**: High-level counts and organization stats
- **Workflow Analysis**: Analyze categorization and pipeline stages

## Prerequisites

- Python 3.10+
- uv (Python package manager)
- Crelate API key

## Getting Your Crelate API Key

1. Log into your Crelate account at https://app.crelate.com
2. Navigate to **Settings → My Settings & Preferences**
3. Find your API key in the API section
4. Copy the key for configuration

**Note:** Your organization administrator controls API access via **Settings → Advanced Settings → User Roles**.

## Installation

### 1. Clone or navigate to the project

```bash
cd ~/mcp-projects/crelate-mcp
```

### 2. Create environment file

```bash
cp .env.example .env
```

Edit `.env` and add your Crelate API key:

```
CRELATE_API_KEY=your_actual_api_key_here
```

### 3. Install dependencies

```bash
uv pip install -e .
```

## Configuration

### Add to Claude Code

Edit your MCP configuration file at `C:\Users\mtjoh\.claude.json`:

```json
{
  "projects": {
    "C:\\Users\\mtjoh": {
      "mcpServers": {
        "crelate": {
          "command": "uv",
          "args": ["run", "C:\\Users\\mtjoh\\mcp-projects\\crelate-mcp\\server.py"],
          "env": {
            "CRELATE_API_KEY": "your_api_key_here"
          }
        }
      }
    }
  }
}
```

**Restart Claude Code** after adding the configuration.

## Available Tools

### Contacts

- `list_contacts(limit, offset, search)` - List contacts with pagination and search
- `get_contact(contact_id)` - Get detailed contact information
- `create_contact(first_name, last_name, email, phone, company_name, title)` - Create new contact
- `update_contact(contact_id, ...)` - Update existing contact

### Candidates

- `list_candidates(limit, offset, search)` - List candidates with pagination and search
- `get_candidate(candidate_id)` - Get detailed candidate information
- `create_candidate(first_name, last_name, email, phone, current_title, current_company)` - Create new candidate

### Jobs

- `list_jobs(limit, offset, status)` - List jobs with optional status filter
- `get_job(job_id)` - Get detailed job information
- `create_job(name, company_name, location, description)` - Create new job posting

### Companies

- `list_companies(limit, offset, search)` - List companies with pagination and search
- `get_company(company_id)` - Get detailed company information
- `create_company(name, website, industry, location)` - Create new company

### Notes & Tasks

- `create_note(body, contact_id, candidate_id, company_id, job_id)` - Create note and attach to record
- `create_task(body, due_date, contact_id, candidate_id, company_id, job_id)` - Create task and attach to record

### Reporting & Analytics Tools

#### Activity Reports
Track interactions, touchpoints, and engagement history:

- `get_activities(limit, offset, activity_type)` - List all activities with optional type filter
- `get_activity_count(activity_type)` - Get total count of activities by type
- `get_contact_history(contact_id, limit, offset)` - Get complete activity history for a contact
- `get_job_history(job_id, limit, offset)` - Get complete activity history for a job

#### Pipeline & Application Reports
Analyze candidate flow through job pipelines:

- `get_applications(job_id, limit, offset)` - List all applications for a specific job
- `get_application_count(job_id, status)` - Count applications by job and optional status
- `get_job_contacts(job_id, limit, offset)` - List all contacts associated with a job
- `get_job_contact_history(job_id, contact_id, limit, offset)` - Get interaction history between job and contact

#### Placement Reports
Track successful hires and placement metrics:

- `get_placements(limit, offset, start_date, end_date)` - List placements with date range filtering
- `get_placement_info(placement_id)` - Get detailed information about a specific placement

#### Source Tracking
Identify where candidates and contacts originated:

- `get_contact_sources(limit, offset)` - List all contact sources with usage stats
- `get_company_sources(limit, offset)` - List all company sources with usage stats

#### User Activity & Productivity
Monitor team member activity and productivity:

- `get_users(limit, offset)` - List all users in the organization
- `get_user_count()` - Get total count of active users
- `get_user_info(user_id)` - Get detailed information about a specific user
- `get_current_user()` - Get information about the authenticated user

#### Financial Reports
Track invoicing and payment data:

- `get_invoices(limit, offset, status)` - List invoices with optional status filter
- `get_invoice_count(status)` - Count invoices by status
- `get_invoice_info(invoice_id)` - Get detailed information about a specific invoice
- `get_payments(invoice_id, limit, offset)` - List payments for a specific invoice

#### Aggregate Metrics & Organization
High-level counts and organization information:

- `get_contact_count(search)` - Get total count of contacts with optional search filter
- `get_job_count(status)` - Get total count of jobs with optional status filter
- `get_company_count(search)` - Get total count of companies with optional search filter
- `get_organization_info()` - Get information about the Crelate organization/account

#### Tags & Workflow Analysis
Analyze categorization and pipeline stages:

- `get_tags(limit, offset, entity_type)` - List tags with optional entity type filter
- `get_tag_categories(limit, offset)` - List all tag categories
- `get_workflow_statuses(entity_type, limit, offset)` - List workflow statuses by entity type

## Usage Examples

### In Claude Code

Once configured, you can interact with Crelate using natural language:

```
"List the most recent 10 candidates"
"Get details for contact ID 12345"
"Create a new candidate named John Smith with email john@example.com"
"Add a note to candidate 67890 saying 'Great interview, moving to next round'"
"Create a task for job 54321 due tomorrow at 3pm"
```

### Direct Python Usage

```python
from server import list_contacts, get_contact, create_candidate

# List contacts
contacts = await list_contacts(limit=10, search="Smith")

# Get specific contact
contact = await get_contact("12345")

# Create candidate
new_candidate = await create_candidate(
    first_name="Jane",
    last_name="Doe",
    email="jane@example.com",
    current_title="Software Engineer"
)
```

## API Reference

This MCP server wraps the Crelate API v3.

**Official Documentation:**
- Swagger UI: https://app.crelate.com/api/pub/v1/docs/g/index
- API Docs: https://app.crelate.com/api3/docs
- Developer Guide: https://help.crelate.com/en/articles/4120536-crelate-api-developer-guide

**Base URL:** `https://app.crelate.com/api3`

**Authentication:** API key passed as query parameter

## Important Notes

### Date Format
All dates must be in **ISO 8601 format in UTC timezone**:
```
2026-01-20T15:00:00Z
```

### Required Fields
- **Company**: `name`
- **Job**: `name`
- **Note**: `body`
- **Task**: `body`
- **Contact**: `firstName`, `lastName`
- **Candidate**: `firstName`, `lastName`

### Lookups
When creating records with relationships (e.g., contact with company), Crelate supports:
- Providing an existing record ID to link
- Providing name fields only to auto-create new records

## Troubleshooting

### API Key Issues

If you get authentication errors:
1. Verify your API key in Crelate settings
2. Check that the key is correctly set in `.env` or MCP config
3. Ensure your user role has API access enabled

### Connection Issues

```bash
# Test the server directly
cd ~/mcp-projects/crelate-mcp
uv run server.py
```

### MCP Not Showing in Claude Code

1. Verify configuration in `~/.claude.json`
2. Check that the server isn't in `disabledMcpServers` array
3. Restart Claude Code
4. Use `/mcp` command to check server status

## Development

### Project Structure

```
crelate-mcp/
├── server.py          # Main MCP server implementation
├── pyproject.toml     # Python dependencies
├── .env.example       # Environment template
└── README.md          # This file
```

### Adding New Tools

To add new Crelate API endpoints:

1. Add a new tool function with `@mcp.tool()` decorator
2. Use `make_crelate_request()` helper for API calls
3. Follow existing patterns for parameter handling
4. Update this README with the new tool

### Testing

```python
# Test individual tools
import asyncio
from server import list_contacts

async def test():
    result = await list_contacts(limit=5)
    print(result)

asyncio.run(test())
```

## Support

**Crelate API Support:** https://help.crelate.com/en/collections/2434134-api-documentation

**MCP Documentation:** https://modelcontextprotocol.io

## License

MIT License - See LICENSE file for details

## Project Info

**Version:** 0.1.0
**Author:** Matt Johnston
**Project:** YourProfitPartners / Work With Your Handz
**Created:** January 14, 2026
