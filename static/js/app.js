/**
 * EduGenie - Production-Level AI Learning Assistant
 * Frontend Modular Application Controller
 */

document.addEventListener("DOMContentLoaded", () => {
  "use strict";

  // ==========================================================================
  // Global Application State
  // ==========================================================================
  const state = {
    currentView: "dashboard",
    theme: localStorage.getItem("edugenie-theme") || "system",
    isGeminiConfigured: false,
    activeModel: "gemini-3.5-flash",
    // Active Q&A State
    lastQaRequest: null,
    lastQaResponse: null,
    // Active Explain State
    lastExplainRequest: null,
    // Active Quiz Session State
    activeQuiz: null,
    quizCurrentIndex: 0,
    userQuizAnswers: {}, // questionId -> selectedOptionKey ("A", "B", "C", "D")
    // History Filter State
    historyFilter: "all",
    historySearch: "",
    historyItems: [],
  };

  // ==========================================================================
  // DOM References Cache
  // ==========================================================================
  const dom = {
    // Layout & Navigation
    views: document.querySelectorAll(".content-view"),
    navItems: document.querySelectorAll(".nav-item"),
    mobileNavToggle: document.getElementById("mobileNavToggle"),
    sidebarCloseBtn: document.getElementById("sidebarCloseBtn"),
    sidebar: document.getElementById("appSidebar"),
    sidebarOverlay: document.getElementById("sidebarOverlay"),
    viewTitle: document.getElementById("currentViewTitle"),
    viewSubtitle: document.getElementById("currentViewSubtitle"),
    aiStatusPill: document.getElementById("aiStatusPill"),
    aiStatusLabel: document.getElementById("aiStatusLabel"),
    themeToggleBtn: document.getElementById("themeToggleBtn"),
    mobileThemeToggle: document.getElementById("mobileThemeToggle"),
    toastContainer: document.getElementById("toastContainer"),

    // Dashboard Home
    dashQuestionsCount: document.getElementById("dashQuestionsCount"),
    dashConceptsCount: document.getElementById("dashConceptsCount"),
    dashQuizzesCount: document.getElementById("dashQuizzesCount"),
    dashAccuracyRate: document.getElementById("dashAccuracyRate"),
    dashRecentActivityContainer: document.getElementById("dashRecentActivityContainer"),

    // Q&A
    qaForm: document.getElementById("qaForm"),
    qaQuestionInput: document.getElementById("qaQuestionInput"),
    qaContextInput: document.getElementById("qaContextInput"),
    qaSubmitBtn: document.getElementById("qaSubmitBtn"),
    qaClearBtn: document.getElementById("qaClearBtn"),
    qaLoadingState: document.getElementById("qaLoadingState"),
    qaEmptyState: document.getElementById("qaEmptyState"),
    qaResultCard: document.getElementById("qaResultCard"),
    qaAnswerText: document.getElementById("qaAnswerText"),
    qaSimpleExplanationText: document.getElementById("qaSimpleExplanationText"),
    qaKeyPointsList: document.getElementById("qaKeyPointsList"),
    qaExampleWrapper: document.getElementById("qaExampleWrapper"),
    qaExampleBox: document.getElementById("qaExampleBox"),
    qaCopyBtn: document.getElementById("qaCopyBtn"),
    qaRegenerateBtn: document.getElementById("qaRegenerateBtn"),
    qaFollowUpInput: document.getElementById("qaFollowUpInput"),
    qaFollowUpBtn: document.getElementById("qaFollowUpBtn"),
    qaModelUsedBadge: document.getElementById("qaModelUsedBadge"),

    // Concept Explanation
    explainForm: document.getElementById("explainForm"),
    explainConceptInput: document.getElementById("explainConceptInput"),
    explainDifficultySelect: document.getElementById("explainDifficultySelect"),
    explainStyleSelect: document.getElementById("explainStyleSelect"),
    explainSubmitBtn: document.getElementById("explainSubmitBtn"),
    explainClearBtn: document.getElementById("explainClearBtn"),
    explainLoadingState: document.getElementById("explainLoadingState"),
    explainEmptyState: document.getElementById("explainEmptyState"),
    explainResultCard: document.getElementById("explainResultCard"),
    explainConceptBadge: document.getElementById("explainConceptBadge"),
    explainDifficultyBadge: document.getElementById("explainDifficultyBadge"),
    explainStyleBadge: document.getElementById("explainStyleBadge"),
    explainSimpleText: document.getElementById("explainSimpleText"),
    explainHowText: document.getElementById("explainHowText"),
    explainExampleBox: document.getElementById("explainExampleBox"),
    explainKeyPointsList: document.getElementById("explainKeyPointsList"),
    explainExamTipsWrapper: document.getElementById("explainExamTipsWrapper"),
    explainExamTipsText: document.getElementById("explainExamTipsText"),
    explainCopyBtn: document.getElementById("explainCopyBtn"),
    explainRegenerateBtn: document.getElementById("explainRegenerateBtn"),

    // Quiz Generator
    quizGenForm: document.getElementById("quizGenForm"),
    quizTopicInput: document.getElementById("quizTopicInput"),
    quizNumSelect: document.getElementById("quizNumSelect"),
    quizDifficultySelect: document.getElementById("quizDifficultySelect"),
    quizPassageInput: document.getElementById("quizPassageInput"),
    quizGenSubmitBtn: document.getElementById("quizGenSubmitBtn"),
    quizLoadingState: document.getElementById("quizLoadingState"),
    quizEmptyState: document.getElementById("quizEmptyState"),
    quizSessionCard: document.getElementById("quizSessionCard"),
    quizTopicBadge: document.getElementById("quizTopicBadge"),
    quizDiffBadge: document.getElementById("quizDiffBadge"),
    quizProgressText: document.getElementById("quizProgressText"),
    quizProgressBarFill: document.getElementById("quizProgressBarFill"),
    quizQuestionNumberTag: document.getElementById("quizQuestionNumberTag"),
    quizQuestionText: document.getElementById("quizQuestionText"),
    quizOptionsContainer: document.getElementById("quizOptionsContainer"),
    quizPrevBtn: document.getElementById("quizPrevBtn"),
    quizNextBtn: document.getElementById("quizNextBtn"),
    quizSubmitBtn: document.getElementById("quizSubmitBtn"),
    quizDotsTrack: document.getElementById("quizDotsTrack"),
    quizResultsCard: document.getElementById("quizResultsCard"),
    quizFinalScoreNum: document.getElementById("quizFinalScoreNum"),
    quizFeedbackHeading: document.getElementById("quizFeedbackTitle"),
    quizFeedbackBody: document.getElementById("quizFeedbackBody"),
    quizCorrectCount: document.getElementById("quizCorrectCount"),
    quizIncorrectCount: document.getElementById("quizIncorrectCount"),
    quizAccuracyPct: document.getElementById("quizAccuracyPct"),
    quizScoreBadge: document.getElementById("quizScoreBadge"),
    quizReviewList: document.getElementById("quizReviewList"),
    quizRetryBtn: document.getElementById("quizRetryBtn"),
    quizNewBtn: document.getElementById("quizNewBtn"),

    // Summarize
    summaryForm: document.getElementById("summaryForm"),
    summaryContentInput: document.getElementById("summaryContentInput"),
    summaryCharCounter: document.getElementById("summaryCharCounter"),
    summarySubmitBtn: document.getElementById("summarySubmitBtn"),
    summaryClearBtn: document.getElementById("summaryClearBtn"),
    summaryLoadingState: document.getElementById("summaryLoadingState"),
    summaryEmptyState: document.getElementById("summaryEmptyState"),
    summaryResultCard: document.getElementById("summaryResultCard"),
    summaryMainText: document.getElementById("summaryMainText"),
    summaryKeyPointsList: document.getElementById("summaryKeyPointsList"),
    summaryTermsGrid: document.getElementById("summaryTermsGrid"),
    summaryQuickRevisionList: document.getElementById("summaryQuickRevisionList"),
    summaryLengthBadge: document.getElementById("summaryLengthBadge"),
    summaryOriginalLengthBadge: document.getElementById("summaryOriginalLengthBadge"),
    summaryCopyBtn: document.getElementById("summaryCopyBtn"),
    summaryDownloadBtn: document.getElementById("summaryDownloadBtn"),
    loadSampleNotesBtn: document.getElementById("loadSampleNotesBtn"),

    // Learning Path
    learningForm: document.getElementById("learningForm"),
    learningTopicInput: document.getElementById("learningTopicInput"),
    learningLevelSelect: document.getElementById("learningLevelSelect"),
    learningTimeInput: document.getElementById("learningTimeInput"),
    learningGoalInput: document.getElementById("learningGoalInput"),
    learningSubmitBtn: document.getElementById("learningSubmitBtn"),
    learningLoadingState: document.getElementById("learningLoadingState"),
    learningEmptyState: document.getElementById("learningEmptyState"),
    learningResultCard: document.getElementById("learningResultCard"),
    learningOverviewText: document.getElementById("learningOverviewText"),
    roadmapTimelineContainer: document.getElementById("roadmapTimelineContainer"),
    learningTopicBadge: document.getElementById("learningTopicBadge"),
    learningLevelBadge: document.getElementById("learningLevelBadge"),
    learningTimeBadge: document.getElementById("learningTimeBadge"),
    learningCopyBtn: document.getElementById("learningCopyBtn"),

    // History
    historyListContainer: document.getElementById("historyListContainer"),
    historySearchInput: document.getElementById("historySearchInput"),
    clearAllHistoryBtn: document.getElementById("clearAllHistoryBtn"),
    historyFilterPills: document.querySelectorAll(".pill-filter"),

    // Progress
    metricQuestionsCount: document.getElementById("metricQuestionsCount"),
    metricConceptsCount: document.getElementById("metricConceptsCount"),
    metricQuizzesCount: document.getElementById("metricQuizzesCount"),
    metricAccuracyPct: document.getElementById("metricAccuracyPct"),
    metricRoadmapsCount: document.getElementById("metricRoadmapsCount"),
    weeklyActivityBarChart: document.getElementById("weeklyActivityBarChart"),

    // Settings Modal
    openSettingsBtn: document.getElementById("openSettingsBtn"),
    settingsModal: document.getElementById("settingsModal"),
    closeSettingsModalBtn: document.getElementById("closeSettingsModalBtn"),
    cancelSettingsBtn: document.getElementById("cancelSettingsBtn"),
    settingsForm: document.getElementById("settingsForm"),
    saveSettingsBtn: document.getElementById("saveSettingsBtn"),
    settingsApiKeyInput: document.getElementById("settingsApiKeyInput"),
    toggleApiKeyVisibilityBtn: document.getElementById("toggleApiKeyVisibilityBtn"),
    settingsModelSelect: document.getElementById("settingsModelSelect"),
    settingsStatusHeading: document.getElementById("settingsStatusHeading"),
    settingsStatusDesc: document.getElementById("settingsStatusDesc"),

    // History Item Detail Modal
    historyDetailModal: document.getElementById("historyDetailModal"),
    closeHistoryDetailModalBtn: document.getElementById("closeHistoryDetailModalBtn"),
    closeHistoryDetailBtn: document.getElementById("closeHistoryDetailBtn"),
    historyDetailTitle: document.getElementById("historyDetailTitle"),
    historyDetailBadge: document.getElementById("historyDetailBadge"),
    historyDetailBody: document.getElementById("historyDetailBody"),
  };

  // View Metadata Dictionary for Header Updates
  const viewMeta = {
    dashboard: {
      title: "Dashboard",
      subtitle: "Learn Smarter with your AI-Powered Study Companion",
    },
    qa: {
      title: "Ask Question",
      subtitle: "Get structured answers, simple explanations, and examples",
    },
    explain: {
      title: "Explain Concept",
      subtitle: "Demystify complex topics by difficulty and pedagogical style",
    },
    quiz: {
      title: "Quiz Generator",
      subtitle: "Test your mastery with rigorous MCQs and instant explanations",
    },
    summarize: {
      title: "Summarize Notes",
      subtitle: "Synthesize textbook chapters and notes into high-yield summaries",
    },
    learning: {
      title: "Personalized Learning Path",
      subtitle: "Visual sequential roadmap adapted to your time and goals",
    },
    history: {
      title: "Activity History",
      subtitle: "Review, search, and reload previous learning sessions",
    },
    progress: {
      title: "Progress & Analytics",
      subtitle: "Real metrics and weekly performance tracked from your activity",
    },
  };

  // ==========================================================================
  // Core Helper: API Request Client with Error Boundaries
  // ==========================================================================
  async function apiCall(endpoint, method = "GET", data = null, submitButton = null) {
    if (submitButton) {
      submitButton.disabled = true;
      submitButton.dataset.originalHtml = submitButton.innerHTML;
      submitButton.innerHTML = `<span class="spinner-ring" style="width:16px;height:16px;border-width:2px;display:inline-block;vertical-align:middle;margin-right:6px;"></span> Processing...`;
    }

    try {
      const options = {
        method: method,
        headers: {
          "Content-Type": "application/json",
          "Accept": "application/json",
        },
      };

      if (data && (method === "POST" || method === "PUT" || method === "PATCH")) {
        options.body = JSON.stringify(data);
      }

      const response = await fetch(endpoint, options);
      const resJson = await response.json();

      if (!response.ok || resJson.success === false) {
        const errorMsg = resJson.message || `Server returned error (${response.status})`;
        throw new Error(errorMsg);
      }

      return resJson.data;
    } catch (err) {
      console.error(`API Call failed on ${endpoint}:`, err);
      showToast(err.message || "Something went wrong. Please try again.", "error");
      throw err;
    } finally {
      if (submitButton) {
        submitButton.disabled = false;
        if (submitButton.dataset.originalHtml) {
          submitButton.innerHTML = submitButton.dataset.originalHtml;
        }
      }
    }
  }

  // ==========================================================================
  // Toast Notification System
  // ==========================================================================
  function showToast(message, type = "info", duration = 3600) {
    const toast = document.createElement("div");
    toast.className = `toast toast-${type}`;
    
    let iconSvg = "ℹ️";
    if (type === "success") iconSvg = "✓";
    else if (type === "error") iconSvg = "✕";

    toast.innerHTML = `<span style="font-weight:700;">${iconSvg}</span> <span>${escapeHtml(message)}</span>`;
    dom.toastContainer.appendChild(toast);

    setTimeout(() => {
      toast.style.transition = "opacity 0.3s ease, transform 0.3s ease";
      toast.style.opacity = "0";
      toast.style.transform = "translateX(20px)";
      setTimeout(() => toast.remove(), 300);
    }, duration);
  }

  function escapeHtml(text) {
    if (!text) return "";
    return String(text)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  // ==========================================================================
  // Theme Management (Light, Dark, System Preference)
  // ==========================================================================
  function applyTheme(themeName) {
    state.theme = themeName;
    localStorage.setItem("edugenie-theme", themeName);

    if (themeName === "system") {
      const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
      document.documentElement.setAttribute("data-theme", prefersDark ? "dark" : "light");
    } else {
      document.documentElement.setAttribute("data-theme", themeName);
    }

    // Sync radio inputs in settings
    const themeRadio = document.querySelector(`input[name="appTheme"][value="${themeName}"]`);
    if (themeRadio) themeRadio.checked = true;
  }

  function toggleThemeQuickly() {
    const currentTheme = document.documentElement.getAttribute("data-theme");
    const nextTheme = currentTheme === "dark" ? "light" : "dark";
    applyTheme(nextTheme);
    showToast(`Switched to ${nextTheme} theme`, "info", 1800);
  }

  // Listen for OS theme changes if on system
  window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", (e) => {
    if (state.theme === "system") {
      document.documentElement.setAttribute("data-theme", e.matches ? "dark" : "light");
    }
  });

  // Apply initially stored theme
  applyTheme(state.theme);

  // ==========================================================================
  // Navigation & View Routing
  // ==========================================================================
  function navigateTo(viewId) {
    if (!viewMeta[viewId]) return;

    state.currentView = viewId;

    // Update active nav button
    dom.navItems.forEach((btn) => {
      btn.classList.toggle("active", btn.dataset.view === viewId);
    });

    // Update visible view container
    dom.views.forEach((view) => {
      view.classList.toggle("active", view.id === `view-${viewId}`);
    });

    // Update Topbar Title & Subtitle
    dom.viewTitle.textContent = viewMeta[viewId].title;
    dom.viewSubtitle.textContent = viewMeta[viewId].subtitle;

    // Close mobile sidebar if open
    closeMobileSidebar();

    // Trigger view-specific data refresh
    if (viewId === "dashboard" || viewId === "progress") {
      loadProgressMetrics();
    } else if (viewId === "history") {
      loadHistory();
    }

    // Scroll to top of viewport
    document.querySelector(".view-content-area").scrollTo({ top: 0, behavior: "smooth" });
  }

  function openMobileSidebar() {
    dom.sidebar.classList.add("open");
    dom.sidebarOverlay.classList.add("active");
  }

  function closeMobileSidebar() {
    dom.sidebar.classList.remove("open");
    dom.sidebarOverlay.classList.remove("active");
  }

  // ==========================================================================
  // System Health & Settings
  // ==========================================================================
  async function checkSystemHealth() {
    try {
      const res = await apiCall("/api/settings", "GET");
      state.isGeminiConfigured = res.is_gemini_configured;
      state.activeModel = res.current_model;

      const dot = document.querySelector(".system-status-dot");
      if (state.isGeminiConfigured) {
        if (dom.aiStatusPill) dom.aiStatusPill.className = "status-pill status-pill-active";
        if (dom.aiStatusLabel) dom.aiStatusLabel.textContent = `Gemini AI (${res.current_model})`;
        if (dom.settingsStatusHeading) dom.settingsStatusHeading.textContent = "Google Gemini Live AI Connected";
        if (dom.settingsStatusDesc) dom.settingsStatusDesc.textContent = `Active model: ${res.current_model}. Ready for live inference.`;
        if (dot) dot.style.backgroundColor = "#10b981";
      } else {
        if (dom.aiStatusPill) dom.aiStatusPill.className = "status-pill status-pill-fallback";
        if (dom.aiStatusLabel) dom.aiStatusLabel.textContent = "Demonstration Mode (Offline)";
        if (dom.settingsStatusHeading) dom.settingsStatusHeading.textContent = "Operating in Demonstration Mode";
        if (dom.settingsStatusDesc) dom.settingsStatusDesc.textContent = "No GEMINI_API_KEY detected in .env. Enter your key below or add it to .env for live Gemini AI.";
        if (dot) dot.style.backgroundColor = "#f59e0b";
      }

      if (dom.settingsModelSelect) {
        dom.settingsModelSelect.value = res.current_model;
      }
    } catch (e) {
      if (dom.aiStatusPill) dom.aiStatusPill.className = "status-pill status-pill-fallback";
      if (dom.aiStatusLabel) dom.aiStatusLabel.textContent = "Offline Mode";
    }
  }

  // ==========================================================================
  // Live Streaming Typewriter Engine
  // ==========================================================================
  let currentActiveTyping = null;

  function typewriterLive(targetElement, fullText, speed = 12, onComplete = null) {
    if (currentActiveTyping) {
      currentActiveTyping.cancel();
      currentActiveTyping = null;
    }

    targetElement.innerHTML = "";
    const cursor = document.createElement("span");
    cursor.className = "live-cursor";
    targetElement.appendChild(cursor);

    let index = 0;
    let isCancelled = false;

    // Type 2-3 characters per tick for fluid responsiveness
    const timer = setInterval(() => {
      if (isCancelled || index >= fullText.length) {
        clearInterval(timer);
        cursor.remove();
        targetElement.textContent = fullText;
        currentActiveTyping = null;
        if (onComplete && !isCancelled) onComplete();
        return;
      }

      const chunk = fullText.slice(index, index + 2);
      targetElement.insertBefore(document.createTextNode(chunk), cursor);
      index += 2;
    }, speed);

    const controller = {
      cancel: () => {
        isCancelled = true;
        clearInterval(timer);
        cursor.remove();
        targetElement.textContent = fullText;
      },
    };

    currentActiveTyping = controller;

    // 1-click allows user to immediately skip animation if they want fast reading
    targetElement.onclick = () => {
      if (currentActiveTyping === controller) {
        controller.cancel();
        currentActiveTyping = null;
        if (onComplete) onComplete();
      }
    };

    return controller;
  }

  // ==========================================================================
  // Module 1: Ask Question (Q&A) - Live Streaming Mode
  // ==========================================================================
  async function handleQaSubmit(e) {
    e.preventDefault();
    const question = dom.qaQuestionInput.value.trim();
    const context = dom.qaContextInput.value.trim();

    if (!question) {
      showToast("Please enter a question before continuing.", "error");
      dom.qaQuestionInput.focus();
      return;
    }

    state.lastQaRequest = { question, context };

    // Toggle UI States
    dom.qaEmptyState.classList.add("hidden");
    dom.qaResultCard.classList.add("hidden");
    dom.qaLoadingState.classList.remove("hidden");

    try {
      const data = await apiCall(
        "/api/qa",
        "POST",
        { question, context: context || null },
        dom.qaSubmitBtn
      );

      state.lastQaResponse = data;
      renderQaResult(data);
      loadProgressMetrics(); // update dashboard count
    } catch (err) {
      dom.qaLoadingState.classList.add("hidden");
      dom.qaEmptyState.classList.remove("hidden");
    }
  }

  function renderQaResult(data) {
    dom.qaLoadingState.classList.add("hidden");
    dom.qaEmptyState.classList.add("hidden");
    dom.qaResultCard.classList.remove("hidden");

    // Dynamic Live Indicator Badge
    dom.qaModelUsedBadge.innerHTML = `<span class="live-indicator-badge"><span class="live-pulse-dot"></span> Streaming Live</span>`;

    // Reset container contents
    dom.qaAnswerText.textContent = "";
    dom.qaSimpleExplanationText.textContent = "";
    dom.qaKeyPointsList.innerHTML = "";
    dom.qaExampleBox.textContent = "";

    // Temporarily soften opacity of remaining sections during live answer stream
    dom.qaSimpleExplanationText.parentElement.style.opacity = "0.2";
    dom.qaKeyPointsList.parentElement.style.opacity = "0.2";
    dom.qaExampleWrapper.style.opacity = "0.2";

    // 1. Live stream Answer
    typewriterLive(dom.qaAnswerText, data.answer, 12, () => {
      // 2. Reveal Simple Explanation
      dom.qaSimpleExplanationText.parentElement.style.transition = "opacity 0.4s ease";
      dom.qaSimpleExplanationText.parentElement.style.opacity = "1";

      typewriterLive(dom.qaSimpleExplanationText, data.simple_explanation, 10, () => {
        // 3. Reveal Key Points with staggered animation
        dom.qaKeyPointsList.parentElement.style.transition = "opacity 0.4s ease";
        dom.qaKeyPointsList.parentElement.style.opacity = "1";

        if (Array.isArray(data.key_points)) {
          data.key_points.forEach((point, idx) => {
            const li = document.createElement("li");
            li.className = "fade-in-stagger";
            li.style.animationDelay = `${idx * 0.1}s`;
            li.textContent = point;
            dom.qaKeyPointsList.appendChild(li);
          });
        }

        // 4. Reveal Example
        if (data.example) {
          dom.qaExampleWrapper.classList.remove("hidden");
          dom.qaExampleWrapper.style.transition = "opacity 0.4s ease";
          dom.qaExampleWrapper.style.opacity = "1";
          dom.qaExampleBox.textContent = data.example;
        } else {
          dom.qaExampleWrapper.classList.add("hidden");
        }

        // Update badge to complete
        dom.qaModelUsedBadge.textContent = data.model_used || "Gemini AI";
        showToast("Answer formulated live!", "success", 2000);
      });
    });
  }

  async function handleQaFollowUp() {
    const followUp = dom.qaFollowUpInput.value.trim();
    if (!followUp) return;

    if (!state.lastQaResponse) {
      showToast("No active question context found.", "error");
      return;
    }

    const previousContext = `Previous Answer Summary: ${state.lastQaResponse.simple_explanation.slice(0, 300)}`;
    dom.qaFollowUpInput.value = "";

    dom.qaResultCard.classList.add("hidden");
    dom.qaLoadingState.classList.remove("hidden");

    try {
      const data = await apiCall(
        "/api/qa",
        "POST",
        {
          question: followUp,
          context: state.lastQaRequest ? state.lastQaRequest.context : null,
          follow_up_to: previousContext,
        },
        dom.qaFollowUpBtn
      );

      state.lastQaResponse = data;
      renderQaResult(data);
    } catch (err) {
      dom.qaLoadingState.classList.add("hidden");
      dom.qaResultCard.classList.remove("hidden");
    }
  }

  // ==========================================================================
  // Module 2: Explain Concept - Live Professor Step Flow
  // ==========================================================================
  async function handleExplainSubmit(e) {
    e.preventDefault();
    const concept = dom.explainConceptInput.value.trim();
    const difficulty = dom.explainDifficultySelect.value;
    const style = dom.explainStyleSelect.value;

    if (!concept) {
      showToast("Please enter a concept to explain.", "error");
      dom.explainConceptInput.focus();
      return;
    }

    state.lastExplainRequest = { concept, difficulty, style };

    dom.explainEmptyState.classList.add("hidden");
    dom.explainResultCard.classList.add("hidden");
    dom.explainLoadingState.classList.remove("hidden");

    try {
      const data = await apiCall(
        "/api/explain",
        "POST",
        { concept, difficulty, style },
        dom.explainSubmitBtn
      );

      renderExplainResult(data);
      loadProgressMetrics();
    } catch (err) {
      dom.explainLoadingState.classList.add("hidden");
      dom.explainEmptyState.classList.remove("hidden");
    }
  }

  function renderExplainResult(data) {
    dom.explainLoadingState.classList.add("hidden");
    dom.explainEmptyState.classList.add("hidden");
    dom.explainResultCard.classList.remove("hidden");

    dom.explainConceptBadge.textContent = data.concept;
    dom.explainDifficultyBadge.textContent = data.difficulty.toUpperCase();
    dom.explainStyleBadge.innerHTML = `<span class="live-indicator-badge"><span class="live-pulse-dot"></span> Live Breakdown</span>`;

    const flowBlocks = document.querySelectorAll(".concept-breakdown-flow .flow-block");
    flowBlocks.forEach((fb) => (fb.style.opacity = "0.25"));

    // Activate Stage 1: Simple Overview
    if (flowBlocks[0]) {
      flowBlocks[0].style.opacity = "1";
      flowBlocks[0].classList.add("flow-step-active");
    }

    typewriterLive(dom.explainSimpleText, data.simple_explanation, 12, () => {
      // Activate Stage 2: How It Works
      if (flowBlocks[0]) flowBlocks[0].classList.remove("flow-step-active");
      if (flowBlocks[1]) {
        flowBlocks[1].style.opacity = "1";
        flowBlocks[1].classList.add("flow-step-active");
      }

      typewriterLive(dom.explainHowText, data.how_it_works, 10, () => {
        if (flowBlocks[1]) flowBlocks[1].classList.remove("flow-step-active");

        // Activate Stage 3: Concrete Example
        if (flowBlocks[2]) {
          flowBlocks[2].style.opacity = "1";
          flowBlocks[2].classList.add("fade-in-stagger");
          dom.explainExampleBox.textContent = data.example;
        }

        // Activate Stage 4: Key Points
        if (flowBlocks[3]) {
          flowBlocks[3].style.opacity = "1";
          dom.explainKeyPointsList.innerHTML = "";
          if (Array.isArray(data.key_points)) {
            data.key_points.forEach((pt, idx) => {
              const li = document.createElement("li");
              li.className = "fade-in-stagger";
              li.style.animationDelay = `${idx * 0.12}s`;
              li.textContent = pt;
              dom.explainKeyPointsList.appendChild(li);
            });
          }
        }

        // Activate Stage 5: Exam Tips
        if (flowBlocks[4]) {
          if (data.exam_tips) {
            flowBlocks[4].classList.remove("hidden");
            flowBlocks[4].style.opacity = "1";
            dom.explainExamTipsText.textContent = data.exam_tips;
          } else {
            flowBlocks[4].classList.add("hidden");
          }
        }

        dom.explainStyleBadge.textContent = data.style.replace("_", " ").toUpperCase();
        showToast("Concept explained live!", "success", 2000);
      });
    });
  }

  // ==========================================================================
  // Module 3: Quiz Generator & Interactive Session
  // ==========================================================================
  async function handleQuizGenerate(e) {
    e.preventDefault();
    const topic = dom.quizTopicInput.value.trim();
    const num_questions = parseInt(dom.quizNumSelect.value, 10);
    const difficulty = dom.quizDifficultySelect.value;
    const passage = dom.quizPassageInput.value.trim();

    if (!topic) {
      showToast("Please enter a quiz topic.", "error");
      dom.quizTopicInput.focus();
      return;
    }

    dom.quizEmptyState.classList.add("hidden");
    dom.quizSessionCard.classList.add("hidden");
    dom.quizResultsCard.classList.add("hidden");
    dom.quizLoadingState.classList.remove("hidden");

    try {
      const data = await apiCall(
        "/api/quiz",
        "POST",
        { topic, num_questions, difficulty, passage: passage || null },
        dom.quizGenSubmitBtn
      );

      state.activeQuiz = data;
      state.quizCurrentIndex = 0;
      state.userQuizAnswers = {};

      dom.quizLoadingState.classList.add("hidden");
      dom.quizSessionCard.classList.remove("hidden");

      renderActiveQuizQuestion();
      showToast(`Quiz generated! ${data.total_questions} questions ready.`, "success");
    } catch (err) {
      dom.quizLoadingState.classList.add("hidden");
      dom.quizEmptyState.classList.remove("hidden");
    }
  }

  function renderActiveQuizQuestion() {
    const quiz = state.activeQuiz;
    if (!quiz || !quiz.questions || quiz.questions.length === 0) return;

    const total = quiz.questions.length;
    const idx = state.quizCurrentIndex;
    const q = quiz.questions[idx];

    dom.quizTopicBadge.textContent = quiz.topic;
    dom.quizDiffBadge.textContent = quiz.difficulty.toUpperCase();

    // Progress
    dom.quizProgressText.textContent = `Question ${idx + 1} of ${total}`;
    const pct = Math.round(((idx + 1) / total) * 100);
    dom.quizProgressBarFill.style.width = `${pct}%`;

    // Question Text
    dom.quizQuestionNumberTag.textContent = `Question ${idx + 1}`;
    dom.quizQuestionText.textContent = q.question;

    // Render Options
    dom.quizOptionsContainer.innerHTML = "";
    q.options.forEach((opt) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "quiz-option-btn";
      if (state.userQuizAnswers[q.id] === opt.key) {
        btn.classList.add("selected");
      }

      btn.innerHTML = `
        <span class="option-badge-key">${opt.key}</span>
        <span class="option-text">${escapeHtml(opt.text)}</span>
      `;

      btn.addEventListener("click", () => {
        state.userQuizAnswers[q.id] = opt.key;
        renderActiveQuizQuestion(); // re-render to update selected style & dots
      });

      dom.quizOptionsContainer.appendChild(btn);
    });

    // Render Dots Track
    dom.quizDotsTrack.innerHTML = "";
    quiz.questions.forEach((item, dotIdx) => {
      const dot = document.createElement("div");
      dot.className = "quiz-dot";
      if (dotIdx === idx) dot.classList.add("active");
      if (state.userQuizAnswers[item.id]) dot.classList.add("answered");
      dom.quizDotsTrack.appendChild(dot);
    });

    // Navigation Buttons State
    dom.quizPrevBtn.disabled = idx === 0;
    if (idx === total - 1) {
      dom.quizNextBtn.classList.add("hidden");
      dom.quizSubmitBtn.classList.remove("hidden");
    } else {
      dom.quizNextBtn.classList.remove("hidden");
      dom.quizSubmitBtn.classList.add("hidden");
    }
  }

  async function handleQuizSubmit() {
    const quiz = state.activeQuiz;
    if (!quiz) return;

    const unanswered = quiz.questions.filter((q) => !state.userQuizAnswers[q.id]);
    if (unanswered.length > 0) {
      const confirmSubmit = confirm(
        `You have ${unanswered.length} unanswered question(s). Do you still wish to submit the quiz?`
      );
      if (!confirmSubmit) return;
    }

    try {
      const result = await apiCall(
        "/api/quiz/evaluate",
        "POST",
        {
          quiz_id: quiz.quiz_id,
          user_answers: state.userQuizAnswers,
        },
        dom.quizSubmitBtn
      );

      renderQuizEvaluation(result);
      showToast("Quiz submitted and evaluated!", "success");
      loadProgressMetrics();
    } catch (err) {
      // Handled in apiCall
    }
  }

  function renderQuizEvaluation(result) {
    dom.quizSessionCard.classList.add("hidden");
    dom.quizResultsCard.classList.remove("hidden");

    dom.quizFinalScoreNum.textContent = `${result.correct_count}/${result.total_questions}`;
    dom.quizScoreBadge.textContent = `Accuracy: ${result.score_percentage}%`;
    dom.quizCorrectCount.textContent = result.correct_count;
    dom.quizIncorrectCount.textContent = result.incorrect_count;
    dom.quizAccuracyPct.textContent = `${result.score_percentage}%`;

    dom.quizFeedbackHeading.textContent = result.passed ? "Well Done! Quiz Passed" : "Good Effort!";
    dom.quizFeedbackBody.textContent = result.feedback;

    // Render review of each question
    dom.quizReviewList.innerHTML = "";
    result.results.forEach((item, index) => {
      const reviewBox = document.createElement("div");
      reviewBox.className = "quiz-review-item";

      const isCorrect = item.is_correct;
      const statusPill = isCorrect
        ? `<span class="pill pill-correct">Correct ✓</span>`
        : `<span class="pill pill-incorrect">Incorrect ✕</span>`;

      const userAnsText = item.user_answer ? `Option ${item.user_answer}` : "Unanswered";
      const correctAnsText = `Option ${item.correct_answer}`;

      reviewBox.innerHTML = `
        <div class="review-question-header">
          <span style="font-size:0.78rem;font-weight:700;color:var(--text-muted);text-transform:uppercase;">Question ${index + 1}</span>
          ${statusPill}
        </div>
        <p class="review-q-text">${escapeHtml(item.question)}</p>
        <div style="font-size:0.84rem;display:flex;gap:16px;">
          <span>Your Answer: <strong>${userAnsText}</strong></span>
          <span style="color:#059669;">Correct Answer: <strong>${correctAnsText}</strong></span>
        </div>
        <div class="review-explanation">
          <strong>Pedagogical Explanation:</strong> ${escapeHtml(item.explanation)}
        </div>
      `;

      dom.quizReviewList.appendChild(reviewBox);
    });
  }

  // ==========================================================================
  // Module 4: Summarize Notes
  // ==========================================================================
  async function handleSummarySubmit(e) {
    e.preventDefault();
    const content = dom.summaryContentInput.value.trim();
    const lengthRadio = document.querySelector('input[name="summaryLength"]:checked');
    const length = lengthRadio ? lengthRadio.value : "medium";

    if (content.length < 20) {
      showToast("Input is too short. Please provide at least a few sentences to summarize.", "error");
      dom.summaryContentInput.focus();
      return;
    }

    dom.summaryEmptyState.classList.add("hidden");
    dom.summaryResultCard.classList.add("hidden");
    dom.summaryLoadingState.classList.remove("hidden");

    try {
      const data = await apiCall(
        "/api/summarize",
        "POST",
        { content, length },
        dom.summarySubmitBtn
      );

      renderSummaryResult(data);
      showToast("Summary synthesized successfully!", "success");
      loadProgressMetrics();
    } catch (err) {
      dom.summaryLoadingState.classList.add("hidden");
      dom.summaryEmptyState.classList.remove("hidden");
    }
  }

  function renderSummaryResult(data) {
    dom.summaryLoadingState.classList.add("hidden");
    dom.summaryEmptyState.classList.add("hidden");
    dom.summaryResultCard.classList.remove("hidden");

    dom.summaryLengthBadge.textContent = `${data.summary_length_type.toUpperCase()} SUMMARY`;
    dom.summaryOriginalLengthBadge.textContent = `${data.original_length_chars} characters original`;

    dom.summaryMainText.textContent = "";
    dom.summaryKeyPointsList.innerHTML = "";
    dom.summaryTermsGrid.innerHTML = "";
    dom.summaryQuickRevisionList.innerHTML = "";

    // Live Typewriter for Summary
    typewriterLive(dom.summaryMainText, data.summary, 12, () => {
      // Key points staggered
      if (Array.isArray(data.key_points)) {
        data.key_points.forEach((kp, idx) => {
          const li = document.createElement("li");
          li.className = "fade-in-stagger";
          li.style.animationDelay = `${idx * 0.1}s`;
          li.textContent = kp;
          dom.summaryKeyPointsList.appendChild(li);
        });
      }

      // Terms staggered
      if (Array.isArray(data.important_terms)) {
        data.important_terms.forEach((item, idx) => {
          const card = document.createElement("div");
          card.className = "term-card fade-in-stagger";
          card.style.animationDelay = `${idx * 0.12}s`;
          card.innerHTML = `
            <div class="term-title">${escapeHtml(item.term)}</div>
            <div class="term-def">${escapeHtml(item.definition)}</div>
          `;
          dom.summaryTermsGrid.appendChild(card);
        });
      }

      // Quick revision
      if (Array.isArray(data.quick_revision)) {
        data.quick_revision.forEach((rev, idx) => {
          const li = document.createElement("li");
          li.className = "fade-in-stagger";
          li.style.animationDelay = `${idx * 0.1}s`;
          li.textContent = rev;
          dom.summaryQuickRevisionList.appendChild(li);
        });
      }

      showToast("Summary synthesized live!", "success", 1800);
    });
  }

  function downloadSummaryAsTxt() {
    const summaryText = dom.summaryMainText.textContent;
    if (!summaryText) return;

    let fullTxt = `EduGenie Content Summary\n========================\n\n`;
    fullTxt += `SUMMARY:\n${summaryText}\n\n`;
    fullTxt += `KEY POINTS:\n`;
    dom.summaryKeyPointsList.querySelectorAll("li").forEach((li) => {
      fullTxt += `• ${li.textContent}\n`;
    });
    fullTxt += `\nQUICK REVISION:\n`;
    dom.summaryQuickRevisionList.querySelectorAll("li").forEach((li) => {
      fullTxt += `[✓] ${li.textContent}\n`;
    });

    const blob = new Blob([fullTxt], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `EduGenie-Summary-${Date.now()}.txt`;
    link.click();
    URL.revokeObjectURL(url);
    showToast("Downloaded summary as TXT!", "success");
  }

  // ==========================================================================
  // Module 5: Personalized Learning Path
  // ==========================================================================
  async function handleLearningSubmit(e) {
    e.preventDefault();
    const topic = dom.learningTopicInput.value.trim();
    const current_level = dom.learningLevelSelect.value;
    const available_time = dom.learningTimeInput.value.trim() || "1 hour/day";
    const goal = dom.learningGoalInput.value.trim() || "Master the concepts";

    if (!topic) {
      showToast("Please provide a topic for your learning path.", "error");
      dom.learningTopicInput.focus();
      return;
    }

    dom.learningEmptyState.classList.add("hidden");
    dom.learningResultCard.classList.add("hidden");
    dom.learningLoadingState.classList.remove("hidden");

    try {
      const data = await apiCall(
        "/api/learn/recommendations",
        "POST",
        { topic, current_level, available_time, goal },
        dom.learningSubmitBtn
      );

      renderLearningPathResult(data);
      loadProgressMetrics();
    } catch (err) {
      dom.learningLoadingState.classList.add("hidden");
      dom.learningEmptyState.classList.remove("hidden");
    }
  }

  function renderLearningPathResult(data) {
    dom.learningLoadingState.classList.add("hidden");
    dom.learningEmptyState.classList.add("hidden");
    dom.learningResultCard.classList.remove("hidden");

    dom.learningTopicBadge.textContent = data.topic;
    dom.learningLevelBadge.textContent = data.current_level.toUpperCase();
    dom.learningTimeBadge.textContent = data.available_time;

    dom.learningOverviewText.textContent = "";
    dom.roadmapTimelineContainer.innerHTML = "";

    // Live Typewriter for Overview
    typewriterLive(dom.learningOverviewText, data.overview, 12, () => {
      if (Array.isArray(data.stages)) {
        data.stages.forEach((stage, idx) => {
          const node = document.createElement("div");
          node.className = "roadmap-stage-node fade-in-stagger";
          node.style.animationDelay = `${idx * 0.15}s`;

          const topicsBadges = (stage.topics || [])
            .map((t) => `<span class="stage-topic-tag">${escapeHtml(t)}</span>`)
            .join("");

          const practiceList = (stage.practice_suggestions || [])
            .map((p) => `<li>${escapeHtml(p)}</li>`)
            .join("");

          const resourceList = (stage.recommended_resources || [])
            .map((r) => `<li>${escapeHtml(r)}</li>`)
            .join("");

          node.innerHTML = `
            <div class="stage-marker-dot">${stage.level_number || idx + 1}</div>
            <div class="stage-header">
              <h4 class="stage-title">${escapeHtml(stage.level_title)}</h4>
              <span class="stage-time">⏱ ${escapeHtml(stage.estimated_time)}</span>
            </div>
            <div class="stage-topics-tags">
              ${topicsBadges}
            </div>
            <div class="stage-section">
              <div class="stage-section-label">Sequence Strategy</div>
              <p class="stage-section-content">${escapeHtml(stage.sequence_guide)}</p>
            </div>
            ${
              practiceList
                ? `<div class="stage-section">
                     <div class="stage-section-label">Hands-On Practice</div>
                     <ul class="styled-bullet-list" style="margin-top:2px;">${practiceList}</ul>
                   </div>`
                : ""
            }
            ${
              resourceList
                ? `<div class="stage-section">
                     <div class="stage-section-label">Recommended Resources</div>
                     <ul class="styled-bullet-list" style="margin-top:2px;">${resourceList}</ul>
                   </div>`
                : ""
            }
          `;

          dom.roadmapTimelineContainer.appendChild(node);
        });
      }
      showToast("Curriculum roadmap generated live!", "success", 1800);
    });
  }

  // ==========================================================================
  // Module 6: History & Activity Storage
  // ==========================================================================
  async function loadHistory() {
    try {
      let url = `/api/history?activity_type=${state.historyFilter}`;
      if (state.historySearch) {
        url += `&search=${encodeURIComponent(state.historySearch)}`;
      }

      const activities = await apiCall(url, "GET");
      state.historyItems = activities;
      renderHistoryList(activities);
    } catch (e) {
      // Ignored
    }
  }

  function renderHistoryList(items) {
    dom.historyListContainer.innerHTML = "";

    if (!items || items.length === 0) {
      dom.historyListContainer.innerHTML = `
        <div class="empty-state-mini" style="padding:48px 0;">
          <div style="font-size:2.2rem;margin-bottom:8px;">📭</div>
          <p class="empty-text">No history records found.</p>
          <span class="empty-subtext">Activities you perform in Q&A, Quizzes, and Roadmaps appear here.</span>
        </div>
      `;
      return;
    }

    const typeIcons = {
      qa: "💬",
      explain: "💡",
      quiz: "📝",
      summary: "📄",
      learning_path: "🗺️",
    };

    items.forEach((item) => {
      const row = document.createElement("div");
      row.className = "history-item-row";

      const icon = typeIcons[item.activity_type] || "📌";
      const dateStr = item.created_at
        ? new Date(item.created_at).toLocaleString(undefined, {
            month: "short",
            day: "numeric",
            hour: "2-digit",
            minute: "2-digit",
          })
        : "Recent";

      row.innerHTML = `
        <div class="history-item-main">
          <div class="history-item-icon">${icon}</div>
          <div class="history-item-texts">
            <span class="history-item-title">${escapeHtml(item.title)}</span>
            <span class="history-item-meta">${escapeHtml(item.subtitle || "")} • ${dateStr}</span>
          </div>
        </div>
        <div class="history-item-actions">
          <button class="btn btn-sm btn-outline view-history-btn" data-id="${item.id}">View Details</button>
          <button class="icon-btn-sm delete-history-btn" data-id="${item.id}" title="Delete record">✕</button>
        </div>
      `;

      // View details click
      row.querySelector(".view-history-btn").addEventListener("click", () => {
        openHistoryDetail(item);
      });

      // Delete click
      row.querySelector(".delete-history-btn").addEventListener("click", async (e) => {
        e.stopPropagation();
        if (confirm("Delete this activity record?")) {
          await apiCall(`/api/history/${item.id}`, "DELETE");
          showToast("Activity deleted", "info", 1800);
          loadHistory();
          loadProgressMetrics();
        }
      });

      dom.historyListContainer.appendChild(row);
    });
  }

  function openHistoryDetail(item) {
    dom.historyDetailTitle.textContent = item.title;
    dom.historyDetailBadge.textContent = item.activity_type.toUpperCase();

    const p = item.payload || {};
    let contentHtml = "";

    if (item.activity_type === "qa") {
      contentHtml = `
        <div class="qa-section-block">
          <h4 class="qa-section-label">Answer</h4>
          <p class="qa-section-content">${escapeHtml(p.answer || "")}</p>
        </div>
        <div class="qa-section-block" style="margin-top:12px;">
          <h4 class="qa-section-label">Simple Explanation</h4>
          <p class="qa-section-content text-callout">${escapeHtml(p.simple_explanation || "")}</p>
        </div>
        ${
          p.key_points
            ? `<div class="qa-section-block" style="margin-top:12px;">
                 <h4 class="qa-section-label">Key Points</h4>
                 <ul class="styled-bullet-list">${p.key_points.map((pt) => `<li>${escapeHtml(pt)}</li>`).join("")}</ul>
               </div>`
            : ""
        }
      `;
    } else if (item.activity_type === "quiz") {
      contentHtml = `
        <div style="font-size:1.1rem;font-weight:700;margin-bottom:12px;">Topic: ${escapeHtml(p.topic || "")} — Score: ${p.correct_count}/${p.total_questions} (${p.score_pct}%)</div>
        <div class="quiz-review-list">
          ${(p.results || [])
            .map(
              (r, i) => `
            <div class="quiz-review-item">
              <div class="review-question-header">
                <strong>Q${i + 1}: ${escapeHtml(r.question)}</strong>
                <span class="pill ${r.is_correct ? "pill-correct" : "pill-incorrect"}">${r.is_correct ? "Correct ✓" : "Incorrect ✕"}</span>
              </div>
              <div style="font-size:0.84rem;margin:6px 0;">Correct Answer: <strong>Option ${r.correct_answer}</strong> (You chose: Option ${r.user_answer || "None"})</div>
              <div class="review-explanation">${escapeHtml(r.explanation || "")}</div>
            </div>
          `
            )
            .join("")}
        </div>
      `;
    } else if (item.activity_type === "explain") {
      contentHtml = `
        <div class="concept-breakdown-flow">
          <p class="flow-step-desc">${escapeHtml(p.simple_explanation || "")}</p>
          <div class="code-or-example-box" style="margin-top:10px;"><strong>Example:</strong> ${escapeHtml(p.example || "")}</div>
          <div style="margin-top:10px;">
            <strong>Key Points:</strong>
            <ul class="styled-bullet-list">${(p.key_points || []).map((k) => `<li>${escapeHtml(k)}</li>`).join("")}</ul>
          </div>
        </div>
      `;
    } else if (item.activity_type === "summary") {
      contentHtml = `
        <div class="summary-section-block">
          <h4 class="summary-section-title">Summary</h4>
          <p class="summary-paragraph">${escapeHtml(p.summary || "")}</p>
          <div style="margin-top:12px;">
            <strong>Key Points:</strong>
            <ul class="styled-bullet-list">${(p.key_points || []).map((k) => `<li>${escapeHtml(k)}</li>`).join("")}</ul>
          </div>
        </div>
      `;
    } else {
      contentHtml = `<pre class="code-or-example-box" style="white-space:pre-wrap;">${escapeHtml(JSON.stringify(p, null, 2))}</pre>`;
    }

    dom.historyDetailBody.innerHTML = contentHtml;
    dom.historyDetailModal.classList.remove("hidden");
  }

  // ==========================================================================
  // Module 7: Real Progress & Analytics
  // ==========================================================================
  async function loadProgressMetrics() {
    try {
      const data = await apiCall("/api/progress", "GET");

      // Update Top KPIs
      if (dom.metricQuestionsCount) dom.metricQuestionsCount.textContent = data.questions_asked;
      if (dom.metricConceptsCount) dom.metricConceptsCount.textContent = data.concepts_explained;
      if (dom.metricQuizzesCount) dom.metricQuizzesCount.textContent = data.quizzes_completed;
      if (dom.metricAccuracyPct) dom.metricAccuracyPct.textContent = `${data.average_quiz_accuracy}%`;
      if (dom.metricRoadmapsCount) dom.metricRoadmapsCount.textContent = data.learning_paths_created;

      // Update Dashboard Counters
      if (dom.dashQuestionsCount) dom.dashQuestionsCount.textContent = data.questions_asked;
      if (dom.dashConceptsCount) dom.dashConceptsCount.textContent = data.concepts_explained;
      if (dom.dashQuizzesCount) dom.dashQuizzesCount.textContent = data.quizzes_completed;
      if (dom.dashAccuracyRate) dom.dashAccuracyRate.textContent = `${data.average_quiz_accuracy}%`;

      // Render Weekly CSS Bar Chart
      renderWeeklyBarChart(data.weekly_activity || []);

      // Render Dashboard Recent Activity
      renderDashboardRecentActivity(data.recent_activities || []);
    } catch (e) {
      // Ignored
    }
  }

  function renderWeeklyBarChart(days) {
    if (!dom.weeklyActivityBarChart) return;
    dom.weeklyActivityBarChart.innerHTML = "";

    const maxCount = Math.max(...days.map((d) => d.count), 5);

    days.forEach((dayItem) => {
      const col = document.createElement("div");
      col.className = "chart-bar-col";

      const heightPct = Math.round((dayItem.count / maxCount) * 100);

      col.innerHTML = `
        <span class="chart-bar-count">${dayItem.count}</span>
        <div class="chart-bar-visual" style="height:${Math.max(heightPct, 6)}%;" title="${dayItem.date}: ${dayItem.count} sessions"></div>
        <span class="chart-bar-label">${dayItem.day}</span>
      `;

      dom.weeklyActivityBarChart.appendChild(col);
    });
  }

  function renderDashboardRecentActivity(recent) {
    if (!dom.dashRecentActivityContainer) return;

    if (!recent || recent.length === 0) {
      dom.dashRecentActivityContainer.innerHTML = `
        <div class="empty-state-mini">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
          <p class="empty-text">No learning activity yet.</p>
          <span class="empty-subtext">Start your first learning session above.</span>
        </div>
      `;
      return;
    }

    const typeIcons = {
      qa: "💬",
      explain: "💡",
      quiz: "📝",
      summary: "📄",
      learning_path: "🗺️",
    };

    let html = `<div style="display:flex;flex-direction:column;gap:10px;">`;
    recent.forEach((item) => {
      const icon = typeIcons[item.activity_type] || "📌";
      const timeStr = item.created_at
        ? new Date(item.created_at).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
        : "";

      html += `
        <div class="history-item-row" style="padding:10px 14px;">
          <div class="history-item-main" style="gap:10px;">
            <div style="font-size:1.1rem;">${icon}</div>
            <div class="history-item-texts">
              <span class="history-item-title" style="font-size:0.88rem;">${escapeHtml(item.title)}</span>
              <span class="history-item-meta" style="font-size:0.74rem;">${escapeHtml(item.subtitle || "")} • ${timeStr}</span>
            </div>
          </div>
        </div>
      `;
    });
    html += `</div>`;

    dom.dashRecentActivityContainer.innerHTML = html;
  }

  // ==========================================================================
  // Settings Form Management
  // ==========================================================================
  async function handleSettingsSubmit(e) {
    if (e && e.preventDefault) e.preventDefault();
    const apiKey = dom.settingsApiKeyInput ? dom.settingsApiKeyInput.value.trim() : "";
    const model = dom.settingsModelSelect ? dom.settingsModelSelect.value : "gemini-3.6-flash";
    const themeRadio = document.querySelector('input[name="appTheme"]:checked');
    const selectedTheme = themeRadio ? themeRadio.value : (state.theme || "system");

    applyTheme(selectedTheme);

    const updatePayload = {
      gemini_model: model,
    };
    if (apiKey) {
      updatePayload.gemini_api_key = apiKey;
    }

    const saveBtn = dom.saveSettingsBtn || document.getElementById("saveSettingsBtn");
    try {
      const res = await apiCall("/api/settings", "POST", updatePayload, saveBtn);
      state.isGeminiConfigured = res.is_gemini_configured;
      state.activeModel = res.current_model;
      if (dom.settingsApiKeyInput) dom.settingsApiKeyInput.value = "";
      if (dom.settingsModal) dom.settingsModal.classList.add("hidden");
      showToast("Configuration saved successfully! AI client reloaded.", "success");
      await checkSystemHealth();
    } catch (err) {
      console.error("Settings save error:", err);
    }
  }

  // ==========================================================================
  // Event Listeners Wiring
  // ==========================================================================

  // Navigation Items
  dom.navItems.forEach((btn) => {
    btn.addEventListener("click", () => navigateTo(btn.dataset.view));
  });

  // Action Cards on Dashboard & Elsewhere
  document.querySelectorAll("[data-navigate]").forEach((elem) => {
    elem.addEventListener("click", () => navigateTo(elem.dataset.navigate));
  });

  // Mobile Drawer
  dom.mobileNavToggle.addEventListener("click", openMobileSidebar);
  dom.sidebarCloseBtn.addEventListener("click", closeMobileSidebar);
  dom.sidebarOverlay.addEventListener("click", closeMobileSidebar);

  // Theme Toggles
  dom.themeToggleBtn.addEventListener("click", toggleThemeQuickly);
  dom.mobileThemeToggle.addEventListener("click", toggleThemeQuickly);

  // Status Pill -> Opens Settings
  dom.aiStatusPill.addEventListener("click", () => {
    dom.settingsModal.classList.remove("hidden");
    checkSystemHealth();
  });

  // Settings Modal Controls
  dom.openSettingsBtn.addEventListener("click", () => {
    dom.settingsModal.classList.remove("hidden");
    checkSystemHealth();
  });
  dom.closeSettingsModalBtn.addEventListener("click", () => dom.settingsModal.classList.add("hidden"));
  dom.cancelSettingsBtn.addEventListener("click", () => dom.settingsModal.classList.add("hidden"));
  dom.settingsForm.addEventListener("submit", handleSettingsSubmit);

  dom.toggleApiKeyVisibilityBtn.addEventListener("click", () => {
    const isPassword = dom.settingsApiKeyInput.type === "password";
    dom.settingsApiKeyInput.type = isPassword ? "text" : "password";
    dom.toggleApiKeyVisibilityBtn.textContent = isPassword ? "Hide" : "Show";
  });

  // History Item Detail Modal
  dom.closeHistoryDetailModalBtn.addEventListener("click", () => dom.historyDetailModal.classList.add("hidden"));
  dom.closeHistoryDetailBtn.addEventListener("click", () => dom.historyDetailModal.classList.add("hidden"));

  // Q&A Events
  dom.qaForm.addEventListener("submit", handleQaSubmit);
  dom.qaClearBtn.addEventListener("click", () => {
    dom.qaQuestionInput.value = "";
    dom.qaContextInput.value = "";
    dom.qaResultCard.classList.add("hidden");
    dom.qaEmptyState.classList.remove("hidden");
    dom.qaQuestionInput.focus();
  });
  dom.qaCopyBtn.addEventListener("click", () => {
    if (state.lastQaResponse) {
      const textToCopy = `Question: ${state.lastQaResponse.question}\n\nAnswer: ${state.lastQaResponse.answer}\n\nSimple Explanation: ${state.lastQaResponse.simple_explanation}\n\nKey Points:\n${(state.lastQaResponse.key_points || []).map((p) => `• ${p}`).join("\n")}`;
      navigator.clipboard.writeText(textToCopy);
      showToast("Copied answer to clipboard!", "success");
    }
  });
  dom.qaRegenerateBtn.addEventListener("click", () => {
    if (state.lastQaRequest) {
      dom.qaQuestionInput.value = state.lastQaRequest.question;
      dom.qaContextInput.value = state.lastQaRequest.context || "";
      dom.qaForm.requestSubmit();
    }
  });
  dom.qaFollowUpBtn.addEventListener("click", handleQaFollowUp);
  dom.qaFollowUpInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") handleQaFollowUp();
  });

  // Suggestion Chips (Generic auto-fill)
  document.querySelectorAll(".chip-btn").forEach((chip) => {
    chip.addEventListener("click", () => {
      const fillText = chip.dataset.fill;
      const topicText = chip.dataset.topic;
      const goalText = chip.dataset.goal;

      if (fillText) {
        if (state.currentView === "qa") {
          dom.qaQuestionInput.value = fillText;
          dom.qaForm.requestSubmit();
        } else if (state.currentView === "explain") {
          dom.explainConceptInput.value = fillText;
          dom.explainForm.requestSubmit();
        } else if (state.currentView === "quiz") {
          dom.quizTopicInput.value = fillText;
        }
      }

      if (topicText && dom.learningTopicInput) {
        dom.learningTopicInput.value = topicText;
        if (goalText) dom.learningGoalInput.value = goalText;
        dom.learningForm.requestSubmit();
      }
    });
  });

  // Explain Events
  dom.explainForm.addEventListener("submit", handleExplainSubmit);
  dom.explainClearBtn.addEventListener("click", () => {
    dom.explainConceptInput.value = "";
    dom.explainResultCard.classList.add("hidden");
    dom.explainEmptyState.classList.remove("hidden");
    dom.explainConceptInput.focus();
  });
  dom.explainCopyBtn.addEventListener("click", () => {
    const textToCopy = `Concept: ${dom.explainConceptBadge.textContent}\n\nOverview:\n${dom.explainSimpleText.textContent}\n\nHow It Works:\n${dom.explainHowText.textContent}\n\nExample:\n${dom.explainExampleBox.textContent}`;
    navigator.clipboard.writeText(textToCopy);
    showToast("Copied concept breakdown!", "success");
  });
  dom.explainRegenerateBtn.addEventListener("click", () => {
    if (state.lastExplainRequest) {
      dom.explainForm.requestSubmit();
    }
  });

  // Quiz Events
  dom.quizGenForm.addEventListener("submit", handleQuizGenerate);
  dom.quizPrevBtn.addEventListener("click", () => {
    if (state.quizCurrentIndex > 0) {
      state.quizCurrentIndex -= 1;
      renderActiveQuizQuestion();
    }
  });
  dom.quizNextBtn.addEventListener("click", () => {
    const total = state.activeQuiz?.questions?.length || 0;
    if (state.quizCurrentIndex < total - 1) {
      state.quizCurrentIndex += 1;
      renderActiveQuizQuestion();
    }
  });
  dom.quizSubmitBtn.addEventListener("click", handleQuizSubmit);
  dom.quizRetryBtn.addEventListener("click", () => {
    if (state.activeQuiz) {
      state.quizCurrentIndex = 0;
      state.userQuizAnswers = {};
      dom.quizResultsCard.classList.add("hidden");
      dom.quizSessionCard.classList.remove("hidden");
      renderActiveQuizQuestion();
    }
  });
  dom.quizNewBtn.addEventListener("click", () => {
    state.activeQuiz = null;
    dom.quizResultsCard.classList.add("hidden");
    dom.quizSessionCard.classList.add("hidden");
    dom.quizEmptyState.classList.remove("hidden");
    dom.quizTopicInput.focus();
  });

  // Summarize Events
  dom.summaryForm.addEventListener("submit", handleSummarySubmit);
  dom.summaryContentInput.addEventListener("input", () => {
    dom.summaryCharCounter.textContent = `${dom.summaryContentInput.value.length} chars`;
  });
  dom.summaryClearBtn.addEventListener("click", () => {
    dom.summaryContentInput.value = "";
    dom.summaryCharCounter.textContent = "0 chars";
    dom.summaryResultCard.classList.add("hidden");
    dom.summaryEmptyState.classList.remove("hidden");
    dom.summaryContentInput.focus();
  });
  dom.summaryCopyBtn.addEventListener("click", () => {
    navigator.clipboard.writeText(dom.summaryMainText.textContent);
    showToast("Summary copied to clipboard!", "success");
  });
  dom.summaryDownloadBtn.addEventListener("click", downloadSummaryAsTxt);
  dom.loadSampleNotesBtn.addEventListener("click", () => {
    dom.summaryContentInput.value = `Operating Systems Notes: Process Scheduling & Memory Management

An operating system acts as an intermediary between user applications and the physical computer hardware. One of its vital roles is Process Scheduling, determining which process on the Ready Queue gets CPU execution time. 

Key CPU scheduling algorithms include:
1. First-Come, First-Served (FCFS): Simple but susceptible to the Convoy Effect.
2. Shortest Job Next (SJN/SJF): Mathematically optimal for minimizing average waiting time, though predicting future burst times is challenging.
3. Round Robin (RR): Preemptive scheduling assigning each process a fixed time slice (quantum), ensuring fair responsiveness in time-sharing environments.

Another cornerstone of modern OS architecture is Virtual Memory Management. Through Paging and Segmentation, the OS maps virtual addresses used by programs into physical memory frames. When a requested page is not in physical RAM, a Page Fault occurs, triggering the OS to retrieve it from disk swap space using replacement policies such as Least Recently Used (LRU). This abstraction ensures robust process isolation, memory protection, and prevents memory leaks from crashing the entire system.`;
    dom.summaryCharCounter.textContent = `${dom.summaryContentInput.value.length} chars`;
    showToast("Loaded sample operating systems notes!", "info", 1800);
  });

  // Learning Path Events
  dom.learningForm.addEventListener("submit", handleLearningSubmit);
  dom.learningCopyBtn.addEventListener("click", () => {
    let copyText = `EduGenie Learning Path: ${dom.learningTopicBadge.textContent}\n========================\n\n`;
    copyText += `Overview: ${dom.learningOverviewText.textContent}\n\n`;
    dom.roadmapTimelineContainer.querySelectorAll(".roadmap-stage-node").forEach((node) => {
      const title = node.querySelector(".stage-title")?.textContent || "";
      const time = node.querySelector(".stage-time")?.textContent || "";
      copyText += `[${title} - ${time}]\n`;
      node.querySelectorAll(".stage-topic-tag").forEach((tag) => {
        copyText += `  - ${tag.textContent}\n`;
      });
      copyText += "\n";
    });
    navigator.clipboard.writeText(copyText);
    showToast("Roadmap outline copied!", "success");
  });

  // History Controls
  dom.historyFilterPills.forEach((pill) => {
    pill.addEventListener("click", () => {
      dom.historyFilterPills.forEach((p) => p.classList.remove("active"));
      pill.classList.add("active");
      state.historyFilter = pill.dataset.filter;
      loadHistory();
    });
  });

  dom.historySearchInput.addEventListener("input", (e) => {
    state.historySearch = e.target.value.trim();
    loadHistory();
  });

  dom.clearAllHistoryBtn.addEventListener("click", async () => {
    if (confirm("Are you sure you want to delete all activity history? This cannot be undone.")) {
      await apiCall("/api/history", "DELETE");
      showToast("All activity history cleared!", "info");
      loadHistory();
      loadProgressMetrics();
    }
  });

  // ==========================================================================
  // Initialization Sequence
  // ==========================================================================
  checkSystemHealth();
  loadProgressMetrics();
  console.log("EduGenie client initialized successfully.");
});
