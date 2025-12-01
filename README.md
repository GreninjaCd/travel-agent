# 🌍 Travel Agent – Project Overview

The **Travel Agent** is a multi-agent, AI-powered travel planning system that combines a **Node.js (Express) API gateway** with a **Python-based intelligent agent backend**.  
It generates personalized travel itineraries using specialized agents, custom tools, and LLM-driven reasoning — all packaged in a **cloud-ready microservice architecture**.

---

## ✨ Key Features

### 🔹 Multi-Agent Architecture
A coordinated set of specialized agents handle:
- Flight search  
- Hotel recommendations  
- Activity & sightseeing suggestions  
- Itinerary refinement  
- Long-term preference learning  

Each agent focuses on a single area, enabling modularity and efficient delegation.

---

### 🔹 Node.js → Python Orchestration
- **Node.js (Express):** Stateless HTTP API layer  
- **Python:** Executes intelligent reasoning  
- Lightweight, high-performance bridge connects both layers seamlessly  

---

### 🔹 LLM-Powered Travel Reasoning
Leverages modern LLMs (e.g., OpenAI models) for:
- Multi-day itinerary generation  
- Constraint handling (budget, dates, travel style)  
- Summarization & personalization  

---

### 🔹 Custom Tools & Data Sources
Modular tools offer expandable travel data integrations:
- Flight search tool  
- Hotel search tool  
- Web search tool  
- Activity recommendation tool  

Easily extendable to real external APIs like:
- Skyscanner  
- Amadeus  
- Booking.com  
- Google Places  

---

### 🔹 User Preference Memory
Stores long-term user preferences such as:
- Budget ranges  
- Preferred airlines & cabin types  
- Hotel star ratings  
- Activity interests  

This enables increasingly personalized future travel plans.

---

### 🔹 Session State Management
Every request generates a session with:
- Event logs  
- Agent messages  
- Tool call traces  
- Intermediate reasoning steps  

Supports debugging, analytics, and continuity across interactions.

---

### 🔹 Context Engineering
Uses dynamic context compaction to keep prompts:
- Efficient  
- Relevant  
- LLM-friendly  

Ensures smooth multi-agent cooperation without exceeding context limits.

---

### 🔹 Observability & Logging
The backend records:
- Agent actions  
- Tool usage  
- Errors & warnings  
- Timing metrics  

Provides transparency and enables future evaluation & optimization.

---

### 🔹 Cloud-Native & Production Ready
Architected for deployment as a containerized microservice:
- **Node.js** → Stateless API layer  
- **Python** → Stateful agent computation engine  

Supports:
- Google Cloud Run  
- Cloud Build  
- Docker  
- Secret Manager  

---

## 🏗️ High-Level Architecture

