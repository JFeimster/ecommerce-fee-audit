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

const auditReadiness = {
  product: 'Ecommerce Fee Audit',
  repo: 'JFeimster/ecommerce-fee-audit.vercel.app',
  siteRoot: 'site',
  embedPage: '/embed.html',
  recommendedVercelRoot: 'site',
  offers: [
    'DIY Fee Audit Lab',
    'DWY Margin Recovery Desk',
    'DFY Ecommerce Finance Ops Desk'
  ],
  disclaimer: 'Not accounting, tax, legal, lending, underwriting, or funding approval advice.'
};

window.ecommerceFeeAudit = auditReadiness;
