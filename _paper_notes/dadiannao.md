---
title: 'DaDianNao: A Machine-Learning Supercomputer'
permalink: /paper-notes/dadiannao/
short_title: DaDianNao
paper_authors: Yunji Chen et al.
paper_venue: MICRO
paper_year: 2014
paper_url: https://doi.org/10.1109/MICRO.2014.58
note_updated: '2026-10-20'
note_status: complete
excerpt: On-chip eDRAM에 weight를 저장하는 구조와 multi-node 연산·통신 방식을 정리했습니다.
topics:
- AI Accelerator
- Memory Architecture
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
  title: 4.1 Node Design
- depth: 2
  id: section-6
  title: 4.2 Tile-based Design
- depth: 2
  id: section-7
  title: 4.3 Multi-Node Mapping
- depth: 1
  id: section-8
  title: 5. Results
- depth: 2
  id: section-9
  title: 5.1 Main characteristics
- depth: 2
  id: section-10
  title: 5.2 Performance
- depth: 1
  id: section-11
  title: 6. Limitation
- depth: 1
  id: section-12
  title: 7. Thought & Questions
---

## 1. Introduction
{: #section-1 }

> 이 논문은 CNN의 병목을 off-chip RAM과의 잦은 data movement/comunication이라고 본다. 즉, Memory-bound를 해결하기 위해 off-chip data movement를 최대한 줄이려고 한다. 그 방법으로, eDRAM을 computation logic 근처에 위치시킨다. 여러 design 철학, data movement path 등을 확인할 수 있다. CNN layer에서 CONV, POOL, LRN과 CLASS가 가지는 특성에 따른 speedup 차이의 이유를 확인할 수 있다.

## 2. Problem
{: #section-2 }

GPU, NN accelerator for Deep Learning은 neural network size limitation이 존재한다. 신경망이 거대해 지기 시작하며 intermediate values가 main memory에 저장될 때, data movement로 인한 power, latency 손해가 발생한다. Off-chip memory와의 통신이 많아질 수록 memory access가 performance bottleneck이 된다.

## 3. Core Idea
{: #section-3 }

Off-chip data movement(access)을 줄이기 위해 weight를 각 node의 on-chip eDRAM에 나누어 보관하는 방법을 택한다. weights 대신 neuron values를 이동시켜 off-chip access와 data movement를 줄이는 방법을 채택한다.

## 4. Architectures & Computation Methods
{: #section-4 }

DianNao accelerator는 GPU성능의 47.91%를 0.53%의 면적으로 구현할 수 있다고 주장한다. 하지만 DianNao의 main limitation은 memory bandwidth이다. 최적의 성능을 내기 위해서는 467.30 GB/s의 bandwidth가 필요하다. 이는 GPU가 제공하는 bandwidth(208GB/s)보다 더 높은 수치이다.

### 4.1 Node Design
{: #section-5 }

DaDianNao는 memory bandwidth의 문제를** 4가지의 design principle**를 통해 해결한다.

1. Synapses(weight)를 neuron(input, activation) 근처에 저장하여 data movement를 최소화 한다.
2. Computation보다 storage의 footprint를 크게 한다.
3. Synapse(weight)가 아닌 neuron을 칩들 사이로 이동시킨다. 이는 neuron의 개수가 synapse(weight)보다 더 작기 때문이다.
  - FC layer를 생각해볼 때, neuron은 다음 layer로 넘어가는 연산에서 data reuse가 있다. 그러나 synapse는 neuron과 한 번 곱해진다. Neuron이 synapse보다 수도 적고, data reuse도 많다. 그래서 neuron이 움직이고, synapse가 fixed되는 것이다.
4. Local storage를 여러 개로 tiling하여 high internal bandwidth를 유지하게 한다.

DaDianNao는 SRAM보다 eDRAM을 사용한다. 그 이유는 방대한 양의 NN model data를 저장하기 위해서는 memory density가 높아야 하기 때문이다. eDRAM은 SRAM보다 2.85x higher storage density를 가진다. 이처럼 많은 양의 data를 저장할 수 있는 RAM을 사용해야 off-chip DRAM access를 줄일 수 있다. Off-chip data movement는 eDRAM을 통한 data movement보다 321x energy consuming을 한다. 이는 off-chip data movement를 최대한 지양해야 함을 의미한다.

그러나 eDRAM이 가지는 구조적 문제인 destructive read, refresh issue를 무시할 수 없다. 이러한 문제를 보완하고자, eDRAM을 4개의 bank로 나누고 synapse를 bank사이에 interleave 한다. 이를통해 여러 bank에 병렬로 접근하여 computation이 쉬지 않고 작동할 수 있게 해준다.

<columns>

  <column ratio="50">
    

<figure><img src="/images/papers/dadiannao/01.png" alt="원 논문의 그림" loading="lazy" decoding="async"></figure>

  </column>
  <column ratio="50">
    

<figure><img src="/images/papers/dadiannao/02.png" alt="원 논문의 그림" loading="lazy" decoding="async"></figure>

  </column>

</columns>

그러나 이렇게 design 했을 때 65,536-bit를 eDRAM ↔ NFU 사이로 이동시켜야 하는데, 이때 필요한 wire의 두께가 NFU보다 크게 되어 wire가 너무 많은 공간을 차지하게 되는 문제가 발생한다. 이를 Figure 4를 통해 그림으로 확인가능하다.

### 4.2 Tile-based Design
{: #section-6 }

이러한 문제를 해결하기 위해 tile-based design을 채택했다. Figure 5를 통해 확인할 수 있다. 하나의 node에 16개의 tile과 central eDRAM, 그리고 하나의 tile에 4개의 tile eDRAM과 NFU로 구성된다. Tile 들은 “fat tree”를 통해 연결되어 input neurons를 공유한다.

전반적인 data movement&instructions를 정리하자면,

  1. **Input neurons가 ”fat tree”를 통해 All tiles에 broadcast 된다.**
  2. **Tile eDRAM에 저장되어 있는 weights와 input neurons가 tile 내부에 있는 NFU에서 연산된다. 각 tile에서 나오는 intermediate values는 local NBout SRAM(or tile eDRAM)에 저장된다.**
  3. **NFU를 통해 Computation이 끝나면, transfer function을 실행시키고, output values가 central eDRAM에 저장된다.**

<figure><img src="/images/papers/dadiannao/03.png" alt="원 논문의 그림" loading="lazy" decoding="async"></figure>

Neurons는 각 node마다 data reuse를 잘 하기 때문에 neurons로 인한 통신량이 상당해도, “a few layers and many-node systems”를 제외하면 bottleneck이 되지 않는다. 

Many-node systems의 경우 상당한 양의 input neurons, weight의 MAC operation을 진행해야한다. 즉 input neurons data가 tiles 내부, node 내부, node 외부와의 movement가 필연적이다. 각 node들이 2D mesh 구조로 연결되고, node interface에는 “**HyperTransport (HT) 2.0 IP block**”가 있어서, node간의 data movement를 도와준다.

  \*HT2.0 IP blocks: 한 방향의 bandwidth는 6.4GB/s, latency는 80ns.

### 4.3 Multi-Node Mapping
{: #section-7 }

input을 node에 mapping하는 방식과 inter-node communication pattern은 layer type에 따라 달라진다.

CONV/POOL/LRN과 같이 spatial feature map을 가지는 layer에서는, 하나의 node가 feature map 하나 전체를 담당하는 것이 아니라 여러 feature map(channel)에 걸친 동일한 spatial 영역을 담당한다.

예를 들어 input activation이

<div class="math-block">\[H\times W\times C_{in}\]</div>

이라고 하자. DaDianNao는 이를 spatial 방향으로 나누어, 한 node가 대략

<div class="math-block">\[H&#x27;\times W&#x27;\times C_{in}\]</div>

형태의 activation block을 담당한다.

이 데이터는 node의 central eDRAM에 저장되고, 계산할 때 fat tree를 통해 tiles에 broadcast된다. 각 tile에서는 tile eDRAM에 저장된 weight와 input activation이 NFU를 통해 연산된다. CONV/POOL의 경우, 이렇게 계산된 output neuron values 역시 output feature map의 특정 spatial 영역에 해당하며, 최종 output은 central eDRAM에 다시 저장된다.

Layer case에 따라 node 내부에서의 data movement만으로 연산이 가능한 경우가 있고, 다른 node의 data를 받아와야 하는 경우도 존재한다.

<figure><img src="/images/papers/dadiannao/04.png" alt="원 논문의 그림" loading="lazy" decoding="async"></figure>

3개의 main layer cases를 통해 어떤식으로 data가 mapping/communication되는지 확인할 수 있다.

1. **CONV/POOL**
  : CONV/POOL layer는 “local connectivity”의 성질을 가지기에, 대부분 node 내부에 존재하는 data로 연산이 가능하다. Boundary 외부의 data가 필요할 때만 외부 node와의 communication이 필요하다. (Figure 8의 red section이 node 0이 output을 만들기 위해 필요한 input neurons data가 위치해 있는 곳이다) 
2. **LRN**
  : multi-node mapping에서 같은 spatial position의 모든 feature map이 같은 node에 mapping되기 때문에 node 내부에서 모든 연산이 가능하다. (외부 node와의 communication이 존재하지 않는다.)
3. **CLASS**
  : CLASS는 각 output neurons가 모든 input neurons의 값을 사용해야 한다. 즉 FC layer라고 할 수 있다. 그렇기에 각 node에 mapping된 모든 data들을 다 사용해야 하기 때문에, 외부 node와의 communication이 많이 필요하다. 이때, 각 node에 할당된 input block을 옆의 node에 순차적으로 전달하여, 각 node가 모든 input block을 한 번씩 받아서 부분합을 만들도록 하는 방법인, “Computing-and-forwarding communication scheme”을 이용한다.(마치 ring pattern과도 같다)

## 5. Results
{: #section-8 }

### 5.1 Main characteristics
{: #section-9 }

<columns>

  <column ratio="50">
    

<figure><img src="/images/papers/dadiannao/05.png" alt="원 논문의 그림" loading="lazy" decoding="async"></figure>

  </column>
  <column ratio="50">
    

<figure><img src="/images/papers/dadiannao/06.png" alt="원 논문의 그림" loading="lazy" decoding="async"></figure>

  </column>

</columns>

Memory cells(eDRAM)이 전체 chip area의 47.55%, 즉 절반 정도를 차지하고 있다. 이는 computation보다 storage의 footprint를 크게 가져가자는 DaDianNao의 철학을 잘 보여준다.

Power consumption of chip에서 HT IP가 소비하는 power는 50.14%로 측정된다. 이를 통해 HT hardware에서 상당한 양의 power를 소모한다는 사실을 확인할 수 있으며, memory bottleneck을 줄인 이후에는 chip-to-chip communication이 새로운 bottleneck이 될 수 있음을 시사한다.

### 5.2 Performance
{: #section-10 }

<figure><img src="/images/papers/dadiannao/07.png" alt="원 논문의 그림" loading="lazy" decoding="async"></figure>

Fig 10에서 DaDianNao가 1-node, 4-node, 16-node, 64-node로 구성될 때 GPU와 비교해서 평균적으로 21.38x, 79.81x, 216.72x, 450.65x의 높은 성능을 보임을 확인할 수 있다. 이러한 성능 향상의 주된 이유는 GPU에 비해 더 많은 operators가 각 node마다 존재하고, on-chip eDRAM이 이 많은 operator들에게 충분한 internal bandwidth를 제공할 수 있기 때문이다.

그러나 Fig 10을 자세히 살펴보면 CONV1, CONV3\*, CONV4\*, full NN의 일부 node configuration이 표현되지 않음을 확인할 수 있다. 이는 각 workload를 수행하기 위해 필요한 input/output neuron values와 weights를 on-chip eDRAM에 모두 저장해야 하는데, 적은 node가 제공하는 storage capacity로는 구현이 불가하기 때문이다. 특히 CONV3\*와 CONV4\*는 각각 약 1.29GB, 1.32GB의 memory capacity를 요구하며, 이를 저장하기 위해 최소 36-node 이상의 system이 필요하다. 따라서 이 두 layer는 64-node system에 해당하는 결과만 존재한다.

LRN layer는 inter-node communication이 없기 때문에 node 수를 증가시켰을 때 가장 좋은 scaling efficiency를 보인다. 그러나 GPU 대비 speedup은 CONV layer에서 더 크게 나타난다. 이는 CONV layer가 computationally intensive하여 DaDianNao의 많은 operators를 더 효과적으로 활용할 수 있기 때문이다. 이에 반해, CLASS layers는 inter-node communication이 많아서 낮은 scaling efficiency를 보임을 확인할 수 있다.

full NN의 scaling은 CLASS layer와 닮아있다. 그러나 오해해서는 안되는 사실은, **full NN에서의 execution time은 CONV가 dominant 하다는 것이다. Table VII를 통해 확인할 수 있다. **

<figure><img src="/images/papers/dadiannao/08.png" alt="원 논문의 그림" loading="lazy" decoding="async"></figure>

이는 full NN에서 특정 CONV layer가 scaling에 취약함을 의미한다. full NN에는 **작은 차원의 CONV layer도 존재한다.** 이 작은 차원의 CONV layer의 data가 64-node machine에 mapping 된다면, **node당 담당하는 workload가 아주 작을 것이다.** 이는 오히려 inter-node communications를 증가시켜서 efficiency를 낮추거나, 모든 node를 다 사용하지 않아서 hardware utilization을 낮추는 trade-off를 불러온다.

<figure><img src="/images/papers/dadiannao/09.png" alt="원 논문의 그림" loading="lazy" decoding="async"></figure>

Figure 12는 DaDianNao가 training 부분에서 GPU와 비교했을 때의 speedup을 보여준다. traning은 32-bits fixed point operators를 하기에, speedup이 inference보다 더 낮음을 확인할 수 있다. 그래도 GPU보다 높은 성능을 보여준다.

Figure 13, 14는 inference, traning에서 GPU 대비 energy reduction을 보여준다. CONV, POOL, LRN은 node 수가 늘어도 energy benefits이 비교적 안정적이나, CLASS의 경우 node의 수가 증가할 수록 energy reduction의 비율은 줄어든다. 그 이유는 CLASS에서 발생하는 많은 inter-node communication으로 인해 HT IPs에서 소비되는 energy가 증가하기 때문이다.

## 6. Limitation
{: #section-11 }

GPU, accelerators는 높은 성능을 내고 있지만, large neural network에서는 memory bandwidth bottleneck이 존재한다. 이를 해결하기 위해 DaDianNao는 multi-chip architecture를 설계하고, off-chip data movement를 줄이기 위해 각 node 내부에 많은 eDRAM을 배치하여 weights를 저장한다. 그러나 system을 scaling하며 node 수가 증가하게 되자 inter-node communication으로 인한 새로운 limitation이 발생한다. 대표적으로 CLASS layer에서는 여러 node에 분산된 input neuron values를 사용해야 하기 때문에 많은 inter-node communication이 발생하며, 이로 인해 HT IPs의 energy consumption과 communication overhead가 증가한다. Bottleneck이 Off-chip memory bandwidth에서 Inter-node communication으로 이동한 것이다.

이러한 문제를 해결하기 위해 기존 2D mesh interconnect 대신 multi-dimensional torus topology를 활용하여 large classifier layer의 scalability를 개선하는 방법이 제시된다.

## 7. Thought & Questions
{: #section-12 }

DaDianNao의 핵심 철학은 inference/training에 필요한 weights를 on-chip eDRAM에 최대한 유지하고, neuron values를 이동시킴으로써, off-chip DRAM access를 줄이는 것으로 이해했다. 그러나 weights가 처음 어떤 과정을 통해 각 node, tile의 eDRAM에 배치되는지, 첫 input feature map이 외부에서 어떤 과정을 통해 central eDRAM에 저장되는지 궁금했다.

또한, CONV에서 input activation이 partition되어 각 node에 mapping되는 방식은 잘 설명되어 있지만, weight(kernel)가 node 및 tile에 어떻게 mapping되는지는 명확하지 않다. Kernel이 여러 node에 replicate되는지, 또는 다른 방식으로 partition되는지가 궁금하다. Weight mapping 방식에 따라 data movement가 달라질 수 있기 때문에, 이에 대해 더 알아보고 싶었다.

DaDianNao는 weights를 on-chip eDRAM에 모두 저장할 수 있다는 가정을 기반으로 한다. 그러나 model과 activation의 크기가 증가할수록 이를 수용하기 위해 더 많은 node가 필요해지고, 이에 따라 storage capacity뿐 아니라 inter-node communication과 system cost 측면의 문제가 발생할 수 있다고 생각했다. 실제로 Result section에서도 CONV3\*, CONV4\*와 같이 memory가 큰 workload는 최소 36개의 node를 필요로 한다. 현재 model의 크기는 과거에 비해 엄청나게 커졌다. 훨씬 커진 workload에서도 ‘모든 weights를 on-chip eDRAM에 저장하고 유지한다’는 DaDianNao의 철학이 어느 정도까지 구현 가능한지 궁금하다.
