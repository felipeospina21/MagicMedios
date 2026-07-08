# MagicMedios Go Migration Plan

This document is a practical implementation guide for rewriting the current Python automation into Go, using `rod` for browser automation and Go-native libraries for the remaining responsibilities.

The goal is not just to "port the code". The goal is to preserve the current behavior, reduce operational friction, and leave the project with a clearer architecture that is easier to maintain, test, and package.

## 1. Current System Snapshot

The current application is a Python CLI automation pipeline:

1. Load environment configuration.
2. Read user input from the terminal.
3. Determine product references and supplier routing.
4. Open websites, scrape product data, and retry when needed.
5. Build a PowerPoint quotation based on a template.
6. Save the final presentation.
7. Increment and persist a consecutive number with locking.
8. Write logs to rotating files.

### Main Python entry points

- [main.py](/home/felipe/projects/MagicMedios/main.py)
- [app.py](/home/felipe/projects/MagicMedios/app.py)
- [scraper.py](/home/felipe/projects/MagicMedios/scraper.py)
- [presentation.py](/home/felipe/projects/MagicMedios/presentation.py)
- [utils.py](/home/felipe/projects/MagicMedios/utils.py)
- [log.py](/home/felipe/projects/MagicMedios/log.py)
- [lock_file.py](/home/felipe/projects/MagicMedios/lock_file.py)

### Current Python dependencies

- `python-pptx` for presentations
- `requests` for HTTP
- `python-dotenv` for env loading
- `pytest-playwright` for browser testing support

## 2. Target Go Architecture

The Go rewrite should be split into small, focused packages. The intent is to keep browser automation, scraping rules, data modeling, document generation, and IO separate.

### Recommended package layout

```text
cmd/magicmedios/main.go
internal/config/
internal/model/
internal/app/
internal/scraper/
internal/scraper/suppliers/
internal/presentation/
internal/logging/
internal/lock/
internal/io/
```

### Proposed responsibility map

- `cmd/magicmedios/main.go`
  - Program entry point.
  - Loads config.
  - Runs the application workflow.

- `internal/config`
  - Reads `.env` and environment variables.
  - Resolves paths and runtime options.

- `internal/model`
  - Defines shared domain types:
    - Client
    - Representative
    - Contact
    - Product data
    - Task result
    - Supplier metadata

- `internal/app`
  - Orchestrates the full workflow.
  - Handles terminal input.
  - Manages retry prompts for missing references.
  - Coordinates scraping and presentation generation.

- `internal/scraper`
  - Owns browser startup, page lifecycle, concurrency, retries, and routing.
  - Implements generic scraping helpers.

- `internal/scraper/suppliers`
  - Contains supplier-specific extraction logic.
  - One file per supplier is recommended to match the current codebase structure.

- `internal/presentation`
  - Creates the quotation deck from a PowerPoint template.
  - Adds footer, headers, client names, product slides, and the policy slide.

- `internal/logging`
  - Sets up structured logs and file rotation.
  - Exposes app-wide loggers.

- `internal/lock`
  - Encapsulates consecutive counter locking and file-safe updates.

- `internal/io`
  - Small helper functions for reading files, resolving paths, and handling filesystem operations cleanly.

## 3. Library Replacement Plan

This section is the practical dependency replacement map.

### Browser automation

Current:

- Python Playwright

Target:

- `rod`

Why:

- It is a strong fit for Chromium automation.
- It supports CSS, XPath, JS evaluation, and page interaction.
- It is well suited for scraping workflows.

What changes:

- Replace `page.locator(...)` calls with Rod selectors.
- Replace Playwright-specific wait patterns with Rod wait patterns.
- Rework any label/role-centric selectors into CSS/XPath/text-based selectors or JS-assisted lookup.

### Environment loading

Current:

- `python-dotenv`

Target:

- `github.com/joho/godotenv`

Usage pattern:

- Load `.env` in `main` as early as possible.
- Keep environment resolution in one config package.

### HTTP requests

Current:

- `requests`

Target:

- Go `net/http`

Usage pattern:

- Build a reusable HTTP client with timeout.
- Wrap request execution with retry logic.
- Decode into typed Go structures where possible.

### Presentation generation

Current:

- `python-pptx`

Target:

- A Go PowerPoint library, ideally one that can:
  - open a template
  - add slides
  - add text boxes
  - add images
  - save to `.pptx`

Candidate direction:

- `unioffice` is a plausible first option.

Important risk:

- The template is currently a `.pptm`, and PowerPoint macro-enabled files can be more brittle than plain `.pptx` when using libraries that primarily target standard OOXML presentation generation.
- This should be validated early with a prototype before committing to the full rewrite.

### Logging

Current:

- Custom Python logging with rotating files

Target:

- `log/slog` for structured logging, plus a rotating file writer if needed

Alternative:

- `logrus` if a more familiar structured logger is preferred

What matters:

- Separate error logs from general logs.
- Preserve daily rotation behavior.
- Keep logs machine-readable and easy to inspect.

### File locking

Current:

- Custom `msvcrt` / `fcntl` file lock wrapper

Target:

- `github.com/gofrs/flock`

Why:

- Simple lock semantics.
- Cross-platform support.
- Clean fit for protecting the consecutive counter file.

## 4. Functional Requirements to Preserve

The Go implementation should preserve these behaviors:

1. Prompt for client name unless running in debug/test mode.
2. Prompt for company name unless running in debug/test mode.
3. Prompt for advisor/user.
4. Parse comma-separated product references.
5. Route references by supplier prefix.
6. Retry browser interactions and retries for missing selectors.
7. Retry missing references after scraping if the user asks to try again.
8. Generate the PowerPoint using the existing template and images.
9. Save output into the configured quotations path.
10. Increment the consecutive counter safely.
11. Write logs to rotating files.

## 5. Behavior Mapping From Python to Go

### `app.py`

This file currently handles:

- argument parsing
- debug/test mode flags
- user prompts
- file path resolution
- consecutive counter handling
- user data retrieval

Go equivalent:

- Put runtime flags in a config struct.
- Move prompt and path logic into `internal/app`.
- Move counter logic into `internal/lock` or a dedicated `internal/counter` package.

### `main.py`

This file currently orchestrates the full workflow.

Go equivalent:

- `main.go` should be very small.
- It should create the app object and call one method such as `Run()`.
- All actual logic should stay in reusable packages.

### `scraper.py`

This file currently:

- launches the browser
- picks the correct supplier extractor
- handles concurrency
- retries browser startup
- retries failed routes

Go equivalent:

- Build a `Scraper` type.
- Give it a browser launcher, browser/page lifecycle management, and supplier dispatch.
- Add a supplier registry keyed by prefix.
- Keep the retry logic centralized instead of repeating it in each supplier.

### `suppliers/*`

Current supplier files are already logically separated.

Go equivalent:

- Keep one file per supplier:
  - `catalogospromo.go`
  - `cdopromo.go`
  - `mppromos.go`
  - `nwpromo.go`
  - `promoop.go`

Each supplier package should expose one main extraction function and only the helpers it needs.

### `presentation.py`

This file is the biggest structural port because it is stateful and template-heavy.

Go equivalent:

- Create a `PresentationBuilder` or `QuotationPresentation` type.
- Give it methods for:
  - initializing from template
  - adding slide scaffolding
  - writing the header
  - writing client details
  - adding product slide content
  - adding footer / policy slide
  - saving the file

### `utils.py`

This file currently centralizes a mix of helpers:

- selector retries
- image URL fetching
- inventory parsing
- HTTP helpers

Go equivalent:

- Split by concern:
  - `internal/scraper/helpers`
  - `internal/io/http`
  - `internal/text`

Avoid recreating a large "misc" file in Go. The migration should reduce this kind of coupling.

## 6. Proposed Implementation Phases

### Phase 1: Set up the Go project skeleton

Deliverables:

- `go.mod`
- base directory structure
- entry point
- config loading
- logging setup
- basic CLI wiring

Tasks:

1. Create the module name.
2. Add `cmd/magicmedios/main.go`.
3. Add config loading through `godotenv`.
4. Add structured logging and log file setup.
5. Add a basic app shell with `Run()` and `Prompt()` style methods.

Exit criteria:

- The app starts in Go.
- It can load `.env`.
- It can print basic configuration and exit cleanly.

### Phase 2: Port shared domain models

Deliverables:

- Go structs/types for all shared entities.

Tasks:

1. Translate `entities/entities.py` into Go structs.
2. Model product data, client data, representative data, contact data, and task results.
3. Add JSON or text-friendly field names if needed for logging/debugging.

Exit criteria:

- Scraper and presentation packages can share the same typed data.

### Phase 3: Port the scraping engine

Deliverables:

- Rod-based browser startup and page control.
- Supplier routing by prefix.
- Sequential scrape flow.
- Retry handling.

Tasks:

1. Create a browser launcher wrapper.
2. Recreate `scrape_product` behavior.
3. Recreate supplier selection based on prefix.
4. Port the supplier extractor methods.
5. Add retry handling for browser startup and transient page failures.

Exit criteria:

- At least one supplier can be scraped end-to-end in Go.
- The app returns typed product data from a real page.

### Phase 4: Port all supplier extractors

Deliverables:

- One Go implementation per supplier.

Tasks:

1. Port the current supplier-specific selectors.
2. Make sure each supplier returns the same data shape as Python.
3. Keep supplier-specific errors explicit and actionable.

Exit criteria:

- All supplier prefixes work in Go.
- The output data matches the Python output closely.

### Phase 5: Port presentation generation

Deliverables:

- Template loading
- Slide scaffolding
- Header/footer writing
- Product slide creation
- Final save

Tasks:

1. Choose and validate the Go PPTX library.
2. Load the existing template.
3. Recreate slide layout rules.
4. Recreate product content rendering.
5. Ensure images load correctly.
6. Verify the saved file opens in PowerPoint.

Exit criteria:

- Generated presentation is visually acceptable.
- The output opens without corruption.
- The slide count and structure match expectations.

### Phase 6: Port counter and locking

Deliverables:

- Safe incrementing of the consecutive number.
- Lock behavior that works on Windows and non-Windows systems.

Tasks:

1. Replace the custom lock-file behavior with `gofrs/flock`.
2. Encapsulate counter read/write logic.
3. Preserve debug-mode counter behavior.

Exit criteria:

- Concurrent runs do not corrupt the counter file.
- The counter increments exactly once per successful quotation.

### Phase 7: Finish the app workflow

Deliverables:

- Full end-to-end Go command.

Tasks:

1. Wire prompts into orchestration.
2. Wire retry flow for not-found references.
3. Save the presentation.
4. Increment the counter.
5. Emit logs.

Exit criteria:

- A full quotation run works without Python.

### Phase 8: Remove dependency on Python

Deliverables:

- Go build/release instructions.
- Windows packaging strategy.

Tasks:

1. Replace Python packaging files with Go build instructions.
2. Decide how to distribute the executable:
   - plain binary
   - installer
   - portable zip
3. Update README usage instructions.

Exit criteria:

- The project can be built and run from Go only.

## 7. Data Flow Design

The Go implementation should follow a single directional flow:

1. Config
2. CLI prompts
3. Reference parsing
4. Supplier routing
5. Scraping
6. Product aggregation
7. Presentation rendering
8. Save output
9. Counter increment
10. Logging

This matters because the current Python code is functional but fairly intertwined. The rewrite is a chance to remove implicit coupling.

## 8. Recommended Internal Interfaces

These interfaces are optional, but they will help the rewrite stay modular.

### Scraper interface

```go
type Scraper interface {
    Scrape(refs []string) ([]ProductData, []string, error)
}
```

### Supplier extractor interface

```go
type SupplierExtractor interface {
    Extract(page *rod.Page, ref string) (ProductData, bool, error)
}
```

### Presentation builder interface

```go
type PresentationBuilder interface {
    SetSlides(contact Contact) error
    AddHeader(representative Representative, consecutive int) error
    AddClientName(client Client) error
    AddCommercialPolicySlide() error
    CreateProductSlide(product ProductData, idx int) error
    Save(path string) error
}
```

### Counter store interface

```go
type CounterStore interface {
    Read() (int, error)
    Increment() (int, error)
}
```

## 9. Validation Strategy

Do not treat the rewrite as complete until these checks pass.

### Browser checks

- Login or landing pages can be opened.
- A known product code can be queried.
- Supplier selectors still resolve correctly.

### Data checks

- The same product input produces equivalent structured output.
- Missing references are reported and retried correctly.

### Presentation checks

- The output file opens in PowerPoint.
- Images render.
- Text boxes are positioned correctly.
- Slide count matches the expected count.

### Counter checks

- The counter increments once per successful run.
- Concurrent runs do not duplicate or skip values.

### Logging checks

- Errors go to the error log.
- Info/debug entries go to the general log.
- Logs rotate without manual cleanup.

## 10. Migration Order Recommendation

Use this order to reduce risk:

1. Create Go skeleton and config.
2. Port shared types.
3. Port browser automation for one supplier.
4. Validate one end-to-end scrape.
5. Port presentation generation.
6. Port remaining suppliers.
7. Port lock/counter handling.
8. Wire the full application flow.
9. Remove Python packaging.

This order is deliberate:

- It validates the hardest external dependency first: browser automation.
- It validates the second hardest dependency next: PowerPoint generation.
- It leaves packaging and cleanup for last, once core functionality is stable.

## 11. Risks and Mitigations

### Risk: PowerPoint template compatibility

Mitigation:

- Prototype early with the existing template.
- Verify the output opens in the exact version of PowerPoint used by the business.

### Risk: Browser selectors drift

Mitigation:

- Keep supplier selectors isolated in one package per supplier.
- Add selector retries and explicit error messages.

### Risk: Hidden behavior in the current Python code

Mitigation:

- Use the Python app as the reference implementation during migration.
- Compare outputs for a fixed set of inputs.

### Risk: Packaging and Windows distribution

Mitigation:

- Decide early whether the target is:
  - a single binary
  - a Windows installer
  - a portable folder

### Risk: File locking semantics on Windows

Mitigation:

- Use a well-tested Go locking library instead of custom cross-platform code.

## 12. Suggested Deliverables Checklist

- [ ] `go.mod`
- [ ] `cmd/magicmedios/main.go`
- [ ] `internal/config`
- [ ] `internal/model`
- [ ] `internal/app`
- [ ] `internal/scraper`
- [ ] `internal/scraper/suppliers`
- [ ] `internal/presentation`
- [ ] `internal/logging`
- [ ] `internal/lock`
- [ ] One working supplier port
- [ ] One working presentation prototype
- [ ] Full end-to-end quotation generation
- [ ] Packaging instructions
- [ ] Updated README

## 13. Acceptance Criteria

The migration is done when:

1. The full quoting workflow runs in Go.
2. The browser automation works with Rod.
3. The presentation output matches the current functional behavior.
4. Logging and counter persistence work reliably.
5. The repo no longer depends on Python for runtime execution.

## 14. Practical Next Step

The next concrete implementation step should be:

1. Scaffold the Go project.
2. Port the config/app bootstrap.
3. Prove one supplier works end-to-end.

That sequence gives you a narrow vertical slice to validate before the rewrite expands.
