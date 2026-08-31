# Research Guidelines

OpenMicroDuck publishes only material suitable for a public research repository.

## Evidence labels

Use the most precise label available:

- **Official product spec** — published product/press specification.
- **Official source** — directly visible in official code, configuration, documentation, or simulation assets.
- **Measured** — physical measurement with method and conditions.
- **Observed** — direct black-box, teardown, protocol, or behavior observation.
- **Inferred / Community reconstruction** — derived from public evidence but not directly confirmed.
- **Assumed** — temporary research or simulation placeholder.
- **Provisional** — visible in official/development material but explicitly not final.

## Public-only rule

Contributions must be appropriate for public disclosure. Do not contribute:

- confidential, leaked, private, or non-public project information;
- credentials, device secrets, private keys, account data, or personal data;
- proprietary CAD, PCB, schematic, firmware, or internal documentation obtained without authorization;
- unrelated private engineering work merely because it could be useful for comparison;
- third-party assets without compatible rights and attribution.

## Write for a reader who is new to robotics

Technical accuracy is not enough if the page is difficult to understand.

For normal explanatory pages:

1. **Explain the job before the code name.** Write “camera/video service (`mediad`)”, not only “`mediad`”.
2. **Show the whole flow first.** A small diagram should come before a long list of modules or parameters when it helps orientation.
3. **Use plain language before specialist terms.** If a term such as daemon, observation, policy, IPC or kinematics matters, explain it in one short sentence the first time.
4. **Do not stack unexplained nouns.** Avoid sentences that require the reader to already know several frameworks, protocols or source-tree names.
5. **Separate overview from reference detail.** Dense tables are appropriate in parameter-reference pages, but they should follow a short “what this means” section.
6. **Prefer one clear diagram over repeated prose.** Do not explain the same architecture three different ways on one page.
7. **Keep paragraphs short.** One paragraph should usually explain one idea.
8. **Answer four questions early:** What is this? What does it do? Where does it sit in the robot? What is confirmed versus uncertain?

A useful architecture style is:

```text
sensor
  ↓
perception
  ↓
behavior decision
  ↓
movement policy
  ↓
motor control
```

Only after that should the page introduce names such as `tofd`, `mediad`, `robotd`, JSON-RPC, Unix sockets, RKNN or ONNX Runtime.

## Reverse-engineering documentation

Good reverse-engineering notes explain:

1. what public artifact or physical observation was used;
2. how the result was derived;
3. what uncertainty remains;
4. whether the result describes a simulation model, development unit, or production product;
5. which revision / commit / firmware version was involved.

Prefer independently created diagrams and tables over copied third-party artwork.

## Reproducibility

Measurements should record, where relevant:

- hardware revision;
- firmware/software version;
- source commit;
- equipment;
- test conditions;
- units;
- sample count;
- uncertainty or variation;
- raw-data location.

## Conflicting sources

Do not erase disagreement. If public sources conflict, document the conflict and explain which source is used for which claim.

## Translation policy

English and Simplified Chinese documentation should preserve the same technical meaning. A translation should not introduce a stronger claim than the source-language document. Future language trees should follow the same rule.
