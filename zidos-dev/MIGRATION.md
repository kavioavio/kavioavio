# Moving the Zidos profile to `zidos-dev`

`zidos-dev/profile/` is the organization profile, staged here so that it can be
reviewed next to the personal profile that shares its design. GitHub shows an
organization profile from `profile/README.md` in the organization's public
`.github` repository.

## Steps

1. Create the `zidos-dev` organization, if it does not exist yet.
2. Create the public repository `zidos-dev/.github`.
3. Copy this directory's `profile/` into it unchanged:
   `profile/README.md` and `profile/assets/header-{light,dark}.svg`.
4. Check the organization page in both GitHub themes, and at phone width:
   below 600 px the header drops the event log and enlarges the type.
5. In this repository, turn the plain `zidos-dev` mention in `README.md` into a
   link to `https://github.com/zidos-dev`.
6. Delete `zidos-dev/` here, keeping `design/`. Change the `org` entry in
   `design/build.py` to write into a checkout of `zidos-dev/.github`, or move
   `design/` there, so both headers keep one source.

Until step 5 the personal README does not link to the organization, so no link
on the public profile points at a page that does not exist yet.

## Before publishing

The organization profile names Zidos and describes it publicly. Re-read the
status table against the current `zidos-core` README on the day of migration:
it states facts that change (desktop, Windows, mobile).
