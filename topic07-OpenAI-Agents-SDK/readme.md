## 🧠 Task 07 — Agentic AI (OpenAI Agents SDK)

## 🔹 **1. Why is the Agent class a `dataclass`?**

The `Agent` class is marked as a **dataclass** to simplify the code structure.
Dataclasses automatically generate methods like `__init__` and `__repr__`, which makes it easier to handle and manage agent-related information such as tools, instructions, and name.

- ✅ This helps keep the code clean and organized while storing all agent configuration in one place.

---

## 🔹 **2a. Why are instructions stored in the Agent class? Why can they also be callable?**

The **system instructions** define how the agent should behave. These are stored in the `Agent` class as a static value or a **callable function**.

* If stored as a **string**, the instructions are fixed.
* If set as a **callable**, they can be **dynamically generated** based on runtime conditions.

- ✅ This makes the agent flexible and more context-aware during execution.

---

## 🔹 **2b. Why is the user prompt passed in the `run()` method? Why is it a `classmethod`?**

The **user prompt** changes every time, so it is passed as a parameter to the `run()` method of the `Runner` class.

* `run()` is a **classmethod**, which means it can be used **without creating an instance** of the class.
* This allows the agent to quickly process prompts and return results.

- ✅ It’s a clean and efficient way to separate agent configuration from user interaction.

---

## 🔹 **3. What is the purpose of the `Runner` class?**

The `Runner` class handles the **execution process** of the agent.
It takes the agent and user prompt and manages how the response is generated.

- ✅ Think of it as the controller that connects the agent’s brain with the user’s question.

---

## 🔹 **4. What are Generics in Python? Why use `TContext`?**

**Generics** allow us to write flexible and reusable code with type safety.

* `TContext` is a **type variable** used to represent any context the agent might need.
* Using generics allows the agent to work with **different types of context** (e.g., dictionaries, custom classes).

- ✅ This adds flexibility while still keeping the code reliable and structured.



💡 **Summary:**
This task helps us understand how the OpenAI Agents SDK is designed to be modular, clean, and powerful by using Python features like `dataclasses`, `classmethods`, and generics.

### 📚 Blog  
Check out my detailed write-up on this topic on Medium:
[![Read on Medium](https://img.shields.io/badge/Read%20on-Medium-000?style=for-the-badge&logo=medium&logoColor=white)](https://medium.com/@ayeshamughal21/understanding-agent-architecture-in-openais-agents-sdk-222fea3e1178)

