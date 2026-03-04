/*  sim-analytics.js  —  ACE Simulation Analytics Helper
 *  Wraps AceSupabase tracking + awardXP for simulation use.
 *
 *  Usage:
 *    const tracker = new SimTracker('ohms-law-sim', 'W3-Z2-N2');
 *    tracker.recordStep({ stepId: 'q1', correct: true, points: 10, loId: 'LO-3.2', category: 'DC Circuits' });
 *    ...
 *    tracker.complete();   // sends summary + awards XP
 *
 *  Include AFTER supabase-client.js so window.AceSupabase is available.
 * ───────────────────────────────────────────────────────────────── */

class SimTracker {
  /**
   * @param {string} simName  - Human-readable simulation identifier (used as lessonId)
   * @param {string} nodeId   - Journey node ID, e.g. 'W3-Z2-N2'
   */
  constructor(simName, nodeId) {
    this.simName  = simName;
    this.nodeId   = nodeId;
    this.steps    = [];           // Array of recorded step objects
    this.startTs  = Date.now();   // Session start timestamp
    this._completed = false;      // Guard against double-complete
  }

  /**
   * Record a single interaction / question / step.
   *
   * @param {Object}  step
   * @param {string}  step.stepId    - Unique step identifier within the sim
   * @param {boolean} step.correct   - Whether the learner got it right
   * @param {number}  [step.points]  - Points earned (default 0)
   * @param {string}  [step.loId]    - Learning objective reference
   * @param {string}  [step.category]- Topic / category label
   */
  recordStep({ stepId, correct, points = 0, loId = null, category = null }) {
    const step = {
      stepId,
      correct: Boolean(correct),
      points: points || 0,
      loId,
      category
    };
    this.steps.push(step);

    // Fire-and-forget per-question analytics if AceSupabase is available
    try {
      if (window.AceSupabase && typeof window.AceSupabase.trackQuestionEvent === 'function') {
        window.AceSupabase.trackQuestionEvent({
          lessonId:      this.simName,
          questionId:    stepId,
          format:        'simulation',
          loId:          loId || '',
          category:      category || '',
          selectedIndex: correct ? 0 : 1,   // 0 = correct choice
          correctIndex:  0,
          isCorrect:     correct,
          points:        step.points
        });
      }
    } catch (e) {
      console.warn('[SimTracker] trackQuestionEvent error:', e);
    }
  }

  /**
   * Calculate current score summary.
   * @returns {{ pct: number, correct: number, total: number, points: number }}
   */
  getScore() {
    const total   = this.steps.length;
    const correct = this.steps.filter(s => s.correct).length;
    const points  = this.steps.reduce((sum, s) => sum + s.points, 0);
    const pct     = total > 0 ? Math.round((correct / total) * 100) : 0;
    return { pct, correct, total, points };
  }

  /**
   * Determine XP award based on score percentage.
   * @returns {number}
   */
  calculateXP() {
    const { pct } = this.getScore();
    if (pct >= 100) return 100;
    if (pct >=  90) return  90;
    if (pct >=  80) return  75;
    if (pct >=  70) return  50;
    if (pct >=  60) return  30;
    return 10; // participation XP
  }

  /**
   * Send session summary via AceSupabase and award XP.
   * Safe to call once — subsequent calls are no-ops.
   */
  complete() {
    if (this._completed) return;
    this._completed = true;

    const { pct, correct, total } = this.getScore();
    const durationSec = Math.round((Date.now() - this.startTs) / 1000);

    // 1. Session summary
    try {
      if (window.AceSupabase && typeof window.AceSupabase.trackSessionSummary === 'function') {
        window.AceSupabase.trackSessionSummary({
          lessonId:         this.simName,
          format:           'simulation',
          questionsSeen:    total,
          questionsCorrect: correct,
          durationSec:      durationSec
        });
      }
    } catch (e) {
      console.warn('[SimTracker] trackSessionSummary error:', e);
    }

    // 2. XP award
    const xp = this.calculateXP();
    try {
      if (typeof awardXP === 'function') {
        awardXP(xp, this.simName + ' completed (' + pct + '%)');
      }
    } catch (e) {
      console.warn('[SimTracker] awardXP error:', e);
    }

    console.log(
      '[SimTracker] %s complete — %d/%d (%d%%) — %d XP — %ds',
      this.simName, correct, total, pct, xp, durationSec
    );
  }
}

// Expose globally so simulation HTML files can use it
window.SimTracker = SimTracker;
