"""Nexus Procurement Hub MCP Server (Reference Solution)

A FastMCP server that exposes three procurement tools against
the procurement.db SQLite database. Read-only access only.

To run:
    pip install fastmcp
    python mcp-server/procurement_server.py

To register in .claude/settings.json, see settings_json_solution.md.
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Optional

from fastmcp import FastMCP

# Database path: relative to where this server file lives.
DB_PATH = Path(__file__).resolve().parent.parent / "data" / "procurement.db"

mcp = FastMCP("Nexus Procurement Hub")


def _query(sql: str, params: tuple = ()) -> list[dict]:
    """Run a read-only SQL query and return rows as dicts."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(sql, params)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def _validate_read_only(sql: str) -> None:
    """Reject any SQL that is not a SELECT statement."""
    stripped = sql.strip().upper()
    if not stripped.startswith("SELECT"):
        raise ValueError("Only SELECT queries are allowed. This server is read-only.")
    forbidden = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE", "TRUNCATE"]
    for word in forbidden:
        if word in stripped.split():
            raise ValueError(
                f"Forbidden keyword '{word}' detected. This server is read-only."
            )


@mcp.tool()
def get_supplier_spend(
    supplier_id: Optional[str] = None,
    category: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> str:
    """Query spend transactions from the procurement database.

    Args:
        supplier_id: Filter by supplier ID (e.g., "SUP001"). Optional.
        category: Filter by category (e.g., "raw-materials"). Optional.
        start_date: Filter transactions on or after this date (YYYY-MM-DD). Optional.
        end_date: Filter transactions on or before this date (YYYY-MM-DD). Optional.

    Returns:
        JSON string with matching spend transactions and a summary total.
    """
    conditions = []
    params = []

    if supplier_id:
        conditions.append("supplier_id = ?")
        params.append(supplier_id)
    if category:
        conditions.append("category = ?")
        params.append(category)
    if start_date:
        conditions.append("date >= ?")
        params.append(start_date)
    if end_date:
        conditions.append("date <= ?")
        params.append(end_date)

    where = " AND ".join(conditions) if conditions else "1=1"
    sql = f"SELECT * FROM spend WHERE {where} ORDER BY date DESC"
    _validate_read_only(sql)

    rows = _query(sql, tuple(params))

    total = sum(r["amount_usd"] for r in rows)
    return json.dumps(
        {
            "transaction_count": len(rows),
            "total_spend_usd": round(total, 2),
            "transactions": rows[:50],
            "note": f"Showing first 50 of {len(rows)} transactions."
            if len(rows) > 50
            else f"Showing all {len(rows)} transactions.",
        },
        indent=2,
    )


@mcp.tool()
def get_open_pos(
    supplier_id: Optional[str] = None,
    status: Optional[str] = None,
    category: Optional[str] = None,
) -> str:
    """Query open purchase orders from the procurement database.

    Args:
        supplier_id: Filter by supplier ID (e.g., "SUP001"). Optional.
        status: Filter by PO status: "open", "partially_received", or "overdue". Optional.
        category: Filter by category (e.g., "logistics"). Optional.

    Returns:
        JSON string with matching open POs and a total exposure amount.
    """
    conditions = []
    params = []

    if supplier_id:
        conditions.append("supplier_id = ?")
        params.append(supplier_id)
    if status:
        conditions.append("status = ?")
        params.append(status)
    if category:
        conditions.append("category = ?")
        params.append(category)

    where = " AND ".join(conditions) if conditions else "1=1"
    sql = f"SELECT * FROM open_pos WHERE {where} ORDER BY delivery_date ASC"
    _validate_read_only(sql)

    rows = _query(sql, tuple(params))

    total_exposure = sum(r["amount_usd"] for r in rows)
    return json.dumps(
        {
            "po_count": len(rows),
            "total_exposure_usd": round(total_exposure, 2),
            "purchase_orders": rows,
        },
        indent=2,
    )


@mcp.tool()
def get_contract_status(
    supplier_id: Optional[str] = None,
    status: Optional[str] = None,
) -> str:
    """Query contract status from the procurement database.

    Args:
        supplier_id: Filter by supplier ID (e.g., "SUP001"). Optional.
        status: Filter by contract status: "active", "expiring_soon", or "expired". Optional.

    Returns:
        JSON string with matching contracts and key dates.
    """
    conditions = []
    params = []

    if supplier_id:
        conditions.append("supplier_id = ?")
        params.append(supplier_id)
    if status:
        conditions.append("status = ?")
        params.append(status)

    where = " AND ".join(conditions) if conditions else "1=1"
    sql = f"SELECT * FROM contracts WHERE {where} ORDER BY end_date ASC"
    _validate_read_only(sql)

    rows = _query(sql, tuple(params))

    return json.dumps(
        {
            "contract_count": len(rows),
            "contracts": rows,
        },
        indent=2,
    )


if __name__ == "__main__":
    mcp.run()
