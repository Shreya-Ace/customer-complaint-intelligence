# 🧠 Customer Complaint Intelligence

An NLP and LLM-powered system that transforms unstructured customer complaints into structured, actionable intelligence for customer support teams.

The system combines traditional NLP techniques with a Large Language Model to identify the nature of a complaint, assess its severity, extract relevant information, and generate resolution support.

---

## 👥 Authors
- **Shreya Singh**

---

## 📌 Overview

Customer complaints are often written as unstructured text, making it difficult for support teams to quickly understand the customer's issue and determine the appropriate response.

Customer Complaint Intelligence addresses this problem by automatically analyzing complaints and producing:

- Complaint category
- Customer intent
- Sentiment
- Urgency
- Extracted entities
- Complaint summary
- Recommended support actions
- Suggested customer response

The project is designed as a modular NLP + LLM pipeline that can be extended into a larger customer-support intelligence platform.

---

## ✨ Features

### Complaint Analysis

The system identifies:

- Category
- Intent
- Sentiment
- Urgency

### NLP Processing

Traditional NLP components are used for:

- Sentiment analysis
- Named Entity Recognition
- Information extraction

### LLM-powered Intelligence

A Groq-hosted Large Language Model is used for:

- Complaint classification
- Intent interpretation
- Urgency assessment
- Contextual reasoning
- Resolution support generation

### Resolution Support

The system generates:

- Complaint summary
- Recommended actions
- Suggested customer response

### Web Interface

A Streamlit dashboard provides an interactive interface for demonstrating the system.

### REST API

A FastAPI backend exposes the complaint analysis functionality through REST endpoints.

---

# 🏗️ System Architecture

```text
                         Customer Complaint
                                │
                                ▼
                    ┌─────────────────────┐
                    │     FastAPI API     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    NLP Processing   │
                    │                     │
                    │ • Sentiment         │
                    │ • Entity Extraction │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      Groq LLM       │
                    │                     │
                    │ • Category          │
                    │ • Intent            │
                    │ • Urgency           │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Resolution Support  │
                    │                     │
                    │ • Summary           │
                    │ • Actions           │
                    │ • Response          │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Streamlit UI      │
                    └─────────────────────┘
