/* Progress Autopilot - CSS Custom Properties Reference */

:root {
  /* ===== COLOR PALETTE ===== */
  
  /* Backgrounds */
  --bg-primary: #f8f9fa;        /* Light grey - main background */
  --bg-secondary: #ffffff;      /* White - cards, inputs */
  
  /* Text */
  --text-primary: #1a1a1a;      /* Dark grey - main text, headings */
  --text-secondary: #6b7280;    /* Medium grey - secondary content */
  --text-muted: #9ca3af;        /* Light grey - disabled, hints */
  
  /* UI */
  --border-color: #e5e7eb;      /* Very light grey - borders, dividers */
  
  /* Semantic Colors */
  --accent-primary: #6366f1;    /* Indigo - main CTA, highlights */
  --accent-secondary: #8b5cf6;  /* Purple - hover states, gradients */
  --success: #10b981;           /* Emerald - completed, positive */
  --warning: #f59e0b;           /* Amber - attention needed */
  --danger: #ef4444;            /* Red - errors, failed */
  --info: #3b82f6;              /* Blue - information */
  
  /* ===== SHADOWS ===== */
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  
  /* ===== TRANSITIONS ===== */
  --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  --transition-short: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  --transition-long: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  
  /* ===== TYPOGRAPHY ===== */
  --font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", "Helvetica Neue", Arial, sans-serif;
  --font-size-xs: 0.75rem;      /* 12px */
  --font-size-sm: 0.875rem;     /* 14px */
  --font-size-base: 1rem;       /* 16px */
  --font-size-lg: 1.125rem;     /* 18px */
  --font-size-xl: 1.5rem;       /* 24px */
  --font-size-2xl: 1.875rem;    /* 30px */
  --font-size-3xl: 2.25rem;     /* 36px */
  
  --font-weight-regular: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;
  
  --line-height-tight: 1.2;
  --line-height-normal: 1.5;
  --line-height-relaxed: 1.6;
  
  /* ===== SPACING ===== */
  --spacing-xs: 0.25rem;        /* 2px */
  --spacing-sm: 0.5rem;         /* 4px */
  --spacing-md: 1rem;           /* 8px */
  --spacing-lg: 1.5rem;         /* 12px */
  --spacing-xl: 2rem;           /* 16px */
  --spacing-2xl: 3rem;          /* 24px */
  
  /* ===== BORDER RADIUS ===== */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-full: 999px;
  
  /* ===== COMPONENT SIZES ===== */
  --button-height: 44px;        /* Touch-friendly minimum */
  --button-padding-x: 1.5rem;
  --button-padding-y: 0.75rem;
  
  --input-height: 44px;
  --input-padding-x: 1rem;
  --input-padding-y: 0.875rem;
  
  --card-padding: 2rem;
  --card-border-radius: 12px;
  
  /* ===== LAYOUT ===== */
  --max-width-container: 1200px;
  --max-width-narrow: 600px;
  --max-width-wide: 1400px;
  
  /* ===== BREAKPOINTS (mobile-first) ===== */
  /* sm: 640px, md: 768px, lg: 1024px, xl: 1280px */
  
  /* ===== Z-INDEX SCALE ===== */
  --z-dropdown: 100;
  --z-sticky: 200;
  --z-fixed: 300;
  --z-modal-backdrop: 400;
  --z-modal: 500;
  --z-popover: 600;
  --z-tooltip: 700;
  --z-notification: 800;
}

/* ===== USAGE EXAMPLES ===== */

/*
 * COLORS
 * ------
 * color: var(--text-primary);           // Main text
 * color: var(--text-secondary);         // Secondary text
 * background: var(--bg-secondary);      // Card backgrounds
 * border-color: var(--accent-primary);  // Interactive elements
 */

/*
 * SHADOWS
 * -------
 * box-shadow: var(--shadow-md);  // Standard shadow
 * box-shadow: var(--shadow-lg);  // Hover shadow
 */

/*
 * TRANSITIONS
 * -----------
 * transition: var(--transition);       // Standard animation
 * transition: var(--transition-short); // Quick micro-interaction
 * transition: var(--transition-long);  // Page transition
 */

/*
 * TYPOGRAPHY
 * -----------
 * font-family: var(--font-family);
 * font-size: var(--font-size-lg);
 * font-weight: var(--font-weight-semibold);
 * line-height: var(--line-height-relaxed);
 */

/*
 * SPACING
 * -------
 * margin: var(--spacing-lg);
 * padding: var(--spacing-md);
 * gap: var(--spacing-xl);
 */

/*
 * COMPONENTS
 * ----------
 * min-height: var(--button-height);
 * padding: var(--button-padding-y) var(--button-padding-x);
 * border-radius: var(--card-border-radius);
 */

/* ===== GRADIENT RECIPES ===== */

/*
 * ACCENT GRADIENT (Primary to Secondary)
 * background: linear-gradient(
 *   135deg,
 *   var(--accent-primary) 0%,
 *   var(--accent-secondary) 100%
 * );
 */

/*
 * SUCCESS GRADIENT
 * background: linear-gradient(
 *   135deg,
 *   var(--success) 0%,
 *   #059669 100%
 * );
 */

/*
 * TEXT GRADIENT
 * background: linear-gradient(
 *   135deg,
 *   var(--accent-primary) 0%,
 *   var(--accent-secondary) 100%
 * );
 * -webkit-background-clip: text;
 * -webkit-text-fill-color: transparent;
 * background-clip: text;
 */

/* ===== ANIMATION TIMING ===== */

/*
 * EASING FUNCTION (Material Design)
 * cubic-bezier(0.4, 0, 0.2, 1)
 * - Fast start, smooth deceleration
 * - Perfect for UI transitions
 */

/*
 * DURATION RECOMMENDATIONS
 * - Micro interactions: 0.2s (hover, focus)
 * - Standard transitions: 0.3s (state changes)
 * - Page transitions: 0.5s (full page moves)
 * - Long animations: 0.8-1s (loading, heavy moves)
 */

/* ===== RESPONSIVE BREAKPOINTS ===== */

/*
 * MOBILE FIRST APPROACH
 * 
 * @media (min-width: 640px) { }  // sm
 * @media (min-width: 768px) { }  // md
 * @media (min-width: 1024px) { } // lg
 * @media (min-width: 1280px) { } // xl
 */

/* ===== STATE MODIFIERS ===== */

/*
 * HOVER STATE
 * box-shadow: var(--shadow-lg);
 * transform: translateY(-2px);
 */

/*
 * FOCUS STATE
 * outline: 2px solid var(--accent-primary);
 * outline-offset: 2px;
 */

/*
 * ACTIVE STATE
 * opacity: 0.9;
 * transform: scale(0.98);
 */

/*
 * DISABLED STATE
 * opacity: 0.5;
 * cursor: not-allowed;
 * pointer-events: none;
 */

/* ===== DARK MODE ===== */

/*
@media (prefers-color-scheme: dark) {
  :root {
    --bg-primary: #0f0f0f;
    --bg-secondary: #1a1a1a;
    --text-primary: #f5f5f5;
    --text-secondary: #b0b0b0;
    --text-muted: #808080;
    --border-color: #2d2d2d;
  }
}
*/

/* ===== UTILITY CLASS EXAMPLES ===== */

/*
.mt-4 { margin-top: var(--spacing-xl); }
.mb-3 { margin-bottom: var(--spacing-lg); }
.px-4 { padding-left: var(--spacing-xl); padding-right: var(--spacing-xl); }
.gap-2 { gap: var(--spacing-md); }
.text-lg { font-size: var(--font-size-lg); }
.font-bold { font-weight: var(--font-weight-bold); }
.rounded-md { border-radius: var(--radius-md); }
*/

/* ===== PERFORMANCE TIPS ===== */

/*
1. Use CSS variables instead of repeating colors
2. Use custom properties for consistency
3. Leverage inheritance (set at :root)
4. Use media queries for breakpoints
5. Combine related variables
6. Document all custom properties
7. Test in different color schemes
8. Ensure sufficient contrast ratios
*/
