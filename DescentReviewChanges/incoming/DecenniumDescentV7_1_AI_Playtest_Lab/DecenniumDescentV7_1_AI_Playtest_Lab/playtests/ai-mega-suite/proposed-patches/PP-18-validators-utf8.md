# Proposed patch — Windows UTF-8 safe validators

**From pack:** 18  
**Canon edit:** NOT APPLIED (proposal only)

## Problem

`validate_public_canon.py` fails decoding JSON with byte 0x9d under charmap. `validate_gameplay_loop.py` can PASS logic then crash printing Unicode arrows under cp1252.

## Proposal

Open text as UTF-8 explicitly; print ASCII-safe status lines or set UTF-8 stdout.

## Evidence

- REG-STATIC validator_rerun.json returncodes.
