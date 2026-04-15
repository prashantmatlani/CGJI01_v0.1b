


# AGENT ORCHESTRATOR — core/agent_orchestrator.py

import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError

# -----------------------------
# IMPORTS (SAFE + FLEXIBLE)
# -----------------------------

from core.agent_wrappers import jung_response

# Try new-style agents first, fallback to old
try:
    from core.agent_wrappers import dream_response
except:
    dream_response = lambda text: "Dream agent not available"

try:
    from agents.shadow_agent import shadow_response
except:
    shadow_response = lambda text: "Shadow agent not available"

try:
    from agents.myth_agent import myth_response
except:
    myth_response = lambda text: "Myth agent not available"

try:
    from agents.epistemic_agent import epistemic_response
except:
    epistemic_response = lambda text: "Epistemic agent not available"

try:
    from agents.bpsy_agent import bpsy_response
except:
    bpsy_response = lambda text: "Biological psyche agent not available"

try:
    from agents.jred_agent import jred_response
except:
    jred_response = lambda text: "Jungian reduction agent not available"

from agents.synthesis_agent import synthesize
from agents.facilitator_agent import facilitator_response

from core.psychological_governance import generate_flags

import warnings
warnings.filterwarnings("ignore")


# -----------------------------
# CONFIG
# -----------------------------
MAX_WORKERS = 3        # 🔥 critical for Ollama stability
AGENT_TIMEOUT = 180    # seconds


# -----------------------------
# MAIN FUNCTION
# -----------------------------
def run_agents(text):

    print(f"\nExecution started at {datetime.now().strftime('%m/%d/%Y %H:%M:%S')}")

    flags = generate_flags(text)

    results = {}

    agents = {
        "jung": jung_response,
        "dream": dream_response,
        "shadow": shadow_response,
        "myth": myth_response,
        "epistemic": epistemic_response,
        "bpsy": bpsy_response,
        "jred": jred_response,
    }

    print(f"\nRunning agents in parallel (max_workers={MAX_WORKERS})...\n")

    # -----------------------------
    # PARALLEL EXECUTION
    # -----------------------------
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:

        future_to_agent = {
            executor.submit(func, text): name
            for name, func in agents.items()
        }

        start_times = {
            name: time.perf_counter()
            for name in agents.keys()
        }

        for future in as_completed(future_to_agent):

            agent = future_to_agent[future]

            try:
                output = future.result(timeout=AGENT_TIMEOUT)

                end = time.perf_counter()
                duration = end - start_times[agent]

                print(
                    f"✓ {agent.capitalize()} Agent finished in "
                    f"{duration:.2f} sec ({duration/60:.2f} min)"
                )

                results[agent] = output

            except TimeoutError:
                print(f"✗ {agent.capitalize()} Agent timed out")
                results[agent] = "Timeout"

            except Exception as e:
                print(f"✗ {agent.capitalize()} Agent failed: {e}")
                results[agent] = f"Error: {e}"

    # -----------------------------
    # SAFE EXTRACTION
    # -----------------------------
    jung_output = results.get("jung", "")
    dream_output = results.get("dream", "")
    shadow_output = results.get("shadow", "")
    myth_output = results.get("myth", "")
    epistemic_output = results.get("epistemic", "")
    bpsy_output = results.get("bpsy", "")
    jred_output = results.get("jred", "")

    # -----------------------------
    # SYNTHESIS
    # -----------------------------
    print(f"\n→ Synthesis Agent started")

    start = time.perf_counter()

    try:
        synthesis_output = synthesize(
            jung_output,
            dream_output,
            shadow_output,
            myth_output,
            epistemic_output,
            bpsy_output,
            jred_output
        )
    except Exception as e:
        synthesis_output = f"Synthesis failed: {e}"

    end = time.perf_counter()

    print(
        f"✓ Synthesis finished in "
        f"{(end-start):.2f} sec ({(end-start)/60:.2f} min)"
    )

    # -----------------------------
    # FACILITATOR
    # -----------------------------
    print(f"\n→ Facilitator Agent started")

    start = time.perf_counter()

    try:
        final_output = facilitator_response(
            text,
            synthesis_output,
            flags
        )
    except Exception as e:
        final_output = f"Facilitator failed: {e}"

    end = time.perf_counter()

    print(
        f"✓ Facilitator finished in "
        f"{(end-start):.2f} sec ({(end-start)/60:.2f} min)"
    )

    # -----------------------------
    # RETURN
    # -----------------------------
    return {
        **results,
        "synthesis": synthesis_output,
        "final": final_output
    }

"""
# -----------------------------
# CONFIG (TUNE THIS)
# -----------------------------
MAX_WORKERS = 3        # 🔥 critical: avoid overloading Ollama
AGENT_TIMEOUT = 180    # seconds per agent


def run_agents(text):

    print(f"\nExecution started at {datetime.now().strftime('%m/%d/%Y %H:%M:%S')}")

    flags = generate_flags(text)

    results = {}

    agents = {
        "jung": jung_response,
        "dream": dream_response,
        "shadow": shadow_response,
        "myth": myth_response,
        "epistemic": epistemic_response,
        "bpsy": bpsy_response,
        "jred": jred_response,
    }

    print(f"\nRunning agents in parallel (max_workers={MAX_WORKERS})...\n")

    # -----------------------------
    # PARALLEL EXECUTION (FIXED)
    # -----------------------------

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:

        future_to_agent = {
            executor.submit(func, text): name
            for name, func in agents.items()
        }

        start_times = {
            name: time.perf_counter()
            for name in agents.keys()
        }

        for future in as_completed(future_to_agent):

            agent = future_to_agent[future]

            try:
                output = future.result(timeout=AGENT_TIMEOUT)

                end = time.perf_counter()

                duration = end - start_times[agent]

                print(
                    f"✓ {agent.capitalize()} Agent finished in "
                    f"{duration:.2f} sec ({duration/60:.2f} min)"
                )

                results[agent] = output

            except TimeoutError:
                print(f"✗ {agent.capitalize()} Agent timed out")
                results[agent] = "Timeout"

            except Exception as e:
                print(f"✗ {agent.capitalize()} Agent failed: {e}")
                results[agent] = f"Error: {e}"

    # -----------------------------
    # SAFE EXTRACTION
    # -----------------------------

    jung_output = results.get("jung", "")
    dream_output = results.get("dream", "")
    shadow_output = results.get("shadow", "")
    myth_output = results.get("myth", "")
    epistemic_output = results.get("epistemic", "")
    bpsy_output = results.get("bpsy", "")
    jred_output = results.get("jred", "")

    # -----------------------------
    # SYNTHESIS
    # -----------------------------

    print(f"\n→ Synthesis Agent started")

    start = time.perf_counter()

    synthesis_output = synthesize(
        jung_output,
        dream_output,
        shadow_output,
        myth_output,
        epistemic_output,
        bpsy_output,
        jred_output
    )

    end = time.perf_counter()

    print(
        f"✓ Synthesis finished in "
        f"{(end-start):.2f} sec ({(end-start)/60:.2f} min)"
    )

    # -----------------------------
    # FACILITATOR
    # -----------------------------

    print(f"\n→ Facilitator Agent started")

    start = time.perf_counter()

    final_output = facilitator_response(
        text,
        synthesis_output,
        flags
    )

    end = time.perf_counter()

    print(
        f"✓ Facilitator finished in "
        f"{(end-start):.2f} sec ({(end-start)/60:.2f} min)"
    )

    # -----------------------------
    # RETURN
    # -----------------------------

    return {
        **results,
        "synthesis": synthesis_output,
        "final": final_output
    }

"""

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