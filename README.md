
# Pak-SmartFlow — Mathematical & Fuzzy Decision Engine

## Project Overview

Pak-SmartFlow is an AI-powered multi-agent traffic intelligence
prototype designed to support traffic safety, compliance analysis,
and decision-making.

This module focuses on the Mathematical/Fuzzy Decision Engine.

The engine combines:

- Traffic risk assessment
- Compliance scoring
- Fuzzy membership functions
- Fuzzy decision scoring
- Final decision scoring
- Human-review-based action recommendations

## Mathematical Risk Model

The prototype calculates Risk Score using:

R = 0.15C + 0.20S + 0.25A + 0.10T + 0.10H + 0.20P

Where:

C = Detection Confidence
S = Violation Severity
A = Safety Risk
T = Traffic Density
H = Vehicle History
P = Predicted Risk

All input values are normalized between 0 and 1.

## Compliance Model

Compliance Score is represented by:

CS = 0.40(PC) + 0.30(1 - VF) + 0.30(DR)

Where:

PC = Payment Compliance
VF = Violation Frequency
DR = Dispute/Resolution Status

## Fuzzy Decision Layer

The engine calculates Low, Medium, and High Risk membership values.

The prototype fuzzy decision score is:

FDS = 0.20L + 0.60M + 1.00H

Where:

L = Low Risk Membership
M = Medium Risk Membership
H = High Risk Membership

## Final Decision Score

The final score combines fuzzy decision output and compliance:

Final Score = 0.70(FDS) + 0.30(1 - CS)

## Prototype Actions

The prototype uses the following illustrative thresholds:

- Score < 0.30 → Information / Warning
- 0.30–0.59 → Notification / Human Review
- Score ≥ 0.60 → Simulated Enforcement Request / Human Review

These thresholds are for prototype demonstration only and are
not official traffic enforcement rules.

## Files

- `pak_smartflow_engine.py` — reusable mathematical/fuzzy engine
- `app.py` — Streamlit demonstration interface
- `pak_smartflow_decision_output.csv` — synthetic test output

## Technology

- Python
- Pandas
- Streamlit
- Rule-based fuzzy membership functions

## Data Policy

The current demonstration uses synthetic/mock data.

No real vehicle database, NADRA system, payment system, banking
system, or personal identity database is connected.

## Human Review and Safety

The system is designed as a decision-support prototype.

A high score must not automatically result in punishment or
enforcement. Any real-world enforcement action should require
review and authorization by the relevant authority.

## Current Role in Pak-SmartFlow

This module provides the mathematical intelligence layer that can
receive inputs from other agents and return risk, fuzzy decision,
compliance, and recommended-action outputs.

## Developer

Zahida Majeed
MPhil Mathematics

Research Area:
Fuzzy Mathematics, Fuzzy Decision-Making, and Aggregation Operators
