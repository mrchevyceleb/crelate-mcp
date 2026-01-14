"""Crelate MCP Server - Model Context Protocol server for Crelate ATS/CRM API."""

import os
from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize MCP server
mcp = FastMCP("Crelate ATS/CRM")

# Crelate API configuration
CRELATE_API_BASE = "https://app.crelate.com/api3"
CRELATE_API_KEY = os.getenv("CRELATE_API_KEY")

if not CRELATE_API_KEY:
    raise ValueError("CRELATE_API_KEY environment variable is required")


async def make_crelate_request(
    endpoint: str,
    method: str = "GET",
    params: dict[str, Any] | None = None,
    json_data: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Make authenticated request to Crelate API."""
    url = f"{CRELATE_API_BASE}/{endpoint}"

    # Add API key to query params
    if params is None:
        params = {}
    params["api_key"] = CRELATE_API_KEY

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.request(
            method=method,
            url=url,
            params=params,
            json=json_data
        )
        response.raise_for_status()
        return response.json()


# ============================================================================
# CONTACT TOOLS
# ============================================================================

@mcp.tool()
async def list_contacts(
    limit: int = 50,
    offset: int = 0,
    search: str | None = None
) -> str:
    """List contacts from Crelate.

    Args:
        limit: Maximum number of contacts to return (default: 50)
        offset: Number of contacts to skip for pagination (default: 0)
        search: Optional search query to filter contacts

    Returns:
        JSON string containing list of contacts with id, name, email, phone
    """
    params = {"limit": limit, "offset": offset}
    if search:
        params["search"] = search

    result = await make_crelate_request("contacts", params=params)
    return str(result)


@mcp.tool()
async def get_contact(contact_id: str) -> str:
    """Get detailed information about a specific contact.

    Args:
        contact_id: The unique ID of the contact

    Returns:
        JSON string containing full contact details
    """
    result = await make_crelate_request(f"contacts/{contact_id}")
    return str(result)


@mcp.tool()
async def create_contact(
    first_name: str,
    last_name: str,
    email: str | None = None,
    phone: str | None = None,
    company_name: str | None = None,
    title: str | None = None
) -> str:
    """Create a new contact in Crelate.

    Args:
        first_name: Contact's first name (required)
        last_name: Contact's last name (required)
        email: Contact's email address
        phone: Contact's phone number
        company_name: Associated company name
        title: Contact's job title

    Returns:
        JSON string containing the created contact details including ID
    """
    contact_data = {
        "firstName": first_name,
        "lastName": last_name
    }

    if email:
        contact_data["email"] = email
    if phone:
        contact_data["phone"] = phone
    if company_name:
        contact_data["companyName"] = company_name
    if title:
        contact_data["title"] = title

    result = await make_crelate_request("contacts", method="POST", json_data=contact_data)
    return str(result)


@mcp.tool()
async def update_contact(
    contact_id: str,
    first_name: str | None = None,
    last_name: str | None = None,
    email: str | None = None,
    phone: str | None = None,
    title: str | None = None
) -> str:
    """Update an existing contact in Crelate.

    Args:
        contact_id: The unique ID of the contact to update
        first_name: Contact's first name
        last_name: Contact's last name
        email: Contact's email address
        phone: Contact's phone number
        title: Contact's job title

    Returns:
        JSON string containing the updated contact details
    """
    update_data = {}

    if first_name:
        update_data["firstName"] = first_name
    if last_name:
        update_data["lastName"] = last_name
    if email:
        update_data["email"] = email
    if phone:
        update_data["phone"] = phone
    if title:
        update_data["title"] = title

    result = await make_crelate_request(
        f"contacts/{contact_id}",
        method="PUT",
        json_data=update_data
    )
    return str(result)


# ============================================================================
# CANDIDATE TOOLS
# ============================================================================

@mcp.tool()
async def list_candidates(
    limit: int = 50,
    offset: int = 0,
    search: str | None = None
) -> str:
    """List candidates from Crelate.

    Args:
        limit: Maximum number of candidates to return (default: 50)
        offset: Number of candidates to skip for pagination (default: 0)
        search: Optional search query to filter candidates

    Returns:
        JSON string containing list of candidates
    """
    params = {"limit": limit, "offset": offset}
    if search:
        params["search"] = search

    result = await make_crelate_request("candidates", params=params)
    return str(result)


@mcp.tool()
async def get_candidate(candidate_id: str) -> str:
    """Get detailed information about a specific candidate.

    Args:
        candidate_id: The unique ID of the candidate

    Returns:
        JSON string containing full candidate details including skills, experience, etc.
    """
    result = await make_crelate_request(f"candidates/{candidate_id}")
    return str(result)


@mcp.tool()
async def create_candidate(
    first_name: str,
    last_name: str,
    email: str | None = None,
    phone: str | None = None,
    current_title: str | None = None,
    current_company: str | None = None
) -> str:
    """Create a new candidate in Crelate.

    Args:
        first_name: Candidate's first name (required)
        last_name: Candidate's last name (required)
        email: Candidate's email address
        phone: Candidate's phone number
        current_title: Candidate's current job title
        current_company: Candidate's current company

    Returns:
        JSON string containing the created candidate details including ID
    """
    candidate_data = {
        "firstName": first_name,
        "lastName": last_name
    }

    if email:
        candidate_data["email"] = email
    if phone:
        candidate_data["phone"] = phone
    if current_title:
        candidate_data["currentTitle"] = current_title
    if current_company:
        candidate_data["currentCompany"] = current_company

    result = await make_crelate_request("candidates", method="POST", json_data=candidate_data)
    return str(result)


# ============================================================================
# JOB TOOLS
# ============================================================================

@mcp.tool()
async def list_jobs(
    limit: int = 50,
    offset: int = 0,
    status: str | None = None
) -> str:
    """List jobs/positions from Crelate.

    Args:
        limit: Maximum number of jobs to return (default: 50)
        offset: Number of jobs to skip for pagination (default: 0)
        status: Optional filter by job status (e.g., 'open', 'closed')

    Returns:
        JSON string containing list of jobs with id, name, status, location
    """
    params = {"limit": limit, "offset": offset}
    if status:
        params["status"] = status

    result = await make_crelate_request("jobs", params=params)
    return str(result)


@mcp.tool()
async def get_job(job_id: str) -> str:
    """Get detailed information about a specific job/position.

    Args:
        job_id: The unique ID of the job

    Returns:
        JSON string containing full job details including description, requirements
    """
    result = await make_crelate_request(f"jobs/{job_id}")
    return str(result)


@mcp.tool()
async def create_job(
    name: str,
    company_name: str | None = None,
    location: str | None = None,
    description: str | None = None
) -> str:
    """Create a new job/position in Crelate.

    Args:
        name: Job title/name (required)
        company_name: Hiring company name
        location: Job location
        description: Job description

    Returns:
        JSON string containing the created job details including ID
    """
    job_data = {"name": name}

    if company_name:
        job_data["companyName"] = company_name
    if location:
        job_data["location"] = location
    if description:
        job_data["description"] = description

    result = await make_crelate_request("jobs", method="POST", json_data=job_data)
    return str(result)


# ============================================================================
# COMPANY TOOLS
# ============================================================================

@mcp.tool()
async def list_companies(
    limit: int = 50,
    offset: int = 0,
    search: str | None = None
) -> str:
    """List companies from Crelate.

    Args:
        limit: Maximum number of companies to return (default: 50)
        offset: Number of companies to skip for pagination (default: 0)
        search: Optional search query to filter companies

    Returns:
        JSON string containing list of companies
    """
    params = {"limit": limit, "offset": offset}
    if search:
        params["search"] = search

    result = await make_crelate_request("companies", params=params)
    return str(result)


@mcp.tool()
async def get_company(company_id: str) -> str:
    """Get detailed information about a specific company.

    Args:
        company_id: The unique ID of the company

    Returns:
        JSON string containing full company details
    """
    result = await make_crelate_request(f"companies/{company_id}")
    return str(result)


@mcp.tool()
async def create_company(
    name: str,
    website: str | None = None,
    industry: str | None = None,
    location: str | None = None
) -> str:
    """Create a new company in Crelate.

    Args:
        name: Company name (required)
        website: Company website URL
        industry: Company industry
        location: Company location

    Returns:
        JSON string containing the created company details including ID
    """
    company_data = {"name": name}

    if website:
        company_data["website"] = website
    if industry:
        company_data["industry"] = industry
    if location:
        company_data["location"] = location

    result = await make_crelate_request("companies", method="POST", json_data=company_data)
    return str(result)


# ============================================================================
# NOTE TOOLS
# ============================================================================

@mcp.tool()
async def create_note(
    body: str,
    contact_id: str | None = None,
    candidate_id: str | None = None,
    company_id: str | None = None,
    job_id: str | None = None
) -> str:
    """Create a note in Crelate and optionally attach it to a record.

    Args:
        body: Note content (required)
        contact_id: Optional contact ID to attach note to
        candidate_id: Optional candidate ID to attach note to
        company_id: Optional company ID to attach note to
        job_id: Optional job ID to attach note to

    Returns:
        JSON string containing the created note details
    """
    note_data = {"body": body}

    if contact_id:
        note_data["contactId"] = contact_id
    if candidate_id:
        note_data["candidateId"] = candidate_id
    if company_id:
        note_data["companyId"] = company_id
    if job_id:
        note_data["jobId"] = job_id

    result = await make_crelate_request("notes", method="POST", json_data=note_data)
    return str(result)


# ============================================================================
# TASK TOOLS
# ============================================================================

@mcp.tool()
async def create_task(
    body: str,
    due_date: str | None = None,
    contact_id: str | None = None,
    candidate_id: str | None = None,
    company_id: str | None = None,
    job_id: str | None = None
) -> str:
    """Create a task in Crelate and optionally attach it to a record.

    Args:
        body: Task description (required)
        due_date: Optional due date in ISO 8601 format (e.g., '2026-01-20T15:00:00Z')
        contact_id: Optional contact ID to attach task to
        candidate_id: Optional candidate ID to attach task to
        company_id: Optional company ID to attach task to
        job_id: Optional job ID to attach task to

    Returns:
        JSON string containing the created task details
    """
    task_data = {"body": body}

    if due_date:
        task_data["dueDate"] = due_date
    if contact_id:
        task_data["contactId"] = contact_id
    if candidate_id:
        task_data["candidateId"] = candidate_id
    if company_id:
        task_data["companyId"] = company_id
    if job_id:
        task_data["jobId"] = job_id

    result = await make_crelate_request("tasks", method="POST", json_data=task_data)
    return str(result)


if __name__ == "__main__":
    # Run with stdio transport for Claude Desktop integration
    mcp.run(transport="stdio")
