# Axie Studio Rebranding Checklist

## Backend Files to Update

### Core Module Rename
- [ ] Rename `src/backend/base/langflow` to `src/backend/base/axie_studio`
- [ ] Update `pyproject.toml` package references
- [ ] Update `setup.py` package references

### Database Files
- [ ] Rename `langflow.db` to `axie_studio.db`
- [ ] Update database references in code

### Configuration Files
- [ ] Update environment variable prefixes from `LANGFLOW_` to `AXIE_STUDIO_`
- [ ] Update configuration files in `src/backend/base/axie_studio/settings.py`
- [ ] Update server configuration in `src/backend/base/axie_studio/server.py`

### Documentation
- [ ] Update all documentation in `docs/` directory
- [ ] Update API documentation
- [ ] Update example files
- [ ] Update README files in subdirectories

### Test Files
- [ ] Update test file references
- [ ] Update test environment variables
- [ ] Update test fixtures

### Migration Files
- [ ] Update Alembic migration files
- [ ] Update database migration scripts

## Steps to Complete Rebranding

1. **Preparation**
   - [ ] Stop all running instances
   - [ ] Create backup of current state
   - [ ] Document current environment variables

2. **Backend Updates**
   - [ ] Run migration script
   - [ ] Update import statements
   - [ ] Update environment variables
   - [ ] Update database references

3. **Documentation Updates**
   - [ ] Update all markdown files
   - [ ] Update API documentation
   - [ ] Update example code
   - [ ] Update configuration examples

4. **Testing**
   - [ ] Update test files
   - [ ] Run test suite
   - [ ] Verify all functionality

5. **Deployment**
   - [ ] Update deployment scripts
   - [ ] Update Docker configurations
   - [ ] Update CI/CD pipelines

## Files to Update

### Python Files
```
src/backend/base/langflow/__init__.py
src/backend/base/langflow/main.py
src/backend/base/langflow/server.py
src/backend/base/langflow/settings.py
src/backend/base/langflow/worker.py
src/backend/base/langflow/langflow_launcher.py
```

### Configuration Files
```
pyproject.toml
setup.py
alembic.ini
```

### Documentation Files
```
docs/*
README.md
CONTRIBUTING.md
```

### Test Files
```
src/backend/tests/*
src/frontend/tests/*
```

## Environment Variables to Update

```
LANGFLOW_DATABASE_URL -> AXIE_STUDIO_DATABASE_URL
LANGFLOW_AUTO_LOGIN -> AXIE_STUDIO_AUTO_LOGIN
LANGFLOW_API_KEY -> AXIE_STUDIO_API_KEY
```

## Next Steps

1. Stop all running processes
2. Create a full backup
3. Run the migration script
4. Test all functionality
5. Update documentation
6. Deploy changes 