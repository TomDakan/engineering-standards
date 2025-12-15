---
title: Delphi Naming Conventions
type: language-guide
language: delphi
topic: naming
version: 1.0.0
---

# Delphi Naming Conventions

## General Rules

*   **Types**: Prefix with `T` (e.g., `TCustomer`).
*   **Interfaces**: Prefix with `I` (e.g., `ICustomerService`).
*   **Fields**: Prefix with `F` (e.g., `FAdHoc`).
*   **Arguments**: Prefix with `A` (e.g., `procedure Update(AName: string)`).
*   **Locals**: Prefix with `L` (e.g., `LResult`).

## Specifics

*   **Components**: We do NOT use Hungarian notation for components (e.g., `btnSubmit`). Use descriptive names `SubmitButton`.
*   **Enums**: Prefix with two or three letters related to the type (e.g., `TStatus = (stActive, stInactive)`).
