<!--
docs/knowledge/rag-basics.md — WHY: corpus note for the RAG demo that also teaches topic 7
itself: local RAG, chunking, retrieval quality, citations, why RAG beats dumping a big doc.
-->

# What RAG Is

Retrieval-Augmented Generation (RAG) means: before the model answers, search a knowledge
base for the passages most relevant to the question and put only those passages into the
prompt. The model then answers from that retrieved evidence and cites it. A local RAG runs
entirely on your machine, with no external vector database or cloud service.

# Why RAG Beats Dumping a Big Document

Pasting a whole manual into the prompt is expensive, slow, and hits the lost-in-the-middle
effect: the relevant paragraph is buried among thousands of irrelevant ones. RAG sends a
few focused chunks, which is cheaper, fits in the window, keeps the relevant text near the
question, and lets every claim point to a source. It also scales: the knowledge base can
be far larger than any context window.

# Chunking

Documents are split into chunks before indexing. Chunk design drives retrieval quality.

- **Split by structure first:** headings are natural topic boundaries, so a chunk rarely
  mixes two topics.
- **Then by size:** long sections are cut into windows of a fixed chunk size.
- **Overlap:** consecutive windows share some words so a sentence cut at a boundary still
  appears whole in at least one chunk.
- **Metadata:** each chunk keeps its source file, heading and a chunk id so answers can be
  cited and results can be filtered by source.

Chunks that are too small lose context; chunks that are too large dilute the match and
waste tokens.

# Retrieval Quality

Lexical retrieval such as BM25 scores chunks by term overlap, weighting rare terms higher
and normalizing for chunk length. It is fast, explainable and has no dependencies. Dense
retrieval uses embeddings to match meaning rather than exact words. Production systems
often combine both (hybrid search) and then apply a reranker. Retrieval quality is
measured with an evaluation set of questions and expected sources, using metrics such as
hit at k (is the right source in the top k results) and recall.

# Citations

Every retrieved chunk carries a citation such as `rag-basics.md#Chunking`. Citations let a
reader verify a claim, make hallucinations visible, and turn "the model said so" into "the
source says so". If nothing relevant is retrieved, the right answer is "not found in the
notes", not an invented one.
