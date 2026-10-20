---
title: "About Me"
permalink: /
excerpt: "KAIST electrical engineering undergraduate interested in energy-efficient AI accelerators and memory-centric computing."
---
<p class="eyebrow">ELECTRICAL ENGINEERING · KAIST</p>
<p class="intro-lead">I'm Junseo Kim (김준서), an undergraduate student in the School of Electrical Engineering at KAIST. I'm interested in energy-efficient AI accelerators, with a particular focus on how data movement and reuse shape hardware performance.</p>
<p class="intro-context">I study accelerator architectures and memory systems through paper reading, connecting the mechanisms of individual designs with their performance and energy trade-offs.</p>

## Research Interests

<ul class="interest-list">
<li><strong>AI Accelerator Architectures</strong><br>NPUs, dataflow, and efficient mapping of neural network workloads.</li>
<li><strong>Data Movement &amp; Reuse</strong><br>Memory hierarchy, on-chip communication, bandwidth, and energy efficiency.</li>
<li><strong>Memory-Centric Computing</strong><br>Processing-in-memory and computing-in-memory with DRAM and non-volatile memories.</li>
</ul>

## Selected Paper Notes

<p lang="ko">AI 가속기의 구조와 데이터 이동을 중심으로 읽고 정리한 논문입니다.</p>
<ul class="note-list">
{% assign selected = 'accelerator-survey,eyeriss,tpu' | split: ',' %}
{% for slug in selected %}{% for note in site.paper_notes %}{% if note.url contains slug %}{% include note-list-item.html note=note compact=true %}{% endif %}{% endfor %}{% endfor %}
</ul>
<a class="more-link" href="{{ '/paper-notes/' | relative_url }}">View all paper notes →</a>
