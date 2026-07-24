# Different Query Analysis

`retriever_comparison.md`에서 `Agreement = different`로 나온 query만 따로 모아 분석한 자료이다.

비교 기준:

- BM25: keyword 기반 sparse retrieval
- TF-IDF: term importance 기반 sparse retrieval
- Dense Ollama: embedding 기반 semantic retrieval

주의:

- `different`는 반드시 실패를 의미하지 않는다.
- 같은 section의 인접 chunk를 고른 경우도 있고, 실제로는 둘 다 관련 있는 경우도 있다.
- BM25/TF-IDF/Dense의 score는 계산 방식이 달라 서로 직접 비교하면 안 된다.

## Overall Pattern

| Pattern | Explanation |
|---|---|
| BM25와 TF-IDF가 같은 chunk를 고르는 경우가 많음 | 둘 다 query keyword와 chunk text의 단어 일치를 중요하게 보기 때문 |
| Dense는 인접 chunk나 broader context를 고르는 경향 | query 전체 의미를 embedding으로 비교하기 때문 |
| 고유명사/technical term query에서는 sparse가 강함 | Self-RAG처럼 정확한 단어가 중요한 경우 BM25/TF-IDF가 본문 설명 chunk를 잘 찾음 |
| broad/paraphrased query에서는 Dense가 좋은 경우도 있음 | 정확한 용어 대신 의미를 풀어쓴 query에서 Dense가 의도에 가까운 chunk를 찾기도 함 |
| Figure/reference/overview chunk가 선택될 수 있음 | PDF 추출 결과에 figure text나 references가 chunk로 포함되어 있기 때문 |

---

## 1. retrieval granularity chunk entity

| Retriever | Top-1 Chunk | Content Summary |
|---|---|---|
| BM25 | `p5_c3` | token retrieval, text chunk, entity retrieval 등 세부 retrieval granularity 유형 설명 |
| TF-IDF | `p5_c3` | BM25와 동일 |
| Dense | `p4_c8` | retrieval granularity의 정의 설명 |

Analysis:

- BM25/TF-IDF는 query에 포함된 `chunk`, `entity`, `retrieval` keyword가 직접 많이 등장하는 `p5_c3`을 선택했다.
- Dense는 query 전체 의미를 보고 retrieval granularity의 정의가 나오는 `p4_c8`을 선택했다.
- 둘 다 관련 있는 chunk이며, 실패라기보다 keyword 중심 검색과 semantic 검색의 관점 차이로 볼 수 있다.

Presentation Point:

> Sparse retrievers selected the detailed chunk/entity explanation, while Dense selected the definition of retrieval granularity.

---

## 2. Self-RAG

| Retriever | Top-1 Chunk | Content Summary |
|---|---|---|
| BM25 | `p12_c4` | 본문에서 Self-RAG의 self-reflective mechanism 설명 |
| TF-IDF | `p12_c4` | BM25와 동일 |
| Dense | `p14_c4` | References에 있는 Self-RAG 논문 citation |

Analysis:

- `Self-RAG`는 고유 모델명이라 정확한 keyword matching이 중요하다.
- BM25/TF-IDF는 Self-RAG가 본문에서 설명되는 chunk를 선택했다.
- Dense는 Self-RAG 논문 제목이 있는 reference chunk를 선택했다.
- reference도 관련은 있지만, 답변 근거로는 본문 설명이 포함된 `p12_c4`가 더 적합하다.

Presentation Point:

> For exact model names, sparse retrievers can find the explanatory body text more directly than Dense.

---

## 3. How does RAG reduce hallucination?

| Retriever | Top-1 Chunk | Content Summary |
|---|---|---|
| BM25 | `p2_c2` | LLM의 hallucination 문제와 한계 설명 |
| TF-IDF | `p2_c2` | BM25와 동일 |
| Dense | `p14_c1` | retrieval로 최신 외부 정보를 제공해 hallucination/outdated knowledge를 완화한다는 결론부 설명 |

Analysis:

- BM25/TF-IDF는 `hallucination` keyword가 직접 등장하는 문제 제기 chunk를 선택했다.
- Dense는 질문의 의미인 “RAG가 어떻게 hallucination을 줄이는가”에 더 가까운 해결 설명 chunk를 선택했다.
- 이 사례는 natural-language query에서 Dense가 keyword matching보다 의도에 가까운 chunk를 찾을 수 있음을 보여준다.

Presentation Point:

> Sparse found the problem statement, while Dense found the explanation of how retrieval helps reduce hallucination.

---

## 4. What are training-free RAG methods?

| Retriever | Top-1 Chunk | Content Summary |
|---|---|---|
| BM25 | `p10_c1` | training-free approaches와 training-based approaches의 분류, prompt/retrieval-guided method 언급 |
| TF-IDF | `p9_c7` | Section 4.1 Training-free 시작 부분 |
| Dense | `p9_c5` | train-free vs training-based의 큰 분류를 소개하는 Section 4 개요 |

Analysis:

- 세 retriever 모두 training section 주변을 찾았다.
- BM25는 methods 분류가 더 직접적으로 나오는 chunk를 선택했다.
- TF-IDF는 `Training-free` section의 시작 chunk를 선택했다.
- Dense는 training 여부에 따른 전체 분류 개요 chunk를 선택했다.
- 모두 관련은 있지만, 질문에 가장 직접적으로 답하는 것은 BM25 결과로 볼 수 있다.

Presentation Point:

> All methods stayed near the right section, but BM25 returned the most method-specific chunk.

---

## 5. What is the difference between sparse retrieval and dense retrieval?

| Retriever | Top-1 Chunk | Content Summary |
|---|---|---|
| BM25 | `p4_c2` | sparse=word-based, dense=vector-space embedding 기반이라는 차이 직접 설명 |
| TF-IDF | `p4_c2` | BM25와 동일 |
| Dense | `p4_c3` | sparse retrieval의 한계와 dense retrieval 설명이 이어지는 chunk |

Analysis:

- BM25/TF-IDF는 sparse와 dense의 정의가 직접 함께 나오는 `p4_c2`를 선택했다.
- Dense는 바로 이어지는 `p4_c3`을 선택했다.
- `p4_c3`도 관련 있지만, 정의가 직접 있는 `p4_c2`가 더 직접적이다.
- 이는 chunk boundary 때문에 인접 chunk가 갈린 사례다.

Presentation Point:

> Different result, but both chunks are adjacent and relevant.

---

## 6. What are pre-retrieval and post-retrieval techniques?

| Retriever | Top-1 Chunk | Content Summary |
|---|---|---|
| BM25 | `p4_c1` | retrieval process와 pre/post-retrieval을 소개하는 section opening |
| TF-IDF | `p5_c4` | entity retrieval 관련 내용으로 다소 빗나감 |
| Dense | `p4_c1` | BM25와 동일 |

Analysis:

- BM25와 Dense는 pre/post-retrieval을 소개하는 section 시작 chunk를 선택했다.
- TF-IDF는 entity retrieval chunk를 선택했는데, query term과 일부 단어가 겹치면서 잘못 끌린 것으로 보인다.
- 이 사례에서는 BM25/Dense가 더 적절하다.

Presentation Point:

> TF-IDF can be sensitive to term overlap and may select a less relevant neighboring technical chunk.

---

## 7. How is Wikipedia used as an external database in RAG?

| Retriever | Top-1 Chunk | Content Summary |
|---|---|---|
| BM25 | `p6_c7` | database가 key-value/embedding 형태로 구성되는 방식 설명 |
| TF-IDF | `p6_c7` | BM25와 동일 |
| Dense | `p14_c0` | Wikipedia external knowledge quality와 future challenge 관련 내용 |

Analysis:

- BM25/TF-IDF는 `database`, `external`, `RAG` keyword가 직접 등장하는 database construction chunk를 선택했다.
- Dense는 Wikipedia와 external knowledge quality가 언급되는 future challenge chunk를 선택했다.
- 질문이 “RAG database로 Wikipedia가 어떻게 쓰이는가”라면 BM25/TF-IDF가 더 직접적이다.
- 질문이 “Wikipedia external knowledge의 품질 문제”라면 Dense 결과도 관련 있다.

Presentation Point:

> Sparse focused on database construction, while Dense focused on Wikipedia as external knowledge quality.

---

## 8. What is input-layer integration?

| Retriever | Top-1 Chunk | Content Summary |
|---|---|---|
| BM25 | `p8_c2` | Retrieval Integration for Generation Augmentation section 시작 |
| TF-IDF | `p8_c2` | BM25와 동일 |
| Dense | `p8_c5` | output-layer integration 설명 |

Analysis:

- BM25/TF-IDF는 input-layer integration이 나오는 section 앞부분을 선택했다.
- Dense는 `integration`의 의미적 유사성 때문에 output-layer integration chunk를 선택했다.
- input/output/intermediate integration은 같은 section에 있어 Dense가 혼동할 수 있다.
- 이 사례에서는 BM25/TF-IDF가 더 적절하다.

Presentation Point:

> Dense confused closely related integration concepts within the same section.

---

## 9. What are independent training, sequential training, and joint training?

| Retriever | Top-1 Chunk | Content Summary |
|---|---|---|
| BM25 | `p9_c6` | training-free, independent, sequential, joint training 분류가 소개되는 부분 |
| TF-IDF | `p9_c6` | BM25와 동일 |
| Dense | `p9_c7` | 네 가지 training methods를 review한다고 말하는 바로 다음 chunk |

Analysis:

- BM25/TF-IDF는 여러 training keyword가 직접 들어간 chunk를 선택했다.
- Dense는 바로 이어지는 training-free section 시작 chunk를 선택했다.
- 둘 다 같은 section의 인접 chunk라 관련성이 높다.
- 다른 결과지만 실패로 보기 어렵다.

Presentation Point:

> This is an adjacent-chunk difference rather than a clear retrieval failure.

---

## 10. What are the future challenges of RA-LLMs?

| Retriever | Top-1 Chunk | Content Summary |
|---|---|---|
| BM25 | `p13_c3` | future challenges section 근처, domain-specific/finance 이후 future directions로 넘어가는 부분 |
| TF-IDF | `p13_c3` | BM25와 동일 |
| Dense | `p1_c2` | abstract/introduction에서 architectures, training strategies, applications, future research를 개괄 |

Analysis:

- BM25/TF-IDF는 `future`, `challenges`, `RA-LLMs` keyword가 등장하는 후반부를 선택했다.
- Dense는 논문 전체 개요와 future research 언급이 있는 introduction chunk를 선택했다.
- Dense는 broad query에서 overview chunk로 이동하는 경향이 있다.
- 실제 future challenges를 찾으려면 BM25/TF-IDF 쪽이 더 직접적이다.

Presentation Point:

> Dense may drift to abstract/overview chunks for broad section-level queries.

---

## 11. Why can irrelevant retrieved passages hurt generation?

| Retriever | Top-1 Chunk | Content Summary |
|---|---|---|
| BM25 | `p9_c0` | irrelevant retrieved passages가 incorrect response/hallucination을 유발할 수 있다는 retrieval necessity 부분 |
| TF-IDF | `p9_c0` | BM25와 동일 |
| Dense | `p6_c6` | retrieved documents를 summary로 압축하는 RECOMP/context compression 관련 chunk |

Analysis:

- BM25/TF-IDF는 `irrelevant`, `retrieved passages`, `generation` 관련 문제 설명 chunk를 선택했다.
- Dense는 retrieved documents 처리/압축 관련 chunk를 선택했다.
- Dense 결과도 retrieval 후처리와 관련은 있지만, 질문의 핵심인 “irrelevant passage가 왜 해로운가”와는 거리가 있다.
- 이 사례에서는 sparse 결과가 더 직접적이다.

Presentation Point:

> Sparse found the risk of irrelevant retrieval, while Dense moved to context compression.

---

## 12. What applications use retrieval-augmented large language models?

| Retriever | Top-1 Chunk | Content Summary |
|---|---|---|
| BM25 | `p11_c7` | MIPS/joint training 관련 chunk로 application 질문에는 다소 애매함 |
| TF-IDF | `p11_c7` | BM25와 동일 |
| Dense | `p1_c1` | abstract에서 RAG의 다양한 task/application 가능성 언급 |

Analysis:

- 이 query는 넓은 applications section을 의도했지만, BM25/TF-IDF는 `retrieval-augmented large language models` 단어에 끌려 training/retrieval chunk를 선택했다.
- Dense는 abstract의 broad application 설명을 선택했다.
- 그러나 구체적인 applications section은 page 12~13 쪽이므로 세 결과 모두 완벽하다고 보기는 어렵다.
- broad query에서는 query formulation이 중요하다.

Presentation Point:

> Broad application queries were difficult for all retrievers; adding more specific terms such as QA, chatbot, recommendation may help.

---

## 13. How can the model use outside knowledge to avoid wrong answers?

| Retriever | Top-1 Chunk | Content Summary |
|---|---|---|
| BM25 | `p8_c7` | intermediate-layer integration과 model capability 향상 관련 chunk |
| TF-IDF | `p8_c7` | BM25와 동일 |
| Dense | `p9_c8` | model parameters에만 의존하지 않고 retrieval로 external sources에서 knowledge를 얻는 training-free 설명 |

Analysis:

- 이 query는 `hallucination`, `RAG`, `external knowledge` 같은 논문 keyword를 직접 쓰지 않고 의미를 풀어쓴 paraphrased query이다.
- BM25/TF-IDF는 `model`, `knowledge` 같은 단어에 반응해 architecture 쪽 chunk를 선택했다.
- Dense는 “내부 parameter에만 의존하지 않고 외부 지식을 활용한다”는 의미에 가까운 chunk를 선택했다.
- Dense가 더 의도에 가까운 사례로 볼 수 있다.

Presentation Point:

> Dense performed better on this paraphrased natural-language query.

---

## 14. How does the system decide whether to retrieve more information?

| Retriever | Top-1 Chunk | Content Summary |
|---|---|---|
| BM25 | `p2_c4` | out-of-scope query에 대해 RAG가 external knowledge를 retrieve하는 예시 |
| TF-IDF | `p4_c1` | retrieval이 필요한지 판단하는 mechanism 소개 |
| Dense | `p4_c1` | TF-IDF와 동일 |

Analysis:

- 질문 의도는 retrieval necessity, 즉 언제 retrieval을 호출할지에 가깝다.
- TF-IDF와 Dense는 이 mechanism이 소개되는 `p4_c1`을 선택했다.
- BM25는 `retrieve`, `information`, `system` 같은 일반 단어에 끌려 RAG 예시 chunk를 선택했다.
- 이 사례에서는 Dense/TF-IDF가 더 적절하다.

Presentation Point:

> Dense and TF-IDF found the retrieval-necessity section, while BM25 matched more literal but broader terms.

---

## 15. What methods modify the user question before searching?

| Retriever | Top-1 Chunk | Content Summary |
|---|---|---|
| BM25 | `p10_c2` | prompt/input query를 refining하는 training-free prompt engineering 부분 |
| TF-IDF | `p6_c6` | retrieved documents를 summary로 압축하는 context compression 부분 |
| Dense | `p1_c3` | introduction beginning |

Analysis:

- 의도는 query rewriting/query expansion이지만, query에 해당 technical term을 직접 쓰지 않았다.
- 세 retriever 모두 정확한 query rewriting chunk를 top-1로 찾지 못했다.
- 이는 paraphrased query가 너무 멀어지면 dense도 반드시 성공하지 않는다는 사례다.
- 더 좋은 query는 `How can RAG rewrite or expand a query before retrieval?`처럼 핵심 용어를 일부 포함하는 것이다.

Presentation Point:

> A paraphrase that is too far from the paper terminology can be difficult for all retrievers.

---

## 16. How can external documents make generated answers more reliable?

| Retriever | Top-1 Chunk | Content Summary |
|---|---|---|
| BM25 | `p1_c4` | external databases가 faithful/timely knowledge를 제공한다는 introduction 설명 |
| TF-IDF | `p1_c4` | BM25와 동일 |
| Dense | `p10_c3` | GENREAD/context document를 생성하고 answer를 만드는 training-free method 설명 |

Analysis:

- BM25/TF-IDF는 `external`, `generated`, `reliable`에 직접 반응해 introduction의 외부 지식 설명을 선택했다.
- Dense는 generated answers와 contextual documents를 연결해 GENREAD 관련 chunk를 선택했다.
- 두 방향 모두 관련 있지만, 질문이 RAG의 일반 원리라면 sparse 결과가 더 자연스럽고, method 사례를 찾는다면 Dense 결과도 의미가 있다.

Presentation Point:

> Dense connected the query to a specific generation-with-context method, while sparse selected the general external-knowledge explanation.

---

## 17. What happens when retrieved information is noisy or unrelated?

| Retriever | Top-1 Chunk | Content Summary |
|---|---|---|
| BM25 | `p6_c4` | retrieved information이 irrelevant/noisy하면 generation을 해칠 수 있고 mitigation strategy가 필요함 |
| TF-IDF | `p9_c1` | non-relevant retrieved passages가 hallucination rate를 높일 수 있음 |
| Dense | `p9_c3` | retrieval frequency/stride 설명 |

Analysis:

- BM25와 TF-IDF는 서로 다른 chunk를 골랐지만 둘 다 noisy/irrelevant retrieval의 위험과 관련 있다.
- Dense는 retrieval frequency 쪽으로 이동해 질문 핵심에서 벗어났다.
- 이 query에서는 sparse retrievers가 더 직접적인 근거를 찾았다.

Presentation Point:

> Sparse retrieval was stronger for noisy/irrelevant retrieval risk because the relevant wording appears explicitly in the paper.

---

## 18. How can a model answer questions about information not seen during training?

| Retriever | Top-1 Chunk | Content Summary |
|---|---|---|
| BM25 | `p9_c5` | training-free/training-based 분류 개요, retrieval frequency와 training section으로 넘어가는 부분 |
| TF-IDF | `p9_c5` | BM25와 동일 |
| Dense | `p9_c8` | model parameters에만 의존하지 않고 external sources에서 knowledge를 동적으로 획득한다는 설명 |

Analysis:

- query는 “학습 때 보지 못한 정보에 어떻게 답하는가”를 묻는 paraphrased semantic query이다.
- BM25/TF-IDF는 `training`, `information` keyword를 기준으로 Section 4 개요 chunk를 선택했다.
- Dense는 내부 parameter에만 의존하지 않고 external knowledge를 retrieve한다는 의미에 더 가까운 chunk를 선택했다.
- Dense가 더 좋은 사례로 볼 수 있다.

Presentation Point:

> Dense can be more useful when the query is paraphrased and asks for the meaning rather than exact paper terminology.

---

## Final Summary for Presentation

`different` query들을 분석하면 다음과 같은 결론을 낼 수 있다.

1. BM25와 TF-IDF는 대부분 비슷한 경향을 보였다.
   - 둘 다 sparse retrieval이라 query keyword와 chunk text의 직접 일치를 중요하게 보기 때문이다.

2. Dense는 더 넓은 의미나 인접 section을 고르는 경향이 있었다.
   - 때로는 질문 의도에 더 가까웠지만, 때로는 abstract/reference/overview chunk로 drift했다.

3. `different`가 반드시 실패는 아니다.
   - `retrieval granularity`, `sparse vs dense retrieval`, `training strategy`처럼 같은 section의 인접 chunk를 고른 경우가 있다.

4. 정확한 technical term query에서는 BM25/TF-IDF가 강했다.
   - `Self-RAG`, `query rewriting`, `input-layer integration` 같은 query는 정확한 단어가 중요하다.

5. paraphrased natural-language query에서는 Dense가 강점을 보인 사례가 있다.
   - `outside knowledge to avoid wrong answers`
   - `information not seen during training`

6. 하지만 paraphrase query에서도 Dense가 항상 이기지는 않았다.
   - query가 논문 용어와 너무 멀어지면 세 retriever 모두 정확한 chunk를 못 찾을 수 있다.

Presentation conclusion:

> In this experiment, sparse retrievers were strong for exact technical-term queries, while Dense retrieval showed potential for paraphrased semantic queries. However, Dense sometimes selected broader overview or adjacent chunks, so retrieval results should be interpreted together with the chunk preview.
