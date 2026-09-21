# NuclearShield Pull Request

Thank you for contributing to NuclearShield.

Please complete the sections below before submitting the pull request.

## Summary

Describe the change clearly and concisely.

## What Changed

Explain the main changes included in this pull request.

- 
- 
- 

## Why This Change Is Needed

Explain the problem being solved or the improvement being introduced.

## Testing

Describe how the change was tested.

Please confirm where applicable:

- [ ] Existing automated tests pass
- [ ] New tests were added for new or changed behavior
- [ ] Ruff checks pass
- [ ] Bandit checks pass
- [ ] Docker Compose configuration was validated
- [ ] Runtime behavior was manually verified

Commands used for validation may be included below:

    pytest -q
    ruff check app tests
    bandit -q -r app -x app/static
    docker compose config

## Documentation

- [ ] README was updated if required
- [ ] CHANGELOG was updated if required
- [ ] Other documentation was updated if required
- [ ] No documentation changes are required

## Safety Boundary

All contributions must preserve NuclearShield's defensive, read-only architecture.

Please confirm:

- [ ] This change remains defensive and read-only
- [ ] No plant-control or command functionality is introduced
- [ ] No offensive exploitation functionality is introduced
- [ ] No real nuclear facility data is included
- [ ] No operational SCADA or I&C data is included
- [ ] No sensitive facility topology or credentials are included
- [ ] No real safety-system, physical-access, personnel, or nuclear material information is included
- [ ] Human authority remains the final decision boundary

## Security Impact

Does this pull request affect security-sensitive functionality?

- [ ] No
- [ ] Yes

If yes, explain the impact without including sensitive operational information.

## Breaking Changes

- [ ] No breaking changes
- [ ] This pull request introduces a breaking change

If applicable, describe the breaking change and required migration steps.

## Final Checklist

- [ ] The change is focused and does not include unrelated modifications
- [ ] Code is understandable and maintainable
- [ ] Tests and validation were completed where applicable
- [ ] Documentation matches implemented behavior
- [ ] Synthetic or fictional data is used for demonstrations
- [ ] The NuclearShield safety boundary is preserved
