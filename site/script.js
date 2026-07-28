const yearTargets = document.querySelectorAll('[data-current-year]');
yearTargets.forEach((target) => {
  target.textContent = new Date().getFullYear();
});

const ctaButtons = document.querySelectorAll('[data-cta]');
ctaButtons.forEach((button) => {
  button.addEventListener('click', () => {
    const action = button.getAttribute('data-cta');
    window.dispatchEvent(new CustomEvent('ecommerceFeeAuditCtaClicked', {
      detail: {
        action,
        source: 'ecommerce-fee-audit-site',
        timestamp: new Date().toISOString()
      }
    }));
  });
});

const recommendations = {
  payouts: {
    lane: 'Payout reconciliation',
    action: 'Start by matching platform settlements to payouts, then payouts to bank deposits. Do not diagnose margin until the cash trail is clean.',
    asset: 'Use the reconciliation rules, column mapping library, and platform-specific payout guides.'
  },
  fees: {
    lane: 'Fee leakage review',
    action: 'Normalize each deduction into the canonical fee taxonomy, compare the current month against baseline, and flag material variance for review.',
    asset: 'Use the monthly fee variance dashboard schema and normalized platform-fee taxonomy.'
  },
  sku: {
    lane: 'SKU contribution margin',
    action: 'Connect sales, COGS, fulfillment, ad spend, refunds, and platform costs before deciding which products deserve more capital.',
    asset: 'Use the SKU contribution margin scorecard.'
  },
  reserves: {
    lane: 'Reserve, hold, and dispute tracking',
    action: 'Separate temporary timing holds from true cost leakage, then document evidence before any dispute or escalation.',
    asset: 'Use the reserve and hold tracker plus dispute documentation playbook.'
  }
};

function buildSignalMessage(formData) {
  const platform = formData.get('platform');
  const pain = formData.get('pain');
  const urgency = formData.get('urgency');
  const rec = recommendations[pain] || recommendations.payouts;

  const platformLabel = {
    shopify: 'Shopify / DTC',
    amazon: 'Amazon Marketplace',
    stripe: 'Stripe / processor',
    multi: 'multi-platform'
  }[platform] || 'platform';

  const urgencyLabel = {
    monthly: 'monthly close cleanup',
    cash: 'cash-pressure triage',
    funding: 'funding-readiness prep'
  }[urgency] || 'next review';

  return `<strong>Recommended lane: ${rec.lane}.</strong> For ${platformLabel} and ${urgencyLabel}, ${rec.action} <span>${rec.asset}</span>`;
}

function initAuditRadar() {
  const forms = document.querySelectorAll('[data-audit-radar-form]');

  forms.forEach((form) => {
    const output = form.closest('.radar-panel, .embed-panel')?.querySelector('[data-audit-output]') || document.querySelector('[data-audit-output]');

    form.addEventListener('submit', (event) => {
      event.preventDefault();
      const formData = new FormData(form);
      const message = buildSignalMessage(formData);

      if (output) {
        output.innerHTML = message;
      }

      window.dispatchEvent(new CustomEvent('ecommerceFeeAuditSignalGenerated', {
        detail: {
          platform: formData.get('platform'),
          pain: formData.get('pain'),
          urgency: formData.get('urgency'),
          message,
          timestamp: new Date().toISOString()
        }
      }));
    });
  });
}

initAuditRadar();

window.ecommerceFeeAudit = {
  product: 'Ecommerce Fee Audit',
  gpt: 'AI Platform Fee Audit Copilot',
  repo: 'JFeimster/ecommerce-fee-audit.vercel.app',
  siteRoot: 'site',
  embedPage: '/embed.html',
  vercelConfig: '/vercel.json inside the site root',
  assetFolders: [
    'site/assets/icons',
    'site/assets/downloads'
  ],
  offers: [
    'DIY Fee Audit Lab',
    'DWY Margin Recovery Desk',
    'DFY Ecommerce Finance Ops Desk'
  ],
  disclaimer: 'Not accounting, tax, legal, lending, underwriting, or funding approval advice.'
};
