"""
integration_examples.py

Copy-paste snippets showing how to wire query_logger.py into your
existing RAG API endpoint (PCOIS2-56). These are examples, not meant
to be run standalone - drop the relevant snippet into your real
endpoint file next to your retrieval + generation calls.
"""

# ---------------------------------------------------------------------------
# Option A: FastAPI
# ---------------------------------------------------------------------------

FASTAPI_EXAMPLE = '''
from fastapi import FastAPI
from pydantic import BaseModel
from query_logger import log_query

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str

@app.post("/query", response_model=QueryResponse)
def query_endpoint(req: QueryRequest):
    retrieved_chunks = retrieve(req.question)          # your existing hybrid retrieval
    answer = generate_answer(req.question, retrieved_chunks)  # your existing grounded generation

    # --- audit log (PCOIS2-57) ---
    log_query(
        question=req.question,
        retrieved_chunks=retrieved_chunks,
        final_answer=answer,
    )

    return QueryResponse(answer=answer)
'''

# ---------------------------------------------------------------------------
# Option B: Flask
# ---------------------------------------------------------------------------

FLASK_EXAMPLE = '''
from flask import Flask, request, jsonify
from query_logger import log_query

app = Flask(__name__)

@app.route("/query", methods=["POST"])
def query_endpoint():
    question = request.json["question"]
    retrieved_chunks = retrieve(question)               # your existing hybrid retrieval
    answer = generate_answer(question, retrieved_chunks) # your existing grounded generation

    # --- audit log (PCOIS2-57) ---
    log_query(
        question=question,
        retrieved_chunks=retrieved_chunks,
        final_answer=answer,
    )

    return jsonify({"answer": answer})
'''

if __name__ == "__main__":
    print("This file just holds example snippets - see FASTAPI_EXAMPLE / FLASK_EXAMPLE.")
