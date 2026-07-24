# Retriever Comparison

BM25, TF-IDF, Dense Ollama retriever의 검색 결과를 같은 query 기준으로 비교한 리포트입니다.

## Top-1 Summary

| Query | BM25 | TFIDF | DENSE | Agreement |
| --- | --- | --- | --- | --- |
| BM25 sparse retrieval | survey_on_rag2_p4_c2<br>p.4 c.2<br>10.2536 | survey_on_rag2_p4_c2<br>p.4 c.2<br>0.3206 | survey_on_rag2_p4_c2<br>p.4 c.2<br>0.6840 | same |
| dense retrieval embedding | survey_on_rag2_p4_c4<br>p.4 c.4<br>8.4658 | survey_on_rag2_p4_c4<br>p.4 c.4<br>0.2264 | survey_on_rag2_p4_c4<br>p.4 c.4<br>0.7364 | same |
| retrieval granularity chunk entity | survey_on_rag2_p5_c3<br>p.5 c.3<br>16.0179 | survey_on_rag2_p5_c3<br>p.5 c.3<br>0.3865 | survey_on_rag2_p4_c8<br>p.4 c.8<br>0.8137 | different |
| query rewriting | survey_on_rag2_p6_c1<br>p.6 c.1<br>7.6821 | survey_on_rag2_p6_c1<br>p.6 c.1<br>0.3090 | survey_on_rag2_p6_c1<br>p.6 c.1<br>0.7195 | same |
| Self-RAG | survey_on_rag2_p12_c4<br>p.12 c.4<br>3.8745 | survey_on_rag2_p12_c4<br>p.12 c.4<br>0.1368 | survey_on_rag2_p14_c4<br>p.14 c.4<br>0.5545 | different |
| How does RAG reduce hallucination? | survey_on_rag2_p2_c2<br>p.2 c.2<br>4.7946 | survey_on_rag2_p2_c2<br>p.2 c.2<br>0.0789 | survey_on_rag2_p14_c1<br>p.14 c.1<br>0.5949 | different |
| What are training-free RAG methods? | survey_on_rag2_p10_c1<br>p.10 c.1<br>7.3679 | survey_on_rag2_p9_c7<br>p.9 c.7<br>0.1854 | survey_on_rag2_p9_c5<br>p.9 c.5<br>0.6831 | different |
| What is the difference between sparse retrieval and dense retrieval? | survey_on_rag2_p4_c2<br>p.4 c.2<br>15.3329 | survey_on_rag2_p4_c2<br>p.4 c.2<br>0.2761 | survey_on_rag2_p4_c3<br>p.4 c.3<br>0.7296 | different |
| What is retrieval granularity in RAG? | survey_on_rag2_p4_c8<br>p.4 c.8<br>10.8842 | survey_on_rag2_p4_c8<br>p.4 c.8<br>0.3599 | survey_on_rag2_p4_c8<br>p.4 c.8<br>0.8829 | same |
| What are pre-retrieval and post-retrieval techniques? | survey_on_rag2_p4_c1<br>p.4 c.1<br>9.1591 | survey_on_rag2_p5_c4<br>p.5 c.4<br>0.1263 | survey_on_rag2_p4_c1<br>p.4 c.1<br>0.7240 | different |
| How is Wikipedia used as an external database in RAG? | survey_on_rag2_p6_c7<br>p.6 c.7<br>11.8128 | survey_on_rag2_p6_c7<br>p.6 c.7<br>0.2185 | survey_on_rag2_p14_c0<br>p.14 c.0<br>0.6892 | different |
| What is input-layer integration? | survey_on_rag2_p8_c2<br>p.8 c.2<br>9.2643 | survey_on_rag2_p8_c2<br>p.8 c.2<br>0.3003 | survey_on_rag2_p8_c5<br>p.8 c.5<br>0.6490 | different |
| What is output-layer integration? | survey_on_rag2_p8_c5<br>p.8 c.5<br>11.5751 | survey_on_rag2_p8_c5<br>p.8 c.5<br>0.4287 | survey_on_rag2_p8_c5<br>p.8 c.5<br>0.6998 | same |
| What is intermediate-layer integration? | survey_on_rag2_p8_c6<br>p.8 c.6<br>9.7364 | survey_on_rag2_p8_c6<br>p.8 c.6<br>0.2713 | survey_on_rag2_p8_c6<br>p.8 c.6<br>0.6375 | same |
| What are independent training, sequential training, and joint training? | survey_on_rag2_p9_c6<br>p.9 c.6<br>21.4215 | survey_on_rag2_p9_c6<br>p.9 c.6<br>0.3571 | survey_on_rag2_p9_c7<br>p.9 c.7<br>0.7061 | different |
| What are the future challenges of RA-LLMs? | survey_on_rag2_p13_c3<br>p.13 c.3<br>16.1196 | survey_on_rag2_p13_c3<br>p.13 c.3<br>0.2781 | survey_on_rag2_p1_c2<br>p.1 c.2<br>0.7390 | different |
| Why can irrelevant retrieved passages hurt generation? | survey_on_rag2_p9_c0<br>p.9 c.0<br>11.0445 | survey_on_rag2_p9_c0<br>p.9 c.0<br>0.2119 | survey_on_rag2_p6_c6<br>p.6 c.6<br>0.6584 | different |
| What applications use retrieval-augmented large language models? | survey_on_rag2_p11_c7<br>p.11 c.7<br>7.7573 | survey_on_rag2_p11_c7<br>p.11 c.7<br>0.1841 | survey_on_rag2_p1_c1<br>p.1 c.1<br>0.7976 | different |
| How can the model use outside knowledge to avoid wrong answers? | survey_on_rag2_p8_c7<br>p.8 c.7<br>10.4938 | survey_on_rag2_p8_c7<br>p.8 c.7<br>0.1668 | survey_on_rag2_p9_c8<br>p.9 c.8<br>0.6897 | different |
| How does the system decide whether to retrieve more information? | survey_on_rag2_p2_c4<br>p.2 c.4<br>10.8123 | survey_on_rag2_p4_c1<br>p.4 c.1<br>0.1244 | survey_on_rag2_p4_c1<br>p.4 c.1<br>0.5963 | different |
| What methods modify the user question before searching? | survey_on_rag2_p10_c2<br>p.10 c.2<br>8.6142 | survey_on_rag2_p6_c6<br>p.6 c.6<br>0.1458 | survey_on_rag2_p1_c3<br>p.1 c.3<br>0.5882 | different |
| How can external documents make generated answers more reliable? | survey_on_rag2_p1_c4<br>p.1 c.4<br>10.2978 | survey_on_rag2_p1_c4<br>p.1 c.4<br>0.1891 | survey_on_rag2_p10_c3<br>p.10 c.3<br>0.6522 | different |
| What happens when retrieved information is noisy or unrelated? | survey_on_rag2_p6_c4<br>p.6 c.4<br>7.1578 | survey_on_rag2_p9_c1<br>p.9 c.1<br>0.1221 | survey_on_rag2_p9_c3<br>p.9 c.3<br>0.5803 | different |
| How can a model answer questions about information not seen during training? | survey_on_rag2_p9_c5<br>p.9 c.5<br>11.4551 | survey_on_rag2_p9_c5<br>p.9 c.5<br>0.1773 | survey_on_rag2_p9_c8<br>p.9 c.8<br>0.7019 | different |
| How can retrieved passages be shortened before being given to the generator? | survey_on_rag2_p6_c6<br>p.6 c.6<br>15.8203 | survey_on_rag2_p6_c6<br>p.6 c.6<br>0.2600 | survey_on_rag2_p6_c6<br>p.6 c.6<br>0.6536 | same |

## Detailed Results

### BM25 sparse retrieval

#### BM25

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 10.2536 | survey_on_rag2_p4_c2 | 4 | we will introduce the major techniques involved in the retrieval of tradi- tional and LLM-based RAGs, including the retriever type, retrieval granularity, pre-... |
| 2 | 7.7527 | survey_on_rag2_p11_c1 | 11 | given input. Regarding the retriever, it can be categorized into two types: 1) Sparse retriever [120, 125], and 2) Dense retriever [61, 69, 197]. The sparse ret... |

#### TFIDF

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.3206 | survey_on_rag2_p4_c2 | 4 | we will introduce the major techniques involved in the retrieval of tradi- tional and LLM-based RAGs, including the retriever type, retrieval granularity, pre-... |
| 2 | 0.1891 | survey_on_rag2_p11_c1 | 11 | given input. Regarding the retriever, it can be categorized into two types: 1) Sparse retriever [120, 125], and 2) Dense retriever [61, 69, 197]. The sparse ret... |

#### DENSE

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.6840 | survey_on_rag2_p4_c2 | 4 | we will introduce the major techniques involved in the retrieval of tradi- tional and LLM-based RAGs, including the retriever type, retrieval granularity, pre-... |
| 2 | 0.6725 | survey_on_rag2_p4_c3 | 4 | 117, 168, 196, 197], where passages are specifically represented as a bag of words and ranked based on term and inverse docu- ment frequencies [ 54]. On top of... |

### dense retrieval embedding

#### BM25

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 8.4658 | survey_on_rag2_p4_c4 | 4 | and docu- ments into continuous vector space with certain criteria, for exam- ple, semantic similarity [61]. Dense retrieval methods are usually trainable, ther... |
| 2 | 7.9205 | survey_on_rag2_p5_c1 | 5 | first symptom sign of a heart attack is sudden cardiac arrest. Angina pectoris is caused by a decrease in myocardial blood flow.  Figure 3: Illustration of the... |

#### TFIDF

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.2264 | survey_on_rag2_p4_c4 | 4 | and docu- ments into continuous vector space with certain criteria, for exam- ple, semantic similarity [61]. Dense retrieval methods are usually trainable, ther... |
| 2 | 0.1902 | survey_on_rag2_p5_c1 | 5 | first symptom sign of a heart attack is sudden cardiac arrest. Angina pectoris is caused by a decrease in myocardial blood flow.  Figure 3: Illustration of the... |

#### DENSE

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.7364 | survey_on_rag2_p4_c4 | 4 | and docu- ments into continuous vector space with certain criteria, for exam- ple, semantic similarity [61]. Dense retrieval methods are usually trainable, ther... |
| 2 | 0.6850 | survey_on_rag2_p4_c3 | 4 | 117, 168, 196, 197], where passages are specifically represented as a bag of words and ranked based on term and inverse docu- ment frequencies [ 54]. On top of... |

### retrieval granularity chunk entity

#### BM25

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 16.0179 | survey_on_rag2_p5_c3 | 5 | REALM [46], RAG [74] and Atlas [55]. A more fine-grained retrieval, i.e., token retrieval, instead can be done with faster searching but will bring more burden... |
| 2 | 12.1890 | survey_on_rag2_p4_c8 | 4 | and data. 3.1.2 Retrieval Granularity. Retrieval granularity denotes the re- trieval unit in which the corpus is indexed, e.g., document, passage, token, or oth... |

#### TFIDF

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.3865 | survey_on_rag2_p5_c3 | 5 | REALM [46], RAG [74] and Atlas [55]. A more fine-grained retrieval, i.e., token retrieval, instead can be done with faster searching but will bring more burden... |
| 2 | 0.3604 | survey_on_rag2_p4_c8 | 4 | and data. 3.1.2 Retrieval Granularity. Retrieval granularity denotes the re- trieval unit in which the corpus is indexed, e.g., document, passage, token, or oth... |

#### DENSE

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.8137 | survey_on_rag2_p4_c8 | 4 | and data. 3.1.2 Retrieval Granularity. Retrieval granularity denotes the re- trieval unit in which the corpus is indexed, e.g., document, passage, token, or oth... |
| 2 | 0.7015 | survey_on_rag2_p5_c3 | 5 | REALM [46], RAG [74] and Atlas [55]. A more fine-grained retrieval, i.e., token retrieval, instead can be done with faster searching but will bring more burden... |

### query rewriting

#### BM25

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 7.6821 | survey_on_rag2_p6_c1 | 6 | of the rewriting step is to clarify the retrieval need in the new query to ease the burden on the retrieval function to comprehend the input and enhance the out... |
| 2 | 5.8957 | survey_on_rag2_p6_c0 | 6 | Conference’17, July 2017, Washington, DC, USA Wenqi Fan, Yujuan Ding, Liangbo Ning, Shijie Wang, Hengyun Li, Dawei Yin, Tat-Seng Chua, and Qing Li on ad-hoc inf... |

#### TFIDF

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.3090 | survey_on_rag2_p6_c1 | 6 | of the rewriting step is to clarify the retrieval need in the new query to ease the burden on the retrieval function to comprehend the input and enhance the out... |
| 2 | 0.1809 | survey_on_rag2_p6_c0 | 6 | Conference’17, July 2017, Washington, DC, USA Wenqi Fan, Yujuan Ding, Liangbo Ning, Shijie Wang, Hengyun Li, Dawei Yin, Tat-Seng Chua, and Qing Li on ad-hoc inf... |

#### DENSE

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.7195 | survey_on_rag2_p6_c1 | 6 | of the rewriting step is to clarify the retrieval need in the new query to ease the burden on the retrieval function to comprehend the input and enhance the out... |
| 2 | 0.5917 | survey_on_rag2_p6_c0 | 6 | Conference’17, July 2017, Washington, DC, USA Wenqi Fan, Yujuan Ding, Liangbo Ning, Shijie Wang, Hengyun Li, Dawei Yin, Tat-Seng Chua, and Qing Li on ad-hoc inf... |

### Self-RAG

#### BM25

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 3.8745 | survey_on_rag2_p12_c4 | 12 | nature of knowledge in the world, another model [152] further accesses large amounts of dynamic information in search engines to generate responses. 5.1.3 Fact... |
| 2 | 2.7607 | survey_on_rag2_p14_c4 | 14 | Zeqiu Wu, Yizhong Wang, Avirup Sil, and Hannaneh Hajishirzi. 2023. Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection. In The Twelft... |

#### TFIDF

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.1368 | survey_on_rag2_p12_c4 | 12 | nature of knowledge in the world, another model [152] further accesses large amounts of dynamic information in search engines to generate responses. 5.1.3 Fact... |
| 2 | 0.0817 | survey_on_rag2_p9_c1 | 9 | re- trieved passages than on the relevant ones. Therefore, it is critical for RA-LLMs to accurately recall the prior knowledge while selec- tively incorporating... |

#### DENSE

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.5545 | survey_on_rag2_p14_c4 | 14 | Zeqiu Wu, Yizhong Wang, Avirup Sil, and Hannaneh Hajishirzi. 2023. Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection. In The Twelft... |
| 2 | 0.5180 | survey_on_rag2_p3_c0 | 3 | A Survey on RAG Meeting LLMs: Towards Retrieval-Augmented Large Language Models Conference’17, July 2017, Washington, DC, USA 2019 2020 2021 2022 2023 2024 RAG... |

### How does RAG reduce hallucination?

#### BM25

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 4.7946 | survey_on_rag2_p2_c2 | 2 | multi-modal fashion report generation [27]. LLMs also achieve promising performance in recommender systems by understanding users’ preferences to- wards items [... |
| 2 | 4.7786 | survey_on_rag2_p16_c2 | 16 | (1). Association for Computational Linguistics, 4582–4597. [84] Zonglin Li, Ruiqi Guo, and Sanjiv Kumar. 2022. Decoupled context processing for context augmente... |

#### TFIDF

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.0789 | survey_on_rag2_p2_c2 | 2 | multi-modal fashion report generation [27]. LLMs also achieve promising performance in recommender systems by understanding users’ preferences to- wards items [... |
| 2 | 0.0766 | survey_on_rag2_p2_c3 | 2 | due to the substantial computational resources required for fine-tuning LLMs with domain-specific or the latest data. This, in turn, significantly hinders the w... |

#### DENSE

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.5949 | survey_on_rag2_p14_c1 | 14 | By enhancing the quality of the external knowledge and tailing robust mechanisms by filtering out low-quality or unreliable information, the RA-LLM systems migh... |
| 2 | 0.5943 | survey_on_rag2_p2_c3 | 2 | due to the substantial computational resources required for fine-tuning LLMs with domain-specific or the latest data. This, in turn, significantly hinders the w... |

### What are training-free RAG methods?

#### BM25

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 7.3679 | survey_on_rag2_p10_c1 | 10 | Existing RA- LLMs approaches can be categorized into two classes: training-free approaches usually directly leverage retrieved information during the inference... |
| 2 | 6.8100 | survey_on_rag2_p9_c7 | 9 | train retriever and generator simultaneously. In the following section, we will comprehensively review the training-free, independent training, sequential train... |

#### TFIDF

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.1854 | survey_on_rag2_p9_c7 | 9 | train retriever and generator simultaneously. In the following section, we will comprehensively review the training-free, independent training, sequential train... |
| 2 | 0.1547 | survey_on_rag2_p10_c1 | 10 | Existing RA- LLMs approaches can be categorized into two classes: training-free approaches usually directly leverage retrieved information during the inference... |

#### DENSE

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.6831 | survey_on_rag2_p9_c5 | 9 | strat- egy, which retrieves information for the prediction of every token during the generation. Overall, applying different frequencies of re- trieval can impa... |
| 2 | 0.6656 | survey_on_rag2_p10_c1 | 10 | Existing RA- LLMs approaches can be categorized into two classes: training-free approaches usually directly leverage retrieved information during the inference... |

### What is the difference between sparse retrieval and dense retrieval?

#### BM25

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 15.3329 | survey_on_rag2_p4_c2 | 4 | we will introduce the major techniques involved in the retrieval of tradi- tional and LLM-based RAGs, including the retriever type, retrieval granularity, pre-... |
| 2 | 14.6225 | survey_on_rag2_p4_c3 | 4 | 117, 168, 196, 197], where passages are specifically represented as a bag of words and ranked based on term and inverse docu- ment frequencies [ 54]. On top of... |

#### TFIDF

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.2761 | survey_on_rag2_p4_c2 | 4 | we will introduce the major techniques involved in the retrieval of tradi- tional and LLM-based RAGs, including the retriever type, retrieval granularity, pre-... |
| 2 | 0.2426 | survey_on_rag2_p4_c3 | 4 | 117, 168, 196, 197], where passages are specifically represented as a bag of words and ranked based on term and inverse docu- ment frequencies [ 54]. On top of... |

#### DENSE

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.7296 | survey_on_rag2_p4_c3 | 4 | 117, 168, 196, 197], where passages are specifically represented as a bag of words and ranked based on term and inverse docu- ment frequencies [ 54]. On top of... |
| 2 | 0.7229 | survey_on_rag2_p4_c2 | 4 | we will introduce the major techniques involved in the retrieval of tradi- tional and LLM-based RAGs, including the retriever type, retrieval granularity, pre-... |

### What is retrieval granularity in RAG?

#### BM25

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 10.8842 | survey_on_rag2_p4_c8 | 4 | and data. 3.1.2 Retrieval Granularity. Retrieval granularity denotes the re- trieval unit in which the corpus is indexed, e.g., document, passage, token, or oth... |
| 2 | 10.5717 | survey_on_rag2_p5_c3 | 5 | REALM [46], RAG [74] and Atlas [55]. A more fine-grained retrieval, i.e., token retrieval, instead can be done with faster searching but will bring more burden... |

#### TFIDF

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.3599 | survey_on_rag2_p4_c8 | 4 | and data. 3.1.2 Retrieval Granularity. Retrieval granularity denotes the re- trieval unit in which the corpus is indexed, e.g., document, passage, token, or oth... |
| 2 | 0.2806 | survey_on_rag2_p5_c3 | 5 | REALM [46], RAG [74] and Atlas [55]. A more fine-grained retrieval, i.e., token retrieval, instead can be done with faster searching but will bring more burden... |

#### DENSE

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.8829 | survey_on_rag2_p4_c8 | 4 | and data. 3.1.2 Retrieval Granularity. Retrieval granularity denotes the re- trieval unit in which the corpus is indexed, e.g., document, passage, token, or oth... |
| 2 | 0.7569 | survey_on_rag2_p4_c2 | 4 | we will introduce the major techniques involved in the retrieval of tradi- tional and LLM-based RAGs, including the retriever type, retrieval granularity, pre-... |

### What are pre-retrieval and post-retrieval techniques?

#### BM25

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 9.1591 | survey_on_rag2_p4_c1 | 4 | consists of several major processes: retrieval, generation, and augmentation, as well as the mechanism to determine whether the retrieval is needed. In this sec... |
| 2 | 8.7430 | survey_on_rag2_p5_c4 | 5 | (E AE) model, which divides the parameter space of language models according to the entity identity. The proposed EAE model aims to learn entity representations... |

#### TFIDF

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.1263 | survey_on_rag2_p5_c4 | 5 | (E AE) model, which divides the parameter space of language models according to the entity identity. The proposed EAE model aims to learn entity representations... |
| 2 | 0.1252 | survey_on_rag2_p4_c1 | 4 | consists of several major processes: retrieval, generation, and augmentation, as well as the mechanism to determine whether the retrieval is needed. In this sec... |

#### DENSE

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.7240 | survey_on_rag2_p4_c1 | 4 | consists of several major processes: retrieval, generation, and augmentation, as well as the mechanism to determine whether the retrieval is needed. In this sec... |
| 2 | 0.7048 | survey_on_rag2_p4_c2 | 4 | we will introduce the major techniques involved in the retrieval of tradi- tional and LLM-based RAGs, including the retriever type, retrieval granularity, pre-... |

### How is Wikipedia used as an external database in RAG?

#### BM25

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 11.8128 | survey_on_rag2_p6_c7 | 6 | stores key-value pairs for knowledge, which can be constructed in various ways. The keys are primarily used for similarity matching, being as sparse vectors suc... |
| 2 | 11.4575 | survey_on_rag2_p14_c0 | 14 | Conference’17, July 2017, Washington, DC, USA Wenqi Fan, Yujuan Ding, Liangbo Ning, Shijie Wang, Hengyun Li, Dawei Yin, Tat-Seng Chua, and Qing Li Quality of Ex... |

#### TFIDF

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.2185 | survey_on_rag2_p6_c7 | 6 | stores key-value pairs for knowledge, which can be constructed in various ways. The keys are primarily used for similarity matching, being as sparse vectors suc... |
| 2 | 0.2172 | survey_on_rag2_p14_c0 | 14 | Conference’17, July 2017, Washington, DC, USA Wenqi Fan, Yujuan Ding, Liangbo Ning, Shijie Wang, Hengyun Li, Dawei Yin, Tat-Seng Chua, and Qing Li Quality of Ex... |

#### DENSE

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.6892 | survey_on_rag2_p14_c0 | 14 | Conference’17, July 2017, Washington, DC, USA Wenqi Fan, Yujuan Ding, Liangbo Ning, Shijie Wang, Hengyun Li, Dawei Yin, Tat-Seng Chua, and Qing Li Quality of Ex... |
| 2 | 0.6759 | survey_on_rag2_p1_c5 | 1 | query or the generated output [62, 103]. Specifically, RAG first invokes the retriever to search and extract the relevant documents from external databases, whi... |

### What is input-layer integration?

#### BM25

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 9.2643 | survey_on_rag2_p8_c2 | 8 | which can reduce the computational costs and also relieve the burden of LMs to identify relevant information in long retrieved documents. 3.3 Retrieval Integrat... |
| 2 | 8.5036 | survey_on_rag2_p8_c4 | 8 | at a time. In general, most black-box generation-based RAG methods apply input-layer integration since neither the intermediate layer of the generation model or... |

#### TFIDF

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.3003 | survey_on_rag2_p8_c2 | 8 | which can reduce the computational costs and also relieve the burden of LMs to identify relevant information in long retrieved documents. 3.3 Retrieval Integrat... |
| 2 | 0.2475 | survey_on_rag2_p8_c4 | 8 | at a time. In general, most black-box generation-based RAG methods apply input-layer integration since neither the intermediate layer of the generation model or... |

#### DENSE

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.6490 | survey_on_rag2_p8_c5 | 8 | Output-Layer Integration. Another kind of augmentation is post-hoc, i.e., output-layer integration, which joints retrieval and generation results. For example,... |
| 2 | 0.6270 | survey_on_rag2_p8_c6 | 8 | integration. REFEED [183] proposes an answer refining mechanism that applies an LLM to evaluate the retrieved information and adjust the initial answer accordin... |

### What is output-layer integration?

#### BM25

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 11.5751 | survey_on_rag2_p8_c5 | 8 | Output-Layer Integration. Another kind of augmentation is post-hoc, i.e., output-layer integration, which joints retrieval and generation results. For example,... |
| 2 | 9.4220 | survey_on_rag2_p8_c4 | 8 | at a time. In general, most black-box generation-based RAG methods apply input-layer integration since neither the intermediate layer of the generation model or... |

#### TFIDF

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.4287 | survey_on_rag2_p8_c5 | 8 | Output-Layer Integration. Another kind of augmentation is post-hoc, i.e., output-layer integration, which joints retrieval and generation results. For example,... |
| 2 | 0.2639 | survey_on_rag2_p8_c4 | 8 | at a time. In general, most black-box generation-based RAG methods apply input-layer integration since neither the intermediate layer of the generation model or... |

#### DENSE

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.6998 | survey_on_rag2_p8_c5 | 8 | Output-Layer Integration. Another kind of augmentation is post-hoc, i.e., output-layer integration, which joints retrieval and generation results. For example,... |
| 2 | 0.6190 | survey_on_rag2_p8_c6 | 8 | integration. REFEED [183] proposes an answer refining mechanism that applies an LLM to evaluate the retrieved information and adjust the initial answer accordin... |

### What is intermediate-layer integration?

#### BM25

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 9.7364 | survey_on_rag2_p8_c6 | 8 | integration. REFEED [183] proposes an answer refining mechanism that applies an LLM to evaluate the retrieved information and adjust the initial answer accordin... |
| 2 | 9.1206 | survey_on_rag2_p8_c8 | 8 | alternative to incorporate a large number of text chunks frequently retrieved, which are challenging to process with input-layer integration due to the input le... |

#### TFIDF

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.2713 | survey_on_rag2_p8_c6 | 8 | integration. REFEED [183] proposes an answer refining mechanism that applies an LLM to evaluate the retrieved information and adjust the initial answer accordin... |
| 2 | 0.2273 | survey_on_rag2_p8_c8 | 8 | alternative to incorporate a large number of text chunks frequently retrieved, which are challenging to process with input-layer integration due to the input le... |

#### DENSE

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.6375 | survey_on_rag2_p8_c6 | 8 | integration. REFEED [183] proposes an answer refining mechanism that applies an LLM to evaluate the retrieved information and adjust the initial answer accordin... |
| 2 | 0.6062 | survey_on_rag2_p8_c5 | 8 | Output-Layer Integration. Another kind of augmentation is post-hoc, i.e., output-layer integration, which joints retrieval and generation results. For example,... |

### What are independent training, sequential training, and joint training?

#### BM25

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 21.4215 | survey_on_rag2_p9_c6 | 9 | However, one potential challenge is that the retriever and generator components are not specifically optimized for downstream tasks, which could easily lead to... |
| 2 | 20.2136 | survey_on_rag2_p10_c1 | 10 | Existing RA- LLMs approaches can be categorized into two classes: training-free approaches usually directly leverage retrieved information during the inference... |

#### TFIDF

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.3571 | survey_on_rag2_p9_c6 | 9 | However, one potential challenge is that the retriever and generator components are not specifically optimized for downstream tasks, which could easily lead to... |
| 2 | 0.3343 | survey_on_rag2_p11_c2 | 11 | retrieval and reformulate the text generation as multiple copy-and-paste operations from existing source text collection. 4.3 Sequential Training Independent tr... |

#### DENSE

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.7061 | survey_on_rag2_p9_c7 | 9 | train retriever and generator simultaneously. In the following section, we will comprehensively review the training-free, independent training, sequential train... |
| 2 | 0.6937 | survey_on_rag2_p11_c2 | 11 | retrieval and reformulate the text generation as multiple copy-and-paste operations from existing source text collection. 4.3 Sequential Training Independent tr... |

### What are the future challenges of RA-LLMs?

#### BM25

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 16.1196 | survey_on_rag2_p13_c3 | 13 | analysis. In addition, financial QA is another primary task of financial analysis, which usually extracts relevant knowledge from financial docu- ments. As prof... |
| 2 | 12.8812 | survey_on_rag2_p1_c2 | 1 | existing research studies in RA-LLMs, covering three pri- mary technical perspectives: architectures, training strategies, and applications. As the preliminary... |

#### TFIDF

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.2781 | survey_on_rag2_p13_c3 | 13 | analysis. In addition, financial QA is another primary task of financial analysis, which usually extracts relevant knowledge from financial docu- ments. As prof... |
| 2 | 0.1730 | survey_on_rag2_p2_c5 | 2 | research from several primary perspectives of RA-LLMs in terms of retrieval, generation, and augmentation in Section 3, as well as the necessity and application... |

#### DENSE

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.7390 | survey_on_rag2_p1_c2 | 1 | existing research studies in RA-LLMs, covering three pri- mary technical perspectives: architectures, training strategies, and applications. As the preliminary... |
| 2 | 0.7133 | survey_on_rag2_p2_c5 | 2 | research from several primary perspectives of RA-LLMs in terms of retrieval, generation, and augmentation in Section 3, as well as the necessity and application... |

### Why can irrelevant retrieved passages hurt generation?

#### BM25

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 11.0445 | survey_on_rag2_p9_c0 | 9 | A Survey on RAG Meeting LLMs: Towards Retrieval-Augmented Large Language Models Conference’17, July 2017, Washington, DC, USA 3.4 Retrieval Augmentation Necessi... |
| 2 | 6.0027 | survey_on_rag2_p8_c6 | 8 | integration. REFEED [183] proposes an answer refining mechanism that applies an LLM to evaluate the retrieved information and adjust the initial answer accordin... |

#### TFIDF

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.2119 | survey_on_rag2_p9_c0 | 9 | A Survey on RAG Meeting LLMs: Towards Retrieval-Augmented Large Language Models Conference’17, July 2017, Washington, DC, USA 3.4 Retrieval Augmentation Necessi... |
| 2 | 0.1167 | survey_on_rag2_p6_c6 | 6 | which adds an intermediate step to process the retrieved documents into a textual summary before in-context augmentation in the generation process. From another... |

#### DENSE

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.6584 | survey_on_rag2_p6_c6 | 6 | which adds an intermediate step to process the retrieved documents into a textual summary before in-context augmentation in the generation process. From another... |
| 2 | 0.6205 | survey_on_rag2_p8_c3 | 8 | the origi- nal input and all retrieved documents into a single sequence as the new input for the generation model. Despite the effectiveness, such integration i... |

### What applications use retrieval-augmented large language models?

#### BM25

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 7.7573 | survey_on_rag2_p11_c7 | 11 | paradigm to that of RAG [74], and Maximum Inner Product Search (MIPS) [15, 29, 119, 131] technique is used to locate the most relevant documents. To employ MIPS... |
| 2 | 6.7752 | survey_on_rag2_p14_c1 | 14 | By enhancing the quality of the external knowledge and tailing robust mechanisms by filtering out low-quality or unreliable information, the RA-LLM systems migh... |

#### TFIDF

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.1841 | survey_on_rag2_p11_c7 | 11 | paradigm to that of RAG [74], and Maximum Inner Product Search (MIPS) [15, 29, 119, 131] technique is used to locate the most relevant documents. To employ MIPS... |
| 2 | 0.1586 | survey_on_rag2_p12_c1 | 12 | et al. [178], etc. Figure 6: A summary of applications of RA-LLMs categorized by NLP applications, downstream tasks, and domain-specific application. Specifical... |

#### DENSE

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.7976 | survey_on_rag2_p1_c1 | 1 | external knowl- edge, providing huge convenience for numerous tasks. Particularly in the era of AI-Generated Content (AIGC), the powerful capac- ity of retrieva... |
| 2 | 0.7946 | survey_on_rag2_p14_c2 | 14 | by leveraging retrieval to provide the latest auxiliary information and teaching LLMs to harness the retrieved external knowledge. With the rapid advancements i... |

### How can the model use outside knowledge to avoid wrong answers?

#### BM25

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 10.4938 | survey_on_rag2_p8_c7 | 8 | add addi- tional complexity and is promising to enhance the capability of the generation model with effective training. Typically, a Transformer module is intro... |
| 2 | 9.3240 | survey_on_rag2_p7_c2 | 7 | [22, 39, 46, 62, 74, 117, 135, 168, 180] to trillion token- level [6]. Domain-specific database is also used for downstream tasks. For example, for the code gen... |

#### TFIDF

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.1668 | survey_on_rag2_p8_c7 | 8 | add addi- tional complexity and is promising to enhance the capability of the generation model with effective training. Typically, a Transformer module is intro... |
| 2 | 0.1635 | survey_on_rag2_p10_c3 | 10 | Instead of retrieving knowledge from a large corpus, GENREAD [182] first prompts a LLM to generate contextual documents based on the query, and then generate an... |

#### DENSE

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.6897 | survey_on_rag2_p9_c8 | 9 | [54, 57, 63], instead of relying solely on the implicit knowledge encoded in the model’s parameters. These approaches have shown significant performance improve... |
| 2 | 0.6377 | survey_on_rag2_p10_c3 | 10 | Instead of retrieving knowledge from a large corpus, GENREAD [182] first prompts a LLM to generate contextual documents based on the query, and then generate an... |

### How does the system decide whether to retrieve more information?

#### BM25

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 10.8123 | survey_on_rag2_p2_c4 | 2 | in conversational tasks [137, 171]. As illustrated in Figure 1, an LLM-based dialog system will not be able to answer well for out-of-scope queries. With the he... |
| 2 | 10.6734 | survey_on_rag2_p12_c3 | 12 | indicate that the quality of the answers may rely more on the output of retrieval. 5.1.2 ChatBot. ChatBot is designed to interact with users in a natural and co... |

#### TFIDF

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.1244 | survey_on_rag2_p4_c1 | 4 | consists of several major processes: retrieval, generation, and augmentation, as well as the mechanism to determine whether the retrieval is needed. In this sec... |
| 2 | 0.1235 | survey_on_rag2_p2_c4 | 2 | in conversational tasks [137, 171]. As illustrated in Figure 1, an LLM-based dialog system will not be able to answer well for out-of-scope queries. With the he... |

#### DENSE

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.5963 | survey_on_rag2_p4_c1 | 4 | consists of several major processes: retrieval, generation, and augmentation, as well as the mechanism to determine whether the retrieval is needed. In this sec... |
| 2 | 0.5805 | survey_on_rag2_p9_c2 | 9 | trainable models to offer self-knowledge as the reference for the adaptive calling of a retriever. In traditional RAGs, retrieval necessity judg- ment has also... |

### What methods modify the user question before searching?

#### BM25

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 8.6142 | survey_on_rag2_p10_c2 | 10 | the LLMs’ generation performance highly depends on the input query, numerous training- free RAG approaches employ external knowledge by refining the original pr... |
| 2 | 7.5505 | survey_on_rag2_p6_c6 | 6 | which adds an intermediate step to process the retrieved documents into a textual summary before in-context augmentation in the generation process. From another... |

#### TFIDF

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.1458 | survey_on_rag2_p6_c6 | 6 | which adds an intermediate step to process the retrieved documents into a textual summary before in-context augmentation in the generation process. From another... |
| 2 | 0.1145 | survey_on_rag2_p5_c2 | 5 | 4: Illustration of the retriever in RA-LLMs, which can be implemented in either dense or sparse manners, each with several key operations. granularity can signi... |

#### DENSE

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.5882 | survey_on_rag2_p1_c3 | 1 | Fine-tuning, In-context Learning, Prompting. ∗Corresponding author: Yujuan Ding 1This is the long version of the survey to appear at KDD 2024 [33] 1 INTRODUCTIO... |
| 2 | 0.5822 | survey_on_rag2_p4_c1 | 4 | consists of several major processes: retrieval, generation, and augmentation, as well as the mechanism to determine whether the retrieval is needed. In this sec... |

### How can external documents make generated answers more reliable?

#### BM25

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 10.2978 | survey_on_rag2_p1_c4 | 1 | in external databases, can provide faithful and timely external knowledge, thereby serving vital functions in various knowledge-intensive tasks. Due to their po... |
| 2 | 9.7011 | survey_on_rag2_p6_c2 | 6 | inspire the language model to rethink the generated results and enhance them. Com- pared to applying only the original query, such augmentation may contribute m... |

#### TFIDF

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.1891 | survey_on_rag2_p1_c4 | 1 | in external databases, can provide faithful and timely external knowledge, thereby serving vital functions in various knowledge-intensive tasks. Due to their po... |
| 2 | 0.1184 | survey_on_rag2_p10_c3 | 10 | Instead of retrieving knowledge from a large corpus, GENREAD [182] first prompts a LLM to generate contextual documents based on the query, and then generate an... |

#### DENSE

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.6522 | survey_on_rag2_p10_c3 | 10 | Instead of retrieving knowledge from a large corpus, GENREAD [182] first prompts a LLM to generate contextual documents based on the query, and then generate an... |
| 2 | 0.6378 | survey_on_rag2_p6_c2 | 6 | inspire the language model to rethink the generated results and enhance them. Com- pared to applying only the original query, such augmentation may contribute m... |

### What happens when retrieved information is noisy or unrelated?

#### BM25

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 7.1578 | survey_on_rag2_p6_c4 | 6 | for the task, or even worse, harm the generation process [159]. Wang et al. [159], Asai et al. [5], Yu et al. [183] propose different strategies to mitigate the... |
| 2 | 6.7920 | survey_on_rag2_p17_c6 | 17 | flow.arXiv preprint arXiv:2304.12825 (2023). [145] Ziteng Sun, Ananda Theertha Suresh, Jae Hun Ro, Ahmad Beirami, Himanshu Jain, and Felix Yu. 2024. Spectr: Fas... |

#### TFIDF

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.1221 | survey_on_rag2_p9_c1 | 9 | re- trieved passages than on the relevant ones. Therefore, it is critical for RA-LLMs to accurately recall the prior knowledge while selec- tively incorporating... |
| 2 | 0.1126 | survey_on_rag2_p6_c4 | 6 | for the task, or even worse, harm the generation process [159]. Wang et al. [159], Asai et al. [5], Yu et al. [183] propose different strategies to mitigate the... |

#### DENSE

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.5803 | survey_on_rag2_p9_c3 | 9 | re- trieval frequency (also called retrieval stride) is an important design aspect to determine the degree of using the retrieval in the gen- eration, thereby g... |
| 2 | 0.5678 | survey_on_rag2_p4_c8 | 4 | and data. 3.1.2 Retrieval Granularity. Retrieval granularity denotes the re- trieval unit in which the corpus is indexed, e.g., document, passage, token, or oth... |

### How can a model answer questions about information not seen during training?

#### BM25

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 11.4551 | survey_on_rag2_p9_c5 | 9 | strat- egy, which retrieves information for the prediction of every token during the generation. Overall, applying different frequencies of re- trieval can impa... |
| 2 | 10.4735 | survey_on_rag2_p12_c2 | 12 | 91]. To address this limitation, the integration of RA-LLMs has played a cru- cial role in advancing the capabilities of QA systems by enhancing their ability t... |

#### TFIDF

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.1773 | survey_on_rag2_p9_c5 | 9 | strat- egy, which retrieves information for the prediction of every token during the generation. Overall, applying different frequencies of re- trieval can impa... |
| 2 | 0.1479 | survey_on_rag2_p10_c3 | 10 | Instead of retrieving knowledge from a large corpus, GENREAD [182] first prompts a LLM to generate contextual documents based on the query, and then generate an... |

#### DENSE

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.7019 | survey_on_rag2_p9_c8 | 9 | [54, 57, 63], instead of relying solely on the implicit knowledge encoded in the model’s parameters. These approaches have shown significant performance improve... |
| 2 | 0.6377 | survey_on_rag2_p9_c2 | 9 | trainable models to offer self-knowledge as the reference for the adaptive calling of a retriever. In traditional RAGs, retrieval necessity judg- ment has also... |

### How can retrieved passages be shortened before being given to the generator?

#### BM25

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 15.8203 | survey_on_rag2_p6_c6 | 6 | which adds an intermediate step to process the retrieved documents into a textual summary before in-context augmentation in the generation process. From another... |
| 2 | 14.6679 | survey_on_rag2_p6_c2 | 6 | inspire the language model to rethink the generated results and enhance them. Com- pared to applying only the original query, such augmentation may contribute m... |

#### TFIDF

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.2600 | survey_on_rag2_p6_c6 | 6 | which adds an intermediate step to process the retrieved documents into a textual summary before in-context augmentation in the generation process. From another... |
| 2 | 0.1972 | survey_on_rag2_p8_c1 | 8 | structure to be altered or parameters to be updated. From another perspec- tive, LLMs, even those open for fine-tuning, are large in scale and difficult to tune... |

#### DENSE

| Rank | Score | Chunk | Page | Preview |
| --- | ---: | --- | ---: | --- |
| 1 | 0.6536 | survey_on_rag2_p6_c6 | 6 | which adds an intermediate step to process the retrieved documents into a textual summary before in-context augmentation in the generation process. From another... |
| 2 | 0.6186 | survey_on_rag2_p6_c3 | 6 | between the retrieval and generation stages [173], particularly for closed-source generators such as LLMs. For example, Yang et al. [173] propose the Pluggable... |

