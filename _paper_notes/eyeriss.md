---
title: 'Eyeriss: An Energy-Efficient Reconfigurable Accelerator for Deep Convolutional
  Neural Networks'
permalink: /paper-notes/eyeriss/
short_title: Eyeriss
paper_authors: Yu-Hsin Chen et al.
paper_venue: IEEE JSSC
paper_year: 2017
paper_url: https://doi.org/10.1109/JSSC.2016.2616357
note_updated: '2026-10-20'
note_status: complete
excerpt: Row Stationary dataflow, memory hierarchy, NoC와 압축 기법을 중심으로 데이터 재사용을 살펴봤습니다.
topics:
- AI Accelerator
- Dataflow
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
  title: 4.1 Architecture Overall
- depth: 2
  id: section-6
  title: 4.2 Energy-Efficient Feature
- depth: 3
  id: section-7
  title: 4.2.1 Row Stationary(RS)
- depth: 4
  id: section-8
  title: 4.2.1.1 1-D Convolution Primitive in a PE
- depth: 4
  id: section-9
  title: 4.2.1.2 2-D Convolution PE set
- depth: 4
  id: section-10
  title: 4.2.1.3 PE Set Mapping
- depth: 4
  id: section-11
  title: 4.2.1.4 Dimensions Beyond 2-D in PE Array
- depth: 4
  id: section-12
  title: 4.2.1.5 Multiple 2-D Convolutions in a PE set
- depth: 4
  id: section-13
  title: 4.2.1.6 Multiple PE Sets in the PE Array
- depth: 4
  id: section-14
  title: 4.2.1.7 PE array processing passes
- depth: 3
  id: section-15
  title: 4.2.2 Exploit Data Statistics
- depth: 2
  id: section-16
  title: 4.3 System Modules
- depth: 3
  id: section-17
  title: 4.3.1 Global Buffer
- depth: 3
  id: section-18
  title: 4.3.2 Network-on-Chip(NoC)
- depth: 4
  id: section-19
  title: 4.3.2.1 Global Input Network (GIN)
- depth: 4
  id: section-20
  title: 4.3.2.2 Global Output Network(GON)
- depth: 4
  id: section-21
  title: 4.3.2.3 Local Network
- depth: 2
  id: section-22
  title: 4.4 Processing Element and Data Gating
- depth: 1
  id: section-23
  title: 5. Results
- depth: 2
  id: section-24
  title: 5.1 AlexNet
- depth: 2
  id: section-25
  title: 5.2 VGG-16
- depth: 1
  id: section-26
  title: 6. Thought
---

<div class="notion-body" markdown="0">
<h1 id="section-1">1. Introduction</h1>
<blockquote>
<p>CNN computation에서 요구하는 data의 양이 상당하다. 이는 data movement 과정에서 소모되는 power의 양이 computation에 비해 더 높다는 뜻이고, CNN accelerator의 throughput, energy efficiency를 높이기 위해서는 data movement를 최대한 줄여야 한다. 이러한 관점에서 Eyeriss는 off-chip DRAM access를 줄일 수 있는 dataflow인 Row Stationary(RS)를 소개한다. 그 외에도 Compression, Data gating(zero data 처리) 등의 기법을 활용한다. 이 논문의 핵심 쟁점은 CNN의 어떤 data를 어떻게 reuse했는지, data가 어떻게 움직이는지이다.</p>
</blockquote>
<h1 id="section-2">2. Problem</h1>
<p>이전의 많은 연구에서, CNN Accelerators는 simulation results로만 발표되었다는 한계가 존재한다. 또한, 이들은 system energy efficiency에 결정적인 요소인 off-chip DRAM access(data movement)를 어떻게 처리할지에 대한 설명이 부족하다. 이에, Eyeriss는 실제로 fabricated된 CNN accelerator를 구현하여, “actual” high throughput과 CNN Accelerator, off-chip DRAM을 포함한 전체 시스템에서의 energy efficiency를 최적화 하였다.</p>
<h1 id="section-3">3. Core Idea</h1>
<p>Eyeriss는 크게 아래 네 가지를 중점적으로 보면 좋다.</p>
<ol type="1">
<li><b>Four Memory-hierarchy</b>
<div class="notion-block">
<p>⇒ spad &lt; PE ↔ PE communication &lt; GLB &lt; off-chip DRAM</p>
</div></li>
<li><b>Row Stationary(RS)</b>
<div class="notion-block">
<p>⇒ 주어진 CNN shape에서 data를 최적으로 mapping하는 기법</p>
</div></li>
<li><b>Network-on-Chip(NoC)</b>
<div class="notion-block">
<p>⇒ RS dataflow를 기반으로 한 data mapping을 구현하는 장치</p>
</div></li>
<li><b>Run-Length Compression(RLC), PE data gating</b>
<div class="notion-block">
<p>⇒ Compression을 통한 data movement를 줄이는 방법과, “0” data를 효율적으로 처리하는 기법</p>
</div></li>
</ol>
<h1 id="section-4">4. Architectures &amp; Computation Methods</h1>
<h2 id="section-5">4.1 Architecture Overall</h2>
<figure>
<img src="/images/papers/eyeriss/01.png" alt="원 논문의 그림" loading="lazy" decoding="async">
</figure>
<div class="notion-block">
<p>Fig.2에서 Eyeriss system architecture를 보여준다.</p>
</div>
<p>DRAM과의 통신을 담당하는 Link Clock, chip의 processing을 담당하는 Core Clock이 독립적으로 동작하며 asynchronous FIFO interface를 통해 communicate한다.</p>
<p>168개의 PE로 구성된 12 <span class="math inline">\(\times\)</span> 14의 PE array, GLB, RLC CODEC, ReLU module로 이루어져있다. Data는 DRAM, GLB, PE↔PE communication, spads 총 4가지의 memory hierarchy를 통해 transfer 된다.</p>
<p>System은 크게 off-chip DRAM ↔ GLB 사이의 통신, 그리고 NoC를 통한 GLB ↔ PE array 사이의 통신으로 나뉜다. 출력 단계에서 ReLU, RLC CODEC module이 통과된다.</p>
<h2 id="section-6">4.2 Energy-Efficient Feature</h2>
<p>Energy-efficiency를 높이기 위해 RS dataflow를 통한 data reuse 기법. 주어진 dataflow에 맞게 data를 mapping하는 것을 도와주는 NoC, 마지막으로 data movement과정에서 Compression을 통해 bandwidth의 부담을 줄여주는 RLC기법 및 “0” data를 효율적으로 처리해주는 data gating 방법 등이 소개된다.</p>
<h3 id="section-7">4.2.1 Row Stationary(RS)</h3>
<p>RS dataflow는 모든 data type(ifmap, filter, psums/ofmap)에 대해서 data movement를 최소화한다. DRAM, GLB와의 접근을 최소화하고 data reuse를 극대화 하는 것에 초점을 맞춘다. CNN에서 크게 3가지의 data reuse의 형태가 존재한다.</p>
<ol type="1">
<li><b>Convolutional Reuse</b>
<div class="notion-block">
<p>: 동일한 ifmap plane에서 filter weight가 reused된다. 이때 filter weight는 E<span class="math inline">\(\times\)</span>F만큼(ofmap plane의 크기) 그리고 ifmap plane의 하나의 pixel data는 보통 R<span class="math inline">\(\times\)</span>S만큼(filter의 크기) reused된다.</p>
</div></li>
<li><b>Filter Reuse</b>
<div class="notion-block">
<p>: filter weight는 한 batch에 포함된 N개의 ifmap에 반복해서 사용된다.</p>
</div></li>
<li><b>Ifmap Reuse</b>
<div class="notion-block">
<p>: ifmap의 pixel data는 M개의 filter와의 연산에서 반복되어 사용된다.</p>
</div></li>
</ol>
<div class="notion-block">
<p>여기서 추가로 psum의 movement를 최소화 하는 관점을 생각할 수 있다. 즉 하나의 output에 속하는 곱셈 결과를 계속 더해가는 방법이다. Ofmaps의 하나의 pixel data를 구하기 위해서는 <span class="math inline">\(C\times R\times S\)</span>번의 MAC operations이 필요하다.</p>
</div>
<p>그러나 ifmap이나 weight의 재사용을 최대화하는 계산 순서에서는 서로 다른 output의 psum이 생성되므로, 여러 psum을 유지해야 한다. 따라서 RS는 이러한 재사용과 psum accumulation을 함께 고려한다.</p>
<h4 id="section-8">4.2.1.1 1-D Convolution Primitive in a PE</h4>
<p>Primitive operation은 filter weights 한 행과 ifmap values 한 행으로 psum values를 만드는 것이다. 각각의 PE는 convolution data reuse, psum accumulation을 위한 PE 내부의 local spad를 사용한다. 1-D convolution primitive에서 PE의 spad의 capacity는 filter의 크기에만 의존하며 filter의 한 행의 크기인(S), filter에 대응되는 ifmap sliding window size(S) 그리고 psum을 저장할 공간 한 개 만큼 필요하다.</p>
<h4 id="section-9">4.2.1.2 2-D Convolution PE set</h4>
<figure>
<img src="/images/papers/eyeriss/02.png" alt="원 논문의 그림" loading="lazy" decoding="async">
</figure>
<p>기본적으로 2D convolution은 여러개의 1D convolution로 구성된다.</p>
<ul>
<li>Filter row는 PE array에 horizontally하게 reused!</li>
<li>Ifmap row는 PE array에 diagonally하게 reused!</li>
<li>psum row는 PE array에서 vertically하게 accumulate!</li>
</ul>
<p>기본적으로 위의 3가지의 경우의 reused되는 경로를 이해하면 된다.</p>
<h4 id="section-10">4.2.1.3 PE Set Mapping</h4>
<figure>
<img src="/images/papers/eyeriss/03.png" alt="원 논문의 그림" loading="lazy" decoding="async">
</figure>
<p>앞으로 살펴볼 여러 CONV layer는 168개의 PE array에 들어맞지 않는 PE set을 가지고 있다. CONV layer의 특성에 따라 PE set이 변화하게 되고, 이 PE set을 어떤 strategy를 사용하여 PE array에 효과적으로 mapping 하는지 알아야 한다. 기본적으로 data를 공유하고 psum을 accumulate할 PE들을 서로 가까이 배치한다.</p>
<p>그러나 PE Set mapping을 할 때 주의해야할 경우 2가지가 존재한다.</p>
<ol type="1">
<li>PE Set이 PE array(168개)보다 더 많은 PE를 가지는 경우
<div class="notion-block">
<p>: 이 경우는 Fig 5의 CONV1에 해당하는 예시를 통해 확인할 수 있다. CONV1는 11 <span class="math inline">\(\times\)</span> 55 = 605개의 PE가 필요하다. 그래서 ofmaps row를 나누어서 처리한다. 이 방법을 strip-mined라고 부르며, 논문에서는 11 <span class="math inline">\(\times\)</span> 7의 크기로 나누어서 처리한다.</p>
</div></li>
<li>PE Set이 PE array보다는 적은 PE를 가지지만, Width 또는 Height가 PE array를 벗어난 경우
<div class="notion-block">
<p>*width(ofmaps row)가 더 큰 경우만 지원한다. Filter row의 크기가 더 큰 경우는 Eyeriss에서 지원하지 않는다. (=높이가 12를 넘는 경우를 지원하지 않음)</p>
</div>
<div class="notion-block">
<p>: 이 경우는 Fig 5의 CONV2에 해당하는 예시를 통해 확인할 수 있다. CONV2는 5 <span class="math inline">\(\times\)</span> 27 = 135개의 PE가 필요하다. PE array보다는 적은 PE를 가지지만, width의 크기가 array의 크기를 초과한다. 이를 해결하기 위해, 5 <span class="math inline">\(\times\)</span> 13, 5 <span class="math inline">\(\times\)</span> 14의 PE segments 두 개로 분리하여, array에 mapping하는 strategy를 사용한다.</p>
</div></li>
</ol>
<p>그 외에, CONV3, CONV4&amp;5는 PE array에 배치하기 쉽다. 오히려 3 <span class="math inline">\(\times\)</span> 13이라는 작은 크기로 인해, 내부에 4개의 PE set를 형성할 수 있다. 이는 후에 다룰 Dimension beyond 2-D in PE array에서 살펴본다.</p>
<h4 id="section-11">4.2.1.4 Dimensions Beyond 2-D in PE Array</h4>
<p>Fig.1에서 보여지는 CNN operation에서 요구하는 computation의 양은 3차원의 형태를 띈다. Batch size(N), number of channel(C), number of filter(M) 이 세 가지의 additional dimension이 존재한다. N, C, M 중 하나를 변화시키고 나머지 두 개의 차원을 고정하면 2D convolution이 사용된다.</p>
<ol type="1">
<li><b>Varying Batch(ifmap)</b>
<div class="notion-block">
<p>: Channel, filter는 고정된 채 ifmap만 달라지며 psum을 구한다. 여러 ofmap의 immediate values가 결과로 도출된다. ⇒ filter reuse</p>
</div></li>
<li><b>Varying filters</b>
<div class="notion-block">
<p>: Ifmap, channel는 고정된 채 filters만 달라지며 psum을 구한다. 하나의 ofmap의 서로 다른 channel에 대한 psum이 결과로 도출된다. ⇒ ifmap reuse</p>
</div></li>
<li><b>Varying Channels</b>
<div class="notion-block">
<p>: ifmap, filters는 고정된 채 channel만 달라지며 psum을 구한다. 이는 하나의 ofmap의 동일한 channel, 동일한 pixel에 대한 psum이 순차적으로 도출된다. 결과로 나온 psum을 바로 합쳐도 문제가 되지 않는다. ⇒ psum accumulation</p>
</div></li>
</ol>
<h4 id="section-12">4.2.1.5 Multiple 2-D Convolutions in a PE set</h4>
<p>여기서 PE의 spad size가 매우 크다면, PE가 여러개의 2-D convolutions을 서로 다른 filters, channels에 대해서 수행할 수 있다.</p>
<ol type="1">
<li>Same ifmap을 서로 다른 filters(p)를 이용해서 연산하는 경우</li>
<li>서로 다른 channels(q)의 연산을 통해 PE가 순차적으로 psum을 accumulate할 수 있게 하는 경우.</li>
</ol>
<p>여기서 p를 PE set이 연산할 filter의 개수, q를 PE set이 연산할 channel의 개수라고 하자. 하나의 PE set에서 p, q에 해당하는 연산을 수행하기 위해 필요한 각 PE의 spad capacity는 아래와 같다.</p>
<ol type="1">
<li><span class="math inline">\(p\times q\times S\)</span>: 하나의 PE에서 사용되는 filter의 weight data</li>
<li><span class="math inline">\(q \times S\)</span>: filter와 match되는 ifmap의 pixel data</li>
<li><span class="math inline">\(p\)</span>: 서로 다른 ofmap의 channel의 psum data를 구별하여 저장할 수 있는 공간.</li>
</ol>
<h4 id="section-13">4.2.1.6 Multiple PE Sets in the PE Array</h4>
<p>PE sets의 크기가 작다면 PE array에서 여러 개의 PE sets를 mapping할 수 있다. 이 경우, 크게 4가지의 이점이 존재한다.</p>
<ol type="1">
<li>PE utilization을 높일 수 있다.</li>
<li>throughput을 향상시킬 수 있다.</li>
<li>ifmaps의 data를 GLB에서 한 번 read했을 때 여러 개의 PE set에 동시에 재사용할 수 있다.</li>
<li>different sets에서 발생하는 psums를 PE array 내부에서 바로 accumulate할 수 있다.</li>
</ol>
<p>먼저 parameter r, t가 가지는 의미부터 살펴보자.</p>
<div class="notion-block">
<p><span class="math inline">\(r\)</span> : PE array에서 사용하는 서로 다른 channel을 사용하는 PE set의 수</p>
<p>⇒ PE array내부에서 r 개의 PE set이 psum을 함께 accumulate 한다.</p>
</div>
<div class="notion-block">
<p><span class="math inline">\(t\)</span> : PE array에서 사용하는 서로 다른 filters를 사용하는 PE set의 수</p>
<p>⇒ t 개의 PE sets이 동일한 ifmap value를 공유한다.</p>
</div>
<p>CONV1, CONV3은 각각 t = 2, t = 4이다. 즉 동일한 ifmap value가 각각의 PE sets에 보내지고, 각 set마다 다른 filter가 사용되어 계산된다.</p>
<p>CONV4,5는 r = t = 2인 경우다. 총 4개의 PE sets이 아래와 같이 담당하고 있다.</p>
<table>
<tr>
<td>PE Set 종류</td>
<td><b>filter 종류</b></td>
<td><b>Input channel 종류</b></td>
</tr>
<tr>
<td>Set 1</td>
<td>A</td>
<td>Channel 1</td>
</tr>
<tr>
<td>Set 2</td>
<td>A</td>
<td>Channel 2</td>
</tr>
<tr>
<td>Set 3</td>
<td>B</td>
<td>Channel 1</td>
</tr>
<tr>
<td>Set 4</td>
<td>B</td>
<td>Channel 2</td>
</tr>
</table>
<div class="notion-block">
<p>Set1, Set3는 channel 1의 ifmap value를, Set2, Set4는 channel 2의 ifmap value를 공유한다. Set1, Set2는 같은 filter와 서로 다른 channel를 가짐으로써, 서로의 psum을 더해준다. 같은 이유로, Set3, Set4도 서로의 psum을 더해준다.</p>
<p>⇒ 같은 filter, 다른 channel을 공유하는 한 쌍의 PE set에서 발생하는 psum은 함께 더해진다.</p>
</div>
<h4 id="section-14">4.2.1.7 PE array processing passes</h4>
<figure>
<img src="/images/papers/eyeriss/04.png" alt="원 논문의 그림" loading="lazy" decoding="async">
</figure>
<p>PE array 내부에서 여러 개의 PE sets가 포함될 수 있고, PE sets 내부에서 여러 channels, filters가 연산될 수 있다. 이를 취합하면 결과적으로 하나의 PE array에서 연산하는 filters, channels의 개수는 아래와 같다.</p>
<ul>
<li><span class="math inline">\(p \times t\)</span>개의 filters</li>
<li><span class="math inline">\(q \times r\)</span>개의 channels</li>
</ul>
<p>Fig.7에서 filters, channels, ifmaps의 scheduling을 보여준다.</p>
<div class="notion-block">
<p>예시로 든 CNN layer는 6개의 channel, 8개의 filter, 4개의 ifmap으로 구성된다. 그리고 한 번의 pass에서는 3개의 channel, 4개의 filter, 2개의 ifmap을 처리할 수 있다. 따라서 총 8번의 pass로 전체 layer를 완전히 처리할 수 있다.</p>
<div class="notion-block">
<p>⇒ <span class="math inline">\(p \times t\)</span> = 4, <span class="math inline">\(q \times r\)</span> = 3, n = 2</p>
</div>
</div>
<p>Pass1, Pass2에서 나온 결과는 아직 미완성된 값이다. 이후의 pass를 거쳐야 완성된 ofmap value를 가질 수 있다. 따라서 이들의 결과를 바로 DRAM에 보내지 않고 GLB에 보관한다. (Intermediate results를 GLB에 보관)</p>
<p>Pass1 → Pass2 에서 동일한 ifmap의 channel 1-3을 사용한다. 이때 사용하는 ifmap을 DRAM에서 두 번 가져올 필요가 없다. 한 번 가져온 후 GLB에 저장하여 사용한다. 이것이 pass에서의 ifmap reuse이다.</p>
<p>이렇게 Pass 거치며 나오는 psums들은 ofmap의 8개의 channels를 구성한다. 이 8개의 ofmap의 psums를 GLB에 저장할 수 있어야 한다.</p>
<p>추가로, 각 filter weight는 4개의 pass당 한 번씩 DRAM에서 PE array로 읽어 온다.</p>
<div class="notion-block">
<p>pass를 어떤 순서로 결정하느냐에 따라 GLB에 저장할 데이터가 달라진다. Fig. 7에는 Pass1 → Pass2 에서 동일한 3개의 channel로 이루어진 두 개의 ifmap을 재사용한다.</p>
<p>⇒ 따라서 GLB에는 6개의 input plane이 저장되어야 한다.(<span class="math inline">\(n \times q \times r\)</span>)</p>
</div>
<div class="notion-block">
<p>그리고 ifmap을 통해 8개의 channel를 가진 2개의 ofmap이 나온다.</p>
<p>⇒ 따라서 GLB에 16개의 output plane이 저장되어야 한다.(<span class="math inline">\(n \times m\)</span>)</p>
</div>
<p>각 경우에 따라 GLB에 저장되어야 할 데이터의 종류, 비율이 달라진다. Layer에 맞추어 GLB의 저장공간을 배분해야 한다.</p>
<h3 id="section-15">4.2.2 Exploit Data Statistics</h3>
<p>Row Stationary가 data reuse관점으로 data movement를 줄여서 에너지 소모를 줄여나갔다면 “B. Exploit Data Statistics”는 CNN의 데이터에는 “0”의 값이 많이 나오는 특성을 추가로 활용하여 에너지를 줄인다. 크게 아래 두 가지의 관점으로 구성된다.</p>
<ul>
<li>“Compression”을 통해 DRAM access를 줄인다.</li>
<li>0이라는 값을 이용하는 unnecessary computation을 skip해서 processing power를 줄인다.</li>
</ul>
<p>CNN 데이터에 0이 많은 이유는 ReLU function 때문이다. Layer가 깊어질수록 “0” 데이터가 더 많아진다. CONV2, CONV5에서는 각각 40%, 75%의 높은 zero data 비율을 가진다.</p>
<figure>
<img src="/images/papers/eyeriss/05.png" alt="원 논문의 그림" loading="lazy" decoding="async">
</figure>
<div class="notion-block">
<p>Fig.8은 0을 모두 다 저장하지 않고, 0의 개수를 저장하는 방법인 RLC(Run-Length Compression)을 제시한다.</p>
</div>
<ol type="1">
<li>0의 개수를 저장하는 5-b number를 “Run”
<div class="notion-block">
<p>⇒ ”Run” 하나당 31개의 연속된 0을 compression 할 수 있다.</p>
</div></li>
<li>0이 아닌 데이터를 저장하는 16-b의 “Level”</li>
<li>Run-Level pair 3개를 묶으면 총 63bit가 나온다. 여기에 압축코드의 마지막 word 인지 표시하는 1-b를 추가하여 64bit로 만든다.</li>
</ol>
<p>첫 layer에 들어가는 입력을 제외한 feature map들을 <b>DRAM에서 RLC 압축 형태로 저장한다.</b></p>
<p>DRAM에서 데이터를 읽을 때:</p>
<ul>
<li><b>DRAM에 저장된 encoded ifmap → RLC decoder에서 decompress → GLB에 저장 → PE에 공급</b></li>
</ul>
<p>계산 결과를 DRAM에 보낼 때:</p>
<ul>
<li><b>GLB의 ofmap → ReLU function(select) → RLC encoder에서 encoding → DRAM에 저장</b></li>
</ul>
<p>이를 통해 ifmap, ofmap에 대한 DRAM access가 CONV1에는 30%, CONV5에서는 75% 정도 줄여졌다. Fig. 9를 통해 overall DRAM access가 RLC를 통해 얼마나 줄어들었는지 확인할 수 있다.</p>
<h2 id="section-16">4.3 System Modules</h2>
<h3 id="section-17">4.3.1 Global Buffer</h3>
<p>Global Buffer, GLB는 PE array 전체가 사용하는 저장소이다.</p>
<p>GLB에는 ifmap, psum, filters가 저장된다.</p>
<ul>
<li>ifmap은 여러 pass에서 재사용되는 값들을 DRAM에서 반복해서 읽는 일을 줄여준다.</li>
<li>psum은 각 pass마다 나오는 intermediate results를 보관하여 최종 ofmap value가 완성될 때 까지 GLB에 보관되어 DRAM과의 access를 줄인다.</li>
</ul>
<p>Eyeriss의 GLB는 108kB이다.</p>
<ul>
<li>100kB는 ifmaps, psums를 저장하는 공간</li>
<li>8kB는 다음 pass에 필요한 filter를 미리 DRAM으로 부터 받아 저장하는 공간이다.
<div class="notion-block">
<p>⇒ 그 이유는, PE array가 연산을 마치고 그 다음 filter를 받아올 때, GLB에 미리 저장해두면 filter를 기다리는 시간을 줄일 수 있기 때문이다.</p>
</div></li>
</ul>
<p>100kB는 총 25개의 bank로 분리된 구조를 가진다. 그 이유는 아래와 같다.</p>
<ol type="1">
<li>CNN layer 종류마다 GLB에 요구되는 ifmaps, psums의 공간이 다르다.
<div class="notion-block">
<p>⇒ 25개의 bank으로 분리하여, layer의 종류마다 bank의 개수를 다르게 할당하여 ifmaps, psums에게 공간을 부여한다.</p>
</div></li>
<li>PE array는 ifmaps, psums에 동시에 접근할 수 있어야 한다.
<div class="notion-block">
<p>⇒ 서로 다른 bank로 ifmaps, psums를 구분하면 PE array가 데이터를 받아올 때 서로가 저장된 bank에 동시에 접근할 수 있다.</p>
</div></li>
</ol>
<h3 id="section-18">4.3.2 Network-on-Chip(NoC)</h3>
<p>NoC는 GLB↔PE array, PE ↔ PE 사이의 data movement를 관리한다. NoC architecture는 크게 아래 3가지를 고려해야 한다.</p>
<ol type="1">
<li>CNN layer에 맞는 RS data flow pattern을 지원해야 한다.</li>
<li>RS dataflow가 만든 data reuse를 활용해서 energy-efficiency를 높여야 한다. (ex. 같은 data를 PE array에서 여러개 필요할 때, 한 번에 여러 PE에 전달해야 한다.)</li>
<li>PE의 속도에 맞는 충분한 bandwidth를 제공해야 한다.</li>
</ol>
<p>이러한 조건에 맞는 custom NoC를 구현한다.</p>
<h4 id="section-19">4.3.2.1 Global Input Network (GIN)</h4>
<p>GIN은 single-cycle multicast를 지원하여, 한 cycle 안에 GLB에서 하나의 데이터를 여러 PE에게 전달해준다.</p>
<p>이때, 168개의 PE중, 특정 데이터를 원하는 PE의 정보를 함께 전달하는 과정이 중요하다.</p>
<p>생각해볼만한 아이디어 중 하나는, 168 bits의 tag를 통해 데이터를 받길 원하는 PE의 정보를 저장하여 전달하는 것이다. 그러나 이 경우, 너무 긴 데이터를 전달하는 것이기에 GIN bus width에 부담을 주어 energy, area 관점에서 손해이다.</p>
<p>이를 해결하기 위해 새로운 방법이 Fig.10을 통해 소개된다.</p>
<figure>
<img src="/images/papers/eyeriss/06.png" alt="원 논문의 그림" loading="lazy" decoding="async">
</figure>
<p>Y-bus, X-bus의 두 단계로 원하는 PE에 data를 전달하는 방식이다.</p>
<ul>
<li>Y-bus: PE array의 세로 방향에 위치하여 각 행에 위치한 12개의 X-bus와 연결됨.</li>
<li>X-bus: 각 행 마다 하나씩 존재하며, 그 행에 위치한 14개의 PE와 연결됨.</li>
</ul>
<p>데이터는 Y-bus를 통해 필요한 X-bus로 전달되고, X-bus를 통해 필요한 PE에게 전달된다. 이때 전달 해야할 PE를 구분하기 위해 “row ID”, “col ID”를 사용한다.</p>
<ul>
<li>Row ID: X-bus가 가지고 있는 ID 값</li>
<li>Col ID: PE가 가지고 있는 ID 값.</li>
</ul>
<p>⇒ 여기서 중요한 개념은, 이 ID값은 절대 물리적인 위치를 뜻하지 않는다. Layer에 맞추어 설정된 값으로, 모든 X-bus가 같은 row ID를 가질 수도 있고, 하나의 X-bus에 동일한 col ID를 지닌 PE가 있을 수도 있다. (Fig.11을 통해 확인할 수 있음)</p>
<p>따라서, 특정 data가 GLB에서 PE array로 이동할 때, (row, col) tag를 함께 이동시키고 tag에 적힌 정보와 일치하는 X-bus, PE가 데이터를 받게 된다.</p>
<p>아래는 추가 정보이다.</p>
<ul>
<li>Multicast Controller(MC): tag의 ID를 비교하여, 올바른 PE에만 데이터가 갈 수 있도록 하는 장치.</li>
<li>Ready signal: PE로 부터 받는 signal로, PE가 동작이 준비되었을 때만 GLB → GIN 으로의 data movement가 일어난다.</li>
</ul>
<h4 id="section-20">4.3.2.2 Global Output Network(GON)</h4>
<p>GIN이 GLB→PE array로 데이터를 공급했다면, GON은 반대로 PE array→GLB로 psums 데이터를 전달한다. GIN과 같은 architecture를 가지고 방향만 반대라고 생각하면 된다.</p>
<h4 id="section-21">4.3.2.3 Local Network</h4>
<p>Local network는 같은 열에서 인접한 두 개의 위, 아래 PE 사이에서 psum을 direct하게 전달해준다. (아래→위 로만 전달이 가능). PE는 GIN을 통해 GLB에서 psum을 받아오는 경우와 LN을 통해 다른 PE로 부터 psum을 받아오는 경우, 총 두 가지가 존재한다. 어떤 방법을 선택할지는 CNN shape에 따른 dataflow mapping에서 결정된다.</p>
<h2 id="section-22">4.4 Processing Element and Data Gating</h2>
<figure>
<img src="/images/papers/eyeriss/07.png" alt="원 논문의 그림" loading="lazy" decoding="async">
</figure>
<p>Fig.12에서 PE architecture를 더 구체적으로 분석한다.</p>
<p>크게 주목할만한 특징으로,</p>
<div class="notion-block">
<p>첫 번째, PE는 <span class="math inline">\(p, q\)</span>의 값에 따라서 spad에서 데이터를 읽는 순서가 달라진다.</p>
<ul>
<li><span class="math inline">\(p\)</span>: 하나의 PE에서 처리하는 서로 다른 filter의 수</li>
<li><span class="math inline">\(q\)</span>: 하나의 PE에서 처리하는 서로 다른 input channel의 수</li>
</ul>
<div class="notion-block">
<p>이 두 개의 parameter는 PE가 한 번에 얼마나 많은 작업량을 처리하느냐 라는 의미와 함께, PE에 존재하는 3개의 spad의 동작 순서까지 결정하는 역할을 한다.</p>
<p>3개의 spad의 종류:</p>
<ol type="1">
<li>Ifmap spad: 12 <span class="math inline">\(\times\)</span> 16b</li>
<li>Filter spad: 224 <span class="math inline">\(\times\)</span>16b</li>
<li>Psum spad: 24 <span class="math inline">\(\times\)</span> 16b</li>
</ol>
</div>
</div>
<div class="notion-block">
<p>두 번째, PE는 3 stage pipeline으로 구성된다.</p>
<p>Spad access를 하는데 stage 하나를 차지하고, 나머지 두 개의 stage는 computation(multiplication, accumulation)에 사용된다.</p>
<div class="notion-block">
<p>마지막으로 “Data gating logic”이다. 앞서 Exploit Data Statistics에서도 언급되었듯이 ifmap value가 “0”일 때 불필요한 연산을 막아서 power를 줄이는 방법이다. Ifmap value가 “0”인지 판별하기 위해 12‘b Zero Buffer가 사용된다. ifmap spad에는 총 12개의 ifmap value가 들어가고, 따라서 12’b Zero Buffer를 통해 12개의 값들 중 무엇이 “0”값을 지니는지 표시할 수 있다. 만약 ifmap value가 ”0“임을 확인했다면,</p>
<ol type="1">
<li>Filter spad를 읽지 않는다</li>
<li>MAC datapath의 불필요한 switching을 막는다.</li>
</ol>
</div>
<p>이를 통해 대략 45%의 PE power consumption을 줄여나갈 수 있다.</p>
</div>
<h1 id="section-23">5. Results</h1>
<figure>
<img src="/images/papers/eyeriss/08.png" alt="원 논문의 그림" loading="lazy" decoding="async">
</figure>
<p>Eyeriss에서 확인할 수 있는 결과 및 특징이다.</p>
<p>Eyeriss 역시 memory에 큰 비중을 두었다. GLB, spads는 전체 면적의 2/3을 차지하며, 그에 반해 연산기는 7.4% 정도만 차지한다.</p>
<p>PE spads가 차지하는 면적은 GLB보다 2.5x 더 컸지만, GLB에 비해 용량은 2/3 정도 밖에 미치지 못한다. 이는 spads가 data reuse 관점에서는 유리하지만 그에 대한 trade off로 low memory density가 존재함을 의미한다.</p>
<h2 id="section-24">5.1 AlexNet</h2>
<p>Eyeriss로 AlexNet를 동작시켰을 때, actual throughput은 peak throughput에 비해 낮았다.</p>
<p>그 이유는 아래와 같다.</p>
<ol type="1">
<li>PE utilization이 88%로, 모든 PE가 다 active state를 유지하지 않았다.</li>
<li>pass 마다 GLB에서 PE array로 데이터를 공급하고 연산을 시작하는 데 시간이 소모된다.</li>
<li>DRAM으로 부터 data를 받아올 때 processing이 멈춘다.</li>
</ol>
<figure>
<img src="/images/papers/eyeriss/09.png" alt="원 논문의 그림" loading="lazy" decoding="async">
</figure>
<p>다음은 chip에서의 전력소모이다.</p>
<div class="notion-block">
<p>Fig. 16을 통해 chip에서 spads, GLB, NoC가 차지하는 전력소모 비율이 높음을 알 수 있다. (CONV1, 45%) 이는, data movement가 computation보다 더 많은 전력을 소모함을 의미한다.</p>
<p>⇒ chip 내부에서 data movement가 전력 소모에 큰 비중을 차지하지만, 이는 off-chip DRAM과의 접근을 최대한 줄이기 위해 내부에서 data reuse를 많이 실시하기 때문이다. 따라서 chip에서의 data movement로 인한 전력 소모의 비중이 높다고 해서 이 system의 에너지 효율이 낮다고 말할 수 없다.</p>
</div>
<figure>
<img src="/images/papers/eyeriss/10.png" alt="원 논문의 그림" loading="lazy" decoding="async">
</figure>
<p>Fig. 17은 voltage를 scaling up 했을 때의 Frame rate와 power consuming이 어떻게 변하는지 보여준다. 속도와 에너지 효율은 서로가 trade-off 관계를 가짐을 확인할 수 있다.</p>
<h2 id="section-25">5.2 VGG-16</h2>
<p>마지막으로 Eyeriss로 VGG-16를 동작시켰을 때의 결과이다.</p>
<p>VGG-16은 AlexNet에 비해 CONV layer가 더 깊고, 연산량도 더 많다. 이는 수행할 MAC operation이 더 많다는 뜻이다.</p>
<p>그러나 MAC operation의 개수로 latency를 온전히 설명할 수 없다.</p>
<figure>
<img src="/images/papers/eyeriss/11.png" alt="원 논문의 그림" loading="lazy" decoding="async">
</figure>
<div class="notion-block">
<p>TABLE VI에서 CONV1-2와 CONV4-2를 비교하자</p>
<ul>
<li>CONV1-2, CONV4-2의 MAC operation 횟수는 동일하다.</li>
<li>그러나 CONV1-2의 latency가 CONV4-2보다 4배 크다.
<div class="notion-block">
<p>⇒ 그 이유는 early layer(CONV1-2)는 deeper layer(CONV4-2)보다 더 많은 processing pass를 지니기 때문이다. Processing pass가 많아질 수록 ramping up 하는데 소요되는 시간이 증가하기 때문에 latency가 더 커지는 것이다.</p>
</div>
<ul>
<li>Early layer가 더 pass가 많은 이유는 feature map의 크기가 더 커서, PE set을 나누어 PE array에 배치해야 하기 때문이라 생각한다. 그에 반해, deeper layer은 feature map의 크기는 작고, channel의 수가 더 많아서 병렬 연산을 활용하기 쉽기에, early layer에 비해 적은 pass로 구성된다고 생각했다.</li>
</ul></li>
</ul>
</div>
<h1 id="section-26">6. Thought</h1>
<p>CNN의 CONV layer에서 throughput과 energy efficiency를 향상시키기 위한 접근법을 이해할 수 있었다. 특히 data reuse를 구현하는 방식을 이전 논문들보다 깊이 있게 공부할 수 있었고, 이 점이 흥미로웠다. 반복되는 데이터에 대한 off-chip DRAM access를 줄이려면 데이터를 memory hierarchy의 어디에 배치하고 어떻게 이동시켜야 하는지 살펴볼 수 있었다. 또한 CNN layer의 shape에 따라 어떤 순서와 규칙으로 계산을 PE에 mapping해야 하는지에 대한 관점도 얻을 수 있었다.</p>
<p>Results에서는 동일한 하드웨어, 동일한 MAC operation을 수행하더라도, layer를 mapping 하는 방식에 따라 실제 latency가 크게 달라질 수 있다는 점을 확인했다. 이러한 결과를 통해 계산에 필요한 데이터를 어떻게 이동시키고, mapping할지가 이 논문에서 가장 중요한 요소 중 하나라고 생각했다.</p>
<p>이 논문을 읽으며 궁금했던 점은 PE의 개수가 “168개”로 정해진 이유이다. PE 수를 늘리는(scaling) 과정에서 어떤 trade-off가 발생하는지, 그리고 어떤 이유로 168개라는 수가 선택되었는지에 대해 알고 싶었다.</p>
<p>현재 연구의 최전선에서 다루는 application과 model은 무엇인지, 어떤 데이터를 재사용할 수 있으며 이를 구현하기 위한 접근법에는 무엇이 있는지 더 공부해보고 싶다. 앞으로 올 on-device AI의 시대에서는, 제한된 area, energy, memory 자원 안에서 원하는 AI model을 동작시켜야 한다. 이 논문에서 제시한 방법론과 문제 해결 전략은 이러한 문제를 해결하는 접근법과 관점을 길러 나가는 데 도움이 된다고 생각한다.</p>
<p>이러한 능력 및 관점을 길러나가고 싶고, 현재로서는 workload의 데이터 특성에 맞춰 dataflow, memory, communication을 설계하는 NPU architecture를 더 깊이 공부해보고 싶다는 생각이 들었다.</p>
</div>
