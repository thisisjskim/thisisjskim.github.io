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

## 1. Introduction
{: #section-1 }

> 이 논문은 SRAM-CIM이 가지는 transistor 및 area overhead, 제한된 weight density, volatility 등의 한계를 보완하기 위한 DRAM, NVM 기반의 CIM을 설명한다. 그러나 DRAM-CIM과 NVM-CIM에서도 leakage, non-linearity, 낮은 signal margin 등의 새로운 문제가 발생하고, 이를 어떤 관점으로 해결했는지를 소개한다.

---

## 2. Problem
{: #section-2 }

ML/AI computation의 energy efficiency를 높이기 위해 SRAM-CIM이 많이 연구되었다. 그러나 SRAM-CIM에도 여러 한계가 존재한다. SRAM-CIM을 구현하기 위해서는 추가적인 computing logic이 필요하고, 이는 transistor 및 area overhead를 발생시킨다. 또한 SRAM은 하나의 cell에 1-bit를 저장하기 때문에 weight density가 제한된다. 전원이 꺼지면 저장된 data가 사라지는 volatility도 존재한다. 이를, DRAM, NVM 기반의 CIM을 통해 이러한 한계의 일부를 보완할 수 있다. DRAM은 더 높은 memory density를 제공하고, NVM은 non-volatility를 가진다. 그러나 이들을 활용했을 때에도 새로운 문제가 발생한다.

---

## 3. Core Idea
{: #section-3 }

이 논문은 DRAM, NVM 기반의 CIM을 활용하여 SRAM-CIM의 주요 한계를 어떻게 보완하는지에 초점을 맞춘다. DRAM-CIM에서는 Gain-Cell, 3T cell, 3T-2C cell 등의 구조를 소개한다. NVM-CIM에서는 computation과 read/write operation을 구현하는 current-based, time-based, hybrid 방법을 설명한다. 각 방법은 서로 다른 trade-off를 가지기 때문에 NN model의 요구사항에 맞추어 선택해야 한다.

---

## 4. Architectures & Computation Methods
{: #section-4 }

### 4.1 DRAM-CIM
{: #section-5 }

#### 4.1.1 Digital-PIM/PNM
{: #section-6 }

- **PIM/PNM**
  - **Computation Logic**: 여기서 설명하는 PIM은 SA 이후에 computing logic을 배치하고, PNM은 DIMM 또는 3D DRAM의 logic die에 computing logic을 배치한다. 두 방법 모두 cell 외부에서 computation이 수행된다.
  - **Benefits**: 기존 memory가 data를 저장하는 역할을 했다면, PIM과 PNM은 일부 computation도 함께 수행할 수 있다.
  - **Challenges**: Computing logic이 cell array 내부에 위치하지 않기 때문에 각 data를 처리할 때 SA가 동작해야 한다. 이는 CIM에 비해 latency, energy efficiency 측면에서 불리할 수 있다.

#### 4.1.2 DRAM
{: #section-7 }

- **1T-1C DRAM-CIM**
  - **Main Structure(Components)**: 일반적인 1T-1C DRAM 구조이다.
  - **Computation Logic**: Cell array 내부에서 computation이 수행된다.
  - **Benefits**: 높은 efficiency와 parallelism을 가지며, 더 많은 bandwidth를 활용할 수 있다.
  - **Challenge**: Destructive read, leakage, noise의 영향이 존재한다.

#### 4.1.3 **Gain-Cell DRAM**
{: #section-8 }

- **Figure.2(a)**
  

<figure><img src="/images/papers/cim-dram-nvm/01.png" alt="원 논문의 그림" loading="lazy" decoding="async"></figure>

  - **Main Structure(Components)**: 2T-1C cell 한 쌍으로, 총 4개의 transistor와 2개의 capacitor로 구성된다. **RBL**과 **WBL**이 분리되어 있다.
  - **Computation Logic**: (**W_L**, **W_H**)를 통해 ternary weight의 \{-1, 0, +1\} state를 표현하고, Input Activation은 wordline을 통해 입력된다. **W**가 High이고 **RWL**이 Low일 때, 즉 **IA**가 ‘1’인 상태에서 **RBL**에 current가 흐른다. 각 complementary cell pair에서 **IA**와 **W**의 multiplication이 발생한다. 또한 여러 4T-2C cell이 **RBLL/RBLR**을 공유하기 때문에 각 cell의 multiplication result가 **RBL**에서 accumulate된다. 따라서 current-based operation으로 볼 수 있다.
  - **Benefits**: 일반적인 1T-1C DRAM과 달리 **RBL**과 **WBL**을 분리하여 non-destructive read path를 구현한다. **RBL**을 computing datapath로 활용할 수 있고, SA의 동작도 줄일 수 있다.
  - **Challenge**: 각 cell의 current mismatch가 연산 결과에 반영되어 accuracy가 낮아질 수 있다. Memory density는 1T-1C DRAM-CIM보다 낮지만 SRAM-CIM보다는 높다.
  이러한 문제를 보완하기 위해 논문에서는 여러 구조를 제시한다.

<figure><img src="/images/papers/cim-dram-nvm/02.png" alt="원 논문의 그림" loading="lazy" decoding="async"></figure>

- **Figure.2(b)**
  - **Main Structure(Components)**: Voltage clipper를 사용한다.
  - **Computation Logic**: Voltage clipper가 각 **RBL**의 voltage를 미리 정해진 값으로 제한한다. 이후 charge sharing을 통해 각 column(**RBL**)의 결과를 accumulate한다.
  - **Benefits**: Voltage clipper를 통해 current mismatch로 인한 error를 줄일 수 있다.
  - **Challenge**: Row parallelism을 활용하지 못하고 column parallelism만 활용한다. Accuracy는 크게 향상되지만, row parallelism을 사용하지 못하기 때문에 latency가 증가할 수 있다.
- **Figure.2(c)**
  - **Main Structure(Components)**: **RBL**을 여러 row segment로 나누는 구조이다.
  - **Computation Logic**: 각 segment에서 1-bit multiplication을 수행한다. 이후 charge sharing을 통해 각 segment의 **RBL**에 나타난 결과를 accumulate한다.
  - **Benefits**: Row parallelism을 활용할 수 있다.
  - **Challenge**: Leakage, coupling 등으로 인한 computation error가 존재한다. 이러한 common-mode error를 제거하기 위해 추가적인 reference cell array가 필요하다.
- **Figure.2(d)**
  - **Main Structure(Components)**: 3T cell 구조이다.
  - **Computation Logic**: 하나의 capacitor에 analog voltage로 4-bit weight를 저장한다. Q1 transistor는 capacitor에 저장된 analog voltage에 따라 동작하며, weight에 대응하는 양의 current를 흘린다. Q2 transistor는 4-bit **IA**를 pulse width, 즉 turn-on time으로 전달받는다. 따라서 current-time multiplication을 통해 4-bit weight와 4-bit **IA**의 multiplication을 수행할 수 있다.
  - **Benefits**: 4b-4b multiplication을 수행할 수 있다.
  - **Challenge**: 하나의 capacitor에 4-bit weight를 저장해야 하기 때문에 큰 capacitor가 필요하다. Leakage와 noise의 영향에도 올바른 analog weight 값을 구별할 수 있어야 하기 때문이다. 또한 current-based operation은 transistor의 non-linearity와 variation으로 인해 accuracy가 제한된다.
- **Figure.2(e)**
  - **Main Structure(Components)**: 3T-2C cell 구조이다.
  - **Computation Logic**: Cell 내부에서 multiplication logic의 voltage domain을 분리한다. Multiplication은 digital domain에서 수행하고, 각 cell의 결과는 **RBL**에서 accumulate한다.
  - **Benefits**: Voltage domain을 분리하여 capacitor의 leakage가 1-bit multiplication에 영향을 주지 않도록 한다. 또한 Fig.2(d)와 비교했을 때 큰 capacitor가 필요하지 않기 때문에 cell density를 높일 수 있다.
  - **Challenge**: 하나의 cell에서는 1-bit multiplication만 수행한다.

### 4.2 NVM-CIM
{: #section-9 }

<columns>

  <column ratio="50">
    

<figure><img src="/images/papers/cim-dram-nvm/03.png" alt="원 논문의 그림" loading="lazy" decoding="async"></figure>

  </column>
  <column ratio="50">
    

<figure><img src="/images/papers/cim-dram-nvm/04.png" alt="원 논문의 그림" loading="lazy" decoding="async"></figure>

    
  </column>

</columns>

#### 4.2.1 Current-Based Operation with Complementary cell
{: #section-10 }

- **Figure.3(a)**
  - **Main Structure(Components)**: 1T-1R cell 한 쌍으로 구성된다.
  - **Computation Logic**: 1T-1R cell 한 쌍을 이용하여 binarized (+1, -1) **W**와 **IA**의 연산을 구현한다. Weight 값에 따라 한 cell은 **LRS**, 다른 cell은 **HRS** state를 가진다. **IA** 값은 **WL**을 통해 입력된다. 따라서 resistance state(weight)와 **WL** state(**IA**)의 관계를 통해 **XNOR operation**이 구현되고, 그 결과가 **BL**에서 accumulate된다. Pull-up transistor와 cell resistance 사이의 voltage division에 의해 **BL** voltage가 결정된다.
  - **Benefits**: Parallelism을 활용하여 높은 efficiency를 얻을 수 있다.
  - **Challenge**: **BL**과 **PU**의 non-ideal resistance로 인해 **BL** voltage가 연산 결과에 대해 non-linear하게 나타난다. 따라서 flash **ADC**를 사용한다.
- **Figure.3(b)**
  - **Main Structure(Components)**: 4T-4R cell 구조이다.
  - **Computation Logic**: Fig.3(a)가 complementary **WL**만 사용했다면, Fig.3(b)는 complementary **BL**도 함께 사용한다. 두 **BL**의 differential voltage를 통해 linear한 출력을 얻을 수 있다. 또한 Fig.3(a)와 같은 두 개의 2T-2R cell로 재구성할 수 있다. 이 경우 density와 efficiency는 높아지지만 accuracy는 낮아진다. NN model의 요구사항에 따라 4T-4R 또는 두 개의 2T-2R mode를 선택할 수 있다.
  - **Benefits**: **ADC**를 통해 linear한 output을 sensing할 수 있다.
  - **Challenge**: 더 많은 transistor와 resistor를 사용하기 때문에 Fig.3(a)에 비해 memory density가 낮다.

#### 4.2.2 Time-Based operation
{: #section-11 }

- **Figure.3(c)**
  - **Main Structure(Components)**: Voltage-to-time converter(VTC), time-to-digital converter(TDC)를 사용한다.
  - **Computation Logic**: **BL**에는 미리 precharge된 parasitic capacitor가 존재한다. NVM cell을 통한 current가 **BL**을 discharge시키며, 이때 발생하는 analog voltage의 변화를 **VTC**를 통해 time domain으로 변환한다. 마지막으로 **TDC**를 통해 digital value로 변환한다.
  - **Benefits**: 연산 중 지속적으로 흐르는 DC current가 없어 더 높은 energy efficiency를 얻을 수 있다.
  - **Challenge**: 여러 converter를 사용하기 때문에 추가적인 peripheral circuit이 필요하다. **BL**의 discharge latency를 이용하는 sensing path와 **VTC**, **TDC** 등이 요구된다.

#### 4.2.3 Hybrid Method
{: #section-12 }

- **Figure.3(d)**
  - **Main Structure(Components)**: Single-level cell(**SLC**), multi-level cell(**MLC**)을 함께 사용한다.
  - **Computation Logic**: **SLC**와 **MLC**는 서로 다른 장점과 trade-off를 가진다.
    - **MLC**: Memory density와 efficiency가 높지만 signal margin과 accuracy가 낮다. 8-bit weight의 하위 6-bit를 저장한다.
    - **SLC**: Accuracy와 signal margin이 높지만 memory density와 efficiency가 낮다. 8-bit weight에서 더 중요한 상위 2-bit를 저장한다.
  - **Benefits**: **SLC**와 **MLC**를 함께 사용하여 throughput, efficiency, computing accuracy 사이의 균형을 맞출 수 있다. NN model의 요구사항에 따라 두 종류의 cell을 어떻게 활용할지 결정해야 한다.
  - **Challenge**: Weight bit를 **SLC**와 **MLC**에 나누어 저장하기 때문에 mapping과 control이 복잡해지고, area overhead도 발생할 수 있다고 생각했다.
  또한 **CIM–NMC hybrid method**에서도 비슷한 accuracy/efficiency trade-off를 확인할 수 있다. CIM은 throughput과 efficiency를 높이고, NMC는 computing accuracy를 높이는 역할을 한다.

---

## 5. Trade-offs and Limitations
{: #section-13 }

<table>

<tr>
<td markdown="span"></td>
<td markdown="span">Benefits</td>
<td markdown="span">Costs / Trade-offs</td>
</tr>
<tr>
<td markdown="span">**SRAM-CIM**</td>
<td markdown="span">안정적인 동작, 높은 accuracy</td>
<td markdown="span">Transistor overhead, 1 bit/cell로 제한되는 weight density, volatility</td>
</tr>
<tr>
<td markdown="span">DRAM-CIM</td>
<td markdown="span">높은 memory density</td>
<td markdown="span">Leakage/noise의 영향, destructive read(1T-1C), refresh overhead, computing accuracy 문제</td>
</tr>
<tr>
<td markdown="span">NVM-CIM</td>
<td markdown="span">Non-volatility</td>
<td markdown="span">Non-linearity, 낮은 signal margin, static current 문제, write 시 높은 voltage와 latency, computing accuracy 문제</td>
</tr>
</table>

기본적으로 cell array 내부에서 computation을 수행하면 data movement, SA overhead, latency를 줄일 수 있다. 또한 cell array 내부의 parallelism을 활용하여 efficiency를 높이고 latency를 낮출 수 있다. 그러나 그에 따른 trade-off도 존재한다. Analog domain에서 computation을 수행할 때 variation, leakage, non-linearity, signal margin 등의 문제가 발생하며, 이는 accuracy를 낮추는 원인이 된다.

## 6. My Thoughts
{: #section-14 }

**Computation(model) mapping을 어떻게 최적화할 수 있는지** 더 깊게 공부해보고 싶었다. 이 논문은 여러 문제를 해결하기 위한 구조적인 접근법을 주로 다룬다고 생각했다. Hybrid Method, 특히 Fig.3(d)를 보며 memory를 어떻게 할당해야 하는지 궁금했다. **SLC**와 **MLC** 두 종류의 cell이 있기 때문에 weight data를 이 둘에 나누어 저장해야 한다. Memory를 **SLC**와 **MLC**로 효과적으로 나누고 할당하는 방법이 있다면 더 알아보고 싶었다.<br>또한 hybrid approach가 NVM-CIM에서만 다루어진 이유도 궁금했다. DRAM-CIM에서도 서로 다른 cell, computation mode, sensing method를 조합하는 hybrid approach를 구현할 수 있는지 궁금했고, 이러한 방법을 활용한 기존 DRAM-CIM 연구가 있는지도 궁금하다. 그뿐만 아니라, 논문에서는 hybrid approach의 challenge, trade-off를 자세하게 설명하지 않는다. Hybrid architecture를 구현할 때 area, control, mapping, accuracy 측면에서 어떤 문제가 발생하는지도 더 알아보고 싶었다.
