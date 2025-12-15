---
title: General Code Review Checklist
type: checklist
version: 1.0.0
tags: [review, quality, verification]
---

{% for standard in core.standards %}

## {{ standard.title }}

{% if standard.checklist %}
{% for group in standard.checklist %}

* **{{ group.title }}**
{% for item in group.rules %}
  * {{ item }}
{% endfor %}
{% endfor %}
{% endif %}
{% endfor %}
