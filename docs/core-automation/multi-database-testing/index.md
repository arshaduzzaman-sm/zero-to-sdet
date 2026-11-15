---
title: "Multi-database testing"
description: "Multi-database testing: a free, step-by-step guide for SDETs, with ready-to-use templates. Coming soon."
level: Intermediate
status: draft
tags:
  - core-automation
---

# Multi-database testing

!!! info "Coming soon"
    This topic is being written. Here is what it will teach you.

## What you will learn

- Why test several databases
- Docker Compose for MySQL, PostgreSQL, SQLite, MongoDB
- Config per database
- One base client, many drivers
- One test on every database with `pytest.mark.parametrize`
- Cross-database comparison (row counts, checksums, values)
- Migration and ETL validation

## Templates you will get

- Full project: `docker-compose.yml`, `config/databases.yaml`, `config/.env.example`, `db_clients/` (`base_client.py` + one per database), `queries/<database>/`, `test_data/`, `tests/` (`conftest.py`, `test_schema.py`, `test_data_integrity.py`, `test_cross_db_compare.py`)
