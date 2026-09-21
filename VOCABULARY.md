# Course vocabulary

A running guide to the words this course uses in a specific sense. It grows
by a section each week, after the session that introduces the terms. Each
entry gives the course's definition, where the term shows up in this repository
or your own project, and where it is defined in a reading you have.

When a term has more than one meaning in the field, the entry says which one
the course means. Use these words in your scope record, your configuration
files and your discussion posts; the rubric reads them in this sense.

Corrections and additions are welcome as pull requests. Cite a source for a
definition, the same way the entries below do.

## Week 1: two lineages, agents that build and play

**Two lineages of game AI.** The classical lineage: finite state machines,
behavior trees, planning, search, reinforcement learning. The generative
lineage: a language model acting inside or on behalf of a game. This course
runs both side by side. Reading: Yannakakis and Togelius, *Artificial
Intelligence and Games*, chapter 1, free at <https://gameaibook.org>.

**Agentic engineering.** The practice this course teaches: agents do work
between decision points, and you decide at the decision points. The final
project's five gates are those decision points. Source: the published
syllabus in CourseWorks, course description.

**Model.** The thing that answers. It responds from its context and its
learned patterns, so an answer can be fluent and unsupported. In this
repository the narrator (`course_game/narrator.py`) is a model with no tools
and no memory of earlier turns; that is why `ask what is behind the door?`
can be confident and wrong.

**Context.** Everything the model can see at the moment it answers:
instructions, the conversation so far, retrieved documents, tool results.
The narrator's context is the `facts` dictionary passed to `narrate()`; if
the room is not in it, the room is not in the answer. Reading: Anthropic,
"Effective Context Engineering for AI Agents"
(<https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>),
assigned for September 28.

**Delegation, Description, Discernment, Diligence.** The four Ds from
*AI Fluency: Framework and Foundations* (Dakan and Feller,
<https://academy.claude.com/courses/ai-fluency-framework-foundations>).
Delegation: what you hand to an agent and what you keep. Description: how you
say what you mean, including context, constraints and the intended outcome.
Discernment: how you judge what comes back and decide to accept, reject or
revise. Diligence: taking responsibility for the result, including
attribution, transparency and effects on others. From Week 2 on, responses
about AI use the terms that fit the argument; not every term in every post.

**Magic circle.** Salen and Zimmerman's name for the boundary a game draws
around itself: inside it the rules hold, outside they stop. Reading:
*Rules of Play*, chapter 9, the PDF in CourseWorks. For an AI player, the
circle is the interface: the `legal_actions` list is the rule set made
explicit, and the engine refuses anything outside it.

**Core loop.** The shortest repeating sequence of action, response and
reward. In *A Dark Room* the first loop is light fire, stoke fire, gather
wood, about thirty seconds long. Source: the GDF reader in CourseWorks.

**Executive Producer and Creative Director.** Your two standing roles. You
set vision, scope, priorities and the quality bar; you resolve disagreements;
you accept or reject work. You are never a member of your own agent team.
Source: syllabus; `AGENTS.md` in this repository.

**Production agents and gameplay agents.** The syllabus's pair. Production
agents design, implement, review, test and release the game. Gameplay agents
act inside it as players, characters, opponents or systems. The midterm
brief says *building agent* and *playing agent* for the same pair; the
syllabus pair is the one on the rubric. Rule of thumb: a production agent may
see the repository; a gameplay agent sees only what `observe()` returns.

**Offline fixture.** The scripted narrator reply used when no live provider
is configured. It exercises the code path without a model call.
`python -m course_game.setup_check --offline --headless` reports on it.
A fixture is never relabeled as a live result (see `AGENTS.md`).

**CI.** Continuous integration: the deterministic tests in `tests/` run on
every push by `.github/workflows/setup-check.yml`. Live-model checks run only
when requested by hand and only after funded access is confirmed.

## Week 2: reading a game as source

**Evidence.** What a claim about a game's rules rests on. Three kinds: code
(what the program does), documents (what the designer said: manuals,
rulebooks, design notes), and play traces (what a player observed). Each
fails differently: code is authoritative and hard to read; a manual is
readable and wrong at edge cases; a trace is true for one run and silent
about the rest.

**`code` / `manual` / `observed` / `assumed`.** The four labels every line
of a rule/source map carries. The fourth is the one that matters: an
`assumed` line is a claim with no evidence yet, and the scope record due
September 28 asks you to separate it from the other three. Example from
class: in `doublespeakgames/adarkroom`, "the fire cools five minutes after a
stoke" is `code` (`script/room.js`, line 6, `_FIRE_COOL_DELAY`); "the
stranger arrives after the second stoke" is `observed` until you find the
`game.builder.level` check near line 712 and relabel it `code`.

**State, legal actions, outcome.** The three columns of a rule/source map.
State: the variables the game tracks (in this repository, the fields of
`World` in `course_game/world.py`). Legal actions: what a player may do in
the current state (the command list in `README.md`, section 2). Outcome:
what an action changes, and whether the episode has ended. The midterm's
machine-playable interface is these three made executable: `reset`,
`observe`, `legal_actions`, `step`, `outcome`.

**Constituative rules.** Salen and Zimmerman's term for the mathematical
structure under a game's stated rules. Their example: 3-to-15 (pick numbers
1 to 9; first to hold three summing to 15 wins) is tic-tac-toe on a magic
square; the constituative rules are what the two games share once the grid
and the Xs are gone. Reading: *Rules of Play*, chapter 12, "Rules on Three
Levels", through CLIO. Related: Koster, *A Theory of Fun*, chapter 5, "What
Games Aren't", on why the fiction around a game's math is dressing.

**Mechanics, dynamics, aesthetics.** The MDA framework. Mechanics are what
the code does (constants, formulas, random draws). Dynamics are what happens
when a player meets the mechanics over time. Aesthetics are what it feels
like. A playing agent sees mechanics and never aesthetics; human playtests
exist for the gap. Reading: Hunicke, LeBlanc and Zubek, "MDA: A Formal
Approach to Game Design and Game Research"
(<https://users.cs.northwestern.edu/~hunicke/MDA.pdf>), assigned for
September 28.

**Agent.** A model in a loop that can call tools and decide its own next
step toward a goal. Anthropic's distinction, which you read for October 5:
a *workflow* follows a code path someone wrote; an *agent* directs its own
process and tool use. In this repository the narrator is neither; the setup
checker is a workflow; your coding assistant is an agent. Reading:
Anthropic, "Building Effective Agents"
(<https://www.anthropic.com/research/building-effective-agents>).

**Agent team.** The agents one student directs. The syllabus's term for it;
the student is its Executive Producer and Creative Director. The midterm
requires at least an implementation agent, a reusable skill and an
independent review task. By term's end the team covers every game-development
role.

**Configuration.** The executable definition of one agent's role: its
instructions, tools, permissions, and what it may see. A prompt alone does
not enforce a boundary; configuration includes code. In this repository the
common settings live in `agent-config.json`. The Configuration Document at
G1 collects the whole team's configurations. Source: syllabus; midterm brief.

**Skill.** A reusable, packaged unit of instructions or tooling an agent can
load for a repeated job. The syllabus accepts a plugin, a skill or an MCP
server as the required executable agent extension artifact. You ship at
least one by the midterm.

**Harness.** The code that runs an agent under controlled conditions and
records what happened. The course means the *Agent Evaluation Harness*: the
runner (`reset`, `observe`, `legal_actions`, `step`, `outcome`), episode and
call limits, deterministic tests in CI, and logged traces. The field also
uses "harness" for the loop and tools wrapped around a model, which is what a
coding assistant is; when a reading says harness, check which sense it means.
Source: syllabus, learning goal 5 and the Agent Evaluation Harness section.

**Orchestration.** Who calls whom, in what order, and who decides. In this
course you orchestrate your agent team by hand, through Asana tasks linked to
pull requests; automating that coordination is optional. Inside a team, the
orchestrator-workers pattern (one agent dispatching subtasks to others) is
one design among several in "Building Effective Agents", and a choice to
justify rather than a default.

**Baseline.** The cheap scripted, heuristic or search player your model
player is compared against on the same interface and the same cases. A
demonstration win without a baseline is weak evidence. Source: midterm brief.

**Episode.** One bounded run of a game from `reset(seed)` to a terminal
`outcome()`, with a step limit, a model-call limit and an explicit reason
for ending. Failed calls count toward the budget.

**Trace.** The recorded sequence of observations, actions and results from
one episode, complete enough that someone else can check the claim you make
about it.

**Coding assistant and runtime provider.** Two independent choices. The
assistant (Claude Code, Codex, Cursor, or an equivalent) is the agent that
helps you build. The provider (Gemini through Vertex AI, Anthropic, OpenAI,
or an equivalent) is the model your game calls at runtime. One live provider
suffices; Gemini through Vertex is the course-funded default once credits
are confirmed. Source: syllabus, tools and accounts section; `README.md`
section 3.

**Scope record.** The September 28 submission: chosen game and evidence,
bounded scope, rule/source map, and one acceptance trace. Formative midterm
evidence, no separate grade.

**Acceptance trace.** One short sequence of legal actions with the expected
state changes and outcome, written before any implementation. It is the
first test case; the midterm's deterministic tests grow from it.

**Bounded scope.** A complete core loop, meaningful decisions, authoritative
state and listable legal actions, a clear ending or episode limit, and a
feasible agent evaluation. Five to eight rooms and two puzzles; a board game
with its complete rules; one arcade level with a fixed-step simulation. More
scope earns no bonus. Source: midterm brief.
