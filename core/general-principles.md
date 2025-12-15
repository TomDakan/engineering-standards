---
title: General Engineering Principles
type: core
version: 1.0.0
tags: [architecture, principles, universal]
description: Universal engineering truths applicable to any language focusing on Integrity, Readability, Reliability, and Security.
---

This document outlines the universal engineering truths that guide our development process, regardless of the specific technology stack.

{% for standard in core.standards %}

## {{ loop.index }}. {{ standard.title }}

{% if standard.principles %}
{% for principle in standard.principles %}
{% if principle.rules %}

### {{ principle.title }}

{% for item in principle.items %}

* **{{ item.title }}**: {{ item.description }}
{% endfor %}
{% else %}
* **{{ principle.title }}**: {{ principle.description }}
{% endif %}
{% endfor %}
{% endif %}
{% endfor %}
