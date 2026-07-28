(() => {
  "use strict";

  const navToggle = document.querySelector("[data-nav-toggle]");
  const nav = document.querySelector("[data-nav]");
  const header = document.querySelector("[data-header]");

  if (navToggle && nav) {
    const closeNav = () => {
      nav.classList.remove("is-open");
      navToggle.setAttribute("aria-expanded", "false");
    };

    navToggle.addEventListener("click", () => {
      const isOpen = nav.classList.toggle("is-open");
      navToggle.setAttribute("aria-expanded", String(isOpen));
    });

    nav.addEventListener("click", (event) => {
      if (event.target.closest("a")) closeNav();
    });

    document.addEventListener("click", (event) => {
      if (!header?.contains(event.target)) closeNav();
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") {
        closeNav();
        navToggle.focus();
      }
    });

    window.addEventListener("resize", () => {
      if (window.innerWidth >= 820) closeNav();
    });
  }

  const radarForm = document.querySelector("[data-radar-form]");
  const radarResult = document.querySelector("[data-radar-result]");

  const laneData = {
    payout: {
      code: "01 / CONTROL",
      title: "Payout reconciliation",
      description:
        "Start by matching settlements and payouts to bank deposits. If the money trail is not clean, every margin opinion is wearing clown shoes.",
      files:
        "Payout or settlement report, matching bank deposits, and the order or transaction export for the same period.",
      check:
        "Confirm date ranges, currencies, duplicate rows, combined deposits, and whether the platform nets reserves or financing deductions."
    },
    fees: {
      code: "02 / CLASSIFY",
      title: "Fee leakage review",
      description:
        "Separate permanent fees from temporary reserves, refunds, taxes, remittances, reimbursements, and timing differences before calling a deduction a leak.",
      files:
        "Detailed balance transactions or settlement lines, prior-period fee summaries, refunds, disputes, reimbursements, and relevant platform descriptions.",
      check:
        "Compare effective fee rates by category and period, preserve original descriptions, and route unresolved adjustments to human review."
    },
    margin: {
      code: "03 / ECONOMICS",
      title: "SKU contribution margin",
      description:
        "Trace what each SKU or channel keeps after product cost, platform fees, fulfillment, shipping, returns, advertising, and attributable software costs.",
      files:
        "Order-level SKU data, product cost or COGS, fulfillment and shipping costs, refunds, advertising, and platform fee exports.",
      check:
        "Validate cost periods, bundle allocation, shipping subsidies, return costs, ad attribution, and whether the same SKU behaves differently by channel."
    },
    reserve: {
      code: "04 / CASH CONTROL",
      title: "Reserve, hold, and dispute tracking",
      description:
        "Build the reserve roll-forward first: opening balance, new holds, releases, amounts applied, aging, documentation, and expected cash impact.",
      files:
        "Reserve or hold activity, payout reports, dispute and chargeback records, reimbursements, negative-balance activity, and matching bank deposits.",
      check:
        "Confirm whether each item is temporary, released, applied, disputed, reimbursed, or still unresolved before treating it as permanent cost."
    }
  };

  const platformNotes = {
    shopify: "For Shopify, include payout transaction details, orders, refunds, labels, app or financing deductions when relevant.",
    amazon: "For Amazon, include settlement reports, FBA or FBM fees, storage, returns, reimbursements, advertising, and reserve activity when relevant.",
    stripe: "For Stripe, include balance transactions, charges, refunds, disputes, currency fees, and instant-payout activity when relevant.",
    multi: "For multi-channel audits, keep platform IDs and currencies intact so settlements are not blended before reconciliation."
  };

  const urgencyNotes = {
    close: "Use the current close period plus a prior comparison period when available.",
    cash: "Prioritize cash-affecting exceptions, expected release timing, and unresolved deposits without assuming funding is the fix.",
    decision: "Do not change pricing, ads, inventory, or channel mix until data quality and contribution assumptions are reviewed.",
    funding: "Complete the audit before preparing a readiness summary; eligibility and terms still depend on human review and provider criteria."
  };

  if (radarForm && radarResult) {
    radarForm.addEventListener("submit", (event) => {
      event.preventDefault();

      if (!radarForm.reportValidity()) return;

      const formData = new FormData(radarForm);
      const platform = String(formData.get("platform") || "");
      const pain = String(formData.get("pain") || "");
      const urgency = String(formData.get("urgency") || "");
      const lane = laneData[pain] || laneData.payout;

      const code = radarResult.querySelector("[data-result-code]");
      const title = radarResult.querySelector("[data-result-title]");
      const description = radarResult.querySelector("[data-result-description]");
      const files = radarResult.querySelector("[data-result-files]");
      const check = radarResult.querySelector("[data-result-check]");

      if (code) code.textContent = lane.code;
      if (title) title.textContent = lane.title;
      if (description) {
        description.textContent = `${lane.description} ${urgencyNotes[urgency] || ""}`.trim();
      }
      if (files) {
        files.textContent = `${lane.files} ${platformNotes[platform] || ""}`.trim();
      }
      if (check) check.textContent = lane.check;

      radarResult.dataset.lane = pain;
      radarResult.scrollIntoView({ behavior: "smooth", block: "center" });

      window.setTimeout(() => {
        title?.setAttribute("tabindex", "-1");
        title?.focus({ preventScroll: true });
      }, 450);
    });
  }

  document.querySelectorAll(".faq-item button").forEach((button) => {
    button.addEventListener("click", () => {
      const item = button.closest(".faq-item");
      const answer = item?.querySelector(".faq-answer");
      const wasExpanded = button.getAttribute("aria-expanded") === "true";

      button.setAttribute("aria-expanded", String(!wasExpanded));
      if (answer) answer.hidden = wasExpanded;
    });
  });

  const year = document.querySelector("[data-year]");
  if (year) year.textContent = String(new Date().getFullYear());
})();
