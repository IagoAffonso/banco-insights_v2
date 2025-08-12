# 📦 Archive - Banco Insights 2.0

This folder contains archived files that are no longer actively used but kept for historical reference and potential future use.

---

## 📁 Archive Structure

### **📄 old_docs/**
**Contents**: Deprecated documentation and obsolete planning files
- `AGENTS.md` - Old agent configuration documentation
- `lovable_frontend_prompt.md` - Legacy frontend requirements (English)
- `lovable_frontend_prompt_pt_br.md` - Legacy frontend requirements (Portuguese)

**Reason for Archiving**: Superseded by current documentation in `docs/` folder

---

### **🚀 deployment_configs/**
**Contents**: Old deployment configurations and setup scripts
- `deploy_to_supabase.py` - Legacy Supabase deployment script
- `deploy_via_supabase_api.py` - Alternative deployment method
- `load_institutions_supabase.py` - Institution data loader
- `test_supabase_connection.py` - Connection testing script
- `supabase_config.env` - Environment configuration

**Reason for Archiving**: 
- Replaced by enhanced deployment in `database/` folder
- Configuration moved to `config/` folder
- Legacy scripts no longer compatible with V2.0 architecture

---

## 🔍 File Inventory

| File | Original Purpose | Archive Date | Replacement |
|------|------------------|--------------|-------------|
| `AGENTS.md` | Agent configuration | Jan 2025 | `CLAUDE.md` |
| `lovable_frontend_prompt.md` | Frontend specs | Jan 2025 | `docs/planning/` |
| `deploy_to_supabase.py` | Database deployment | Jan 2025 | `database/deploy_schema.py` |
| `supabase_config.env` | Environment config | Jan 2025 | `config/` folder |

---

## ⚠️ Important Notes

### **Before Using Archived Files**
1. **Check Current Alternatives**: Most functionality has been superseded
2. **Review Compatibility**: Archived code may not work with current structure
3. **Update Dependencies**: Legacy files may have outdated requirements
4. **Test Thoroughly**: Validate any restored functionality

### **Restoration Process**
If you need to restore an archived file:
1. Copy to appropriate current folder structure
2. Update imports and dependencies
3. Test compatibility with current codebase
4. Update documentation to reflect restoration

---

## 🗑️ Future Cleanup

### **Safe to Delete (After 6 months)**
- Legacy deployment scripts once V2.0 is stable
- Old frontend prompts once React frontend is complete
- Duplicate configuration files

### **Keep Indefinitely**
- Historical documentation for reference
- Original deployment scripts as backup
- Configuration examples for different environments

---

## 📚 Related Documentation

- **Current Setup**: See `README.md` in project root
- **Current Deployment**: See `database/README.md`
- **Current Config**: See `config/` folder
- **Development Guidelines**: See `CLAUDE.md`

---

**Archive Policy**: Files are moved here instead of deleted to maintain project history and enable future reference if needed.

**Last Review**: January 2025  
**Next Cleanup**: July 2025