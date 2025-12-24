For any requested change or task which is not trivial, you should always assess the situation, test your assumptions in the console (e.g., small repros or focused checks), make tests, and then present a detailed plan of action before ANY change to the code. Run relevant unit tests after the edit (not before), unless explicitly requested otherwise.
You'll enact your plan of action after the plan has been approved by the user.

**Exception:** The planning and wait for approval process is not needed when asked to add documentation.

## ⚠️ IMPORTANT: When In Doubt, Ask First

Do not blindly interpret and enact changes if:

- The requirements or desiderata are not clear.
- There are two or more drastically different approaches to solve an issue.
- Some evidence you found would lead you to take bold or significant choices.
- You noticed something else that seems to be wrong or not working as expected while trying to perform a requested task.

**Always ask to confirm the course of action before proceeding.** When in doubt, ask.

## Track learning points

Update progressively this document when you learn something about how to better perform your tasks related to this project. This could be coding best practices, implementation details, overall design decisions, corrections and remarks from the user, etc.

Update the list below with the new learning points:

```yaml
- name: git write confirmation
  description: Always ask for explicit user confirmation before performing any write operation to the git repository, such as commit, push, or other actions that modify git history.
  scope: git operations
```
