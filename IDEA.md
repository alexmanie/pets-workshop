# Spec Kit Idea Assessment

## Set up

```bash
specify init --here --force --integration copilot
specify extension add assess
```

## Workflow

1. Capture the idea

```bash
/speckit-assess-intake "Let users create new pets." slug=create-pet
```

2. Research the evidence

```bash
/speckit-assess-research slug=create-pet
```

3. Define the problem

```bash
/speckit-assess-define slug=create-pet
```

4. Shape possible solutions

```bash
/speckit-assess-shape slug=create-pet
```

5. Make the decision

```bash
/speckit-assess-decide slug=create-pet
```

## Optional handoff to SDD

```bash
/speckit-specify Use the handoff summary in .specify/assessments/create-pet/decision.md to specify the approved create-pet concept.
```

