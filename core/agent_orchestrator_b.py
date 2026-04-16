
#AGENT ORCHESTRATOR — core/agent_orchestrator.py

import time

from agents.jung_agent import jung_response
from agents.dream_agent import dream_response
from agents.shadow_agent import shadow_response
from agents.myth_agent import myth_response
from agents.epistemic_agent import epistemic_response
from agents.bpsy_agent import bpsy_response
from agents.jred_agent import jred_response
from agents.synthesis_agent import synthesize
from agents.facilitator_agent import facilitator_response
from core.psychological_governance import generate_flags


from datetime import datetime, date, timedelta
import calendar
from dateutil.relativedelta import relativedelta

import warnings
warnings.filterwarnings("ignore")
import sys


def run_agents(text):
    
    # Execution timer
    s = datetime.now()
    exects = datetime.now().strftime("%m-%d-%Y %H:%M:%S")

    #print(f"\nExecution started at: {s.strftime("%m/%d/%Y %H:%M:%S")}")

    flags = generate_flags(text)
    
    results = {}

    # --- Jung Agent ---
    #print("→ Starting Jung Agent")
    print(f"\n→ Jung Agent started at: {datetime.now().strftime('%m/%d/%Y %H:%M:%S')}")
    start = time.perf_counter()
    jung_output = jung_response(text)
    end = time.perf_counter()
    #print(f"✓ Jung Agent done ({end - start:.2f} seconds)")
    print(f"✓ Jung Agent done in {(end - start)/60:.2f} minutes ({end - start:.2f} seconds), on {datetime.now().strftime('%m-%d-%Y %H:%M:%S')}")
    results["jung"] = jung_output

    # --- Dream Agent ---
    print(f"\n→ Dream Agent started at: {datetime.now().strftime('%m/%d/%Y %H:%M:%S')}")
    start = time.perf_counter()
    dream_output = dream_response(text)
    end = time.perf_counter()
    print(f"✓ Dream Agent done in {(end - start)/60:.2f} minutes ({end - start:.2f} seconds), on {datetime.now().strftime('%m-%d-%Y %H:%M:%S')}")
    results["dream"] = dream_output

    # --- Shadow Agent ---
    print(f"\n→ Shadow Agent started at: {datetime.now().strftime('%m/%d/%Y %H:%M:%S')}")
    start = time.perf_counter()
    shadow_output = shadow_response(text)
    end = time.perf_counter()
    print(f"✓ Shadow Agent done in {(end - start)/60:.2f} minutes ({end - start:.2f} seconds), on {datetime.now().strftime('%m-%d-%Y %H:%M:%S')}")
    results["shadow"] = shadow_output

    # --- Myth Agent ---
    print(f"\n→ Myth Agent started at: {datetime.now().strftime('%m/%d/%Y %H:%M:%S')}")
    start = time.perf_counter()
    myth_output = myth_response(text)
    end = time.perf_counter()
    print(f"✓ Myth Agent done in {(end - start)/60:.2f} minutes ({end - start:.2f} seconds), on {datetime.now().strftime('%m-%d-%Y %H:%M:%S')}")
    results["myth"] = myth_output

    # --- Epistemic Agent ---
    print(f"\n→ Epistemic Agent started at: {datetime.now().strftime('%m/%d/%Y %H:%M:%S')}")
    start = time.perf_counter()
    epistemic_output = epistemic_response(text)
    end = time.perf_counter()
    print(f"✓ Epistemic Agent done in {(end - start)/60:.2f} minutes ({end - start:.2f} seconds), on {datetime.now().strftime('%m-%d-%Y %H:%M:%S')}")
    results["epistemic"] = epistemic_output

    # --- BPsy ---
    #print("→ Starting BPsy Agent")
    print(f"\n→ BPsy Agent started at: {datetime.now().strftime('%m/%d/%Y %H:%M:%S')}")
    start = time.perf_counter()
    bpsy_output = bpsy_response(text)
    end = time.perf_counter()
    print(f"✓ BPsy Agent done in {(end - start)/60:.2f} minutes ({end - start:.2f} seconds), on {datetime.now().strftime('%m-%d-%Y %H:%M:%S')}")
    results["bpsy"] = bpsy_output

    # --- JRed ---
    #print("→ Starting JRed Agent")
    print(f"\n→ JRed Agent started at: {datetime.now().strftime('%m/%d/%Y %H:%M:%S')}")
    start = time.perf_counter()
    jred_output = jred_response(text)
    end = time.perf_counter()
    print(f"✓ JRed Agent done in {(end - start)/60:.2f} minutes ({end - start:.2f} seconds), on {datetime.now().strftime('%m-%d-%Y %H:%M:%S')}")
    results["jred"] = jred_output

    # --- Synthesis Agent ---
    print(f"\n→ Synthesis Agent started at: {datetime.now().strftime('%m/%d/%Y %H:%M:%S')}")
    start = time.perf_counter()

    #final_output = synthesize(results)

    #"""
    synthesis_output = synthesize(
        jung_output,
        dream_output,
        shadow_output,
        myth_output,
        epistemic_output,
        bpsy_output,
        jred_output
    )
    #"""

    end = time.perf_counter()
    print(f"✓ Synthesis Agent done in {(end - start)/60:.2f} minutes ({end - start:.2f} seconds), on {datetime.now().strftime('%m-%d-%Y %H:%M:%S')}")
    print("✓ Synthesis complete")


    # --- Facilitator ---
    #print("→ Starting Facilitator Agent")
    print(f"\n→ Facilitator Agent started at: {datetime.now().strftime('%m/%d/%Y %H:%M:%S')}")
    start = time.perf_counter()
    final_output = facilitator_response(text, synthesis_output, flags)
    #final_output = facilitator_response(text, final_output, flags)
    print(f"✓ Facilitator Agent done in {(time.perf_counter() - start)/60:.2f} minutes ({time.perf_counter() - start:.2f}s)")
    

    #return final_output
    
    return {
    "jung": jung_output,
    "dream": dream_output,
    "shadow": shadow_output,
    "myth": myth_output,
    "epistemic": epistemic_output,
    "bpsy": bpsy_output,
    "jred": jred_output,
    "synthesis": synthesis_output,
    "final": final_output
    }

"""
def run_agents(text):

    print("→ Starting Jung Agent")
    jung_output = jung_response(text)
    print("✓ Jung Agent done")

    print("→ Starting Dream Agent")
    dream_output = dream_response(text)
    print("✓ Dream Agent done")

    print("→ Starting Shadow Agent")
    shadow_output = shadow_response(text)
    print("✓ Shadow Agent done")

    print("→ Starting Myth Agent")
    myth_output = myth_response(text)
    print("✓ Myth Agent done")

    print("→ Starting Epistemic Agent")
    epistemic_output = epistemic_response(text)
    print("✓ Epistemic Agent done")

    print("→ Starting Synthesis Agent")
    final_output = synthesize(
        jung_output,
        dream_output,
        shadow_output,
        myth_output,
        epistemic_output
    )
    print("✓ Synthesis complete")

    return final_output
"""


"""
def run_agents(text):
    outputs = {
        "jung": jung_response(text),
        "dream": dream_response(text),
        "shadow": shadow_response(text),
        "myth": myth_response(text),
        "epistemic": epistemic_response(text),
    }

    return synthesize(outputs)
"""


"""
def run_agents(text):
    print("→ Starting Jung Agent")
    jung_output = jung_response(text)
    print("✓ Jung Agent done")

    return {
        "jung": jung_output
    }
"""