# Open C-RAN Monitor

A containerized monitoring stack for experimental Cloud-RAN (C-RAN) testbed environments.

## Overview

This project provides real-time monitoring infrastructure for C-RAN deployments using industry-standard tools:

- **Prometheus** — Time-series metrics collection
- **Grafana** — Visualization and dashboards  
- **Custom Exporter** — C-RAN specific metrics

## Motivation

Inspired by research on experimental C-RAN platforms, this monitoring stack addresses the need for observability in wireless testbed environments. Managing multi-site data centers at Walton Group taught me the importance of comprehensive monitoring — this project applies those principles to C-RAN infrastructure.

**Reference:**
> Gashteroodkhani et al., "Architecture and Benchmark of an Experimental CRAN Platform over CPRI," IEEE INFOCOM 2024

## Architecture
## Architecture

## Architecture

```mermaid
flowchart TD
  subgraph CRAN["C-RAN Testbed (Conceptual)"]
    RU1["RU1"] --- FH["Fronthaul (CPRI)"]
    RU2["RU2"] --- FH
    RU3["RU3"] --- FH
    FH --> DU1["DU1"]
    FH --> DU2["DU2"]
    DU1 --> CU["CU"]
    DU2 --> CU
  end

  CU --> EXP["CRAN Exporter :8000/metrics"]
  EXP --> PRO["Prometheus :9090"]
  PRO --> GRA["Grafana :3000"]
