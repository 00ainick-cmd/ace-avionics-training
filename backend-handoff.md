# CAET Prep Backend Handoff

*This document is formatted as a prompt to be given to an AI agent responsible for backend integration.*

## Context
The front-end design for the CAET Prep Dashboard has been overhauled. We now have three distinct modes:
1. **Journey**: A 100-node node map for microlessons.
2. **Classroom**: Traditional Rise modules, study materials, and an AI NotebookLM integration.
3. **Practice**: Drill, Flash Cards, and Battle ACE.

Your goal is to build out the Supabase backend infrastructure, update the JSON files to support the new unified Practice modes, and ensure XP is tracked globally across the platform.

## Task 1: Question Bank JSON Normalization
We currently have disparate JSON question formats (e.g., `jeopardy.html` uses specific schemas for Battle ACE, while earlier modules might use something else).
1. **Analyze** the original JSON files in `question-banks/`.
2. **Normalize** these into a single schema that can fuel:
   - **Battle ACE** (Jeopardy categories/values).
   - **Flash Cards** (Front/Back concept).
   - **Drills** (Multiple choice questions with specific right/wrong states).
3. Ensure the `practice.html` query parameter (`?category=cat-1`) successfully fetches the unified JSON array for that category to be dispersed into any of the 3 modes.

## Task 2: Supabase Initialization & Schema
We need a robust tracking schema. Set up a Supabase project and define clear SQL migrations for:
- `users`: Core authentication info.
- `user_progress`: Track global XP, Streak (in days), and Readiness average.
- `journey_nodes`: Track completion of the 100 microlessons (`journey.html`). Each node completion grants XP.
- `module_mastery`: Track percentage mastery across the 8 specific CAET categories (MRD, BET, CNS, etc.).

## Task 3: LocalStorage Fallback & Sync Wrapper
Create a `/shared/db-sync.js` utility wrapper.
- The dashboard currently uses functions like `getTotalXP()`, `getCatMastery()`, and `isModuleDone()` strictly through `localStorage`.
- Update these functions to asynchronously write to Supabase.
- Implement an offline-first capability: read from `localStorage` immediately for fast UI rendering, while asynchronously syncing changes to Supabase in the background. If Supabase cannot be reached, fallback gracefully to LocalStorage offline caching.

## Design Requirements
- Do NOT alter the visual styles of `dashboard.html`, `journey.html`, `classroom.html`, or `practice.html`.
- Ensure you only return data payloads to the front-end that are securely sanitized.
