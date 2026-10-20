---
title: A Survey on Deep Learning Hardware Accelerators for Heterogeneous HPC Platforms
permalink: /paper-notes/accelerator-survey/
short_title: DNN Accelerator Survey
paper_authors: Cristina Silvano et al.
paper_venue: ACM Computing Surveys
paper_year: 2025
paper_url: https://doi.org/10.1145/3729215
note_updated: '2026-10-20'
note_status: complete
excerpt: GPU·TPU·ASIC과 PIM/CIM의 설계 전략을 데이터 이동, sparsity, energy efficiency 관점에서 연결했습니다.
topics:
- Survey
- AI Accelerator
- PIM / CIM
note_toc:
- depth: 1
  id: section-1
  title: 1. Introduction
- depth: 1
  id: section-2
  title: 2. Accelerators
- depth: 2
  id: section-3
  title: 2.1 GPU-based accelerators
- depth: 2
  id: section-4
  title: 2.2 TPU-based accelerators
- depth: 2
  id: section-5
  title: 2.3 Hardware Accelerators
- depth: 3
  id: section-6
  title: 2.3.1 FPGAs
- depth: 3
  id: section-7
  title: 2.3.2 ASICs
- depth: 3
  id: section-8
  title: 2.3.3 Accelerators for Sparse Matrices
- depth: 2
  id: section-9
  title: 2.4 Accelerators Based on Emerging Technologies
- depth: 3
  id: section-10
  title: 2.4.1 Processing-in-Memory(PIM)
- depth: 3
  id: section-11
  title: 2.4.2 In-Memory Computing(IMC, CIM)
- depth: 3
  id: section-12
  title: 2.4.3 Neuromorphic Accelerators
- depth: 1
  id: section-13
  title: 3. Thought & Summary
---

# 1. Introduction
{: #section-1 }

High-Performance Computing(HPC)의 발전으로 더 많은 데이터를 빠르게 처리할 수 있게 되면서, 더 복잡한 AI model의 학습과 실행도 가능해졌다. 이 논문은 CPU, GPU뿐만 아니라 TPU, FPGA, ASIC, NPU, 그리고 PIM과 non-volatile memory 기반 IMC(CIM) 등 다양한 AI accelerator의 구조와 접근법을 다룬다. 각 accelerator의 특징과 핵심 아이디어를 살펴보고 기존 연구 사이의 연관성을 파악함으로써, AI accelerator의 전반적인 발전 흐름과 performance 및 energy efficiency를 높이기 위한 여러 전략을 이해할 수 있다.

<figure><img src="/images/papers/accelerator-survey/01.png" alt="원 논문의 그림" loading="lazy" decoding="async"></figure>

# 2. Accelerators
{: #section-2 }

## 2.1 GPU-based accelerators
{: #section-3 }

GPU는 많은 연산을 동시에 수행할 수 있다. Training뿐만 아니라 ML operation을 상당히 가속할 수 있다. GPU의 성능을 측정할 때 크게 theoretical peak performance, memory bandwidth를 고려한다. 그러나 실제 “final performance”를 확인하기 위해서는 특정 workload를 시행해서 성능을 직접 측정해야 한다. 이때 사용되는 benchmark가 ”MLPerf”이다.

NVIDIA, AMD, Intel 모두 GP-GPU architectures를 개발한다. 이들의 hardware 특징은 유사한 점이 많으나, terminology는 차이가 있다. NVIDIA는 Single Instruction Multiple Thread(SIMT)를 사용하고 AMD, Intel은 SIMD를 사용한다.

  - SIMT: 한 번에 여러 Thread를 묶어서 공통된 instruction을 수행하는 것
    - Thread: 특정 연산을 수행하는 하나의 작업 단위
  - SIMD: 여러 data들이 같은 Instruction을 수행하는 것

Table 3의 결과를 통해 trade-off에 대해 생각할 수 있다. 

첫 번째로, 각 회사의 GP-GPU의 성능을 보면 Precision을 Double → Single로 낮췄을 때 performance가 증가한다. 이를 통해 performance를 높이는 방법으로 precision을 줄이는 방법을 생각할 수 있고, DL workload에서 요구하는 precision을 잘 찾아서 높은 성능, 괜찮은 수준의 accuracy를 만족하는 접근을 생각할 수 있다. 

두 번째로, Memory bandwidth가 높을수록 전체적인 performance가 좋다. 그러나 trade-off로 power consumption이 높아진다는 특징이 존재한다. 높은 성능을 요구할수록 그에 따라 더 높은 power가 요구된다는 사실을 확인할 수 있다.

마지막으로, 높은 성능을 위해 많은 core를 병렬 처리하게 되면 energy efficiency가 줄어들게 된다고 명시한다.

지금의 trade-off에 대한 내용은 GPU에 국한된 것이 아닌, 전반적인 accelerator에서 거의 공통되게 나타나는 특징이라 생각한다. 이러한 관점을 바탕으로 특정 accelerator가 어떤 목적을 달성하기 위해 무엇을 희생했는지 볼 수 있을 것이다.

## 2.2 TPU-based accelerators
{: #section-4 }

<p class="related-note"><a href="/paper-notes/tpu/">TPU — Paper Note ↗</a></p>

(위 링크는 이전 TPU v1 paper를 읽고 정리한 내용이다.)

TPU v1은 inference-oriented design이었다. 실제 논문에서도 domain-specific for inference를 위해 설계되었다고 한다. 그러나 TPU v2, TPU v3로 넘어가면서 inference, training 모두 지원한다. 이를 위해 BF16 floating-point 형식을 사용한다. 또한 기존 TPU v1의 256<span class="math-inline" markdown="0">\(\times\)</span>256 systolic array에서 4배 정도 작아진 128<span class="math-inline" markdown="0">\(\times\)</span>128 크기의 systolic array로 변화하였다(underutilize되는 경우를 완화하기 위해). 그 외에도, TPU v1의 20x가 넘는 off-chip memory bandwidth를 가진다. 아래 표를 통해 차이를 구분하였다.

<table>

<tr>
<td markdown="span"></td>
<td markdown="span">**TPU v1**</td>
<td markdown="span">**TPU v2, TPU v3**</td>
</tr>
<tr>
<td markdown="span">Target workload</td>
<td markdown="span">**Inference**</td>
<td markdown="span">**Training, Inference**</td>
</tr>
<tr>
<td markdown="span">Precision</td>
<td markdown="span">8-bit integer</td>
<td markdown="span">**BF16 floating-point**</td>
</tr>
<tr>
<td markdown="span">Systolic array size</td>
<td markdown="span">256<span class="math-inline" markdown="0">\(\times\)</span>256 systolic array 사용</td>
<td markdown="span">칩당 두 개의 core가 한 개 또는 두 개의 128<span class="math-inline" markdown="0">\(\times\)</span>128 systolic array 사용</td>
</tr>
<tr>
<td markdown="span">Memory Bandwidth</td>
<td markdown="span">30 GiB/s</td>
<td markdown="span">TPU v1의 대략 20배 이상</td>
</tr>
</table>

Habana Labs and Intel의 accelerators인 “Goya”, “Gaudi”에 대한 설명을 간단하게 한다. 

Goya는 GEMM engine, TPU(TPC), DDR4 등으로 구성된다. 몇 가지 특징을 살펴보자면, (아래 사진은 Goya의 architecture를 간단히 나타낸 것이다.)

<figure><img src="/images/papers/accelerator-survey/02.png" alt="원 논문의 그림" loading="lazy" decoding="async"></figure>

먼저 TPU의 local memory가 hardware, software에 의해 둘 다 관리될 수 있다. Software에 의해 관리된다는 의미는 프로그램의 종류, 특징에 따라 효율적으로 data movement를 설정하여 최적화할 수 있다는 뜻이다. 

또한 TPU는 mixed-precision operation을 통해 workload에 맞는 precision을 제공하여 accuracy를 비슷하게 유지하며 performance, energy-efficiency를 높인다.

Goya는 inference를, Gaudi는 training을 주요 대상으로 한다. Gaudi는 Goya에 사용된 TPC를 발전시키고, HBM과 BF16 지원 등 training을 위한 기능을 강화하였다.

또한 뒤에 소개되는 Graphcore의 Mk1, Mk2 IPU는 high power-efficiency, cost-efficiency memory hierarchy의 전략을 사용한다. 가격이 높은 HBM을 사용하는 것 대신 상대적으로 저렴한 DRAM과 많은 on-chip SRAM을 조합하여, off-chip memory access를 줄이는 방법을 채택한다.

그 외에도, IBM에서는 Hybrid-FP8 형식을 도입하여 workload에 따른 precision을 조합하는 방법을 소개한다. Bit 수를 낮추게 되었을 때 얻는 Bandwidth, cost, latency, performance 등의 이점을 가져가면서 accuracy는 비슷하게 유지하려는 접근이다.

이 section에서도 확인할 수 있는 점은, 앞서 다루었던 접근들이 유사하게 반복된다는 사실이다.

## 2.3 Hardware Accelerators
{: #section-5 }

<figure><img src="/images/papers/accelerator-survey/03.png" alt="원 논문의 그림" loading="lazy" decoding="async"></figure>

Fig.2를 통해 GPUs, ASICs, FPGAs의 performance, power consumption을 표현한다. Dashed-line은 energy-efficiency level을 의미한다. ASICs, GPUs는 높은 energy-efficiency를 보이는 동시에, high performance(throughput)을 가지는 경향이 있다. 그에 반해, FPGAs는 performance보다 낮은 power consumption을 우선하는 특정 inference tasks에 적합함을 확인할 수 있다.

<figure><img src="/images/papers/accelerator-survey/04.png" alt="원 논문의 그림" loading="lazy" decoding="async"></figure>

Hardware에서 발생하는 가장 큰 문제 중 하나는 off-chip DRAM access로 인해 발생하는 energy, latency cost이다. Fig.3는 off-chip DRAM access를 줄이기 위한 data reuse, stationary strategies이다. 크게 3가지의 전략으로 구성된다.

  1. Weight stationary dataflow

      &#58; weight가 PE의 local memory에 저장되고, external DRAM으로 부터 제공되는 activation에 재사용됨.

  2. Output stationary dataflow

      &#58; partial sum이 PE의 local memory에 저장되고, computation이 끝나기 전까지 생성되는 intermediate results를 local에 유지하며 사용함.

  3. Input stationary dataflow

      &#58; input activation을 PE의 local memory에 저장하여 재사용하고, weight가 external DRAM을 통해 PE에 공급됨.


특정 data를 local memory 근처에 두는 방법 외에도, 숫자를 표현하는 bit 수를 줄이는 quantization을 통해서도 data movement, memory capacity, computation cost 측면의 이점을 가질 수 있다. 그러나 precision을 낮추면 accuracy도 줄어들게 된다(trade off). 낮은 precision에서도 비슷한 accuracy를 얻기 위해 parameter, operation의 수가 2\~11배 정도 필요하다. 이는 복잡한 문제를 해결하는데 명확한 한계가 존재한다.

### 2.3.1 FPGAs
{: #section-6 }

What is FPGAs?

  FPGAs는 만들어진 hardware 내부에 computation 기능을 구현할 수 있는 장치가 있어서, 사용자의 설정을 통해 원하는 회로 동작을 구성할 수 있는 특징을 가진다. 즉, FPGAs는 특정 workload에 맞춘 computation structure를 구현할 수 있고, workload의 여러 요구에 대응하기 용이한 장점을 가지고 있다.
  FPGA 기반 accelerator는 크게 3가지로 구성된다
    1. General-purpose processor

        &#58; software workload를 시행하는 역할

    2. Computational module

        &#58; DL operations을 담당한다.(convolution, pooling, softmax function)

    3. Memory hierarchy

        &#58; external DRAM과의 data movement를 효율적으로 구성하기 위한 장치.

  FPGAs는 edge application에서 주로 사용되었지만, 경우에 따라 datacenter에서도 사용된다. 최근 이러한 FPGAs의 throughput을 높이며 최적화 하기 위한 연구가 관심을 받고 있으며, CGRAs 라는 대안이 소개된다.

**What is CGRAs?**

  FPGAs 처럼 computation에 맞춰서 구성을 바꿀 수 있다. CGRAs는 word-level arithmetic, logic, memory operation을 수행하는 PE array가 reconfigurable하게 연결되어 있는 특징을 가진다. PE 사이의 dataflow를 workload에 맞게 변경하여 원하는 computation을 구성할 수 있다.
  CGRAs는 PE 사이의 경로를 수정하기에 FPGAs 보다 회로를 재구성하는데 사용되는 비용이 작고, workload에 맞는 dataflow를 더 빠르고 효율적으로 수정할 수 있다.
  그러나 CGRAs의 PE가 “word-level”이기 때문에 word-level에 맞지 않는(더 적거나 더 많은 bit사이의 연산) workload를 구현하기 어려울 수 있다. 즉 FPGAs에 비해 회로를 수정할 수 있는 자유도가 낮다.

### 2.3.2 ASICs
{: #section-7 }

이 section은 다양한 종류의 ASICs에 대한 설명이 담겨 있다.

NPU는 크게 두 가지 분류로 나눌 수 있다.

  1. Single-chip NPUs
  2. NPUs integrated in the general purpose CPU
    ⇒ CPU가 처리하는 AI task를 NPU에 offloading하는 방식이다.
  NPU는 DNNs의 CONV, FC layer의 계산을 위해 적절한 양의 PE가 배치된 형태로 구성된다. PE 내부는 weight buffer, MAC units 등으로 구성되어 있으며, 이를 통해 DL에 필요한 multiplication, accumulation, activation 등을 수행할 수 있다.

RRAM, PCM 등을 이용한 NVM의 in situ matrix-vector multiplication을 활용한 경우도 존재한다. Analog CIM의 개념 일부가 들어간 이 회로는 data가 input으로 들어갈 때(digital → analog), 그리고 output으로 나갈 때(analog → digital)만 data converter가 사용된다. 즉, intermediate results는 analog computation으로 이루어진다. 이러한 구조를 통해 높은 energy-efficiency를 가질 수 있다.

ASICs는 custom accelerator로서 dataflow(data reuse pattern)를 최적화하여 system efficiency를 높인다. 먼저 off-chip memory access를 줄이는 접근을 활용한 DianNao family에 속하는 DaDianNao, ShiDianNao의 특징을 살펴본다.

- DaDianNao

    &#58; on-chip eDRAM 안에 workload의 weight를 다 저장하고, input activation(neurons)을 이동시키는 방법을 채택한다. Weight stationary dataflow를 이용하여 data reuse를 활용한다. (아래 링크는 DaDianNao를 정리한 자료이다)

  

<p class="related-note"><a href="/paper-notes/dadiannao/">DaDianNao — Paper Note ↗</a></p>

- ShiDianNao

    &#58; CNN application을 대상으로 하며, weight sharing strategy를 사용한다. CNN parameters를 on-chip SRAM에 저장하여 off-chip DRAM access를 피한다.


다음 살펴볼 accelerator는 Eyeriss이다. 앞선 DianNao family는 off-chip DRAM access를 대부분 줄이고, 거의 모든 data(parameters)를 on-chip DRAM, SRAM에 옮기는 전략을 사용했다면, Eyeriss는 off-chip DRAM access를 비용을 포함하여 high throughput, high energy efficiency를 보여준다. Eyeriss에서 사용된 전략은 아래와 같다.

1. RS dataflow를 활용하여 CONV에서의 data reuse를 크게 활용한다.
2. NoC architecture가 multi-cast 방식으로 single cycle마다 정해진 PE에 data를 전달해준다.
3. Run-Length Compression(RLC)를 활용하여 memory bandwidth, capacity 등의 부담을 줄인다.
4. PE data gating을 통해 zero data에서 발생하는 불필요한 연산을 줄인다.

이에 대한 자세한 설명은, 아래 링크를 통해 확인할 수 있다.

<p class="related-note"><a href="/paper-notes/eyeriss/">Eyeriss — Paper Note ↗</a></p>

다음은 Orlando SoC이다. SRAM 기반의 CNN accelerator이다. 단순히 가속만 하는 것이 아닌 여러 기능이 집약되어 실제 application을 실행한다. ARM-based host subsystem이 포함되어 software를 관리하고, chip-to-chip multilink, high I/O interfaces로 구성되어 외부와의 통신까지 전방위적으로 다루는 특징이 존재한다. 하나의 chip에서 acceleration, storage, software, communication을 수행한다는 점을 주목할 수 있다.

IBM에서 소개하는 AI accelerator는 training, inference를 위해 설계되었다. Training을 효율적으로 구현하기 위해 DLFloat16이라는 특별한 precision을 사용하였다. 그리고, systolic array와 SIMD engine을 같이 사용한다는 특징이 존재한다. 또한, 두 개의 corelet(작은 연산 단위)과 하나의 scratchpad memory(spad)가 연결된 구조로 이루어져 있다. 이러한 구조를 통해 scalability를 높일 수 있다. 데이터의 이동은 software를 통해 결정된다. 이에 이어서, 2022년에는 four-core-mixed-precision AI chip을 소개하는데, 이 chip은 4개의 core와 여러 개의 precision을 활용하여 training, inference를 low-precision으로 시행하되, accuracy의 감소는 거의 없게 구현한다. 

마지막 Qualcomm에서는 4-way VLIW architecture를 소개하였고, 이를 통해 instruction 차원에서도 performance를 끌어올리는 접근이 가능함을 알 수 있다.

이번 section을 통해, AI accelerator에서 energy efficiency를 높이는 관점 및 목적에 맞는 ASICs design 철학을 확인할 수 있었다.

### 2.3.3 Accelerators for Sparse Matrices
{: #section-8 }

Sparse Matrix는 “0”이 원소로 많이 존재하는 matrix이다. ”0” value를 더하거나 곱하여 누적해도 결과(partial sum)에 영향을 미치지 못한다. 따라서 “0” value에 해당하는 값들을 연산 과정에 참여시키지 않도록 하여 latency를 줄이고, energy-efficiency, performance를 높이는 전략을 소개한다.

처음 다루는 예시로는 앞서 언급했던 Eyeriss이다. Eyeriss에서는 크게 두 가지의 전략을 사용한다. 먼저, Compressed Sparse Columns (CSC)을 통해 data를 압축하는 기법이 있고, “0” value를 detect하는 buffer를 통해 “0” value인 data를 연산에 참여시키지 않게 하여 불필요한 switching을 막는 방법을 사용한다. 더 발전되어, Eyeriss v2에서는 CSC 기법을 메모리에 저장하고 불러오는 과정에만 사용하는 것이 아닌, 실제 computation process에서도 이 압축된 데이터를 활용하는 특징을 가진다. 

\*이 내용은 Eyeriss paper review에 언급되어 있으며, 원문에서는 Run-Length Compression을 설명한다. 

<p class="related-note"><a href="/paper-notes/eyeriss/">Eyeriss — Paper Note ↗</a></p>

그 뒤로는 여러 architecture에서 sparsity를 활용한 사례를 설명한다.

<table>

<tr>
<td markdown="span">Architecture</td>
<td markdown="span">Sparsity 활용 방법</td>
</tr>
<tr>
<td markdown="span">**Cnvlutin**</td>
<td markdown="span">Activation을 압축하고, skip 한다</td>
</tr>
<tr>
<td markdown="span">**Cambricon-X**</td>
<td markdown="span">PE가 CSR format으로 압축된 weight를 저장하고, computation 실행</td>
</tr>
<tr>
<td markdown="span">**EIE**</td>
<td markdown="span">Compress weight + 0 activation skip</td>
</tr>
<tr>
<td markdown="span">**NullHop**</td>
<td markdown="span">CIS 기법으로 weight 압축 + 0 activation skip</td>
</tr>
</table>

SCNN은 CSR format을 통해 weight, activation sparsity를 둘 다 활용한다. 또한, Cartesian product-based computation 활용하여 효율을 높인다. 이 방법은 activation과 weight의 묶음으로 만들 수 있는 multiplication을 전부 나열하고(data reuse) 여기서 나온 값들의 output 위치를 구분하여 적절한 위치로 보내는 방식이다.

다음으로는, sparse matrix의 특징을 활용하는 task를 여러 PE에 균등하게 분배하여 PE load imbalance를 줄이는 관점이 소개된다. Task를 여러 PE에게 균등하게 분배할 수 있도록 offline software scheme으로 해결하는 접근과 sparse matrix의 구조를 수정하여 해결하는 접근이 존재한다.

UCNN에서는 “0” 데이터를 활용하는 것 뿐만 아니라 반복되어 사용되는 nonzero weights를 활용한다. 같은 weight가 곱해진 여러 연산을 하나로 묶어서 computation을 줄이는 전략이다. 이를 통해 memory에 저장되는 model size를 줄인다.

그 뒤로는 sparse matrix를 활용하기 위한 dataflow, scheduling 기법, GPU에서 sparsity를 활용하는 방안 등이 소개된다.

이 section에서 얻을 수 있는 통찰은 sparse matrix의 특성 및 이를 어떻게 활용하여 성능 향상을 이루어낼 수 있는지에 대한 접근법이다. 단순하게 ‘압축한다’, ‘skip 한다’ 가 아닌, 만약 특정 상황에서 sparsity를 활용하고 싶을 때, 

  - weight와 activation 중 어떤 값을 선택하여(혹은 둘 다) compression, skip을 할지, 
  - 반복되는 특정 weight를 한 번에 묶을지, 
  - 이렇게 처리된 데이터를 어떻게 load imbalance 없이 PE에게 분배할지, 
  - Sparse matrix에 pattern을 부여하거나, 특정 dataflow를 설계할지,

등의 사고로 확장해 나갈 수 있었다.

## 2.4 Accelerators Based on Emerging Technologies
{: #section-9 }

Off-chip memory access를 줄이기 위한 노력이 상당히 많이 이루어졌음을 앞서 여러 section을 통해 확인할 수 있다. 이는 곧 높은 성능을 내기 위해서는 process(computation) modules와 memory architecture를 함께 설계하여 최적화하는 것이 필연적임을 의미한다. 결국 이 section에서 설명하는 내용도 유사하다. DNN operation을 수행할 때 발생하는 상당한 data movement로 발생하는 cost를 어떻게 줄일 것인지, latency는 어떻게 낮출 것인지, energy-efficiency는 어떻게 높일 것인지의 관점으로 보면 된다. 그러나 앞선 section과의 차이점은 “memory”에 집중하여 이를 해결하려고 한다는 점이다.

### 2.4.1 Processing-in-Memory(PIM)
{: #section-10 }

PIM의 기본 원리는 간단하다. Computation을 memory(DRAM) 내부 혹은 근처에서 실행하는 것이다. 이를 통해, DRAM의 internal bandwidth를 활용하여 더 높은 수준의 병렬 연산을 가능하게 하고, host와 memory 사이의 data transfer의 부담을 줄이는 등의 이점을 가진다. DRAM의 어느 영역에서 computation이 실행됨에 따라 PIM은 크게 3가지로 분류할 수 있다.

1. In-subarray(Cell-level) PIMs

    &#58; 연산이 local sense amplifiers에서 발생

2. Bank-level PIMs

    &#58; column decoder 이후 단계에서 연산이 발생(memory bank에 logic 존재)

3. Logic-die level PIMs

    &#58; 3D-stacked memory block의 logic die에서 연산이 발생


<figure><img src="/images/papers/accelerator-survey/05.png" alt="원 논문의 그림" loading="lazy" decoding="async"></figure>

Fig. 6에서 PIM이 어떻게 분류되는지 더 자세하게 확인할 수 있다. 

In-subarray PIMs 중 인상 깊었던 것은 PIM-DRAM이다.

  이 survey에서 소개되는 PIM-DRAM은 in-subarray에서 multiplication을 수행하고, accumulation과 activation function은 bank에서 수행되는 특징이 있다. 이를 통해 하나의 구조에서도 연산의 종류에 따라 level을 달리 두는 접근도 가능함을 확인할 수 있다.

다음으로는 logic die-level PIMs를 다룬다. 여러 PIMs가 소개되었지만, 근본이라고 볼 수 있는 Neurocube, Tetris architecture와 인상 깊었던 전략을 사용했던 NeuralHMC를 대표적으로 정리하였다.

  - Neurocube

      &#58; 16개의 vault로 이루어지며, 각 vault에 속한 logic die마다 PE(연산장치)와 PNG(data movement를 관리하는 장치)가 존재한다. 연산에 필요한 데이터들은 TSV, vault controller를 통해 logic die로 전달된다. Output stationary dataflow를 사용한다는 특징도 존재한다.

  - Tetris

      &#58; Neurocube와 유사하다. 그러나 data movement를 더 효율적으로 구성하였다. 각 vault에 속한 logic die에 14 <span class="math-inline" markdown="0">\(\times\)</span> 14 systolic PE array, small SRAM buffer가 존재한다. 또한 Eyeriss에서 언급되었던 row stationary dataflow를 활용하여 data reuse를 극대화한다는 특징이 존재한다.

  - NeuralHMC

      &#58; weight access로 발생하는 cost를 줄이기 위한 전략으로, 기존 FP32로 표현된 데이터를 온전히 주고받는 방법에서 5 or 8-bit cluster index 기법으로 변경하여 memory consumption을 줄인다.

      \*cluster index: 반복되는 weight에 고유 번호를 지정하여, weight의 정보를 주고받을 때 weight의 실제 값이 아닌, 고유 번호를 주고받음으로써 weight로 인한 부담을 줄이는 것이다.

마지막으로 bank-level PIM이다. Newton과 HBM-PIM이 예시로 등장하는데, 이 둘의 큰 차이점은 programmability이다. Newton은 fixed dataflow의 특징을 가진다. 이는 범용적인 계산에는 취약할 수 있으나, 특정 목적에 맞는 task에는 큰 효율을 보인다는 장점이 존재한다. 반대로 HBM-PIM은 function-in-memory DRAM으로 소개되며, 두 개의 bank마다 programmability를 제공하는 PCU가 포함된 구조이다.

<figure><img src="/images/papers/accelerator-survey/06.png" alt="원 논문의 그림" loading="lazy" decoding="async"></figure>

<p class="related-note"><a href="/paper-notes/pim-overview/">PIM Circuits Overview — Paper Note ↗</a></p>

각 PIM architecture의 logic의 구현 방법, 특징, trade-off, strategy 등은 위 정리를 통해 더 자세하게 확인할 수 있다. 앞서 설명이 부족했던 In-subarray PIMs의 AMBIT, DRISA, Bank-level PIMs의 Newton, HBM-PIM 그리고 Logic-die level PIMs의 Neurocube, Tetris 등을 더 자세히 확인할 수 있다.

### 2.4.2 In-Memory Computing(IMC, CIM)
{: #section-11 }

<p class="related-note"><a href="/paper-notes/pim-overview/">PIM Circuits Overview — Paper Note ↗</a></p>

<p class="related-note"><a href="/paper-notes/cim-dram-nvm/">CIM With DRAM and NVM — Paper Note ↗</a></p>

위의 두 정리는 더 자세한 CIM architecture 원리를 다룬다. 본 survey에서는 기본적인 접근, 전략 등에 대해 살펴본다.

CIM은 memory wall, compute wall을 모두 해결하기 위한 방안으로서, memory와 accelerator의 기술을 통합한다. 현재로서는 full-digital CIM이 실제 NPU같은 system에 함께 통합되기 수월하다고 말한다. 그 이유는 간단하다, analog computation이 가지는 문제점인 ADC/DAC issue, analog non-ideality 등의 문제 때문이다. 실제 digital 기반의 SRAM CIM은 높은 energy efficiency, area efficiency를 보인다.

다음으로는 NVM based CIM에 대해 소개된다.

- **ISAAC**: RRAM 기반의 tile-based architecture
  - in-situ MAC unit에서 data encoding, processing steps가 결합된다.
  - pipeline 구조로 external eDRAM에서 데이터를 공급받는다.
  - 16-bit의 data format을 가지며, single cycle에 1-bit만 처리한다. 따라서 모든 input data를 처리하기 위해서는 16 cycles가 필요하다.
  - 다른 tile 간의 computation process는 pipelined 되어있다.
- **PipeLayer**
  - 동일한 weight 데이터를 여러 군데 저장하여, 동일한 weight를 사용하는 데이터들의 연산을 병렬적으로 수행하는 전략.
- **PRIME**
  - PE를 더 추가하는 대신, RRAM array의 일부를 acceleration에 활용하는 전략.

위에서 살펴본, NVM based CIM은 analog domain에서 연산이 이루어진다. 그래서 **ADC로 인한 부담이 존재**한다. ADC를 사용하는 빈도를 줄이기 위해서, accumulation을 analog-domain에서 수행하는 방법을 사용한다. 기존에는 자릿수마다 ADC를 통해 digital data로 변환하였다면, 이제는 자리값에 해당하는 가중치를 반영하여 ADC를 거치기 전에, 먼저 analog domain 형태로 합친다.

다음은, PCM-based의 DNN inference에 대해 소개한다. Architecture는 크게 세 가지의 구성을 가진다.

  1. Analog cores: PCM을 통해 MVM operation을 수행한다
  2. On-chip communication network: core들 사이의 데이터 전달을 담당한다.
  3. Digital logic: activation function, normalization 등과 같이 MVM이 아닌 다른 연산을 수행한다.
  오직 analog core로만 구성된 것이 아닌, digital logic을 결합하여 MVM이 아닌 다른 연산의 효율을 높이는 전략을 확인할 수 있다.

뒤에서도 이와 비슷한 내용을 다룬다. Analog CIM은 MVM-oriented workloads를 처리할 때는 효율적이나, low-reuse kernels, batch normalization, activation과 같은 연산에는 비효율적이라고 설명한다.

⇒ 이러한 문제를 완화하기 위해, PCM-based accelerator와 general-purpose core를 결합한 analog-digital edge system을 제안한다.

이를 통해, 특정 연산을 가속해도 가속이 되지 않은 연산이 또 다른 병목 현상을 발생한다는 것, 그리고 이를 해결하기 위한 방법으로 digital core와의 역할 분담을 한다는 전략 등의 사고를 확장해나갈 수 있었다.

### 2.4.3 Neuromorphic Accelerators
{: #section-12 }

Neuromorphic computing은 간단히 설명하자면, 데이터를 저장하는 memory, 연산을 수행하는 processor가 분리되어 있는 기존의 방식인 von Neumann-based architecture가 아닌, PE와 memory가 합쳐진 여러 단위 사이에서 정보를 주고받으며 계산하는 방식이다. 이러한 neuromorphic을 이용한 chip들은 높은 neuron, synapse density, energy efficiency를 가지기 때문에 edge computing을 구현함에 있어서 유리하다.

**Small-scale**

- **SpiNNaker chip (for SNN, neuroscience simulation acceleration)**

    &#58; distributed von Neumann approach를 사용한다(processor의 연산을 주위 processor와 나누어 가지며 정보를 주고받는 방식). 또한, Globally Asynchronous, Locally Synchronous(GALS)를 통해, local 영역은 내부 clock으로 맞춰 동작되고, local 영역 사이에서 데이터를 주고받을 때는 clock에 맞추지 않고 통신할 수 있게 한다(spike event가 발생했을 때 바로 전달).

- **Full-custom digital hardware (for accelerating specific workloads)**

    &#58; SNN에 맞춘 회로를 전용으로 설계하여, 더 높은 density, energy efficiency를 보이게 할 수 있다. 마치 SNN 전용 ASIC으로 생각할 수 있을 것이다.

  - **45nm design in Reference \[176\]**

      &#58; Leaky Integrate-and-Fire neurons를 사용하고, S-STDP 방식으로 synapses가 update된다. 256개의 neurons, 64k synapses를 저장할 수 있는 용량을 가진다.

      \*Leaky Integrate-and-Fire neurons는 뉴런의 특징을 의미한다. 시간이 지나면 신호가 줄어드는(leaky) 현상, spike가 누적되는 현상(Integrate), 그리고 threshold를 넘으면 output spike를 발생시키는(Fire) 현상이 구현된 것이다.
      \*Stochastic Synaptic Time Dependant Plasticity (S-STDP)란, spike의 시간적 관계에 따라서 synapse weight가 확률적으로 (Stochastic) 변화하는 방식이다.
  - **ODIN, MorphIC chip**

      &#58; ODIN chip은 neuron, synapse의 규모는 동일하지만, SDSP 기반의 synapse를 사용하고, 다른 공정을 사용한다. MorphIC chip은 ODIN core 4개를 이용하여 설계한 chip이다. SNN용 NPU를 위한 시도였다.

      \*SDSP: Spike-Driven Synaptic Plasticity: spike의 발생에 따라 synaptic weight를 변화시키는 방식

위에서 언급된 Neuromorphic accelerators는 각각 작은 규모의 회로이다. 다음은, 수많은 neuron, synapse가 포함된 더 큰 규모의 Neuromorphic platforms을 처리하기 위해 만들어진 accelerators에 대해 살펴본다.

**Large-scale**

  - **IBM TrueNorth**

      &#58; 1M neurons, 256M개의 binary **non-plastic** synapses를 포함하며 GALS design으로 설계되었다. TrueNorth는 3개의 뉴런의 결합으로 다양한 동작을 수행할 수 있다.

  - **Loihi (balanced with versatility and efficiency)**

      &#58; 앞선 예시들과 달리, Loihi는 fully asynchronous design으로 설계되었다. Loihi의 neuron은 LIF model을 기반으로 하며, 여기에 몇 가지 동작 기능이 추가되었다. 또한 **compartment의 개수를 설정**할 수 있고, spike-based plasticity rule을 programming할 수 있다. 이는 synaptic weight를 갱신하는 규칙을 설정할 수 있음을 의미한다.

      \*구현한 기능
      1. Axonal delay: spike가 전달될 때의 delay 설정
      2. Refractory delay: neuron에 firing이 발생한 후 다시 firing이 발생하지 못하게 하는 시간을 설정
      3. Spike latency: spike가 발생하는 시점의 latency 설정
      4. Threshold adaptation: neuron의 threshold가 주변 상태에 따라 변화하는 기능

neuromorphic chip의 설계에서는 **versatility, efficiency**를 함께 고려해야 한다. Versatility는 neuron의 동작, synapse plasticity 등의 규칙을 지원하는 정도를 의미한다.  

  ⇒ versatility가 높다는 것은 chip에서 다양한 기능을 구현할 수 있다는 뜻이다. 
  ⇒ 그러나 다양한 기능을 구현하기 위해서는 추가 자원이 요구될 수 있다. 
  ⇒ 자연스럽게 efficiency에 부담이 가해지는 trade-off가 발생한다.

구조의 다양성(versatility)과 효율(efficiency)은 서로 trade-off 관계이다. 앞서 언급한 예시들이 어떤 설계 목표를 가지고 제작되었는지 아래 표를 통해 정리했다.

<table>

<tr>
<td markdown="span">Focus</td>
<td markdown="span">name</td>
<td markdown="span">meaning</td>
</tr>
<tr>
<td markdown="span">**Versatility-driven**</td>
<td markdown="span">**SpiNNaker**</td>
<td markdown="span">distributed von Neumann 구조로서, software 명령을 통해 동작이 구현된다.</td>
</tr>
<tr>
<td markdown="span">**Efficiency-driven**</td>
<td markdown="span">**ODIN, MorphIC**</td>
<td markdown="span">full-custom digital hardware로서, higher density, energy-efficiency를 보이지만, 특정 workloads의 구현에 특화된다.</td>
</tr>
<tr>
<td markdown="span">**Balanced trade-off**</td>
<td markdown="span">**Loihi**</td>
<td markdown="span">Neuromorphic design 구조이면서, 일부 neurons, synapse 규칙을 유연하게 수정할 수 있다.</td>
</tr>
</table>

# 3. Thought & Summary
{: #section-13 }

아래 표는 survey에서 다룬 주요 문제와 해결 전략, 그리고 그에 따른 trade-off를 정리한 것이다. 이러한 전략은 특정 chip에만 국한되지 않으며, 다양한 accelerator의 성능과 energy efficiency를 높이기 위한 공통적인 접근법이다.

<table>

<tr>
<td markdown="span">Problem</td>
<td markdown="span">해결 방법, 전략</td>
<td markdown="span">새롭게 제시되는 문제, Trade-off</td>
</tr>
<tr>
<td markdown="span">**Off-chip data movement**</td>
<td markdown="span">stationary strategies 사용,<br />DaDianNao의 on-chip weight 저장, Eyeriss의 data reuse, PIM,CIM</td>
<td markdown="span">저장 용량, internal data movement,</td>
</tr>
<tr>
<td markdown="span">**높은 bit 수로 인해 발생하는 cost**</td>
<td markdown="span">Quantization; Low precision, mixed precision, and cluster index</td>
<td markdown="span">Accuracy가 줄어들거나, 복잡한 structure 구성을 요구한다.</td>
</tr>
<tr>
<td markdown="span">**sparse matrix의 불필요한 연산 발생**</td>
<td markdown="span">Zero skipping , Compression</td>
<td markdown="span">압축 정보 처리, scheduling, PE load imbalance</td>
</tr>
<tr>
<td markdown="span">**Analog data의 잦은 ADC/DAC 사용으로 인한 cost 발생.**</td>
<td markdown="span">accumulation을 analog-domain에서 수행하는 방법을 사용</td>
<td markdown="span">low accuarcy, analog non-ideality</td>
</tr>
<tr>
<td markdown="span">**일부 연산만 가속하여 남은 연산이 전체 성능을 낮추는 문제**</td>
<td markdown="span">PCM accelerator와 digital core를 결합한다.</td>
<td markdown="span">데이터 전달 비용, 처리 속도 차이로 인한 대기</td>
</tr>
</table>

본 논문을 통해 다양한 DNN accelerator의 종류와 설계 목적을 살펴보고, 기존에 읽었던 논문들에서 공통적으로 나타나는 문제와 해결 전략을 연결할 수 있었다. Accelerator마다 구조와 목적에 따라 접근 방식은 다르지만, data movement를 줄이거나 quantization을 활용하는 등 성능과 energy efficiency를 높이기 위한 전략을 공유하고 있음을 확인할 수 있었다.

이를 통해 특정 accelerator를 설계할 때 어떤 문제와 조건을 고려해야 하는지, 이를 해결하기 위해 기존 연구에서 어떤 방법을 제시했는지 살펴볼 수 있었다. 또한 같은 문제라도 workload의 특성과 설계 조건에 따라 해결 방법이 달라질 수 있음을 알게 되었다. 이 survey를 통해 주어진 조건에서 accelerator를 설계할 때 고려해야 할 기본적인 지식과 관점을 넓힐 수 있었다.

인상 깊게 보았던 주제는 “Quantization”이다. 많은 accelerator가 quantization을 적극적으로 도입하여 energy efficiency를 높이려는 접근을 사용하고 있음을 확인할 수 있었다. 또한 quantization에도 다양한 방법이 존재한다는 점을 알게 되었고, 이를 어떻게 구현하는지, quantization으로 인한 accuracy 감소를 어떻게 줄일 수 있는지 더 학습해보고 싶었다.
