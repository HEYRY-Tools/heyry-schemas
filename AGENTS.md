# AGENTS – Operational Rules for HEYRY Schemas

This repository is governed by strict, deterministic automation rules.
All AI agents, code generators, and automated tools MUST follow every
instruction below with no exceptions.

## 1. Repository Purpose

This repository is the authoritative public registry of all HEYRY Tools
JSON Schemas. Every schema, example, script, and workflow MUST conform to
a consistent structure and versioning model.

Agents may NOT add business logic, IoT code, or product code. Only schema
maintenance files and validation utilities are allowed.

## 2. Do Not Modify These Files

AI agents MUST NOT modify:
- README.md
- LICENSE
- AGENTS.md

Unless explicitly instructed in a prompt.

## 3. Schema Structure Requirements

All schemas MUST:
- Use JSON Schema Draft-07.
- Include: `$schema`, `$id`, `title`, `description`, `schema_version`,
  `domain`, `owner_role`, `status`.
- Place schemas only under `schemas/<domain>/<schema-name>/v<major>/`.
- Name all schema files `<schema-name>.schema.json`.
- Use `$id` URLs of the form:
  `https://schema.heyry.tools/<domain>/<schema-name>/v<major>/<schema-name>.schema.json`.
  If a prompt, example, or legacy file shows `https://schemas.heyry.tools/` or any
  other host, agents MUST still normalize to `https://schema.heyry.tools/`.
- Before defining new structures, agents MUST check whether a base schema
  already exists (e.g., identifiers, semantic versions, metadata) and
  reuse those schemas as building blocks via `$ref`, `allOf`, or other
  JSON Schema composition features whenever applicable.

Agents MUST validate that:
- `$id` path matches folder path.
- `schema_version` is valid semver (MAJOR.MINOR.PATCH).
- `additionalProperties` rules follow the spec of each schema type.

Agents MUST run `invoke check` before every submission. This command runs the
full validation suite and MUST pass with no errors.

## 4. Examples

All example JSON files MUST:
- Live under `examples/<domain>/<version>/`.
- Include a `$schema` property pointing to the correct public URL.
- Fully validate against the referenced schema.

## 5. Scripts

Only the following script types are allowed:
- Schema metadata validation
- Schema linting
- Example validation
- Index generation (`index.json`)
- Internal tooling required to maintain the registry

Scripts MUST NOT depend on external services, network calls, or any
non-standard Python libraries.

## 6. GitHub Actions

Agents MUST maintain `.github/workflows/validate-schemas.yml` so that:
- All schemas are validated on push and PR
- All examples validate against their `$schema`
- Python 3.12 is used
- `jsonschema` is installed from `requirements.txt`

## 7. No External Code Contributions

This repository is reference-only and does NOT accept external
contributions. Agents MUST NOT create:
- CONTRIBUTING.md
- Pull request templates
- Issue templates

Unless explicitly requested.

## 8. Determinism

All agent output MUST be deterministic:
- No ambiguous language
- No placeholder text
- No TODO markers
- No assumptions outside the instructions in the user’s prompt

## 9. Safety

Agents MUST NOT introduce:
- Dynamic code execution
- Remote includes
- External schema fetches
- Uncontrolled recursion
- Undocumented fields

## 10. Goal

Ensure the repository stays:
- Clean
- Deterministic
- Predictable
- Governed
- Consistent
- Always machine-valid

These rules apply to ALL AI code and schema generation.
