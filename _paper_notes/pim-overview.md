---
title: An Overview of Processing-in-Memory Circuits for Artificial Intelligence and
  Machine learning
permalink: /paper-notes/pim-overview/
short_title: PIM Circuits Overview
paper_authors: Donghyuk Kim, Tony Tae-Hyoung Kim
paper_venue: IEEE Journal on Emerging and Selected Topics in Circuits and Systems
paper_year: 2022
paper_url: https://doi.org/10.1109/JETCAS.2022.3160455
note_updated: '2026-10-20'
note_status: complete
excerpt: 메모리 내부·주변 연산의 분류와 AMBIT, DRISA, Newton, HBM-PIM 등의 구조를 정리했습니다.
topics:
- Memory architectures
- PIM
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
  title: 4.1 SRAM-PIM
- depth: 2
  id: section-6
  title: 4.2 DRAM-PIM
- depth: 2
  id: section-7
  title: 4.3 ReRAM-PIM
- depth: 3
  id: section-8
  title: 4.3.1 State of the Art ReRAM based PIM
- depth: 3
  id: section-9
  title: 4.3.2 New Directions for ReRAM PIM Research
- depth: 2
  id: section-10
  title: 4.4 Software Stack
- depth: 1
  id: section-11
  title: 5. Challenge/Limitations
- depth: 1
  id: section-12
  title: 6. My Thoughts, Comments
---

# 1. Introduction
{: #section-1 }

> 이 논문은 Processing-in-Memory(PIM)가 연구되는 이유와 함께 현재까지 연구되어진 SRAM, DRAM, ReRAM 기반의 PIM을 포괄적으로 설명한다. 각 memory type을 사용했을 때에 따른 장점과, trade-off를 여러 관점에서 분석한다. 그 외에, hardware적 관점이 아닌 software적 측면에서 PIM architecture를 어떻게 발전시켜나갔는지도 서술한다.

---

# 2. Problem
{: #section-2 }

AI/ML의 MAC operation은 많은 data를 필요로 하며, conventional von-Neumann architecture에서는 이러한 data가 memory와 processor 사이를 반복적으로 이동한다. 이러한 많은 data communication은 높은 energy consumption을 발생시킨다.

현재 conventional von-Neumann architecture에서는 processing elements와 memory가 분리되어 있다. 이러한 문제를 해결하기 위해 PIM architectures가 연구되었고, 각 processing elements는 computing circuit과 memory의 역할을 동시에 수행할 수 있다. 그러나 SRAM, DRAM, ReRAM 기반의 PIM이 가지는 구조적 문제들이 많이 존재한다.

processing elements와 memory가 분리되어 있으면 processor가 매 연산마다 memory에서 huge data를 받아와야 하고, 이는 전력 측면에서 손실이 발생할 뿐 아니라 memory bandwidth에 따른 bottleneck, 즉 memory bound을 유발한다.

---

# 3. Core Idea
{: #section-3 }

SRAM, DRAM, ReRAM을 기반으로 한 PIM에서 제시된 여러 구조를 살펴본다. 각 구조에서 얻을 수 있는 benefits와 challenges를 전반적으로 확인할 수 있다. various operation을 어떤  circuit design을 통해 구현했는지 확인할 수 있다. Computation이 memory 내부와 가까워 질 수록, internal bandwidth를 극대화할 수 있지만 accuracy, area constraint 등의 trade-off가 발생한다. 반대로 accuracy를 높이기 위해서 새로운 bitline, logic 등을 추가하게 되면 area overhead가 발생한다. paper에서 어떤 특징을 높이기 위해, 어떻게 설계했고 trade-off를 줄이기 위해 어떤 idea를 제시했는지를 확인할 수 있다.

---

# 4. Architectures & Computation Methods
{: #section-4 }

## 4.1 SRAM-PIM
{: #section-5 }

<figure><img src="/images/papers/pim-overview/01.png" alt="원 논문의 그림" loading="lazy" decoding="async"></figure>

- **SRAM-based PIM cells**
  - **Computation Logic**:  기본적으로 <span class="math-inline" markdown="0">\(WL\)</span>을 통해 input data가 들어온다. SRAM의 각 cell(<span class="math-inline" markdown="0">\(Q_b\)</span>)에 weight가 저장되어 있다. 따라서 input(1/0)과 weight(1/0)의 multiplication result가 <span class="math-inline" markdown="0">\(BL\)</span>을 통해 표현된다. figure. 2(b)\~(d)에서는 read&write의 <span class="math-inline" markdown="0">\(BL\)</span>을 분리하였다. <span class="math-inline" markdown="0">\(RBL\)</span>에 multiplication result가 표현된다. fig. 2.(c)는 <span class="math-inline" markdown="0">\(Q, Q_b\)</span>각각에 <span class="math-inline" markdown="0">\(RBL\)</span>이 연결되어, weight 값을 +1/-1로 표현할 수 있고, fig. 2.(d)는 MOSCAP을 추가하여 residual analog non-idealities를 줄였다. 각 Bitline에 여러개의 cell이 연결되어 있고, cell 에서 multiplication이 발생하고, bitline에서 accumulation되는 공통적인 특징을 지닌다(이 특징은 PIM에서 많이 나타난다).
  - **Benefits**: fig.2.(a)는 기존 SRAM의 구조를 그대로 사용해서 memory density 가 다른 예시에 비해 높다. fig.2.(b)는 read&write bitline을 분리하였기에, read disturbance issue를 해결한다. fig.2.(c)는 weight를 다양하게 표현할 수 있어서 various MAC operation을 수행할 수 있다. 마지막으로 fig,2.(d)는 MOSCAP을 통해 residual analog non-idealities를 최소화할 수 있다. 
  - **Challenges** : 2.(a)는 read disturbance issue를 발생시킨다. 2.(a)\~(c) 모두 limited dynamic range, non-idealities issue 등이 존재한다. 2.(a)→2.(d)로 가면서 문제점들을 보완하고, 기능을 추가함으로 인해 area overhead issue가 크게 발생하게 된다.

<figure><img src="/images/papers/pim-overview/02.png" alt="원 논문의 그림" loading="lazy" decoding="async"></figure>

- **SRAM-based accumulation mode**
  - **Computation Logic**: 각 cell에서 multiplication이 발생하고, 이로써 발생하는 result를 column에 accumulate하는 방법을 크게 4가지로 분류하였다. 
  - **Benefits**: current-mode는 가장 단순하고 area도 많이 차지하지 않는다. voltage-mode는 pull-up, pull-down transistors를 이용하여 높은 dynamic range를 유지할 수 있다. 3.(c),(d)는 capacitor를 사용하여 high energy efficiency, throughput performance를 보인다.
  - **Challenge**: current mode → voltage mode → capacitor based mode로 갈 수록 area overhead가 증가한다. 그와 반대로 갈 수록 non-linearity issue가 크게 증가하고, dynamic range도 많이 제한된다고 생각했다.(My intuition)
  

<figure><img src="/images/papers/pim-overview/03.png" alt="원 논문의 그림" loading="lazy" decoding="async"></figure>

- **Digital SRAM PIM**
  - **Main Structure(Components)**: 6T SRAM, XNOR, 1-bit full adder
  - **Computation Logic**: multiplication&accumulation을 digital logic을 통해 처리한다.
  - **Benefits**: ADC/DAC overhead, PVT variation (Process, Voltage, Temperature), non-linearity issue 등을 해결할 수 있다. 
  - **Challenge**: memory, computation blocks로 인한 large unit PIM cell로 인하여 더 많은 area를 소비한다. 즉 memory density가 크게 줄어들게 된다.

## 4.2 **DRAM-PIM**
{: #section-6 }

- **Cell level DRAM-PIM**
  

<figure><img src="/images/papers/pim-overview/04.png" alt="원 논문의 그림" loading="lazy" decoding="async"></figure>

  - **Computation Logic**: 
    - Fig.6.(a)는 DRAM-Cell “C”의 state가 0일 때 AND operation, state가 1일 때 OR operation을 실행하는 DRAM-PIM이다. A,B,C transistor의 <span class="math-inline" markdown="0">\(WL\)</span>가 동시에 active(**TRA**:Triple Row Access)되며 operation이 실행된다. 
    - Fig.6.(b)는 DCC를 이용하여 NOT operation을 구현한다. Sense Amplifier의 inverted value를 DCC와 연결시킨다. n-wordline이 active되면 source에 저장된 state의 NOT operation이 된 값이 저장되고, d-wordline이 active되면 source의 state가 그대로 저장된다.
    - Fig.6.(c)는 3T-1C-NOR operation을 구현한다. 2개의 M3 transistor가 각각 wordline과 대응되고, M2 transistor는 capacitor에 저장된 state에 따라 activation이 결정된다. M2 transistor는 하나의 bitline을 공유하며, 한 개의 M2 transistor가 active되어도, bitline과 GND가 연결되어 bitline의 charge가 줄어들게 되고 이를 <span class="math-inline" markdown="0">\(SA\)</span>가 감지하는 방식을 통해 NOR operation이 구현된다.
    - Fig.6.(d),(e)는 logic gate를 <span class="math-inline" markdown="0">\(SA\)</span> 아래에 배치하여 특정 operation을 구현한다.
  - **Benefits**: cell 단위에서 operation을 구현하기 때문에 internal bandwidth를 극대화 한다.
  - **Challenge**: 6.(b)는 wordline 한 개를 더 추가해야 한다. 6.(d),(e)에서 logic gate를 cell pitch안에 추가하는 것이 area overhead를 유발하고, 물리적 한계도 존재한다. 전반적으로 특정 operation을 구현하기 위해 logic gate, line 등을 추가할 때 생기는 area constraint issue가 가장 큰 문제이다.
- **Bank level DRAM-PIM**
  

<figure><img src="/images/papers/pim-overview/05.png" alt="원 논문의 그림" loading="lazy" decoding="async"></figure>

  - **Main Structure(Components)**: 
    - Fig.7.(b) : 16 multipliers, 16 adders in a reduction tree, 16-bit accumulator register.
    - Fig.7.(c) :** PCU blocks**(interface unit, execution unit, register unit)** per two banks**, PIM controller
  - **Computation Logic**: 
    - Fig.7.(b) : 각 multiplier 마다 memory cell에서 column selector를 거쳐 나온 data의 값이 전달되고, 다른 하나는 모든 multiplier에 공통으로 모든 memory banks에 전달된 input vector이다. 이 두 개의 input operands가 각 multiplier에 전달된다. 이후, reduction tree를 거치며 accumulation이 일어난다.
    - Fig.7.(c) : PIM controller가 normal/PIM state를 조정한다. PIM state일 때 register unit의 **CRF**에 저장된 PIM instructions를 PCU가 실행한다.
  - **Benefits**: cell-level에서의 area constraint를 해결하기 위해, bank parallelism을 사용하여 internal bandwidth를 보완하였다.
  - **Challenge**: cell-level보다 낮은 internal bandwidth를 가진다.
- **3-d level DRAM-PIM**
  

<figure><img src="/images/papers/pim-overview/06.png" alt="원 논문의 그림" loading="lazy" decoding="async"></figure>

  - **Main Structure(Components)**: 3-d PIM은 bottom에 logic die, 그리고 stacked memories가 top에 배치된 구조이다. **HMC**는 16개의 **vault**로 구성된다.
    - Fig.8.(b): Neurocube는 logic die에서 각 vault마다 PNG, PE가 배치되어 있다.
    - Fig.8.(c): Tetris intergrates a PE array with a global buffer per vault.
    - i**PIM**: 3-d PIM과 bank-level PIM structure를 합친 구조이다.** **logic die에는 control core가, memory die에는 execution 역할을 하는 PG가 배치되어 있다.
  - **Computation Logic**: 기본적으로 memory dies와 logic die가 TSV를 통해 data communication을 한다.
    - Fig.8.(b): PNG는 vault controller를 이용하여 vault 내부의 데이터 접근 순서를 관리하고, PE에 데이터를 넘겨준다. PE에는 여러 개의 MAC이 병렬로 연결되어 연산을 돕는다. PE는 2-d mesh network structure를 통해 PE간의 inter communication이 가능하다.
    - Fig.8.(c): Tetris는 global buffer와 PE array structure를 추가함으로써 input data reuse를 극대화 한다.
    - **iPIM**: control core가 intra/inter-vault data communication을 관리하고 instruction decoding을 실시함으로써 **SIMB ISA**를 지원한다. memory die의 PG에서는 bank에서memory-bound operation을 실시해서 parallel execution을 극대화 한다.
  - **Benefits**: data communications을 logic die와 memory die 사이에 진행하여 energy-efficient, high bandwidth의 benefits을 가진다.
  - **Challenge**: 3-D stacked die의 strict physical/timing constraint 때문에 구현이 어렵고  Neurocube/Tetris/iPIM은 모두 simulation으로만 평가됐다.

## 4.3 **ReRAM-PIM**
{: #section-7 }

- **Current mode & Voltage mode**
  

<figure><img src="/images/papers/pim-overview/07.png" alt="원 논문의 그림" loading="lazy" decoding="async"></figure>

  - **Main Structure(Components)**: ReRAM-based PIM으로 fig.9.(a)는 current mode, fig.9.(b)는 voltage mode로 구현한다.
  - **Computation Logic**: 
    - current-mode: <span class="math-inline" markdown="0">\(V_{read} → SL,V_{REF}→BL, weight→G_{ij},IA(0,1)→WL\)</span>의 구조에서 weight와 Input vector의 multiplication의 결과가 bitline에서 accumulate되어 current source로 표현된다. 이후, current ADC를 통해 digital value로 변환된다.
    - voltage mode: <span class="math-inline" markdown="0">\(GND → SL,V_{pre}→BL, weight→G_{ij},IA(0,1)→WL\)</span>의 구조에서 bitline capacitor’s discharge가 input vector와 weight의 multiplication의 결과와 비례하다. 따라서 BL voltage를 통해 accumulated result를 측정할 수 있고, Voltage ADC를 통해 digital value로 변환한다.
  - **Benefits**: 
    - current-mode: **larger sensing margin,** faster sensing speed.
    - voltage-mode: only consume dynamic power
  - **Challenge**: 
    - current-mode: static current must be present for the entire sensing period → it leads poor energy efficiency.
    - voltage-mode: lower sensing margin.
    ⇒ Because ReRAM device has non-ideality issue, sensing margin이 더욱 중요하다. 따라서 sensing margin이 높은 current-mode가 주로 사용된다.
- **PIPW & SIPW**
  

<figure><img src="/images/papers/pim-overview/08.png" alt="원 논문의 그림" loading="lazy" decoding="async"></figure>

  - **Main Structure(Components)**: MSB: IN\[1\], LSB: IN\[0\]를 표현한다. 2-bit weight는 3개의 ReRAM device로 이루어진다. MSB 2개, LSB 1개로 구성된 이유는, 자리값을 표현하기 위함이다.
  - **Computation Logic**: 
    - **PIPW: **IN\[0\] → marco\[0\], IN\[1\] → marco\[1\]에 입력함으로써, two input bit를 동시에 처리한다. 이때, 두 marco는 같은 weight 값을 공유한다. (duplicated weight)
    - **SIPW: **하나의 marco에 two input bit를 순차적으로 입력한다. IN\[0\]의 연산 결과는 capacitor를 통해 저장되고, 그 뒤의 연산과 합쳐진다.
  - **Benefits**: 
    - **PIPW: **여러 marco에서 input bit를 빠르게 병렬 연산을 한다.
    - **SIPW: **marco를 적게 써서 area의 이득을 본다.
  - **Challenge**: Both of them have large BL current-distributions on the read path issue. To improve MAC accuarcy → PIPW, SIPW에서 발생한 current를 merge하는 extra circuits가 필요하다.
- **Ternary weight in ReRAM**
  

<figure><img src="/images/papers/pim-overview/09.png" alt="원 논문의 그림" loading="lazy" decoding="async"></figure>

  - **Main Structure(Components)**: There are two array ; Positive array, Negative array
  - **Computation Logic**: Positive array에서는 weight “+1”을 LRS로, “0”을 HRS로 표현하고, negative array에서는 weight “-1”을 LRS로, “0”을 HRS로 표현한다. 최종 ternary multiplication 결과는 positive array와 negative array에서 생성된 current를 결합하여 얻는다.
  - **Benefits**: \{-1,0,+1\} 총 3가지의 state를 표현할 수 있다.
  - **Challenge**: “+1”에 해당하는 analog current 값은 <span class="math-inline" markdown="0">\(I_{LRS}\)</span>에 해당한다. 그리고 “0”에 해당하는 값은 <span class="math-inline" markdown="0">\(I_{HRS}\)</span> or “**no current**”이다. One column에 9개의 cell이 연결되어 있다고 하자.  이때 만약 어떤 column에서 “+1”라는 값이 도출되었을 때, **BL current**는 <span class="math-inline" markdown="0">\(I_{LRS}\)</span> \~ <span class="math-inline" markdown="0">\(I_{LRS}+8I_{HRS}\)</span> 의 범위로 표현된다. 이러한 **BL current distribution**으로 인해 sensing margin이 낮아진다. 

### 4.3.1 State of the Art ReRAM based PIM
{: #section-8 }

1. 더 복잡한 ML algorithms and datasets의** **accuracy requirement를 만족할 수 있는 PIM을 요구한다. (더 높은 MAC precision을 요구한다)
2. ReRAM-based PIM은 NN models accelerating만 많이 연구되었다. 다양한 종류의 ML algorithms에 대한 연구가 아직 많이 남아있다.
3. 현재는 Analog ReRAM이 가지는 장점보다 단점(large device variation)이 더 크게 느껴져서, Digital ReRAM이 더 선호된다. 그러나 device가 발전함에 따라 area cost에 이점이 있는 Analog ReRAM이 선호될 가능성이 높다.

### 4.3.2 New Directions for ReRAM PIM Research
{: #section-9 }

⇒ ReRAM PIM Research에 새로운 방향을 paper에서 크게 3가지 제시한다.

1. **ReRAM coprocessor**: 단일 marco가 아닌 full computing system으로 발전해나가는 것
2. **Security & Reliability**
3. **Versatile PIM functions**: MAC뿐만 아닌 다양한 Boolean logic도 지원

## 4.4 Software Stack
{: #section-10 }

- **PIM software stack**
  - **Main Structure(Components)**: PIM framework, PIM library, PIM runtime, PIM device driver
  - **Computation Logic**: 
    - **PIM framework**: 다양한 custom operation을 구현할 수 있도록 정의
    - **PIM library**: custom operation의 요청에 응답하는 low-level routines. Basic linear algebra subprograms (BLAS)을 사용한다.
    - **PIM runtime**:
      - PIM framework를 최적화 -\> 어떤 operation을 PIM으로 offload할지 결정하고 어떤 instructions가 발생될지 조정
      - PIM instructions, operand data의 memory usage를 조정
      - PIM instruction에 맞는 PIM kernel을 구성
    - **PIM Device Driver**: PIM operation을 위한 memory space를 실제로 할당**<br>**
- **PIM Offloading Execution**

    &#58; 어떤 operation이 PIM을 통해 효율적으로 연산될 수 있는지 결정하는 것이 중요하다.<br>PIM-friendly operations을 구별하고, 알맞는 operations을 PIM에 offloading 해야 한다.

  - **specialized PIM logic (can only execute specific operations)**

      &#58; specialized PIM logic은 수행 가능한 operation이 제한되어 있어서 어떤 operation이 PIM-friendly인지 판단하기 쉽다.

  - **PIM logic with general-purpose cores**

      &#58; General-purpose PIM core에서는 다양한 operation을 실행할 수 있기에 어떤 operation을 PIM에 offload해야 할지 판단하기 어렵다. 이때, PIM은 ‘low data locality’를 가지는 memory-intensive operation을 PIM-friendly로 선정할 수 있다. (이를 판별하는 4단계의 방법이 제시되었다.)

      ⇒ low data locality이기 때문에, data를 off-chip memory에서 가져와도 reuse를 못해서 data movement cost가 크다. 이러한 operation은 PIM에 유리하다.
- **Data mapping**
  - **DRAM-based bank-level PIM**

      &#58; 연산에 사용되는 data가 **같은 bank에 존재**하여 global bus의 사용량을 줄이고, 같은 bank에 data가 함께 존재해도, **같은 row에 data가 존재**하여 연속적으로 읽으면, 다른 row의 data를 읽을 때 발생되는 precharge, activation commands 등으로 발생하는 additional delays를 줄일 수 있다. \*memory access pattern을 보고 자동으로 memory mapping해주는 mechanism도 연구되었다.

  - **ReRAM-based PIM**

      &#58; CNN에서 3D kernels를 여러개의 1 x 1 x D matrics로 쪼개고 각각을 서로 다른 PIM PE에 배치하는 방법이 있다. 이 방법은 PE들 사이의 internal data movement를 활용하여 weight와 input data reuse를 최대화할 수 있다.

- **PIM execution scheduling**
  - **Load balancing**

      &#58; 많은 offloaded executions가 PIM 쪽에 queueing되면 GPU–PIM 간 load imbalance가 발생할 수 있다. 이 경우 GPU가 PIM의 queue가 처리될 때까지 기다리게 되어 전체 system performance가 저하될 수 있다.

  - **Channel balancing**

      &#58; RX/TX channel utilization의 불균형을 방지하기 위해 pending offloading request의 수와 RX/TX bandwidth utilization rate에 threshold를 설정하고, threshold에 도달하면 추가적인 PIM offloading을 제한한다.

  - **Concurrent execution scheduling**

      &#58; Kernel dependency information, affinity prediction model, execution time prediction model을 이용하여 어떤 kernel들을 병렬로 실행할 수 있는지, 어떤 computation core에서 실행하는 것이 적절한지, 실행 시간이 얼마나 걸릴지를 판단하여 GPU와 PIM을 효율적으로 동시에 활용한다.

- **Cache coherence**
  - **Coherence for Near Data Accelerators (CoNDA)**

      &#58; CPU와 DRAM-based 3-D PIM 사이의 cache coherence를 효율적으로 관리하기 위한 방식이다. CoNDA에서는 PIM이 optimistic execution mode 동안 coherence request를 발생시키지 않고 연산을 수행한다. 대신 PIM read, PIM write, CPU write가 발생한 memory address를 추적한다. 이 동안 modified data는 memory에 바로 반영하지 않는다. 이후 PIM execution이 끝나면 기록된 정보를 바탕으로 updated shared data에 대해서만 coherence를 처리한다. 이는 PIM 연산 중 발생하는 불필요한 coherence request를 줄이는 효과를 보인다.


---

# 5. Challenge/Limitations
{: #section-11 }

- **Data Converter Overhead**
  Analog CIM에서 in-memory computation을 수행하기 위해서는 digital input을 analog domain으로 변환해야 하며, MAC operation 이후 analog output을 다시 digital domain으로 변환해야 한다. 이때 DAC와 ADC가 필요하다.
  CIM의 특성을 활용하여 off-chip data movement를 줄여 von-Neumann bottleneck을 완화했지만, on-chip 내부에서 발생하는 data converter overhead issue가 남아있다. high-performance & high-density로 구성된 memory array에 DAC/ADC(extra circuits)을 추가함으로써, memory design parameter의 악화 및 unintended area/power overhead가 발생한다.
  이 문제를 해결하기 위해 기존 memory/peripheral resources를 최대한 재사용하는 방법이 중요하다. \[59\]처럼 기존의 eDRAM bitcells, inherent charge share operation을 활용하여 data converter의 기능을 할 수 있게 하는 방법은 area overhead를 줄인다. 또한, DAC/ADC의 precision을 낮추는 방법을 통해서도 area/power overhead를 줄일 수 있지만 accuracy와의 trade-off를 고려해야 한다.
- **Test Accuracy**
  Ideal software model과는 달리 실제 CIM에서는 non-linearity 등의 issue로 인해 accuracy drop이 발생할 수 있다. 이를 해결하기 위해 hardware calibration과 network retraining 기법을 활용할 수 있다. 실제로 이 두 기법을 활용했을 때 test accuracy가 software accuracy에 매우 가까워지는 것을 확인할 수 있다.
- **Intra-Memory Data Movement**
  CIM은 off-chip data movement를 최소화하여 data movement energy를 줄인다. 그러나 data duplication과 extra intra-memory data movement로 인해 extra energy consumption이 발생할 수 있다. 특히 conventional im2col-based algorithm에서는 input data의 duplication으로 인해 cache/bandwidth usage가 증가할 수 있다. 이를 해결하기 위해 matrix lowering scheme과 direct convolution algorithm 기법이 사용될 수 있다.
  - Direct convolution은 neighboring SRAM bit-cells의 data를 recycle하여 extra data duplication 및 intra-memory data movement를 최소화한다.

# 6. My Thoughts, Comments
{: #section-12 }

“An Overview of Processing-in-Memory Circuits for Artificial Intelligence and Machine Learning”을 통해 memory type에 따른 다양한 PIM structure, operation method, benefits, challenges, trade-off 등을 알 수 있었다. 또한 hardware의 관점뿐만 아니라 software의 관점에서도 PIM을 바라볼 수 있었고, 이를 통해 software와 computer architecture에 대한 추가적인 학습이 필요하다는 점을 느꼈다.

특히 PIM은 하나의 정해진 구조를 가지는 것이 아니라, processing logic을 memory hierarchy의 어느 level에 배치하는지에 따라 매우 다양한 structure로 구현될 수 있다는 점이 인상적이었다. DRAM만 보더라도 cell-level, bank-level, 3-D level과 같이 processing logic을 integration하는 위치에 따라 서로 다른 benefits와 trade-off가 나타난다. 또한 이러한 다양성은 DRAM에만 한정되지 않고 SRAM, ReRAM과 같이 서로 다른 memory type에서도 각 memory의 특성에 맞는 다양한 PIM architecture와 computation method로 확장될 수 있다.

이를 통해 PIM 연구에서는 processing logic을 어느 위치에, 어떤 방식으로 추가할지, 어떤 memory type과 computation method를 선택할지 등 다양한 design을 고려할 수 있으며, 그만큼 여러 방향의 연구를 시도할 수 있다고 느꼈다. 

최근 삼성전자에서 공개한 “LPDDR5X-PIM”를 비롯하여 SK Hynix의 ”AiM” 역시 PIM 기술이 활용된 메모리이다. 실제 PIM 기술이 산업에서 어느정도로 사용되고 있고, 어떤 방식으로 processing logic을 integration 하고 있는지, 어떤 PIM structure를 채택하여 생산하고 있는지 궁금하다.
