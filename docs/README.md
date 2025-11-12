# Medical Triage AI - Documentation

This folder contains comprehensive documentation for the Medical Triage AI prompt engineering system.

## 📚 Documentation Files

### 1. [PROMPT_STRATEGY.md](PROMPT_STRATEGY.md)
**Comprehensive Strategy Guide** - 30,000+ words

Complete documentation covering:
- Australian health standards compliance (ATS, RACGP)
- Detailed prompt architecture and design philosophy
- Comprehensive guardrail system with 8 global rules
- Individual specifications for all 5 prompts
- Output format enforcement strategies
- Validation strategies with code examples
- Clinical safety measures
- Best practices and troubleshooting
- Complete validation suite (Appendix A)
- Testing examples (Appendix B)
- Version history and glossary

**Use this for:**
- Understanding the overall system design
- Learning about guardrail implementation
- Implementing validators
- Troubleshooting specific issues
- Onboarding new developers

### 2. [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
**Quick Reference Guide** - At-a-glance information

Concise cheat sheets for:
- DO's and DON'Ts
- ATS category quick reference
- Output format templates
- Validation checklist
- Red flag triggers
- Australian terminology
- Common errors and fixes
- Safety principles

**Use this for:**
- Day-to-day reference while coding
- Quick validation checks
- Remembering output formats
- Emergency ATS category lookup
- Australian vs American terminology

## 🎯 Which Document Should I Use?

| Scenario | Document |
|----------|----------|
| I need to understand the overall prompt strategy | PROMPT_STRATEGY.md |
| I'm implementing a new validator function | PROMPT_STRATEGY.md (Appendix A) |
| I forgot the exact ATS categories | QUICK_REFERENCE.md |
| I need to check if output format is correct | QUICK_REFERENCE.md |
| I'm troubleshooting why output validation fails | PROMPT_STRATEGY.md (Troubleshooting) |
| I need an example of proper triage output | QUICK_REFERENCE.md (Templates) |
| I'm writing test cases for prompts | PROMPT_STRATEGY.md (Appendix B) |
| I need to know prohibited phrases | QUICK_REFERENCE.md (DON'Ts) |
| I want to understand guardrail philosophy | PROMPT_STRATEGY.md (Guardrail System) |
| Quick lookup of Australian medical terms | QUICK_REFERENCE.md (Terminology) |

## 🏥 Australian Standards Reference

Both documents are aligned with:

- **Australasian Triage Scale (ATS)** - 5-category emergency triage system
- **RACGP Standards 5th Edition** - Royal Australian College of General Practitioners documentation standards
- **Australian Privacy Principles** - Patient confidentiality and data handling
- **Australian Medical Terminology** - Correct spelling and units

## 🔄 Document Updates

These documents should be reviewed and updated:
- **Quarterly**: Regular review for accuracy
- **When prompts change**: Keep in sync with `utils/prompts.py`
- **When standards update**: ATS or RACGP guideline changes
- **When issues found**: Add to troubleshooting section

## 📁 Related Files

### Core System Files
- **`utils/prompts.py`** - All prompt definitions (the source of truth)
- **`utils/validators.py`** - Validation functions (see PROMPT_STRATEGY.md Appendix A for complete code)
- **`tests/test_prompts.py`** - Test cases (see PROMPT_STRATEGY.md Appendix B for examples)

### Application Files
- **`app.py`** - Main Streamlit application
- **`pages/`** - Application pages
- **`README.md`** - Project README (root level)

## 🚀 Quick Start for Developers

1. **Read this first**: [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - 5 minutes
2. **Then deep dive**: [PROMPT_STRATEGY.md](PROMPT_STRATEGY.md) - 30 minutes
3. **Review code**: `utils/prompts.py` - see prompts in action
4. **Implement validation**: Use Appendix A code from PROMPT_STRATEGY.md
5. **Test**: Use examples from Appendix B

## 📊 Documentation Stats

| Document | Word Count | Read Time | Last Updated |
|----------|-----------|-----------|--------------|
| PROMPT_STRATEGY.md | ~30,000 | 30-45 min | Oct 2024 |
| QUICK_REFERENCE.md | ~2,500 | 5-10 min | Oct 2024 |
| README.md (this file) | ~500 | 2-3 min | Oct 2024 |

## 🔍 Search Tips

Both Markdown files support text search (Ctrl+F / Cmd+F):

**Common searches:**
- "ATS 2" - Find ATS category 2 information
- "guardrail" - Find guardrail strategies
- "prohibited" - Find what NOT to do
- "example" - Find code or output examples
- "validation" - Find validation strategies
- "red flag" - Find emergency triggers
- "Australian" - Find Australian-specific requirements

## 🤝 Contributing

When updating documentation:

1. Update the relevant section in the appropriate document
2. Update version/date in document header
3. Add entry to version history (if major change)
4. Update this README if new sections added
5. Keep documentation in sync with code changes

## 📮 Questions?

For questions about:
- **Documentation content**: Review full PROMPT_STRATEGY.md
- **Quick lookups**: Check QUICK_REFERENCE.md
- **Code implementation**: See `utils/prompts.py`
- **System issues**: Consult Troubleshooting section in PROMPT_STRATEGY.md

---

