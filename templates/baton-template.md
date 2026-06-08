# Baton Template

> Copy this template and fill in every field. Delete this comment block when done.

### baton-NNN: [descriptive-kebab-case-name]
- **Status**: in-progress
- **Owner**: [agent-identifier] (session-id or tmux-pane)
- **Started**: YYYY-MM-DDTHH:MM:SSZ
- **Updated**: YYYY-MM-DDTHH:MM:SSZ
- **Input**: What this agent received — link the previous baton's `Next` field here if applicable
- **Output**:
  - [artifact 1 — commit SHA, PR number, file path, etc.]
  - [artifact 2]
- **Next**: Complete task description for the next agent. Must be self-contained — a fresh session should be able to start work from this alone.
- **Handoff-to**: [agent type + specific task focus]
- **Blockers**: None | [describe blocker + what's needed to unblock]
- **Verify**:
  ```bash
  # Concrete commands that produce pass/fail output
  ```

---

## Checklist (delete after filling)

- [ ] Baton number is sequential
- [ ] Name describes the output, not the process
- [ ] Status is set correctly (in-progress → completed | blocked)
- [ ] Timestamps are ISO 8601 UTC
- [ ] Output has concrete artifacts (not descriptions)
- [ ] Next field is self-contained (no "see previous conversation")
- [ ] Verify block is copy-paste-runnable
- [ ] Blockers field is filled (write "None" if clear)
