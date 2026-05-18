import { analytics } from "./firebase";
import { logEvent } from "firebase/analytics";

export type Variant = 'A' | 'B';

/**
 * Gets the current stored variant for an experiment, or randomly assigns a new one.
 */
export function getOrAssignVariant(experimentName: string): Variant {
  if (typeof window === "undefined") return 'A';
  
  const storageKey = `ab_test_${experimentName}`;
  const existing = localStorage.getItem(storageKey);
  
  if (existing === 'A' || existing === 'B') {
    return existing as Variant;
  }
  
  // Assign randomly 50/50
  const assigned: Variant = Math.random() < 0.5 ? 'A' : 'B';
  localStorage.setItem(storageKey, assigned);
  
  // Log experiment assignment to Firebase Analytics
  if (analytics) {
    try {
      logEvent(analytics, "view_experiment", {
        experiment_name: experimentName,
        variant_assigned: assigned
      });
      console.log(`[A/B Testing] Assigned Variant ${assigned} for ${experimentName}`);
    } catch (e) {
      console.error("Failed to log view_experiment event", e);
    }
  }
  
  return assigned;
}

/**
 * Tracks a user conversion (e.g. click) for the A/B test.
 */
export function logExperimentConversion(experimentName: string, variant: Variant, actionName: string) {
  if (typeof window === "undefined") return;
  
  if (analytics) {
    try {
      logEvent(analytics, "conversion_experiment", {
        experiment_name: experimentName,
        variant: variant,
        action_name: actionName
      });
      console.log(`[A/B Testing] Tracked Conversion for ${experimentName} (${variant}) on action: ${actionName}`);
    } catch (e) {
      console.error("Failed to log conversion_experiment event", e);
    }
  }
}
