/**
 * CareerCraft AI - Interactive Frontend Controller
 */

// Global State
let currentAnalysisData = null;
let sampleResumes = [];
let radarChartInstance = null;
let selectedFile = null;

// Initialize Lucide Icons
function refreshIcons() {
  if (window.lucide) {
    window.lucide.createIcons();
  }
}

// DOM Elements
document.addEventListener("DOMContentLoaded", () => {
  initApp();
});

async function initApp() {
  setupEventListeners();
  await loadSampleResumes();
  refreshIcons();
}

function setupEventListeners() {
  // Tabs for Upload vs Paste
  const tabUpload = document.getElementById("tabUploadFile");
  const tabPaste = document.getElementById("tabPasteText");
  const viewUpload = document.getElementById("viewUploadFile");
  const viewPaste = document.getElementById("viewPasteText");

  tabUpload.addEventListener("click", () => {
    tabUpload.className = "flex-1 pb-3 text-sm font-semibold border-b-2 border-sky-500 text-sky-400 flex items-center justify-center space-x-2 transition";
    tabPaste.className = "flex-1 pb-3 text-sm font-semibold border-b-2 border-transparent text-slate-400 hover:text-slate-200 flex items-center justify-center space-x-2 transition";
    viewUpload.classList.remove("hidden");
    viewPaste.classList.add("hidden");
  });

  tabPaste.addEventListener("click", () => {
    tabPaste.className = "flex-1 pb-3 text-sm font-semibold border-b-2 border-sky-500 text-sky-400 flex items-center justify-center space-x-2 transition";
    tabUpload.className = "flex-1 pb-3 text-sm font-semibold border-b-2 border-transparent text-slate-400 hover:text-slate-200 flex items-center justify-center space-x-2 transition";
    viewPaste.classList.remove("hidden");
    viewUpload.classList.add("hidden");
  });

  // File Dropzone
  const dropZone = document.getElementById("dropZone");
  const fileInput = document.getElementById("fileInput");
  const selectedFileInfo = document.getElementById("selectedFileInfo");
  const selectedFileName = document.getElementById("selectedFileName");

  dropZone.addEventListener("click", () => fileInput.click());

  dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("border-sky-400", "bg-slate-900/90");
  });

  dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("border-sky-400", "bg-slate-900/90");
  });

  dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("border-sky-400", "bg-slate-900/90");
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFileSelected(e.dataTransfer.files[0]);
    }
  });

  fileInput.addEventListener("change", (e) => {
    if (e.target.files && e.target.files.length > 0) {
      handleFileSelected(e.target.files[0]);
    }
  });

  function handleFileSelected(file) {
    selectedFile = file;
    selectedFileName.textContent = `${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
    selectedFileInfo.classList.remove("hidden");
    hideError();
  }

  // Textarea Word / Char count
  const resumeTextArea = document.getElementById("resumeTextArea");
  const charCount = document.getElementById("charCount");
  const wordCount = document.getElementById("wordCount");

  resumeTextArea.addEventListener("input", () => {
    const text = resumeTextArea.value;
    charCount.textContent = text.length;
    wordCount.textContent = text.trim() ? text.trim().split(/\s+/).length : 0;
  });

  // Analyze Button
  document.getElementById("btnAnalyze").addEventListener("click", handleAnalyze);

  // Reset Button
  document.getElementById("btnReset").addEventListener("click", () => {
    document.getElementById("resultsSection").classList.add("hidden");
    document.getElementById("inputSection").classList.remove("hidden");
    document.getElementById("btnReset").classList.add("hidden");
    document.getElementById("btnExportReport").classList.add("hidden");
    window.scrollTo({ top: 0, behavior: "smooth" });
  });

  // Export Report Button
  document.getElementById("btnExportReport").addEventListener("click", exportAnalysisReport);

  // Result Navigation Tabs
  const navTabs = document.querySelectorAll(".nav-tab");
  navTabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      navTabs.forEach((t) => {
        t.classList.remove("active", "bg-sky-500/15", "text-sky-400", "border-sky-500/30");
        t.classList.add("text-slate-400");
      });
      tab.classList.add("active", "bg-sky-500/15", "text-sky-400", "border-sky-500/30");
      tab.classList.remove("text-slate-400");

      const targetId = tab.getAttribute("data-target");
      document.querySelectorAll(".tab-content").forEach((content) => {
        content.classList.add("hidden");
      });
      document.getElementById(targetId).classList.remove("hidden");
      refreshIcons();
    });
  });

  // Filter Jobs Listeners
  document.getElementById("jobSearchInput").addEventListener("input", filterAndRenderJobs);
  document.getElementById("filterCategory").addEventListener("change", filterAndRenderJobs);
  document.getElementById("filterMinMatch").addEventListener("change", filterAndRenderJobs);

  // Custom JD Match
  document.getElementById("btnMatchCustomJD").addEventListener("click", handleCustomJDMatch);

  // Cover Letter Generator
  document.getElementById("btnGenerateCoverLetter").addEventListener("click", handleGenerateCoverLetter);
  document.getElementById("btnCopyCoverLetter").addEventListener("click", () => {
    const text = document.getElementById("coverLetterOutput").value;
    if (text) {
      navigator.clipboard.writeText(text);
      alert("Cover letter copied to clipboard!");
    }
  });
}

// Load Sample Profiles
async function loadSampleResumes() {
  try {
    const res = await fetch("/api/sample-resumes");
    sampleResumes = await res.json();
    const container = document.getElementById("samplePillsContainer");
    container.innerHTML = "";

    sampleResumes.forEach((sample) => {
      const pill = document.createElement("button");
      pill.className = "px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 border border-slate-700 text-xs text-slate-200 hover:text-sky-300 transition flex items-center space-x-1.5";
      pill.innerHTML = `
        <span class="w-2 h-2 rounded-full bg-sky-400"></span>
        <span class="font-medium">${sample.name}</span>
        <span class="text-slate-500 text-[10px]">(${sample.title.split(" ")[0]})</span>
      `;
      pill.addEventListener("click", () => {
        loadSampleIntoForm(sample);
      });
      container.appendChild(pill);
    });
  } catch (err) {
    console.error("Failed to load sample resumes", err);
  }
}

function loadSampleIntoForm(sample) {
  // Switch to paste tab
  document.getElementById("tabPasteText").click();
  const textarea = document.getElementById("resumeTextArea");
  textarea.value = sample.text.trim();
  textarea.dispatchEvent(new Event("input"));
  // Trigger analysis automatically
  handleAnalyze();
}

function showError(msg) {
  const banner = document.getElementById("errorBanner");
  const msgElem = document.getElementById("errorMessage");
  msgElem.textContent = msg;
  banner.classList.remove("hidden");
  refreshIcons();
}

function hideError() {
  document.getElementById("errorBanner").classList.add("hidden");
}

// Handle Analyze
async function handleAnalyze() {
  hideError();
  const isPasteActive = !document.getElementById("viewPasteText").classList.contains("hidden");
  const textVal = document.getElementById("resumeTextArea").value.trim();

  if (isPasteActive && (!textVal || textVal.split(/\s+/).length < 15)) {
    showError("Please paste a valid resume text (at least 15 words).");
    return;
  }

  if (!isPasteActive && !selectedFile) {
    showError("Please select or drop a resume file (PDF, DOCX, or TXT).");
    return;
  }

  // Show loading
  document.getElementById("inputSection").classList.add("hidden");
  document.getElementById("loadingOverlay").classList.remove("hidden");
  document.getElementById("resultsSection").classList.add("hidden");
  refreshIcons();

  try {
    const formData = new FormData();
    if (isPasteActive) {
      formData.append("text", textVal);
    } else {
      formData.append("file", selectedFile);
    }

    const res = await fetch("/api/analyze", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.detail || "Analysis failed");
    }

    currentAnalysisData = data;
    renderResults(data);

    // Show Results
    document.getElementById("loadingOverlay").classList.add("hidden");
    document.getElementById("resultsSection").classList.remove("hidden");
    document.getElementById("btnReset").classList.remove("hidden");
    document.getElementById("btnExportReport").classList.remove("hidden");

    window.scrollTo({ top: 0, behavior: "smooth" });
  } catch (err) {
    document.getElementById("loadingOverlay").classList.add("hidden");
    document.getElementById("inputSection").classList.remove("hidden");
    showError(err.message || "Failed to analyze resume.");
  }
}

// Render Results Pipeline
function renderResults(data) {
  const parsed = data.parsed;
  const evalData = data.evaluation;
  const jobMatches = data.job_matches;

  // 1. Candidate Header
  document.getElementById("candidateName").textContent = parsed.contact.name || "Candidate Profile";
  const contactsContainer = document.getElementById("candidateContacts");
  contactsContainer.innerHTML = "";

  if (parsed.contact.email) {
    contactsContainer.innerHTML += `<span class="flex items-center space-x-1"><i data-lucide="mail" class="w-3.5 h-3.5 text-sky-400"></i><span>${parsed.contact.email}</span></span>`;
  }
  if (parsed.contact.phone) {
    contactsContainer.innerHTML += `<span class="flex items-center space-x-1"><i data-lucide="phone" class="w-3.5 h-3.5 text-sky-400"></i><span>${parsed.contact.phone}</span></span>`;
  }
  if (parsed.contact.linkedin) {
    contactsContainer.innerHTML += `<a href="${parsed.contact.linkedin}" target="_blank" class="text-sky-400 hover:underline flex items-center space-x-1"><i data-lucide="external-link" class="w-3.5 h-3.5"></i><span>LinkedIn</span></a>`;
  }
  if (parsed.contact.github) {
    contactsContainer.innerHTML += `<a href="${parsed.contact.github}" target="_blank" class="text-sky-400 hover:underline flex items-center space-x-1"><i data-lucide="github" class="w-3.5 h-3.5"></i><span>GitHub</span></a>`;
  }

  document.getElementById("metricTotalSkills").textContent = evalData.metrics_summary.total_skills;
  document.getElementById("metricTotalWords").textContent = evalData.metrics_summary.total_words;
  document.getElementById("metricQuantBullets").textContent = `${evalData.metrics_summary.quantified_bullets_count} / ${evalData.metrics_summary.total_bullets_analyzed}`;

  // 2. ATS Scorecard
  renderScorecard(evalData);

  // 3. Render Strengths & Improvements
  renderStrengthsAndFixes(evalData);

  // 4. Render Bullet Rewrites
  renderBulletRewrites(evalData.bullet_rewrites);

  // 5. Render Job Matches
  filterAndRenderJobs();

  // 6. Pre-fill Cover Letter Form
  document.getElementById("clJobTitle").value = jobMatches.length > 0 ? jobMatches[0].title : "Software Engineer";
  document.getElementById("clCompany").value = "Hiring Team";
  handleGenerateCoverLetter();

  // 7. Render Extracted Skills Tree
  renderSkillsTree(parsed.skills);

  // 8. Render Default Interview Prep
  renderInterviewPrep(jobMatches.length > 0 ? jobMatches[0] : null);

  refreshIcons();
}

// Render ATS Score Card & Radar Chart
function renderScorecard(evalData) {
  const score = evalData.overall_score;
  const scoreNumber = document.getElementById("scoreNumber");
  const scoreCircle = document.getElementById("scoreCircle");
  const scoreGrade = document.getElementById("scoreGrade");
  const scoreVerdict = document.getElementById("scoreVerdict");

  // Animate Number Counter
  let count = 0;
  const interval = setInterval(() => {
    if (count >= score) {
      scoreNumber.textContent = score;
      clearInterval(interval);
    } else {
      count += 2;
      scoreNumber.textContent = Math.min(count, score);
    }
  }, 20);

  // Stroke Dashoffset Calculation (circumference = 2 * PI * 42 ≈ 263.89)
  const offset = 264 - (score / 100) * 264;
  scoreCircle.style.strokeDashoffset = offset;

  if (score >= 80) {
    scoreCircle.setAttribute("class", "text-emerald-400 transition-all duration-1000 ease-out");
    scoreGrade.className = "px-3 py-1 rounded-full text-xs font-bold bg-emerald-500/15 text-emerald-400 border border-emerald-500/30";
  } else if (score >= 60) {
    scoreCircle.setAttribute("class", "text-sky-400 transition-all duration-1000 ease-out");
    scoreGrade.className = "px-3 py-1 rounded-full text-xs font-bold bg-sky-500/15 text-sky-400 border border-sky-500/30";
  } else {
    scoreCircle.setAttribute("class", "text-amber-400 transition-all duration-1000 ease-out");
    scoreGrade.className = "px-3 py-1 rounded-full text-xs font-bold bg-amber-500/15 text-amber-400 border border-amber-500/30";
  }

  scoreGrade.textContent = evalData.grade;
  scoreVerdict.textContent = evalData.verdict;

  // Sub Scores Progress Bars
  const subScoresContainer = document.getElementById("subScoresList");
  subScoresContainer.innerHTML = "";
  Object.values(evalData.sub_scores).forEach((item) => {
    subScoresContainer.innerHTML += `
      <div class="space-y-1">
        <div class="flex justify-between text-xs font-medium">
          <span class="text-slate-300">${item.label} <span class="text-slate-500">(${item.weight})</span></span>
          <span class="text-sky-400 font-bold">${item.score}/100</span>
        </div>
        <div class="w-full h-2 bg-slate-900 rounded-full overflow-hidden">
          <div class="h-full bg-gradient-to-r from-sky-500 to-indigo-500 rounded-full transition-all duration-700" style="width: ${item.score}%"></div>
        </div>
      </div>
    `;
  });

  // Radar Chart
  renderRadarChart(evalData.sub_scores);
}

function renderRadarChart(subScores) {
  const ctx = document.getElementById("atsRadarChart").getContext("2d");
  if (radarChartInstance) {
    radarChartInstance.destroy();
  }

  const labels = Object.values(subScores).map((s) => s.label);
  const dataValues = Object.values(subScores).map((s) => s.score);

  radarChartInstance = new Chart(ctx, {
    type: "radar",
    data: {
      labels: labels,
      datasets: [
        {
          label: "ATS Performance Score",
          data: dataValues,
          backgroundColor: "rgba(14, 165, 233, 0.25)",
          borderColor: "#38bdf8",
          pointBackgroundColor: "#38bdf8",
          pointBorderColor: "#fff",
          pointHoverBackgroundColor: "#fff",
          pointHoverBorderColor: "#38bdf8",
          borderWidth: 2,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        r: {
          angleLines: { color: "rgba(148, 163, 184, 0.2)" },
          grid: { color: "rgba(148, 163, 184, 0.2)" },
          pointLabels: {
            color: "#94a3b8",
            font: { size: 10, family: "Inter" },
          },
          ticks: {
            display: false,
            stepSize: 20,
            max: 100,
            min: 0,
          },
          suggestedMin: 0,
          suggestedMax: 100,
        },
      },
      plugins: {
        legend: { display: false },
      },
    },
  });
}

// Render Strengths and Actionable Fixes
function renderStrengthsAndFixes(evalData) {
  const strengthsList = document.getElementById("strengthsList");
  strengthsList.innerHTML = "";
  evalData.strengths.forEach((str) => {
    strengthsList.innerHTML += `
      <li class="flex items-start space-x-2.5">
        <i data-lucide="check" class="w-4 h-4 text-emerald-400 shrink-0 mt-0.5"></i>
        <span>${str}</span>
      </li>
    `;
  });

  const improvementsList = document.getElementById("improvementsList");
  improvementsList.innerHTML = "";

  // Critical issues
  evalData.critical_issues.forEach((crit) => {
    improvementsList.innerHTML += `
      <li class="p-2.5 rounded-xl bg-rose-500/10 border border-rose-500/25 flex items-start space-x-2.5 text-rose-300">
        <i data-lucide="alert-triangle" class="w-4 h-4 text-rose-400 shrink-0 mt-0.5"></i>
        <span><strong>Critical:</strong> ${crit}</span>
      </li>
    `;
  });

  // Improvement items
  evalData.improvements.forEach((imp) => {
    const isWarn = imp.type === "warning";
    const color = isWarn ? "text-amber-300 bg-amber-500/10 border-amber-500/25" : "text-sky-300 bg-sky-500/10 border-sky-500/25";
    const icon = isWarn ? "alert-circle" : "info";
    improvementsList.innerHTML += `
      <li class="p-2.5 rounded-xl ${color} border flex items-start space-x-2.5">
        <i data-lucide="${icon}" class="w-4 h-4 shrink-0 mt-0.5"></i>
        <span>${imp.message}</span>
      </li>
    `;
  });
}

// Render Bullet Rewrites
function renderBulletRewrites(rewrites) {
  const container = document.getElementById("bulletRewritesContainer");
  container.innerHTML = "";

  if (!rewrites || rewrites.length === 0) {
    container.innerHTML = `<p class="text-xs text-slate-400">All bullet points are strong with quantifiable metrics and active verbs!</p>`;
    return;
  }

  rewrites.forEach((rw, idx) => {
    const card = document.createElement("div");
    card.className = "p-4 rounded-xl bg-slate-900/60 border border-slate-700/70 space-y-2";
    card.innerHTML = `
      <div class="flex items-center justify-between text-xs">
        <span class="font-semibold text-amber-400 flex items-center space-x-1">
          <i data-lucide="alert-circle" class="w-3.5 h-3.5"></i>
          <span>Issue: ${rw.issue}</span>
        </span>
        <button class="btn-copy-rewrite text-sky-400 hover:text-sky-300 text-[11px] font-medium flex items-center space-x-1" data-text="${encodeURIComponent(rw.suggested)}">
          <i data-lucide="copy" class="w-3 h-3"></i>
          <span>Copy Rewrite</span>
        </button>
      </div>
      <div class="text-xs text-slate-400 bg-slate-950/60 p-2.5 rounded-lg border border-slate-800 line-through decoration-rose-400/60">
        ${rw.original}
      </div>
      <div class="text-xs text-emerald-300 bg-emerald-950/20 p-2.5 rounded-lg border border-emerald-500/30 flex items-start space-x-2">
        <i data-lucide="sparkles" class="w-4 h-4 text-emerald-400 shrink-0 mt-0.5"></i>
        <div class="flex-1">
          <strong>Recommended XYZ Rewrite:</strong><br />
          ${rw.suggested}
        </div>
      </div>
    `;
    container.appendChild(card);
  });

  // Attach copy listeners
  container.querySelectorAll(".btn-copy-rewrite").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      const text = decodeURIComponent(btn.getAttribute("data-text"));
      navigator.clipboard.writeText(text);
      btn.innerHTML = `<i data-lucide="check" class="w-3 h-3 text-emerald-400"></i> <span class="text-emerald-400">Copied!</span>`;
      refreshIcons();
      setTimeout(() => {
        btn.innerHTML = `<i data-lucide="copy" class="w-3 h-3"></i> <span>Copy Rewrite</span>`;
        refreshIcons();
      }, 2000);
    });
  });
}

// Filter and Render Jobs Grid
function filterAndRenderJobs() {
  if (!currentAnalysisData) return;
  const matches = currentAnalysisData.job_matches || [];
  const search = document.getElementById("jobSearchInput").value.toLowerCase();
  const category = document.getElementById("filterCategory").value;
  const minMatch = parseInt(document.getElementById("filterMinMatch").value, 10);

  const filtered = matches.filter((job) => {
    const matchesSearch =
      job.title.toLowerCase().includes(search) ||
      job.description.toLowerCase().includes(search) ||
      job.matched_skills.some((s) => s.toLowerCase().includes(search)) ||
      job.missing_required.some((s) => s.toLowerCase().includes(search));

    const matchesCategory = category === "all" || job.category.toLowerCase() === category.toLowerCase();
    const matchesScore = job.match_percentage >= minMatch;

    return matchesSearch && matchesCategory && matchesScore;
  });

  document.getElementById("jobCountLabel").textContent = `Showing ${filtered.length} matching roles`;
  const grid = document.getElementById("jobMatchesGrid");
  grid.innerHTML = "";

  if (filtered.length === 0) {
    grid.innerHTML = `<div class="col-span-2 text-center py-12 text-slate-400 text-sm">No job roles found matching current filter criteria.</div>`;
    return;
  }

  filtered.forEach((job) => {
    const card = document.createElement("div");
    card.className = "glass-card bg-slate-800/70 border border-slate-700/80 rounded-2xl p-6 backdrop-blur-xl space-y-4 flex flex-col justify-between";
    
    // Matched skills pills
    const matchedPills = job.matched_skills
      .map((s) => `<span class="px-2 py-0.5 rounded-md bg-emerald-500/15 text-emerald-400 border border-emerald-500/25 text-[11px] font-medium">${s}</span>`)
      .join("");

    // Missing skills pills
    const missingPills = job.missing_required
      .map((s) => `<span class="px-2 py-0.5 rounded-md bg-amber-500/15 text-amber-400 border border-amber-500/25 text-[11px] font-medium">${s}</span>`)
      .join("");

    card.innerHTML = `
      <div class="space-y-3">
        <div class="flex items-start justify-between gap-2">
          <div>
            <span class="text-[11px] font-semibold text-sky-400 uppercase tracking-wider">${job.category} • ${job.level}</span>
            <h4 class="text-base font-bold text-white mt-0.5">${job.title}</h4>
          </div>
          <div class="text-right">
            <div class="inline-flex items-center space-x-1 px-2.5 py-1 rounded-full bg-sky-500/15 border border-sky-500/30 text-sky-300 text-xs font-extrabold">
              <span>${job.match_percentage}% Match</span>
            </div>
            <span class="text-[10px] text-slate-400 block mt-0.5">${job.salary_range}</span>
          </div>
        </div>

        <p class="text-xs text-slate-300 leading-relaxed">${job.description}</p>

        <!-- Matched Skills -->
        <div class="space-y-1">
          <span class="text-[11px] font-semibold text-emerald-400 uppercase tracking-wider block">Your Matching Skills (${job.matched_skills.length})</span>
          <div class="flex flex-wrap gap-1">${matchedPills || '<span class="text-slate-500 text-xs">None</span>'}</div>
        </div>

        <!-- Missing Skills Gap -->
        ${
          job.missing_required.length > 0
            ? `
        <div class="space-y-1">
          <span class="text-[11px] font-semibold text-amber-400 uppercase tracking-wider block">Critical Missing Skills (${job.missing_required.length})</span>
          <div class="flex flex-wrap gap-1">${missingPills}</div>
        </div>
        `
            : ""
        }

        <!-- Learning Roadmap -->
        ${
          job.learning_roadmap && job.learning_roadmap.length > 0
            ? `
        <div class="p-3 rounded-xl bg-slate-900/60 border border-slate-700/60 space-y-1">
          <span class="text-[11px] font-semibold text-slate-300 flex items-center space-x-1">
            <i data-lucide="graduation-cap" class="w-3.5 h-3.5 text-sky-400"></i>
            <span>Recommended Upskilling Resource:</span>
          </span>
          <p class="text-xs text-slate-400"><strong>${job.learning_roadmap[0].topic}:</strong> ${job.learning_roadmap[0].resource}</p>
        </div>
        `
            : ""
        }
      </div>

      <!-- Quick Action Footer -->
      <div class="pt-4 border-t border-slate-700/70 flex items-center justify-between gap-2">
        <button class="btn-job-cover-letter px-3 py-1.5 rounded-lg bg-sky-500/10 hover:bg-sky-500/20 text-sky-400 border border-sky-500/30 text-xs font-medium transition flex items-center space-x-1" data-title="${job.title}">
          <i data-lucide="pen-tool" class="w-3 h-3"></i>
          <span>Tailor Cover Letter</span>
        </button>
        <button class="btn-job-interview-prep px-3 py-1.5 rounded-lg bg-slate-700 hover:bg-slate-600 text-slate-200 text-xs font-medium transition flex items-center space-x-1" data-job='${encodeURIComponent(JSON.stringify(job))}'>
          <i data-lucide="messages-square" class="w-3 h-3"></i>
          <span>Interview Prep</span>
        </button>
      </div>
    `;

    grid.appendChild(card);
  });

  // Attach quick action listeners
  grid.querySelectorAll(".btn-job-cover-letter").forEach((btn) => {
    btn.addEventListener("click", () => {
      const title = btn.getAttribute("data-title");
      document.getElementById("clJobTitle").value = title;
      document.querySelector('[data-target="tabCoverLetter"]').click();
      handleGenerateCoverLetter();
    });
  });

  grid.querySelectorAll(".btn-job-interview-prep").forEach((btn) => {
    btn.addEventListener("click", () => {
      const job = JSON.parse(decodeURIComponent(btn.getAttribute("data-job")));
      renderInterviewPrep(job);
      document.querySelector('[data-target="tabInterviewPrep"]').click();
    });
  });

  refreshIcons();
}

// Handle Custom JD Match
async function handleCustomJDMatch() {
  if (!currentAnalysisData) return;
  const jdText = document.getElementById("customJDTextArea").value.trim();
  if (!jdText || jdText.length < 20) {
    alert("Please paste a comprehensive job description.");
    return;
  }

  const btn = document.getElementById("btnMatchCustomJD");
  btn.innerHTML = `<i data-lucide="loader" class="w-4 h-4 animate-spin"></i><span>Analyzing...</span>`;
  refreshIcons();

  try {
    const res = await fetch("/api/match-custom-jd", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        resume_text: currentAnalysisData.parsed.raw_text,
        job_description: jdText,
      }),
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Match failed");

    const analysis = data.match_analysis;
    document.getElementById("customJDResultArea").classList.remove("hidden");
    document.getElementById("customJDScore").textContent = `${analysis.job_match_score}%`;
    document.getElementById("customJDMatchedCount").textContent = analysis.total_matched;
    document.getElementById("customJDMissingCount").textContent = analysis.missing_skills.length;

    // Matched skills pills
    const matchedContainer = document.getElementById("customJDMatchedSkillsPills");
    matchedContainer.innerHTML = analysis.matched_skills
      .map((s) => `<span class="px-2 py-0.5 rounded-md bg-emerald-500/15 text-emerald-400 border border-emerald-500/25 text-xs">${s}</span>`)
      .join("") || `<span class="text-xs text-slate-500">None detected</span>`;

    // Missing skills pills
    const missingContainer = document.getElementById("customJDMissingSkillsPills");
    missingContainer.innerHTML = analysis.missing_skills
      .map((s) => `<span class="px-2 py-0.5 rounded-md bg-amber-500/15 text-amber-400 border border-amber-500/25 text-xs font-medium">${s}</span>`)
      .join("") || `<span class="text-xs text-emerald-400">No major skill gaps identified!</span>`;

    // Tailoring Tips
    const tipsList = document.getElementById("customJDTailoringTips");
    tipsList.innerHTML = analysis.tailoring_recommendations.map((t) => `<li>${t}</li>`).join("");

    refreshIcons();
  } catch (err) {
    alert(err.message || "Failed to compare against job description.");
  } finally {
    btn.innerHTML = `<i data-lucide="scan-line" class="w-4 h-4"></i><span>Calculate Target Match & Gaps</span>`;
    refreshIcons();
  }
}

// Generate Cover Letter
async function handleGenerateCoverLetter() {
  if (!currentAnalysisData) return;
  const parsed = currentAnalysisData.parsed;
  const jobTitle = document.getElementById("clJobTitle").value.trim() || "Software Engineer";
  const company = document.getElementById("clCompany").value.trim() || "Hiring Team";

  const btn = document.getElementById("btnGenerateCoverLetter");
  btn.innerHTML = `<i data-lucide="loader" class="w-4 h-4 animate-spin"></i><span>Generating...</span>`;
  refreshIcons();

  try {
    const res = await fetch("/api/generate-cover-letter", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        candidate_name: parsed.contact.name || "Candidate",
        contact_info: parsed.contact,
        skills: parsed.skills.all_skills,
        job_title: jobTitle,
        company_name: company,
        experience_summary: parsed.sections.summary || "",
      }),
    });

    const data = await res.json();
    document.getElementById("coverLetterOutput").value = data.cover_letter;
  } catch (err) {
    console.error("Cover letter generation error", err);
  } finally {
    btn.innerHTML = `<i data-lucide="wand-sparkles" class="w-4 h-4"></i><span>Generate Customized Cover Letter</span>`;
    refreshIcons();
  }
}

// Render Interview Prep Accordions
async function renderInterviewPrep(job) {
  if (!currentAnalysisData) return;
  const parsed = currentAnalysisData.parsed;
  const jobTitle = job ? job.title : "Software Engineer";
  const missingSkills = job ? job.missing_required : [];

  try {
    const res = await fetch("/api/generate-interview-prep", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        skills: parsed.skills.all_skills,
        job_title: jobTitle,
        missing_skills: missingSkills,
      }),
    });

    const data = await res.json();
    const questions = data.questions || [];
    const container = document.getElementById("interviewQuestionsContainer");
    container.innerHTML = "";

    questions.forEach((q, idx) => {
      const card = document.createElement("div");
      card.className = "p-4 rounded-xl bg-slate-900/60 border border-slate-700/70 space-y-3";
      card.innerHTML = `
        <div class="flex items-start justify-between gap-2">
          <div class="space-y-1">
            <span class="px-2 py-0.5 rounded-full bg-sky-500/10 text-sky-400 border border-sky-500/20 text-[10px] font-bold uppercase tracking-wider">${q.category}</span>
            <h4 class="text-sm font-bold text-white">${idx + 1}. ${q.question}</h4>
          </div>
        </div>
        
        <div class="p-3 rounded-lg bg-slate-950/70 border border-slate-800 space-y-2 text-xs">
          <div class="text-slate-300">
            <strong class="text-amber-400 flex items-center space-x-1">
              <i data-lucide="lightbulb" class="w-3.5 h-3.5"></i>
              <span>Recruiter Coaching Tip:</span>
            </strong>
            <p class="mt-0.5 text-slate-400">${q.tip}</p>
          </div>
          <div class="border-t border-slate-800 pt-2 text-slate-300">
            <strong class="text-emerald-400 flex items-center space-x-1">
              <i data-lucide="target" class="w-3.5 h-3.5"></i>
              <span>Recommended STAR Answer Framework:</span>
            </strong>
            <pre class="font-sans text-slate-400 mt-1 whitespace-pre-line">${q.star_framework}</pre>
          </div>
        </div>
      `;
      container.appendChild(card);
    });

    refreshIcons();
  } catch (err) {
    console.error("Interview prep error", err);
  }
}

// Render Categorized Skills Tree
function renderSkillsTree(skillsData) {
  const container = document.getElementById("skillsCategoriesContainer");
  document.getElementById("totalSkillsCountBadge").textContent = `${skillsData.total_count} Total Skills`;
  container.innerHTML = "";

  const categorized = skillsData.categorized || {};
  Object.entries(categorized).forEach(([category, skills]) => {
    const card = document.createElement("div");
    card.className = "p-4 rounded-xl bg-slate-900/60 border border-slate-700/70 space-y-2";
    card.innerHTML = `
      <h4 class="text-xs font-bold text-sky-400 uppercase tracking-wider flex items-center justify-between">
        <span>${category}</span>
        <span class="text-slate-500">${skills.length}</span>
      </h4>
      <div class="flex flex-wrap gap-1.5 pt-1">
        ${skills.map((s) => `<span class="px-2.5 py-1 rounded-lg bg-slate-800 text-slate-200 border border-slate-700 text-xs">${s}</span>`).join("")}
      </div>
    `;
    container.appendChild(card);
  });
}

// Export Analysis Report
function exportAnalysisReport() {
  if (!currentAnalysisData) return;
  const parsed = currentAnalysisData.parsed;
  const evalData = currentAnalysisData.evaluation;
  const jobs = currentAnalysisData.job_matches;

  const reportMarkdown = `# CareerCraft AI - Resume & Career Diagnostics Report
Candidate: ${parsed.contact.name || "Candidate"}
Overall ATS Score: ${evalData.overall_score}/100 (${evalData.grade})
Total Skills Extracted: ${evalData.metrics_summary.total_skills}
Word Count: ${evalData.metrics_summary.total_words} words

---

## 1. ATS Sub-Scores
${Object.values(evalData.sub_scores)
  .map((s) => `- **${s.label}**: ${s.score}/100 (${s.weight})`)
  .join("\n")}

## 2. Key Strengths
${evalData.strengths.map((st) => `- ✅ ${st}`).join("\n")}

## 3. Critical Improvements & Fixes
${evalData.critical_issues.map((cr) => `- ❌ [Critical] ${cr}`).join("\n")}
${evalData.improvements.map((im) => `- ⚠️ [${im.type.toUpperCase()}] ${im.message}`).join("\n")}

## 4. Top Job Suggestions & Skill Gap
${jobs
  .slice(0, 5)
  .map(
    (j) => `### ${j.title} (${j.match_percentage}% Match)
- **Category & Level**: ${j.category} | ${j.level}
- **Salary Range**: ${j.salary_range}
- **Matching Skills**: ${j.matched_skills.join(", ")}
- **Missing Requirements**: ${j.missing_required.join(", ") || "None"}
`
  )
  .join("\n")}

---
Generated by CareerCraft AI
`;

  const blob = new Blob([reportMarkdown], { type: "text/markdown" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `CareerCraft_Report_${(parsed.contact.name || "Candidate").replace(/\s+/g, "_")}.md`;
  a.click();
  URL.revokeObjectURL(url);
}

