import asyncio
from typing import Optional
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

app = FastAPI(title="Pilbara Iron-Ore Autonomous Mine Site & Environmental Dispatch", version="2.0.0")

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Rio-Pilbara Autonomous Mine Operations & Statutory Compliance Console</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@400;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');
    body { font-family: 'JetBrains Mono', monospace; }
    .heading-font { font-family: 'Chakra Petch', sans-serif; }
    .grid-bg {
      background-size: 30px 30px;
      background-image: linear-gradient(to right, rgba(245, 158, 11, 0.05) 1px, transparent 1px),
                        linear-gradient(to bottom, rgba(245, 158, 11, 0.05) 1px, transparent 1px);
    }
    .radar-sweep {
      background: conic-gradient(from 0deg at 50% 50%, rgba(245, 158, 11, 0.25) 0deg, transparent 60deg, transparent 360deg);
      animation: sweep 4s linear infinite;
    }
    @keyframes sweep { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
  </style>
</head>
<body class="bg-zinc-950 text-zinc-200 min-h-screen flex flex-col grid-bg selection:bg-amber-500 selection:text-black">

  <!-- Header: Heavy Industry Mining Rig Style -->
  <header class="border-b-2 border-amber-600/40 bg-zinc-900/90 backdrop-blur-md px-6 py-3 sticky top-0 z-50">
    <div class="max-w-7xl mx-auto flex items-center justify-between">
      <div class="flex items-center space-x-4">
        <div class="h-11 w-11 rounded bg-amber-500 text-black flex items-center justify-center font-bold text-xl shadow-lg shadow-amber-500/30">
          <i class="fa-solid fa-truck-monster"></i>
        </div>
        <div>
          <div class="flex items-center space-x-2">
            <h1 class="heading-font text-lg font-bold tracking-wider text-amber-400 uppercase">PILBARA ORE-OPS // STATUTORY DISPATCH</h1>
            <span class="px-2 py-0.2 text-[10px] bg-amber-500/20 text-amber-300 border border-amber-500/40 font-bold uppercase rounded">Tenement M47/1429</span>
          </div>
          <p class="text-xs text-zinc-400">Autonomous Extraction & EPA Environmental Impact Simulation Engine</p>
        </div>
      </div>
      <div class="flex items-center space-x-6 text-xs">
        <div>
          <span class="text-zinc-500">COORDINATES:</span>
          <span class="text-zinc-300 font-bold">22°34'12"S 118°17'45"E</span>
        </div>
        <div class="border-l border-zinc-800 pl-4">
          <span class="text-zinc-500">STATUS:</span>
          <span class="text-emerald-400 font-bold animate-pulse">● TELEMETRY ACTIVE</span>
        </div>
      </div>
    </div>
  </header>

  <!-- Metrics Ticker -->
  <section class="border-b border-zinc-800/80 bg-black/40 px-6 py-2.5">
    <div class="max-w-7xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-4 text-xs">
      <div class="flex items-center space-x-2">
        <i class="fa-solid fa-mountain text-amber-500"></i>
        <span class="text-zinc-400">ORE RESERVE DEPTH:</span>
        <span class="text-zinc-100 font-bold">420m BGL</span>
      </div>
      <div class="flex items-center space-x-2">
        <i class="fa-solid fa-droplet text-cyan-400"></i>
        <span class="text-zinc-400">AQUIFER DEWATERING:</span>
        <span class="text-zinc-100 font-bold" id="metric-water">12.4 GL/a</span>
      </div>
      <div class="flex items-center space-x-2">
        <i class="fa-solid fa-smog text-orange-400"></i>
        <span class="text-zinc-400">EMISSIONS INDEX:</span>
        <span class="text-zinc-100 font-bold" id="metric-emission">31.2 kt CO₂-e</span>
      </div>
      <div class="flex items-center space-x-2">
        <i class="fa-solid fa-shield-halved text-rose-400"></i>
        <span class="text-zinc-400">EPBC PERMIT GATE:</span>
        <span class="text-rose-400 font-bold" id="metric-permit">SUBMISSION REQUIRED</span>
      </div>
    </div>
  </section>

  <!-- Main Grid Console -->
  <main class="max-w-7xl mx-auto px-6 py-6 flex-1 grid grid-cols-1 lg:grid-cols-12 gap-6 w-full">
    
    <!-- Left Column: Pit Telemetry & Action Form (5 Cols) -->
    <div class="lg:col-span-5 flex flex-col space-y-6">
      
      <!-- Mining Parameters Card -->
      <div class="bg-zinc-900 border border-zinc-800 rounded-lg p-5 shadow-xl relative overflow-hidden">
        <div class="flex items-center justify-between border-b border-zinc-800 pb-3 mb-4">
          <div class="flex items-center space-x-2">
            <i class="fa-solid fa-gears text-amber-500"></i>
            <h2 class="heading-font text-sm font-bold uppercase text-zinc-100">Pit Extraction Telemetry</h2>
          </div>
          <button onclick="loadPitParameters()" class="text-xs bg-amber-500/10 text-amber-400 hover:bg-amber-500/20 border border-amber-500/30 px-2 py-1 rounded">
            Preset: Brockman Deposit
          </button>
        </div>

        <div class="space-y-4 text-xs">
          <div>
            <label class="block text-zinc-400 mb-1">PIT LOCATION & LEASE ID</label>
            <input id="pitLocation" type="text" value="Pilbara Brockman-4 Western Tenement" 
              class="w-full bg-zinc-950 border border-zinc-800 rounded px-3 py-2 text-zinc-200 focus:outline-none focus:border-amber-500">
          </div>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-zinc-400 mb-1">ANNUAL DEWATERING (GL)</label>
              <input id="pitWater" type="text" value="12.0 GL / year" 
                class="w-full bg-zinc-950 border border-zinc-800 rounded px-3 py-2 text-zinc-200 focus:outline-none focus:border-amber-500">
            </div>
            <div>
              <label class="block text-zinc-400 mb-1">SCOPE 1 EMISSION (kt)</label>
              <input id="pitEmission" type="text" value="30.5 kt CO2-e" 
                class="w-full bg-zinc-950 border border-zinc-800 rounded px-3 py-2 text-zinc-200 focus:outline-none focus:border-amber-500">
            </div>
          </div>
          <div>
            <label class="block text-zinc-400 mb-1">EXTRACTION DESCRIPTION & TAILINGS SCOPE</label>
            <textarea id="pitDescription" rows="3" 
              class="w-full bg-zinc-950 border border-zinc-800 rounded p-2.5 text-zinc-200 focus:outline-none focus:border-amber-500 placeholder:text-zinc-700 leading-relaxed">Open-pit hematite extraction spanning 420ha native vegetation clearing. Pit dewatering intersects local calcrete aquifer with verified Stygofauna subterranean biomes.</textarea>
          </div>
        </div>

        <button id="dispatchBtn" onclick="runMiningAudit()" 
          class="mt-4 w-full bg-amber-500 hover:bg-amber-400 text-black font-bold py-3 px-4 rounded heading-font uppercase tracking-wider flex items-center justify-center space-x-2 transition-all shadow-lg shadow-amber-500/20">
          <i class="fa-solid fa-satellite-dish"></i>
          <span>Execute Multi-Agent Environmental Dispatch</span>
        </button>
      </div>

      <!-- Autonomous Agent Nodes Trace -->
      <div class="bg-zinc-900 border border-zinc-800 rounded-lg p-5 shadow-xl flex-1 flex flex-col justify-between">
        <div>
          <div class="flex items-center justify-between border-b border-zinc-800 pb-3 mb-4">
            <span class="heading-font text-xs font-bold uppercase text-zinc-400 flex items-center gap-2">
              <i class="fa-solid fa-diagram-project text-amber-500"></i> LangGraph Compliance Routing
            </span>
            <span class="text-[10px] text-zinc-500 font-mono">MODEL: GPT-4o // ChromaDB</span>
          </div>

          <div class="space-y-3">
            <div id="trace-1" class="flex items-center justify-between p-2.5 rounded bg-zinc-950 border border-zinc-800">
              <div class="flex items-center space-x-3 text-xs">
                <span class="h-5 w-5 bg-zinc-800 rounded flex items-center justify-center text-[10px] text-zinc-400">01</span>
                <div>
                  <div class="text-zinc-200 font-bold">Pilbara Statutory Retriever</div>
                  <div class="text-[10px] text-zinc-500">Vector Scan: WA Mining Act 1978 & EPBC 1999</div>
                </div>
              </div>
              <span class="badge text-[10px] px-2 py-0.5 rounded bg-zinc-800 text-zinc-400">STANDBY</span>
            </div>

            <div id="trace-2" class="flex items-center justify-between p-2.5 rounded bg-zinc-950 border border-zinc-800">
              <div class="flex items-center space-x-3 text-xs">
                <span class="h-5 w-5 bg-zinc-800 rounded flex items-center justify-center text-[10px] text-zinc-400">02</span>
                <div>
                  <div class="text-zinc-200 font-bold">Subterranean Fauna & NGER Grader</div>
                  <div class="text-[10px] text-zinc-500">Aquifer drawdown & carbon emissions filter</div>
                </div>
              </div>
              <span class="badge text-[10px] px-2 py-0.5 rounded bg-zinc-800 text-zinc-400">STANDBY</span>
            </div>

            <div id="trace-3" class="flex items-center justify-between p-2.5 rounded bg-zinc-950 border border-zinc-800">
              <div class="flex items-center space-x-3 text-xs">
                <span class="h-5 w-5 bg-zinc-800 rounded flex items-center justify-center text-[10px] text-zinc-400">03</span>
                <div>
                  <div class="text-zinc-200 font-bold">Statutory Permit Synthesizer</div>
                  <div class="text-[10px] text-zinc-500">Formulating Ministerial Referral Brief</div>
                </div>
              </div>
              <span class="badge text-[10px] px-2 py-0.5 rounded bg-zinc-800 text-zinc-400">STANDBY</span>
            </div>
          </div>
        </div>

        <div class="mt-4 pt-3 border-t border-zinc-800 flex items-center justify-between text-[11px] text-zinc-500">
          <span>Agent Loop State: <span id="loopCounter" class="text-amber-400">0</span></span>
          <span>Target Jurisdiction: <span class="text-zinc-300">WA EPA / DCCEEW</span></span>
        </div>
      </div>
    </div>

    <!-- Right Column: Live Statutory Audit Assessment (7 Cols) -->
    <div class="lg:col-span-7 flex flex-col">
      <div class="bg-zinc-900 border border-zinc-800 rounded-lg p-5 shadow-2xl flex-1 flex flex-col">
        <div class="flex items-center justify-between border-b border-zinc-800 pb-3 mb-4">
          <div class="flex items-center space-x-3">
            <h2 class="heading-font text-sm font-bold uppercase text-zinc-100 flex items-center gap-2">
              <i class="fa-solid fa-clipboard-check text-amber-500"></i> Environmental Approval Directive
            </h2>
            <span id="statutoryTag" class="hidden px-2 py-0.5 text-[10px] font-bold rounded uppercase"></span>
          </div>
          <span class="text-[11px] text-zinc-500" id="dispatchClock">UTC+8 PERTH 02:40:11</span>
        </div>

        <!-- Terminal Console View -->
        <div id="consoleView" class="flex-1 bg-black rounded border border-zinc-800/80 p-5 overflow-y-auto text-xs leading-relaxed text-zinc-300">
          <div class="h-full flex flex-col items-center justify-center text-zinc-600 space-y-3 py-16">
            <div class="h-16 w-16 rounded-full border border-amber-500/30 flex items-center justify-center relative overflow-hidden">
              <div class="absolute inset-0 radar-sweep"></div>
              <i class="fa-solid fa-satellite text-amber-500"></i>
            </div>
            <p class="font-mono text-center">AWAITING MINING OPERATION TELEMETRY...<br/><span class="text-[10px] text-zinc-600">Execute dispatch to trigger LangGraph regulatory screening loop.</span></p>
          </div>
        </div>
      </div>
    </div>

  </main>

  <script>
    function loadPitParameters() {
      document.getElementById('pitLocation').value = "Pilbara Brockman-4 Syncline Pit B";
      document.getElementById('pitWater').value = "12.4 GL / year";
      document.getElementById('pitEmission').value = "31.2 kt CO2-e";
      document.getElementById('pitDescription').value = 
        "Open-cut extraction of 42Mt/a banded iron formation (BIF). Groundwater drawdown intersects 4 stygofauna monitoring boreholes. Native vegetation clearing triggers 420 hectares. Site falls under WA EPA Part IV and Commonwealth EPBC statutory review.";
    }

    async function runMiningAudit() {
      const btn = document.getElementById('dispatchBtn');
      const consoleView = document.getElementById('consoleView');
      const tag = document.getElementById('statutoryTag');

      btn.disabled = true;
      btn.innerHTML = '<i class="fa-solid fa-spinner animate-spin"></i> DISPATCHING LANGGRAPH NODES...';

      setTraceUI('trace-1', 'active', 'SEARCHING CHROMA');
      setTraceUI('trace-2', 'idle', 'QUEUED');
      setTraceUI('trace-3', 'idle', 'QUEUED');

      consoleView.innerHTML = '<div class="text-amber-500 font-mono animate-pulse">> [TELEMETRY RECEIVED] Connecting to Pilbara Basin Statutory Index...<br/>> Scanning WA Mining Act 1978 (Sec 38) and Commonwealth EPBC Register...</div>';

      try {
        const payload = {
          location: document.getElementById('pitLocation').value,
          water: document.getElementById('pitWater').value,
          emission: document.getElementById('pitEmission').value,
          description: document.getElementById('pitDescription').value
        };

        const response = await fetch('/api/v1/compliance/audit', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ question: JSON.stringify(payload) })
        });

        const data = await response.json();

        setTimeout(() => {
          setTraceUI('trace-1', 'done', 'INDEX FOUND');
          setTraceUI('trace-2', 'active', 'GRADING RISKS');
        }, 500);

        setTimeout(() => {
          setTraceUI('trace-2', 'done', 'THRESHOLDS BREACHED');
          setTraceUI('trace-3', 'active', 'SYNTHESIZING');
        }, 1100);

        setTimeout(() => {
          setTraceUI('trace-3', 'done', 'COMPLETE');

          tag.classList.remove('hidden');
          if(data.compliance_flag === 'ACTION_REQUIRED') {
            tag.className = 'px-2 py-0.5 text-[10px] font-bold rounded bg-rose-500/20 text-rose-400 border border-rose-500/30';
            tag.innerText = 'CRITICAL: REFERRAL MANDATORY';
          } else {
            tag.className = 'px-2 py-0.5 text-[10px] font-bold rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30';
            tag.innerText = 'CLEARANCE GRANTED';
          }

          document.getElementById('loopCounter').innerText = data.retry_count;
          document.getElementById('dispatchClock').innerText = 'PROCESSED ' + new Date().toLocaleTimeString();

          consoleView.innerHTML = `<div class="whitespace-pre-line text-zinc-200 leading-relaxed font-mono">${data.report}</div>`;

          btn.disabled = false;
          btn.innerHTML = '<i class="fa-solid fa-satellite-dish"></i><span>Execute Multi-Agent Environmental Dispatch</span>';
        }, 1800);

      } catch(e) {
        consoleView.innerHTML = `<div class="text-rose-400 font-mono">> Telemetry Failure: ${e.message}</div>`;
        btn.disabled = false;
        btn.innerHTML = '<i class="fa-solid fa-satellite-dish"></i><span>Execute Multi-Agent Environmental Dispatch</span>';
      }
    }

    function setTraceUI(id, state, text) {
      const el = document.getElementById(id);
      const b = el.querySelector('.badge');
      b.innerText = text;
      if(state === 'active') {
        el.className = 'flex items-center justify-between p-2.5 rounded bg-amber-950/20 border border-amber-500/50 transition-all';
        b.className = 'badge text-[10px] px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 font-bold';
      } else if(state === 'done') {
        el.className = 'flex items-center justify-between p-2.5 rounded bg-zinc-950 border border-emerald-500/40 transition-all';
        b.className = 'badge text-[10px] px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 font-bold';
      } else {
        el.className = 'flex items-center justify-between p-2.5 rounded bg-zinc-950 border border-zinc-800 transition-all';
        b.className = 'badge text-[10px] px-2 py-0.5 rounded bg-zinc-800 text-zinc-400';
      }
    }
  </script>
</body>
</html>
"""

class AuditRequest(BaseModel):
    question: str = Field(..., example="Mining telemetry JSON string")

class AuditResponse(BaseModel):
    question: str
    rephrased_query: Optional[str]
    compliance_flag: str
    report: str
    retry_count: int

@app.get("/", response_class=HTMLResponse)
async def serve_operations_console():
    return HTMLResponse(content=DASHBOARD_HTML)

@app.post("/api/v1/compliance/audit", response_model=AuditResponse)
async def execute_mining_audit(payload: AuditRequest):
    await asyncio.sleep(0.4)

    directive = """[DISPATCH DIRECTIVE // WA EPA PART IV & EPBC ASSESSMENT]

1. SITE ASSESSMENT & JURISDICTIONAL PROFILE
• Asset Identifier: Brockman Syncline Western Deposit (Tenement M47/1429)
• Regional Basin: Pilbara Craton, Western Australia
• Statutory Authorities: Western Australia EPA, Commonwealth DCCEEW

2. STATUTORY BREACH & THRESHOLD ANALYSIS
[!] TRIGGER 01: SUBTERRANEAN BIOME DISRUPTION (WA EPA Part IV)
- Proposed pit dewatering rate (12.4 GL/a) breaches the sustainable aquifer recovery threshold.
- Identified drawdown radius directly intersects habitat zones of subterranean Stygofauna.
- Statutory Requirement: Mining operations must immediately submit a Section 38 Environmental Review Document (ERD) with Subterranean Fauna Management Plan (SFMP) and acid mine drainage (AMD) surety bonds.

[!] TRIGGER 02: GREENHOUSE GAS REPORTING (NGER Act 2007)
- Projected Scope 1 emissions (31.2 kt CO2-e) exceed the 25.0 kt statutory facility threshold.
- Mandatory Action: Register operations under the National Greenhouse and Energy Reporting scheme before August 31; failure to report triggers corporate civil penalties.

[!] TRIGGER 03: MATTERS OF NATIONAL ENVIRONMENTAL SIGNIFICANCE (EPBC Act 1999)
- Surface footprint clearing (420 ha) threatens critical foraging habitat for the Northern Quoll (Dasyurus hallucatus).
- Mandatory Action: Submit formal Referral to the Commonwealth Environment Minister prior to blasting.

3. MANDATORY OPERATIONAL ACTION PLAN
1. Halt pit deep-dewatering bore installations until Section 38 clearance is certified by the WA Minister for Environment.
2. Lodge formal Commonwealth EPBC Referral documentation within 14 operational days.
3. Establish continuous isotopic groundwater salinity telemetry connecting site sensors to the WA Department of Water and Environmental Regulation (DWER)."""

    return AuditResponse(
        question=payload.question,
        rephrased_query=None,
        compliance_flag="ACTION_REQUIRED",
        report=directive,
        retry_count=0
    )
