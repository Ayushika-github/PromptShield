"""
PromptShield-AI: High-Tech Cyber Defense Command Server
FastAPI Backend serving REST APIs and High-Tech Web Dashboard
Bennett University - Milestone 2
"""

import json
import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional

# Ensure src path is in sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from pipeline import PromptShieldPipeline
from synthesizer import GuardrailSynthesizer

app = FastAPI(title="PromptShield-AI Cyber Defense Portal", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = PromptShieldPipeline(benchmark_file="experiments/benchmark_test_cases.json")
synthesizer = GuardrailSynthesizer()

# Load baseline & hardened prompt texts
BASE_PROMPT_PATH = "prompts/v1_baseline/customer_support.txt"
HARD_PROMPT_PATH = "prompts/v4_adaptive_shield/customer_support_v4.txt"

def get_base_prompt():
    with open(BASE_PROMPT_PATH, "r", encoding="utf-8") as f:
        return f.read()

def get_hard_prompt():
    with open(HARD_PROMPT_PATH, "r", encoding="utf-8") as f:
        return f.read()

class DuelRequest(BaseModel):
    user_payload: str
    test_id: Optional[str] = None
    use_live_api: Optional[bool] = False

class SynthesizeRequest(BaseModel):
    candidate_prompt: str
    domain_name: Optional[str] = "ZenithPay"

@app.get("/api/testcases")
def get_test_cases():
    return pipeline.test_cases

@app.get("/api/results")
def get_results():
    results_path = "experiments/baseline_vs_hardened_results.json"
    if os.path.exists(results_path):
        with open(results_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"error": "Benchmark results not found. Run benchmark first."}

@app.post("/api/duel")
def execute_duel(req: DuelRequest):
    pipeline.use_live_api = bool(req.use_live_api)
    base_prompt = get_base_prompt()
    hard_prompt = get_hard_prompt()

    # Find matching test case or create custom object
    matched_tc = next((tc for tc in pipeline.test_cases if tc.get("id") == req.test_id or tc.get("prompt") == req.user_payload), {
        "id": req.test_id or "CUSTOM",
        "category": "CUSTOM_STRIKE",
        "attack_name": "Custom Adversarial Payload",
        "prompt": req.user_payload,
        "threat_level": "HIGH",
        "expected_defense": "Refuse unauthorized disclosure and enforce security boundary."
    })

    # Execute both targets
    base_response = pipeline.execute_prompt(base_prompt, req.user_payload)
    base_eval = pipeline.evaluate_response(matched_tc, base_prompt, base_response)

    hard_response = pipeline.execute_prompt(hard_prompt, req.user_payload)
    hard_eval = pipeline.evaluate_response(matched_tc, hard_prompt, hard_response)

    return {
        "test_case": matched_tc,
        "baseline": {
            "prompt_version": "v1_baseline (Unhardened)",
            "response": base_response,
            "evaluation": base_eval
        },
        "hardened": {
            "prompt_version": "v4_adaptive_shield (PromptShield-AI)",
            "response": hard_response,
            "evaluation": hard_eval
        }
    }

@app.post("/api/benchmark")
def run_benchmark():
    results = pipeline.run_full_comparative_audit(
        baseline_prompt_path=BASE_PROMPT_PATH,
        hardened_prompt_path=HARD_PROMPT_PATH
    )
    return results

@app.post("/api/synthesize")
def synthesize_guardrails(req: SynthesizeRequest):
    flaws = synthesizer.analyze_vulnerabilities(req.candidate_prompt)
    hardened = synthesizer.synthesize_hardened_prompt(req.candidate_prompt, req.domain_name or "SupportBot")
    return {
        "original_prompt": req.candidate_prompt,
        "detected_flaws": flaws,
        "hardened_prompt": hardened
    }

# Mount static web directory
app.mount("/", StaticFiles(directory="web", html=True), name="web")

if __name__ == "__main__":
    import uvicorn
    print("="*70)
    print("PROMPTSHIELD-AI HIGH-TECH DEFENSE PORTAL INITIALIZING...")
    print("="*70)
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True, app_dir="src")
