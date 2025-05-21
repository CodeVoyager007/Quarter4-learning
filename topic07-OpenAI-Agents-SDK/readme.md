# 🧠 Task 07 — Agentic AI (OpenAI Agents SDK)

This task explores the architecture and internal logic of OpenAI’s `Agents SDK`.  
We’ll look at how it uses Python features like `@dataclass`, `classmethods`, and `generics` to create smart and modular agents.

## 🔹 1. Why is the `Agent` class a `dataclass`?

The `Agent` class is marked as a **dataclass** to simplify and streamline the code structure.  
Dataclasses automatically generate boilerplate methods like `__init__`, `__repr__`, etc., making it easier to handle agent-related properties such as tools, instructions, and name.

✅ *This helps keep the code clean, readable, and centralized for all agent configurations.*

## 🔹 2a. Why are instructions stored in the `Agent` class? Why can they also be callable?

The **system instructions** define how the agent should behave. These can be stored as:

- A **string** → for static, fixed instructions  
- A **callable** → to dynamically generate instructions at runtime (e.g., based on time or context)

✅ *This makes the agent more flexible and adaptive to varying environments.*

## 🔹 2b. Why is the user prompt passed in the `run()` method? Why is it a `classmethod`?

The **user prompt** changes with every interaction — that’s why it is passed dynamically to the `run()` method.

- `run()` is a **classmethod**, meaning it can be invoked without creating an instance of `Runner`
- It’s designed to be **stateless, reusable, and clean**

✅ *Perfect for quickly processing user input with the existing agent configuration.*

## 🔹 3. What is the purpose of the `Runner` class?

The `Runner` class is responsible for managing the **execution lifecycle** of the agent.

- It accepts the `Agent` and user input
- Connects tools, context, and logic to generate a response

✅ *Think of it as the “engine” that powers the brain of your agent.*

## 🔹 4. What are Generics in Python? Why use `TContext`?

**Generics** allow developers to write flexible, reusable, and type-safe code.

- `TContext` is a **type variable** used to represent any form of context the agent might need
- It allows agents to work with different data types (e.g., `dict`, custom classes)

✅ *This promotes code reusability and structure while supporting diverse agent behaviors.*

## ✨ Summary

This task highlights the **modular, clean, and intelligent design** of OpenAI’s Agents SDK — using powerful Python features like:

- `@dataclass` for simplicity  
- `classmethod` for efficient method calls  
- `Generics` for type flexibility  

Together, they form the foundation of creating smart, reusable, and scalable AI agents 🤖💡

## 📚 Blog

Want to dive deeper? Check out my detailed breakdown on Medium!  
&nbsp;  
[![Read on Medium](https://img.shields.io/badge/Read%20on-Medium-000?style=for-the-badge&logo=medium&logoColor=white)](https://medium.com/@ayeshamughal21/understanding-agent-architecture-in-openais-agents-sdk-222fea3e1178)

> _“Written with logic, love, and late-night chai ☕ by Ayesha Mughal”_
