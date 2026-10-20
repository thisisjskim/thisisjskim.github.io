---
title: In-Datacenter Performance Analysis of a Tensor Processing Unit
permalink: /paper-notes/tpu/
short_title: TPU
paper_authors: Norman P. Jouppi, Cliff Young, Nishant Patil, David Patterson, et al.
paper_venue: ISCA
paper_year: 2017
paper_url: https://doi.org/10.1145/3079856.3080246
note_updated: '2026-10-20'
note_status: complete
excerpt: TPU v1의 연산 배열, 메모리 구조, Roofline과 활용률을 중심으로 정리했습니다.
topics:
- AI Accelerator
- Systolic Array
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
  title: 4.1 Main Structure(Components)
- depth: 2
  id: section-6
  title: 4.2 Computation Logic
- depth: 1
  id: section-7
  title: 5. Results
- depth: 2
  id: section-8
  title: 5.1 Benchmark
- depth: 2
  id: section-9
  title: 5.2 Performance
- depth: 3
  id: section-10
  title: 5.2.1 TPU performance
- depth: 3
  id: section-11
  title: 5.2.2 CPU&GPU performance
- depth: 3
  id: section-12
  title: 5.2.3 Cost-Performance, TCO, and Performance/Watt
- depth: 3
  id: section-13
  title: 5.2.4 Energy Proportionality
- depth: 3
  id: section-14
  title: 5.2.5 Evaluation of Alternative TPU Designs
- depth: 1
  id: section-15
  title: 6. Discussion
- depth: 2
  id: section-16
  title: 6.1 Fallacy
- depth: 2
  id: section-17
  title: 6.2 Pitfall
- depth: 1
  id: section-18
  title: 7. Thought
---

# 1. Introduction
{: #section-1 }

> 이 논문은 실제 Google Datacenter에서 NN application의 연산 요구량이 증가하여 기존 CPU, GPU기반의 datacenter에 부담이 가기 시작하자, 이를 해결하기 위해 자체적으로 제작한 NN inference용 domain-specific custom ASIC인 TPU에 대해 설명한다. TPU를 설계 할 때 고려했던 조건 (response time, accumulator size,,, etc)을 설명한다. TPU가 CPU, GPU(K80)보다 월등한 performance와 power efficiency를 가짐을 보여준다. 또한 TPU가 가지는 문제점, 한계와 앞으로 무엇을 더 발전나가야 할지를 서술한다.

---

# 2. Problem
{: #section-2 }

NN application이 Google의 Datacenter 연산 수요를 증가시킨다. NN application은 weight, activation 사이의 수많은 multiplication&accumulation operation을 요구한다. 일반적으로 수많은 연산은 GPU를 통해 해결할 수 있을 것이라 생각하지만, 현재 이 논문에서 다루는 “inference”의 경우, end-users-facing service이기 때문에, response time이 throughput보다 중요하다. 기존의 높은 throughput을 제공하는데 유리한 GPU(K80)는 response time을 고려한 inference model에서 잘 맞지 않는다. 또한 inference의 특성상, training 처럼 정확한 정밀도를 요구하지 않다. 이러한 종합적인 요구사항에 맞춘 custom ASIC가 google에게 필요했다.

# 3. Core Idea
{: #section-3 }

Inference만을 특화로 acceleration하기 위해 chip안에 불필요한 기능을 제외하여 Buffer, Matrix Multiply Unit, Accumulators의 영향력을 키운다. TPU의 성능을 보여주는 Roofline performance model에 대해 자세히 분석해야 하고, 각 NN model이 roofline에서 위치하는 점을 확인하고, 그 의미를 파악해야 한다. Throughput이 아닌 response time에 집중하여 TPU의 batch size를 결정한다. TPU가 가지는 문제점과, 앞으로 발전해나갈 방향을 확인한다.

# 4. Architectures & Computation Methods
{: #section-4 }

TPU는 Google Datacenter의 NN inference 수요가 증가함에 따라, 기존 CPU를 사용했을 때 발생되는 비용과 전력의 부담을 완화하고자 만들어졌다.

<figure><img src="/images/papers/tpu/01.png" alt="원 논문의 그림" loading="lazy" decoding="async"></figure>

## 4.1 **Main Structure(Components)**
{: #section-5 }

- CPU와 통합한 것이 아닌** PCIe에 연결되는 coprocessor 형태**로 만들어졌다.
- **Matrix Multiply Unit**: 256 x 256 8-bit MAC으로 구성된다.
- **Accumulator**: 4MiB of 32-bit의 용량을 가진다. 
  - 4MiB = 4096 x 256-elements, 32-bit accumulators이다. 이는 multiplication의 1 cycle에서 나온 256-elements partial sum 묶음을 총 4096번 저장할 수 있음을 의미한다. 이렇게 설계한 이유는 TPU가 peak performance에 도달하려면 약 1350 ops/byte의 operational intensity가 필요하다는 점에 기반한다. TPU가 최상의 성능을 내기 위해 accumulator의 용량을 2048로 넉넉하게 잡고(\~1350을 다 수용할 수 있게끔), 이후 double buffering까지 만족시켜주기 위해 또 한 번 두 배로 하여 최종적으로 4096개의 256-element accumulator로 결정했다.
- **Unified Buffer**: TPU 내부의 24 MiB on-chip storage로, 주로 intermediate activation/result를 저장한다. Matrix Multiply Unit의 input으로 다시 사용될 수 있으며, 한 layer의 output을 다음 layer의 input으로 재사용하기 위해 활용된다. 
  - UB역시 Matrix Multiply Unit의 pitch에 맞추어서 제작되었다.
- **Off chip 8GiB DRAM(=Weight Memory), on chip weight FIFO, weight buffer** : weight의 값을 받아오고, Matrix Multiply Unit에서 사용되기 까지 weight가 이동하는 경로 및 저장소
- **DMA controller**: CPU Host memory ↔ UB 사이의 data transfers

Structure를 살펴보면 UB, Matrix Unit이 die면적의 2/3정도를 차지하는 반면, control은 약 2%만 차지하는 것을 확인할 수 있다. 이를 통해 TPU가 NN model의 accelerator의 역할만을 위해 특별히 제작된 것임을 확인할 수 있다.

## 4.2 **Computation Logic**
{: #section-6 }

TPU는 Matrix Multiply Unit에서 input data, weight의 8-bit multiplication이 발생한다. multiplication의 결과는 16-bit products의 범위를 가지게 되고, 이 결과는 32-bit Accumulator에 누적된다. 이후 Activation 과정을 거치게 되며, 이 모든 작업이 끝난 값은 Unified Buffer에 저장되어 다음 layer의 연산의 input으로 이동하게 된다.

TPU는 Hardware design&debugging을 간단히 하기 위해서 host server(CPU)가 TPU instruction을 보내준다. 즉 instructions가 PCIe bus를 통해 전달되고, 이 속도는 상대적으로 느리다. 따라서 TPU instructions는 CISC tradition을 따른다.

- CISC tradition: TPU instruction 하나가 TPU내부에서 최대한 많은 일을 할 수 있도록 설계한 것; 하나의 instruction이 많은 일을 해야 PCIe를 통한 불필요한 instruction movement를 줄일 수 있기 때문. TPU instructions’ CPI는 대략 10\~20에 해당한다.

TPU instructions는 12개가 존재하며 그중 중요한 5가지는 아래와 같다.

1. Read_Host_Memory: CPU host memory를 UB로 읽어오는 것
2. Read_Weights: weight memory의 data를 Matrix Multiply Unit까지 읽어오는 것
3. MatrixMultiply/Convolve: Matrix Multiply Unit의 연산을 실행시키는 것
4. Activate: Accumulators → Activate → UB로의 operation을 실행
5. Write_Host_Memory: UB의 data를 CPU host memory로 write
  TPU는 matrix unit이 멈추지 않고 바쁘게 돌아가도록 설계했다. CISC에 대해 4-stage pipelline을 사용하여 instruction이 서로 연관이 없을 때 동시에 진행될 수 있게 한다. 특정 instruction이 끝날 때 까지 멈추지 않고, 다른 여러개의 instruction을 받아서 실행하게 한다. 
- Read_Weights의 경우 Weights가 Matrix unit까지 완전히 이동하지 않은 상태여도, instruction을 완료하게 하여 weight가 이동하는 동안 다른 instruction을 진행할 수 있게 한다.

그러나 weight가 Matrix unit이 시작할 때 까지 이동이 되지 않았다면 stall이 발생한다. 이 외에도 layer1의 output이 layer2의 input으로 들어가는, 즉 서로 영향을 미치는 작업의 경우도 동시에 실행하지 않고 작업이 끝날 때 까지 기다리도록 했다. 이를 “delay slot”으로 설명한다.

- 아래는 systolic execution(array)에서 weight가 preload되어 있는 상태를 보여주는 예시이다. (이 논문에서 다루는 TPU도 weight가 preload되어 있는 systolic execution을 보여줌)
  

<figure><img src="/images/papers/tpu/02.gif" alt="원 논문의 그림" loading="lazy" decoding="async"></figure>

  TPU는** ”systolic execution”**을 이용하여 UB를 통해 data를 읽고, 쓰는 과정을 대폭 축소했다. 하나의 data(activation)가 Matrix unit 내부에서 이동하며 data reuse를 높였다.
  TPU는 software 측면에서도 matrix unit이 멈추지 않도록 설계되었다. 먼저 TPU는 CPU/GPU와의 호환성을 높이기 위해 기존 TensorFlow based code를 그대로 활용할 수 있게 TPU software stack을 설계했다. Software stack은 크게 두 가지로 나뉜다.
- Kernel Driver: memory management, interrupts만 관리한다.
  → 장기적으로 안정적, lightweight하게 설계됨
- User Space Driver: TPU execution, data reformatting, API → TPU instruction translating, application binary 생성
  → 자주 변동됨, user space driver가 특정 model을 처음 compiling할 때는 시간이 많이 소요된다. 그러나 두 번째 실행부터는 program, weight를 재사용하여 최대 속도로 실행된다.
  TPU는 <span class="math-inline" markdown="0">\(\frac{TPU compute time}{I/O time}\)</span> 의 비율을 크게 하는 것이 목적이다. 즉 CPU와의 data movement로 발생하는 시간보다 TPU내부에서 computing에 많은 시간을 쓴다는 뜻이다. 
  결국, 최종적인 TPU의 목표는 모든 inference model을 TPU 내부에서 처리할 수 있게 되어, CPU와의 interactions을 줄이는 것이다.

# 5. Results
{: #section-7 }

## 5.1 Benchmark
{: #section-8 }

Paper에서 TPU의 성능을 비교할 때, 실제 datacenter에서 사용될 수 있는 hardware와 workload를 이용하였다. 추가적으로 SECDED protection까지 만족시켜야 한다. CPU의 “Haswell processor”, GPU의 “NVIDIA K80”이 위 조건을 만족하는 chip으로 선정되었다. CPU는 “Turbo mode”를 제외한 상태로 측정했다. NN model에서는 AVX를 자주 사용하고, datacenter 특성상 대부분의 CPU core가 활성화되기 때문에 현실적으로 datacenter에서 높은 Turbo mode가 자주 사용되지 않는다고 판단했기 때문이다. 같은 맥락으로 GPU의 “Boost mode”도 제외되었다. Boost mode를 사용할 경우 power consumption과 cooling issue 등으로 인해 K80 card의 수를 줄여야 하는 trade-off가 생긴다. 이 경우 throughput과 Total Cost of Ownership 측면에서 손해를 볼 수 있기 때문에, GPU 역시 Boost mode를 고려하지 않은 상태로 TPU와 성능을 비교하였다. 추가적으로 공정한 성능 비교를 위해 performance/die로 normalized한다.

## 5.2 Performance
{: #section-9 }

**“Roofline Performance model”**을 이용해서 성능을 비교한다.

- **x-axis: FLOPs/(DRAM byte accessed)**
  - 1byte를 가져왔을 때 그 data가 얼마나 reuse되는지 나타낸다. **(Operational Intensity)**
- **y-axis: FLOPs/sec**
  - 1초에 얼마나 많은 FLOPs operation을 진행했는지를 나타낸다. **(Performance)**

<span class="math-inline" markdown="0">\(Performance(P)=Bandwidth(BW)\times Intensity(I)\)</span>

  - low intensity → memory bound → slanted
  - high intensity → compute bound → flat

      &#58; 이 관계를 통해 Roofline Performance model에서 특정 NN model이 memory bound or compute bound로 인해 성능이 제한되었음을 확인할 수 있다.


### 5.2.1 **TPU performance**
{: #section-10 }

TPU에 맞게 Roofline model의 **Operational Intensity(x-axis)**의 단위를 **Ops**/**weight byte**로 조정한다. 

  - **FLOPs → Ops(integer operations)**
  - **DRAM byte accessed → weight byte:** TPU에서 NN application을 operating할 때 전체 weight의 값이 on-chip에 저장되지 못하고, weight memory(off-chip)에서 제공받아야 하기 때문이다.

<figure><img src="/images/papers/tpu/03.png" alt="원 논문의 그림" loading="lazy" decoding="async"></figure>

Figure 5를 통해, TPU의 ridge point는 1350 Ops/weight byte이고 TPU의 peak compute에 비해 weight memory bandwidth가 낮은 상태이며, 최대 성능을 내기 위해서는 high weight reuse가 요구됨을 알 수 있다. 

- **MLPs/LSTMs**: low weight reuse → low ops/weight byte → **memory-bound**
- **CNN0**: high weight reuse → high ops/weight byte → **compute-bound**

그러나 “CNN1’은 high weight reuse임에도 **비교적 낮은 computation performance를 보인다. **크게 2가지 이유를 Table 3에서 확인할 수 있다.** **(Table 3는 performance counters를 통해 TPU operation의 비중을 보여준다)

1. “CNN1”의 Array active cycles은 46.2%로 Matrix unit이 matrix operation이 전체의 절반정도만 진행된다. 또한, active한 cycle 안에서 MAC utilization이 약 절반이다. 그 이유는, CNN1의 some layers에서 shallow feature depths가 발생하기 때문이다. 즉, channel의 수가 적어서 MACs에 충분한 data를 제공하지 못하여 모든 MACs를 활성화하지 못한다. 
2. CNN1은 약 35%의 cycle을 weight load를 기다리는 데 사용한다. CNN1에서 4개의 FC layers의 Intensity가 “32”로 작게 나타나기 때문이다. CNN1의 전체 Intensity는 높을지라도, 몇몇 layers에서의 Intensity가 낮게 나타나서 bottleneck이 발생하게 된다.

<figure><img src="/images/papers/tpu/04.png" alt="원 논문의 그림" loading="lazy" decoding="async"></figure>

### 5.2.2 CPU&GPU performance
{: #section-11 }

<figure><img src="/images/papers/tpu/05.png" alt="원 논문의 그림" loading="lazy" decoding="async"></figure>

<figure><img src="/images/papers/tpu/06.png" alt="원 논문의 그림" loading="lazy" decoding="async"></figure>

Figure 6은 CPU의 Roofline model, Figure 7은 GPU의 Roofline model이다. 두 Roofline model에서 공통적으로 6개의 NN applications가 Roofline ceiling의 S아래에 위치한다. **그 이유는 “Response Time” 때문이다. **많은 NN applications는 사람들의 실제 사용하는 service이기 때문에 사용자의 요청에 응답하는 시간(response time)이 중요하다. 즉 latency가 특정 값(In this papar, it is **7ms**)을 넘어서는 안된다. inference에서는 절대적으로 높은 throughput보다, 적절한 throughput과 낮은 latency가 선택됨을 보여준다.

<figure><img src="/images/papers/tpu/07.png" alt="원 논문의 그림" loading="lazy" decoding="async"></figure>

Table 4는 number of batch를 늘렸을 때 response time, IPS(=throughput)의 변화를 보여준다. batch의 수를 늘리면 weight를 여러 input에 더 많이 반복해서 사용할 수 있게 되어 throughput이 증가하지만, trade-off로 latency가 증가하게 된다. **CPU와 GPU는 latency를 7ms로 맞췄을 때 각각 전체 성능의 42%, 37%만 활용 가능하다.** 그러나, TPU는 80%의 높은 수치를 보여준다.

<figure><img src="/images/papers/tpu/08.png" alt="원 논문의 그림" loading="lazy" decoding="async"></figure>

Table 5는 각 NN application에서 host CPU와 TPU가 PCIe를 통해 통신하는 시간을 TPU execution time 대비 비율로 보여준다. CPU가 application을 수행하는 시간은 포함되지 않는다. (측정하기 어렵기 때문)

<figure><img src="/images/papers/tpu/09.png" alt="원 논문의 그림" loading="lazy" decoding="async"></figure>

<figure><img src="/images/papers/tpu/10.png" alt="원 논문의 그림" loading="lazy" decoding="async"></figure>

Table 6는 TPU의 performance를 보여주는 지표이다. GM, WM은 각각 geometric mean, weighted mean이다. (weight mean은 NN application의 사용빈도를 가중치로 두어 구한 평균이다.) 평균GM을 했을 때, TPU는 CPU의 14.5X, GPU의 13.2X의 성능을 보인다. WM일 때는 CPU의 29.2X, GPU의 15.3X의 더 높은 성능을 보임을 확인할 수 있다. Figure 8을 통해 TPU가 CPU/GPU에 비해 높은 Ops/sec을 가짐을 확인할 수 있다.

### 5.2.3 Cost-Performance, TCO, and Performance/Watt
{: #section-12 }

<figure><img src="/images/papers/tpu/11.png" alt="원 논문의 그림" loading="lazy" decoding="async"></figure>

실제 datacenter를 구축할 때 절대적인 성능 보다도 cost-performance의 비율이 더 중요하다. 이를 잘 나타내는 수치로는 TCO(Total Cost of Ownership)가 있는데, 본 paper에서는 business reasons으로 인해 그 다음으로 의미있는 수치인 Performance/Watt를 통해 각 chip의 cost-performance를 비교한다.

- **total performance/Watt:** Includes power consumed by the host CPU server
- **incremental performance/Watt:** Subtracts the host CPU server power

TPU는 CPU/GPU에 비해 더 높은 Performance/Watt를 가짐을 확인할 수 있다.

### 5.2.4 Energy Proportionality
{: #section-13 }

<figure><img src="/images/papers/tpu/12.png" alt="원 논문의 그림" loading="lazy" decoding="async"></figure>

Figure 10에서 incremental power(TPU, K80), total power(TPU+Haswell/2, K80+Haswell/4, Haswell)를 확인할 수 있다. 총 2가지의 관점에서 해석해야 한다. 

  - 절대적인 power를 얼마나 소비하는가
  - **energy proportionality**: workload의 사용량에 따라서 power consumption이 변화하는지를 확인해야 한다. 

**이 관점에서 TPU는 total, incremental에서 전체 power는 낮지만 energy proportionality는 좋지 않음**을 알 수 있다. Workload를 10%만 사용했을 때에도 100%를 사용할 때 사용하는 power의 88%를 소모하고 있다.

그럼에도 TPU 자체의 power는 매우 낮고, TPU를 사용했을 때 얻는 performance 이득이 매우 높기에 datacenter에서 TPU를 사용하는 것이 전체적인 큰 이익을 가져다 준다.

### 5.2.5 Evaluation of Alternative TPU Designs
{: #section-14 }

<figure><img src="/images/papers/tpu/13.png" alt="원 논문의 그림" loading="lazy" decoding="async"></figure>

Figure 11에서는 TPU의 각 parameters를 scaling 했을 때 TPU의 performance를 확인 한다. 총 5개의 경우를 나누어서 비교한다.

1. memory: Weigh memory bandwidth
2. clock: clock rate를 증가시킨다
3. clock+: clock rate와 accumulator 수를 함께 증가
4. matrix: Matrix Multiply Unit의 차원을 증가
5. matrix+: Matrix Multiply Unit의 차원과 그에 맞는 accumulator 수를 함께 증가

그 결과, memory bandwidth를 증가시키는 것이 가장 큰 performance 향상을 보임을 알 수 있다(평균적으로 memory bandwidth가 4X 증가할 때, performance는 3X 증가). 이는 TPU에서 memory bound로 인한 bottleneck이 크게 작용했음을 의미한다. 

clock rate를 상승시키는 것은 MLPs, LSTMs에는 큰 효과를 보지 못하지만, compute-bound를 가지는 CNNs에서는 clock rate를 4X 했을 때, performance가 2X 증가한다. 

오히려 matrix의 차원을 증가시켰을 때 성능이 떨어짐을 확인할 수 있다. Matrix의 차원을 높이면 tiling 횟수는 줄어들지만, 각 tile마다 소요되는 연산 시간도 함께 증가한다. 또한 internal fragmentation을 모두 고려했을 때, 오히려 더 연산에 큰 시간이 소요되어 성능이 저하된다.

  internal fragmentation: matrix가 Matrix Unit과 맞지 않아서 MAC의 일부가 낭비되는 현상

TPU에 GDDR5 memory를 사용하면 memory bandwidth를 약 5배 높일 수 있다. 이는 roofline ridge point를 1350 → 250으로 옮겨준다. GDDR5를 사용했을 때 Performance의 Weighted mean이 3.9X 향상이 된다. (Host server를 고려하면 3.2X 향상)

  - GDDR5를 사용하면 기존 DDR3에 비해 10%정도의 면적을 더 차지하게 된다. 그러나 이를 Unified Buffer를 24MiB→14MiB로 줄여서 전체 면적을 맞춰줄 수 있다. UB를 줄여도 되는 이유는, storage allocator의 개선과GDDR5의 높은 Memory bandwidth가 UB의 부담을 덜어주기 때문이다.
  - GDDR5를 이용했을 때 TPU가 소비하는 power도 증가하지만, 더 높은 performance를 내기 때문에 total-performance/Watt는 증가한다. 이는 Figure 9에서 TPU’를 통해 볼 수 있다.

# 6. Discussion
{: #section-15 }

Discussion에서는 Fallacy(잘못된 오해), Pitfall(주의점)을 설명한다.

## 6.1 Fallacy
{: #section-16 }

- NN inference applications in datacenter은 throughput을 response time과 비슷하게 가치를 매겼을 것이다.
  ⇒ User-facing application에서 사용자가 기다리는 시간 때문에 response time의 요구가 더욱 강했다.
- K80 GPU가 NN inference model에 강했다.
  ⇒ K80은 high throughput performance를 내기 위해 제조되었기에 response time이 중요한 inference model에 맞지 않았다.
- K80의 Boost mode을 작동시키면 더 좋은 효율을 보였을 것이다.
  ⇒ Boost mode를 작동시키면 clock rate를 증가시키지만, 그에 따른 power consuming도 증가한다. Clock rate의 증가로 인해 1.4X의 performance증가가 발생해도, power도 1.3X 더 많이 사용되기에 performance/Watt 측면에서 큰 차이가 없다.
- 더 최신의 기술, 더 발전된 CPU or GPU를 사용하면 TPU와 크게 차이가 없을 것이다
  ⇒ 실제 CPU를 TPU처럼 8-bit integer로 최적화 시켜 사용했을 때 하나의 DNN에서 3.5X의 성능 향상을 보였다. 그러나, 모든 DNN이 똑같은 성능 향상을 보인다고 가정해도 TPU의 performance/Watt가 더 높다.
  ⇒ 비교대상을 K80이 아닌 더 최신의 GPU인 NVIDIA P40으로 했다면 성능 비교의 차이가 달라졌을 수도 있지만, 일단 P40은 TPU의 성능을 측정하고 비교했던 시기에 존재하지 않았고, P40이 strict response time bounds(\~7ms)에서 얼마나 높은 연산 능력을 보일지도 확실하지 않다. 또한 같은 논리로, 더 발전된GDDR5를 탑재한 TPU’로 비교한다면 TPU가 더 높은 성능을 보일 수도 있다.
- TPU를 발전시키기 위해서는 hardware upgrade(like DDR3→GDDR5)가 유일하다. (Software 측면에서 더이상 발전시키기 어려울 것이다)
  ⇒ CNN1은 TPU의 Roofline performance model 아래에 위치한다. 간단하게 말해서, MAC utilization이 모두 활성화 되지 않았다. 분명 hardware를 개선하여 해결할 수 도 있지만, 모든 MAC을 활성화시키는 software 개선 또한 방법이 될 수도 있다. 아직 여러 방면에서 TPU의 performance를 향상시킬 방법이 존재함을 주장한다.

## 6.2 Pitfall
{: #section-17 }

- 여러 Architects에서 중요한 NN model tasks를 다루지 않았다.
  ⇒ 실제 datacenter에서 사용하는 NN models는 MLPs(61%), LSTMs(29%)이다. 그러나 그 당시 여러 연구에서는 CNNs을 많이 다루었는데 CNN은 datacenter에서 5%정도만 차지한다. CNNs도 중요하지만, 실제 많이 사용되는 MLPs, LSTMs를 accelerate하는 연구도 많이 필요하다.
- Inference Per Second(IPS)는 성능을 측정에 좋은 metric이 아니다.
  ⇒ IPS는 NN model의 구조적인 complexity에 따라 다르게 측정된다. 따라서 IPS가 절대적인 성능의 우위를 뜻하지 않는다.
- Performance counters를 hardware의 구성 이후 마지막에 생각한다.
  ⇒ Performance counters가 있었기에, TPU가 어느 부분에서 bottleneck이 생기는지 알 수 있다. 이는 설계를 할 때 중요한 요소이다. 실제로 paper에서는 더 많은 performance counters가 있었으면 좋았을 것이라고 언급하기도 한다.

# 7. Thought
{: #section-18 }

특정 상황에 맞추어 설계한 domain specific custom ASIC 중 가장 유명한 TPU의 설계 방향성을 알 수 있었다. 설계를 할 때 무엇을 중점적으로 고려하는지, 어떤 값을 높이기 위해서 무엇을 희생하는지를 확인할 수 있다. 

TPU의 peak compute에 비해 낮은 성능을 가지는 이유중 하나로 memory bandwidth가 computation에 비해 낮기 때문이라고 한다. 이에, weight reuse가 중요하다고 언급한다. TPU에서 각 NN application에 따라 weight reuse를 어떻게 활용하는지 궁금했다. Systolic data flow를 활용하여 activation data movement를 줄이는 방법은 설명하지만, 실제 layer에 따른 weight가 어떤 방식으로 mapping되는지는 자세하게 다루지 않는다. Mapping 방법에 따른 weight reuse, MAC utilization의 관점에서도 더 깊게 공부해보고 싶었다.

CNN1의 performance가 Roofline model의 아래에 위치한다고 논문에서 설명한다. 그 이유중 하나로 CNN1의 특정 layer가 적은 channel를 가져서 그 layer에서 사용되는 filter weight가 Matrix Unit 보다 작아서 MAC이 underutilized 되기 때문이라고 이해했다. 사용되지 않는 MAC에 독립적인 operation을 수행할 수 있게 만들 수는 없는지 궁금했다. Weight가 Matrix Unit 내부에 mapping 되는 dataflow를 더 명확하게 이해할 수 있다면, 이 문제를 해결하는 과정에서 어떤 한계가 존재하는지 명확하게 알 수 있다고 생각한다.

Evaluation of Alternative TPU designs section에서 Matrix size를 scaling 했을 때의 performance의 변화가 의아했다. 이 논문에서 matrix를 scaling up 했을 때의 문제를 설명하는 예시로 600x600 matrix를 들었다. 600x600의 size를 지닌 matrix는 분명 256x256의 크기를 가진 Matrix Unit이 512x512의 크기를 가진 Matrix Unit보다 더 낮은 latency를 보인다. 그러나 다른 예시에서는 결과가 다를 수도 있다고 생각한다. 나는 주어진 workload의 크기에 따라 이 결과는 달라질 수 있다고 생각한다. 

그뿐만 아니라, 만약 matrix의 크기를 scaling up 하는 것이 효과가 없거나 성능이 감소한다면, scaling down을 왜 더 하지 않았는지에 대한 이유도 궁금했다. 실제 Figure 11에서 0.5x 의 scaling down을 했을 때 performance가 감소하지 않으며, 오히려 소폭 상승했음을 확인할 수 있다. 왜 TPU는 Figure 11에서 보이는 결과대로 matrix의 크기를 scaling down 하지 않았는지 궁금했다. 만약 scaling down을 한다면, 남는 die area를 더 활용해서 matrix의 크기를 줄인 효과를 넘어선 성능 향상을 보일 수도 있을 것이라고 생각했기 때문이다. 이 쟁점에 대해서도 더 깊게 알아가고 싶었다.

마지막으로, 이 논문에서의 benchmark는 너무 오래되었다. 현재는 정말 Attention, Transformer 를 비롯해서 더 발전된 AI models가 사용된다. 현재 TPU가 지금의 AI model를 더 발전된 GPU와 비교했을 때도 더 높은 성능을 보이는지 궁금하고, 어떻게 발전되었는지에 대해 알아보고 싶다.
