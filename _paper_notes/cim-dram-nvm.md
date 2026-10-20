---
title: An Overview of Computing-in-Memory Circuits With DRAM and NVM
permalink: /paper-notes/cim-dram-nvm/
short_title: CIM With DRAM and NVM
paper_authors: Sangjin Kim, Hoi-Jun Yoo
paper_venue: 'IEEE Transactions on Circuits and Systems II: Express Briefs'
paper_year: 2024
paper_url: https://doi.org/10.1109/TCSII.2023.3333851
note_updated: '2026-10-20'
note_status: complete
excerpt: DRAM·NVM 기반 CIM의 연산 원리와 ADC/DAC, 정밀도·효율의 trade-off를 정리했습니다.
topics:
- PIM / CIM
- Memory Circuits
note_toc:
- depth: 1
  id: section-1
  title: 1. Introduction
- depth: 1
  id: section-2
  title: 2. Problem
- depth: 1
  id: section-3
  title: 3. Core Idea
- depth: 1
  id: section-4
  title: 4. Architectures & Computation Methods
- depth: 2
  id: section-5
  title: 4.1 DRAM-CIM
- depth: 3
  id: section-6
  title: 4.1.1 Digital-PIM/PNM
- depth: 3
  id: section-7
  title: 4.1.2 DRAM
- depth: 3
  id: section-8
  title: 4.1.3 Gain-Cell DRAM
- depth: 2
  id: section-9
  title: 4.2 NVM-CIM
- depth: 3
  id: section-10
  title: 4.2.1 Current-Based Operation with Complementary cell
- depth: 3
  id: section-11
  title: 4.2.2 Time-Based operation
- depth: 3
  id: section-12
  title: 4.2.3 Hybrid Method
- depth: 1
  id: section-13
  title: 5. Trade-offs and Limitations
- depth: 1
  id: section-14
  title: 6. My Thoughts
---

<div class="notion-body" markdown="0">
<h1 id="section-1">1. Introduction</h1>
<blockquote>
<p>이 논문은 SRAM-CIM이 가지는 transistor 및 area overhead, 제한된 weight density, volatility 등의 한계를 보완하기 위한 DRAM, NVM 기반의 CIM을 설명한다. 그러나 DRAM-CIM과 NVM-CIM에서도 leakage, non-linearity, 낮은 signal margin 등의 새로운 문제가 발생하고, 이를 어떤 관점으로 해결했는지를 소개한다.</p>
</blockquote>
<hr />
<h1 id="section-2">2. Problem</h1>
<p>ML/AI computation의 energy efficiency를 높이기 위해 SRAM-CIM이 많이 연구되었다. 그러나 SRAM-CIM에도 여러 한계가 존재한다. SRAM-CIM을 구현하기 위해서는 추가적인 computing logic이 필요하고, 이는 transistor 및 area overhead를 발생시킨다. 또한 SRAM은 하나의 cell에 1-bit를 저장하기 때문에 weight density가 제한된다. 전원이 꺼지면 저장된 data가 사라지는 volatility도 존재한다. 이를, DRAM, NVM 기반의 CIM을 통해 이러한 한계의 일부를 보완할 수 있다. DRAM은 더 높은 memory density를 제공하고, NVM은 non-volatility를 가진다. 그러나 이들을 활용했을 때에도 새로운 문제가 발생한다.</p>
<hr />
<h1 id="section-3">3. Core Idea</h1>
<p>이 논문은 DRAM, NVM 기반의 CIM을 활용하여 SRAM-CIM의 주요 한계를 어떻게 보완하는지에 초점을 맞춘다. DRAM-CIM에서는 Gain-Cell, 3T cell, 3T-2C cell 등의 구조를 소개한다. NVM-CIM에서는 computation과 read/write operation을 구현하는 current-based, time-based, hybrid 방법을 설명한다. 각 방법은 서로 다른 trade-off를 가지기 때문에 NN model의 요구사항에 맞추어 선택해야 한다.</p>
<hr />
<h1 id="section-4">4. Architectures &amp; Computation Methods</h1>
<h2 id="section-5">4.1 DRAM-CIM</h2>
<h3 id="section-6">4.1.1 Digital-PIM/PNM</h3>
<ul>
<li><b>PIM/PNM</b>
<ul>
<li><b>Computation Logic</b>: 여기서 설명하는 PIM은 SA 이후에 computing logic을 배치하고, PNM은 DIMM 또는 3D DRAM의 logic die에 computing logic을 배치한다. 두 방법 모두 cell 외부에서 computation이 수행된다.</li>
<li><b>Benefits</b>: 기존 memory가 data를 저장하는 역할을 했다면, PIM과 PNM은 일부 computation도 함께 수행할 수 있다.</li>
<li><b>Challenges</b>: Computing logic이 cell array 내부에 위치하지 않기 때문에 각 data를 처리할 때 SA가 동작해야 한다. 이는 CIM에 비해 latency, energy efficiency 측면에서 불리할 수 있다.</li>
</ul></li>
</ul>
<h3 id="section-7">4.1.2 DRAM</h3>
<ul>
<li><b>1T-1C DRAM-CIM</b>
<ul>
<li><b>Main Structure(Components)</b>: 일반적인 1T-1C DRAM 구조이다.</li>
<li><b>Computation Logic</b>: Cell array 내부에서 computation이 수행된다.</li>
<li><b>Benefits</b>: 높은 efficiency와 parallelism을 가지며, 더 많은 bandwidth를 활용할 수 있다.</li>
<li><b>Challenge</b>: Destructive read, leakage, noise의 영향이 존재한다.</li>
</ul></li>
</ul>
<h3 id="section-8">4.1.3 <b>Gain-Cell DRAM</b></h3>
<ul>
<li><b>Figure.2(a)</b>
<figure>
<img src="/images/papers/cim-dram-nvm/01.png" alt="원 논문의 그림" loading="lazy" decoding="async">
</figure>
<ul>
<li><b>Main Structure(Components)</b>: 2T-1C cell 한 쌍으로, 총 4개의 transistor와 2개의 capacitor로 구성된다. <b>RBL</b>과 <b>WBL</b>이 분리되어 있다.</li>
<li><b>Computation Logic</b>: (<b>W_L</b>, <b>W_H</b>)를 통해 ternary weight의 {-1, 0, +1} state를 표현하고, Input Activation은 wordline을 통해 입력된다. <b>W</b>가 High이고 <b>RWL</b>이 Low일 때, 즉 <b>IA</b>가 ‘1’인 상태에서 <b>RBL</b>에 current가 흐른다. 각 complementary cell pair에서 <b>IA</b>와 <b>W</b>의 multiplication이 발생한다. 또한 여러 4T-2C cell이 <b>RBLL/RBLR</b>을 공유하기 때문에 각 cell의 multiplication result가 <b>RBL</b>에서 accumulate된다. 따라서 current-based operation으로 볼 수 있다.</li>
<li><b>Benefits</b>: 일반적인 1T-1C DRAM과 달리 <b>RBL</b>과 <b>WBL</b>을 분리하여 non-destructive read path를 구현한다. <b>RBL</b>을 computing datapath로 활용할 수 있고, SA의 동작도 줄일 수 있다.</li>
<li><b>Challenge</b>: 각 cell의 current mismatch가 연산 결과에 반영되어 accuracy가 낮아질 수 있다. Memory density는 1T-1C DRAM-CIM보다 낮지만 SRAM-CIM보다는 높다.</li>
</ul>
<div class="notion-block">
<p>이러한 문제를 보완하기 위해 논문에서는 여러 구조를 제시한다.</p>
</div></li>
</ul>
<figure>
<img src="/images/papers/cim-dram-nvm/02.png" alt="원 논문의 그림" loading="lazy" decoding="async">
</figure>
<ul>
<li><b>Figure.2(b)</b>
<ul>
<li><b>Main Structure(Components)</b>: Voltage clipper를 사용한다.</li>
<li><b>Computation Logic</b>: Voltage clipper가 각 <b>RBL</b>의 voltage를 미리 정해진 값으로 제한한다. 이후 charge sharing을 통해 각 column(<b>RBL</b>)의 결과를 accumulate한다.</li>
<li><b>Benefits</b>: Voltage clipper를 통해 current mismatch로 인한 error를 줄일 수 있다.</li>
<li><b>Challenge</b>: Row parallelism을 활용하지 못하고 column parallelism만 활용한다. Accuracy는 크게 향상되지만, row parallelism을 사용하지 못하기 때문에 latency가 증가할 수 있다.</li>
</ul></li>
<li><b>Figure.2(c)</b>
<ul>
<li><b>Main Structure(Components)</b>: <b>RBL</b>을 여러 row segment로 나누는 구조이다.</li>
<li><b>Computation Logic</b>: 각 segment에서 1-bit multiplication을 수행한다. 이후 charge sharing을 통해 각 segment의 <b>RBL</b>에 나타난 결과를 accumulate한다.</li>
<li><b>Benefits</b>: Row parallelism을 활용할 수 있다.</li>
<li><b>Challenge</b>: Leakage, coupling 등으로 인한 computation error가 존재한다. 이러한 common-mode error를 제거하기 위해 추가적인 reference cell array가 필요하다.</li>
</ul></li>
<li><b>Figure.2(d)</b>
<ul>
<li><b>Main Structure(Components)</b>: 3T cell 구조이다.</li>
<li><b>Computation Logic</b>: 하나의 capacitor에 analog voltage로 4-bit weight를 저장한다. Q1 transistor는 capacitor에 저장된 analog voltage에 따라 동작하며, weight에 대응하는 양의 current를 흘린다. Q2 transistor는 4-bit <b>IA</b>를 pulse width, 즉 turn-on time으로 전달받는다. 따라서 current-time multiplication을 통해 4-bit weight와 4-bit <b>IA</b>의 multiplication을 수행할 수 있다.</li>
<li><b>Benefits</b>: 4b-4b multiplication을 수행할 수 있다.</li>
<li><b>Challenge</b>: 하나의 capacitor에 4-bit weight를 저장해야 하기 때문에 큰 capacitor가 필요하다. Leakage와 noise의 영향에도 올바른 analog weight 값을 구별할 수 있어야 하기 때문이다. 또한 current-based operation은 transistor의 non-linearity와 variation으로 인해 accuracy가 제한된다.</li>
</ul></li>
<li><b>Figure.2(e)</b>
<ul>
<li><b>Main Structure(Components)</b>: 3T-2C cell 구조이다.</li>
<li><b>Computation Logic</b>: Cell 내부에서 multiplication logic의 voltage domain을 분리한다. Multiplication은 digital domain에서 수행하고, 각 cell의 결과는 <b>RBL</b>에서 accumulate한다.</li>
<li><b>Benefits</b>: Voltage domain을 분리하여 capacitor의 leakage가 1-bit multiplication에 영향을 주지 않도록 한다. 또한 Fig.2(d)와 비교했을 때 큰 capacitor가 필요하지 않기 때문에 cell density를 높일 수 있다.</li>
<li><b>Challenge</b>: 하나의 cell에서는 1-bit multiplication만 수행한다.</li>
</ul></li>
</ul>
<h2 id="section-9">4.2 NVM-CIM</h2>
<div class="notion-columns">
<div class="notion-column" style="flex: 50">
<figure>
<img src="/images/papers/cim-dram-nvm/03.png" alt="원 논문의 그림" loading="lazy" decoding="async">
</figure>
</div>
<div class="notion-column" style="flex: 50">
<figure>
<img src="/images/papers/cim-dram-nvm/04.png" alt="원 논문의 그림" loading="lazy" decoding="async">
</figure>
<div class="notion-empty" aria-hidden="true">

</div>
</div>
</div>
<h3 id="section-10">4.2.1 Current-Based Operation with Complementary cell</h3>
<ul>
<li><b>Figure.3(a)</b>
<ul>
<li><b>Main Structure(Components)</b>: 1T-1R cell 한 쌍으로 구성된다.</li>
<li><b>Computation Logic</b>: 1T-1R cell 한 쌍을 이용하여 binarized (+1, -1) <b>W</b>와 <b>IA</b>의 연산을 구현한다. Weight 값에 따라 한 cell은 <b>LRS</b>, 다른 cell은 <b>HRS</b> state를 가진다. <b>IA</b> 값은 <b>WL</b>을 통해 입력된다. 따라서 resistance state(weight)와 <b>WL</b> state(<b>IA</b>)의 관계를 통해 <b>XNOR operation</b>이 구현되고, 그 결과가 <b>BL</b>에서 accumulate된다. Pull-up transistor와 cell resistance 사이의 voltage division에 의해 <b>BL</b> voltage가 결정된다.</li>
<li><b>Benefits</b>: Parallelism을 활용하여 높은 efficiency를 얻을 수 있다.</li>
<li><b>Challenge</b>: <b>BL</b>과 <b>PU</b>의 non-ideal resistance로 인해 <b>BL</b> voltage가 연산 결과에 대해 non-linear하게 나타난다. 따라서 flash <b>ADC</b>를 사용한다.</li>
</ul></li>
<li><b>Figure.3(b)</b>
<ul>
<li><b>Main Structure(Components)</b>: 4T-4R cell 구조이다.</li>
<li><b>Computation Logic</b>: Fig.3(a)가 complementary <b>WL</b>만 사용했다면, Fig.3(b)는 complementary <b>BL</b>도 함께 사용한다. 두 <b>BL</b>의 differential voltage를 통해 linear한 출력을 얻을 수 있다. 또한 Fig.3(a)와 같은 두 개의 2T-2R cell로 재구성할 수 있다. 이 경우 density와 efficiency는 높아지지만 accuracy는 낮아진다. NN model의 요구사항에 따라 4T-4R 또는 두 개의 2T-2R mode를 선택할 수 있다.</li>
<li><b>Benefits</b>: <b>ADC</b>를 통해 linear한 output을 sensing할 수 있다.</li>
<li><b>Challenge</b>: 더 많은 transistor와 resistor를 사용하기 때문에 Fig.3(a)에 비해 memory density가 낮다.</li>
</ul></li>
</ul>
<h3 id="section-11">4.2.2 Time-Based operation</h3>
<ul>
<li><b>Figure.3(c)</b>
<ul>
<li><b>Main Structure(Components)</b>: Voltage-to-time converter(VTC), time-to-digital converter(TDC)를 사용한다.</li>
<li><b>Computation Logic</b>: <b>BL</b>에는 미리 precharge된 parasitic capacitor가 존재한다. NVM cell을 통한 current가 <b>BL</b>을 discharge시키며, 이때 발생하는 analog voltage의 변화를 <b>VTC</b>를 통해 time domain으로 변환한다. 마지막으로 <b>TDC</b>를 통해 digital value로 변환한다.</li>
<li><b>Benefits</b>: 연산 중 지속적으로 흐르는 DC current가 없어 더 높은 energy efficiency를 얻을 수 있다.</li>
<li><b>Challenge</b>: 여러 converter를 사용하기 때문에 추가적인 peripheral circuit이 필요하다. <b>BL</b>의 discharge latency를 이용하는 sensing path와 <b>VTC</b>, <b>TDC</b> 등이 요구된다.</li>
</ul></li>
</ul>
<h3 id="section-12">4.2.3 Hybrid Method</h3>
<ul>
<li><b>Figure.3(d)</b>
<ul>
<li><b>Main Structure(Components)</b>: Single-level cell(<b>SLC</b>), multi-level cell(<b>MLC</b>)을 함께 사용한다.</li>
<li><b>Computation Logic</b>: <b>SLC</b>와 <b>MLC</b>는 서로 다른 장점과 trade-off를 가진다.
<ul>
<li><b>MLC</b>: Memory density와 efficiency가 높지만 signal margin과 accuracy가 낮다. 8-bit weight의 하위 6-bit를 저장한다.</li>
<li><b>SLC</b>: Accuracy와 signal margin이 높지만 memory density와 efficiency가 낮다. 8-bit weight에서 더 중요한 상위 2-bit를 저장한다.</li>
</ul></li>
<li><b>Benefits</b>: <b>SLC</b>와 <b>MLC</b>를 함께 사용하여 throughput, efficiency, computing accuracy 사이의 균형을 맞출 수 있다. NN model의 요구사항에 따라 두 종류의 cell을 어떻게 활용할지 결정해야 한다.</li>
<li><b>Challenge</b>: Weight bit를 <b>SLC</b>와 <b>MLC</b>에 나누어 저장하기 때문에 mapping과 control이 복잡해지고, area overhead도 발생할 수 있다고 생각했다.</li>
</ul>
<div class="notion-block">
<p>또한 <b>CIM–NMC hybrid method</b>에서도 비슷한 accuracy/efficiency trade-off를 확인할 수 있다. CIM은 throughput과 efficiency를 높이고, NMC는 computing accuracy를 높이는 역할을 한다.</p>
</div></li>
</ul>
<hr />
<h1 id="section-13">5. Trade-offs and Limitations</h1>
<table>

<tr>
<th scope="col"></th>
<th scope="col">Benefits</th>
<th scope="col">Costs / Trade-offs</th>
</tr>
<tr>
<th scope="row"><b>SRAM-CIM</b></th>
<td>안정적인 동작, 높은 accuracy</td>
<td>Transistor overhead, 1 bit/cell로 제한되는 weight density, volatility</td>
</tr>
<tr>
<th scope="row">DRAM-CIM</th>
<td>높은 memory density</td>
<td>Leakage/noise의 영향, destructive read(1T-1C), refresh overhead, computing accuracy 문제</td>
</tr>
<tr>
<th scope="row">NVM-CIM</th>
<td>Non-volatility</td>
<td>Non-linearity, 낮은 signal margin, static current 문제, write 시 높은 voltage와 latency, computing accuracy 문제</td>
</tr>
</table>
<p>기본적으로 cell array 내부에서 computation을 수행하면 data movement, SA overhead, latency를 줄일 수 있다. 또한 cell array 내부의 parallelism을 활용하여 efficiency를 높이고 latency를 낮출 수 있다. 그러나 그에 따른 trade-off도 존재한다. Analog domain에서 computation을 수행할 때 variation, leakage, non-linearity, signal margin 등의 문제가 발생하며, 이는 accuracy를 낮추는 원인이 된다.</p>
<h1 id="section-14">6. My Thoughts</h1>
<p><b>Computation(model) mapping을 어떻게 최적화할 수 있는지</b> 더 깊게 공부해보고 싶었다. 이 논문은 여러 문제를 해결하기 위한 구조적인 접근법을 주로 다룬다고 생각했다. Hybrid Method, 특히 Fig.3(d)를 보며 memory를 어떻게 할당해야 하는지 궁금했다. <b>SLC</b>와 <b>MLC</b> 두 종류의 cell이 있기 때문에 weight data를 이 둘에 나누어 저장해야 한다. Memory를 <b>SLC</b>와 <b>MLC</b>로 효과적으로 나누고 할당하는 방법이 있다면 더 알아보고 싶었다.<br />또한 hybrid approach가 NVM-CIM에서만 다루어진 이유도 궁금했다. DRAM-CIM에서도 서로 다른 cell, computation mode, sensing method를 조합하는 hybrid approach를 구현할 수 있는지 궁금했고, 이러한 방법을 활용한 기존 DRAM-CIM 연구가 있는지도 궁금하다. 그뿐만 아니라, 논문에서는 hybrid approach의 challenge, trade-off를 자세하게 설명하지 않는다. Hybrid architecture를 구현할 때 area, control, mapping, accuracy 측면에서 어떤 문제가 발생하는지도 더 알아보고 싶었다.</p>
<div class="notion-empty" aria-hidden="true">

</div>
</div>
