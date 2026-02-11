---
name: nexport-ui-fixtures-my-courses
description: "UiTests fixtures for My Courses/My Training coverage (seeding data, login-as, selectors, and common pitfalls)."
---

# NexPort UI Fixtures: My Courses / My Training

## When to use
- When adding or updating My Courses (My Training) Playwright coverage.
- When UiTests need deterministic enrollments for the My Courses view.

## Fixture flow (UiTests)
- Ensure org exists:
  - `POST /UiTests/EnsureOrganization?shortName=<ORG>`
- Seed My Training fixtures:
  - `POST /UiTests/EnsureMyTrainingFixtures?organizationShortName=<ORG>`
- Login as persona (loopback only):
  - `POST /UiTests/LoginAsMyTrainingPersona?persona=student&organizationShortName=<ORG>`
  - Sign-on URLs are single-use; always fetch fresh and allow redirect to set auth cookies.

## What EnsureMyTrainingFixtures should guarantee
- Subscription + membership for the persona.
- Active section + training plan enrollments.
- Required profile fields are satisfied to avoid redirect to EditMyProfile.
- My Courses preferences set to Sort=Date and Filter=All (avoids category pagination null-ref when no categories).

## Stable selectors
- Prefer table layout for deterministic selectors.
- Enrollment title: `#Title{EnrollmentId}`
- Filters panel: `#enrollment-filters`

## Common pitfalls
- `#enrollment-filters` timeout usually means `/MyCourses/Enrollments` 500; check server log.
- Category sort path can null-ref pagination when no categories exist; force Sort=Date in fixtures.
- Required profile fields trigger redirect to EditMyProfile; fill required values during fixture seeding.

## Related files
- `NexPortVirtualCampus/Controllers/UiTestsController.cs`
- `NexPort.UiTests/MyTraining/MyTrainingSmokeTests.cs`
- `NexPort.UiTests/Infrastructure/UiTestUrlResolver.cs`
- `NexPortVirtualCampus/Views/MyCourses/*.cshtml`
