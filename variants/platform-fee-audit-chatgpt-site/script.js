"use strict";

const lanes = {
  "Payouts do not match": {
    label: "START HERE",
    title: "Payout reconciliation",
    why: "Your first job is to tie settlement activity to bank deposits before treating any variance as a fee or a loss.",
    steps: ["Match payout IDs to deposits", "Flag partial deposits and timing gaps", "Separate known fees from unknown adjustments"]
  },
  "Fees keep creeping": {
    label: "FOLLOW THE MONEY",
    title: "Fee leakage review",
    why: "Recurring fee variance deserves a clean classification pass before it turns into assumed platform error or silent margin erosion.",
    steps: ["Normalize fee descriptions", "Compare rate / basis changes", "Queue unresolved exceptions for review"]
  },
  "SKUs may be upside down": {
    label: "SKU TRIAGE",
    title: "SKU contribution margin",
    why: "Gross sales can hide products that only look alive because they are burning cash more slowly than the dashboard refreshes.",
    steps: ["Map revenue and direct costs", "Include fulfillment, ad, return, and fee burdens", "Rank products by contribution—not vanity revenue"]
  },
  "Money is stuck": {
    label: "UNFREEZE CASH",
    title: "Reserve, hold, and dispute tracking",
    why: "A reserve or hold is not automatically a permanent loss. Track release dates, disputes, and unresolved exceptions separately.",
    steps: ["Create a reserve register", "Track holds, refunds, and disputes", "Separate timing pressure from true margin pressure"]
  }
};

document.getElementById("route-audit").addEventListener("click", function () {
  const platform = document.getElementById("platform").value;
  const pain = document.getElementById("pain").value;
  const urgency = document.getElementById("urgency").value;
  const lane = lanes[pain];
  const result = document.getElementById("radar-result");
  document.getElementById("result-label").textContent = lane.label;
  document.getElementById("result-title").textContent = lane.title;
  document.getElementById("result-copy").textContent = platform + " + " + urgency.toLowerCase() + ": " + lane.why;
  const steps = document.getElementById("result-steps");
  steps.innerHTML = "";
  lane.steps.forEach(function (step) {
    const item = document.createElement("li");
    item.textContent = "✓ " + step;
    steps.appendChild(item);
  });
  steps.hidden = false;
  document.getElementById("result-cta").hidden = false;
  result.classList.add("revealed");
});
