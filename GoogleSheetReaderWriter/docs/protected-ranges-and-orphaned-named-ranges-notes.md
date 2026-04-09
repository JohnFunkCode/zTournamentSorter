# Protected Ranges And Orphaned Named Ranges Notes

This document captures the practical lessons learned while enhancing Google Sheets support in this project.

The intended audience is a future Codex-assisted effort to update the tutorial at:

- `https://github.com/JohnFunkCode/GoogleSheetReaderWriter`

The focus here is not generic Google Sheets theory. It is the implementation journey, the failure modes we hit, and the design decisions that proved useful.

## Why This Work Was Needed

The project originally wrote spreadsheet data successfully, but later enhancements introduced more advanced Google Sheets features:

- protected ranges
- per-timeslot named ranges
- totals-sheet named ranges
- cross-sheet formulas using named ranges

Those features exposed several operational problems:

1. protected-range requests behaved differently depending on which Google account authenticated
2. spreadsheet reuse caused duplicate named-range failures
3. some named ranges appeared to become orphaned and could not be cleaned up through the normal API path
4. Google Sheets write quota had to be managed more proactively

## Protected Range Journey

### Initial Symptom

When the app was run by a non-owner user, Google Sheets operations that previously worked began failing with permission-style errors.

The suspicion was that protected ranges were the difference, because ordinary writes and formatting had worked before those protections were added.

That turned out to be correct.

### What The Code Was Doing

The upload flows were:

- deleting existing protected ranges during reset
- recreating new protected ranges after writing sheet data

At first, the protected ranges were created with empty editor lists, effectively:

- `editors: {"users": []}`

That created a mismatch:

- the OAuth user could authenticate successfully
- the OAuth user could often still edit normal cells
- but the OAuth user could fail when trying to create, update, or delete protected ranges

### Important Learning

Protected-range management is more permission-sensitive than ordinary spreadsheet editing.

It is not enough for the authenticated account to have basic editor access to the spreadsheet.

The acting account also needs to remain allowed in the protected-range editor set.

### First Fix

We added a config-driven list of accounts allowed to remain in protected ranges:

- `protected_range_editor_accounts`

That list was added to:

- `GoogleSheetReaderWriter/config/config.yaml`
- `GoogleSheetReaderWriter/config/config.example.yaml`

We then threaded that list through the Google Sheets write paths so that protected ranges are created with explicit allowed editors.

### Second Fix

We hit another Google Sheets error:

- `You can't remove yourself as an editor.`

That exposed another subtlety:

- even if a configured allowlist exists, the currently authenticated user still has to be included in the final editor list for the specific request being made

So we added logic to merge:

- configured protected-range editor accounts
- the currently authenticated Google account

This was implemented centrally so multiple report-writing paths could reuse it.

### Resulting Design Rule

For workflows that create or reset protected ranges:

1. the authenticated user must have editor-level spreadsheet access
2. the authenticated user must be included in the protected-range editor accounts
3. the code should automatically merge the active authenticated account into the final protected-range editor list

### Documentation Lesson

Any tutorial update should make this explicit:

- Google authentication success does not imply protected-range management success
- protected ranges are a second permission layer
- the acting account must remain in the allowed editors list

## Drive Folder Access Journey

### Symptom

During orphan recovery, the code attempted to create a replacement spreadsheet in the configured Drive folder.

That failed for one authenticated user with:

- Drive `404 File not found`

Even though the user had successfully authenticated and could interact with some spreadsheets.

### Important Learning

A configured Drive folder is part of the permission model.

The authenticated user needs to be able to:

- see the folder
- access the folder
- create files inside the folder

It is possible for a user to authenticate correctly and still fail later because they cannot create a replacement spreadsheet in the configured folder.

### Fix

We hardened spreadsheet creation so that:

- it first tries to create the spreadsheet in the configured Drive folder
- if Drive returns `403` or `404` for that folder, it logs the problem
- then falls back to creating the spreadsheet in the authenticated user's Drive root

### Documentation Lesson

Any future tutorial should explicitly distinguish:

- access to an existing spreadsheet
- access to a Drive folder
- ability to create replacement spreadsheets in that folder

Those are related, but not identical.

## Named Range Journey

### First Problem: Duplicate Time-Slot Named Ranges

The project creates many named ranges for tournament score sheets.

Initially, named range names were based on:

- worksheet title
- dojo name

That worked until reruns started failing with duplicate-name errors even after normal cleanup.

### Fix

We changed the timeslot named-range naming scheme to include the actual Google `sheet_id`.

Conceptually, the name now includes:

- normalized worksheet title
- sheet id
- normalized dojo name

That made timeslot named ranges unique per physical sheet instance instead of only unique per visible sheet title.

### Result

The ordinary timeslot named ranges stopped colliding on rerun.

## Totals Sheet Named Range Journey

### Design Goal

The `Totals` tab needed stable named ranges for the bottom total row so those values could be reused elsewhere, especially by the `Leader Board` tab.

Those names were intentionally stable, for example:

- `Arvada_Total`
- `Aurora_Total`

### Problem

Stable spreadsheet-wide names are exactly the kind of names that can collide across reruns and sheet recreation.

We first attempted to handle this by:

- reading existing named ranges
- using `updateNamedRange` if one existed
- using `addNamedRange` otherwise

That was not enough.

## Orphaned Named Range Journey

### Symptom

Google Sheets would reject creation of a totals named range like:

- `Broomfield_Total`

with an error saying the name already existed.

But the API call used to enumerate named ranges did not return that name at all.

That meant:

- the code could not delete it during reset
- the code could not update it by id
- but Google still refused to let the name be reused

### Working Theory

The most likely explanation is an orphaned named range left behind from older spreadsheet states, especially after sheet deletion or earlier iterations of the code.

These appear to behave like hidden or broken `#REF` named ranges:

- they may not appear in normal `namedRanges` enumeration
- but they still block reuse of the name

### What We Confirmed

The normal reset path was already deleting all visible named ranges and all visible protected ranges.

So the problem was not that the reset logic forgot to clean up the ordinary visible resources.

The problem was that some named ranges were no longer visible through the normal API response.

### Defensive Fix

We added explicit detection for this condition.

The logic now:

1. tries to create or update totals-sheet named ranges normally
2. if Google says a name already exists
3. re-reads named ranges from the API
4. if the named range still cannot be found by name
5. raises a dedicated `OrphanNamedRangeError`

This is important because it distinguishes:

- ordinary duplicate names that the code can repair through `updateNamedRange`
- hidden/orphaned duplicates that cannot be repaired in place

### Recovery Fix

Once an orphan is detected, the tournament score upload now:

1. logs that the existing spreadsheet contains orphaned named ranges
2. creates a replacement spreadsheet
3. updates `sheet_registry.yaml` to point to the replacement spreadsheet id
4. retries the upload once against the fresh spreadsheet

This turned a hard failure into a recoverable workflow.

### Important Constraint

The code does **not** truly delete hidden orphaned named ranges from the old spreadsheet.

Instead, it recognizes that the spreadsheet is no longer safe to reuse and moves the workflow to a clean spreadsheet.

That is an important design choice and should be documented honestly in any tutorial update.

## Reset-Phase Hardening: What It Can And Cannot Do

### What The Reset Phase Now Does Reliably

Before rewriting the tournament score spreadsheet, the code now resets:

- all visible named ranges
- all visible protected ranges
- all old tabs except the first reusable tab
- stale cell values on the reused first tab

This is the correct order for the visible resources:

1. delete named ranges first
2. delete protected ranges
3. delete tabs
4. rewrite

Deleting visible named ranges before deleting tabs reduces the chance of creating new broken references.

### What The Reset Phase Cannot Reliably Do

The reset phase cannot guarantee deletion of named ranges that Google no longer exposes through the normal `namedRanges` API response.

That is why the spreadsheet-replacement fallback exists.

### Documentation Lesson

The tutorial should not overpromise.

It should say something like:

- the reset logic removes all visible named ranges and protected ranges
- if the spreadsheet still contains hidden orphaned named ranges from an older state, the safest recovery is to create a fresh spreadsheet

## Write Quota Journey

### Initial Problem

As the sheet-writing logic became more feature-rich, Google Sheets started returning:

- `429`
- write requests per minute per user quota errors

### Fixes

We reduced the number of writes by:

- batching values updates
- batching named-range creation where possible

Then we added proactive write throttling:

- a central per-user write limiter
- a 50 writes/minute safety ceiling below Google's 60 writes/minute quota

Later, we increased the minimum sleep interval used by the limiter so it would prefer fewer, larger pauses instead of many tiny pauses.

### Documentation Lesson

A tutorial update should mention both:

- request batching
- proactive write pacing

Reactive retry by itself is not enough for a workflow that regularly approaches the write quota.

## Practical Takeaways For The Future Tutorial

If this work is later folded back into the `GoogleSheetReaderWriter` tutorial, the most important practical takeaways are:

1. distinguish authentication from authorization
   - the authenticated account still needs sheet, folder, and protected-range access
2. explain protected ranges as a separate permission concern
   - ordinary sheet editor access may not be enough
3. explain Drive folder access as part of the document-creation path
   - especially when replacement spreadsheets may be created
4. discuss visible named ranges versus orphaned named ranges
   - ordinary cleanup can remove visible ranges
   - orphaned ranges may require spreadsheet replacement
5. recommend spreadsheet replacement as the safest recovery path once hidden orphaned names are detected
6. mention write quota management
   - batch writes
   - add a write limiter

## Suggested Sections For A Future Tutorial Update

If the upstream tutorial is updated later, these section titles would be reasonable candidates:

- `Protected Ranges And The Authenticated User`
- `Why The Signed-In Account Must Stay In The Protected-Range Editor List`
- `Drive Folder Access Is Separate From Spreadsheet Access`
- `Cleaning Up Visible Named Ranges Before Reusing A Spreadsheet`
- `How To Detect Orphaned Named Ranges`
- `When To Recreate A Spreadsheet Instead Of Reusing It`
- `Batching And Pacing Google Sheets Writes`

## Final Summary

The main lessons from this debugging cycle are:

- protected ranges introduced a second permission layer that had to be handled explicitly
- the authenticated user must be part of the protected-range editor set
- Drive folder access matters separately from spreadsheet access
- visible named ranges can be cleaned up normally, but orphaned named ranges may survive and block reuse
- once orphaned named ranges are detected, creating a fresh spreadsheet is safer than trying to keep repairing the old one
- proactive write pacing is necessary once the workflow becomes write-heavy

That combination of lessons is the core material worth carrying into the future tutorial update.
