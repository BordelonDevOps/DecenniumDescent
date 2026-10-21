# FT84 — New complete-case navigator

Every row links by exact ID to CASEBOOK.json and SPECIFICATION_REPORT.json. These are finite authoring specifications; world permissions and actual acquisitions remain disclosed premises. Original78+28 source cases remain separately unchanged.

## FT84-01-written

Rank-one learning uses its real route

**Scope:** SOURCE_QUALIFIED_ISOLATED_SPECIFICATION

```json
{
  "walletCp": 3150,
  "materialsConsumed": {
    "lines": [
      {
        "id": "paper-A",
        "category": "mundane",
        "quantity": 4,
        "unitCp": 25,
        "indivisible": true,
        "required": 3,
        "lineExactCp": 75,
        "reductionFactor": "3/4"
      },
      {
        "id": "ink-A",
        "category": "mundane",
        "quantity": 5,
        "unitCp": 100,
        "indivisible": false,
        "required": "15/4",
        "lineExactCp": 375,
        "reductionFactor": "3/4"
      },
      {
        "id": "rare-ink-R",
        "category": "rare",
        "quantity": 4,
        "unitCp": 100,
        "indivisible": false,
        "required": 4,
        "lineExactCp": 400,
        "reductionFactor": 1
      }
    ],
    "exactTotalCp": 850,
    "finalPurchaseCp": 850
  },
  "materialsRemaining": [
    {
      "id": "paper-A",
      "quantity": 1
    },
    {
      "id": "ink-A",
      "quantity": "5/4"
    },
    {
      "id": "rare-ink-R",
      "quantity": 0
    }
  ],
  "teacherFeeCp": 0,
  "bookEntries": [
    "Detect Magic ritual-record only"
  ],
  "normalWizardBookAcquisition": false,
  "credits": {
    "requiredSeconds": 14400,
    "creditedSeconds": 14400,
    "pendingSeconds": 0,
    "lostSeconds": 0,
    "actualActiveSeconds": 14400,
    "elapsedSeconds": 14400,
    "complete": true,
    "completionOpportunities": 1,
    "trace": [
      {
        "event": {
          "start": 0,
          "seconds": 14400
        },
        "before": {
          "creditSeconds": 0,
          "pendingSeconds": 0,
          "lostSeconds": 0,
          "activeSeconds": 0,
          "time": 0
        },
        "after": {
          "creditSeconds": 14400,
          "pendingSeconds": 0,
          "lostSeconds": 0,
          "activeSeconds": 14400,
          "time": 14400
        }
      }
    ]
  },
  "RP": 0,
  "noCastOrXP": true
}
```

## FT84-01-teacher

Rank-one learning uses its real route

**Scope:** SOURCE_QUALIFIED_ISOLATED_SPECIFICATION

```json
{
  "walletCp": 2040,
  "materialsConsumed": {
    "lines": [
      {
        "id": "paper-A",
        "category": "mundane",
        "quantity": 4,
        "unitCp": 25,
        "indivisible": true,
        "required": 4,
        "lineExactCp": 100,
        "reductionFactor": 1
      },
      {
        "id": "ink-A",
        "category": "mundane",
        "quantity": 5,
        "unitCp": 100,
        "indivisible": false,
        "required": 5,
        "lineExactCp": 500,
        "reductionFactor": 1
      },
      {
        "id": "rare-ink-R",
        "category": "rare",
        "quantity": 4,
        "unitCp": 100,
        "indivisible": false,
        "required": 4,
        "lineExactCp": 400,
        "reductionFactor": 1
      }
    ],
    "exactTotalCp": 1000,
    "finalPurchaseCp": 1000
  },
  "materialsRemaining": [
    {
      "id": "paper-A",
      "quantity": 0
    },
    {
      "id": "ink-A",
      "quantity": 0
    },
    {
      "id": "rare-ink-R",
      "quantity": 0
    }
  ],
  "teacherFeeCp": 960,
  "bookEntries": [
    "Detect Magic ritual-record only"
  ],
  "normalWizardBookAcquisition": false,
  "credits": {
    "requiredSeconds": 28800,
    "creditedSeconds": 28800,
    "pendingSeconds": 0,
    "lostSeconds": 0,
    "actualActiveSeconds": 28800,
    "elapsedSeconds": 28800,
    "complete": true,
    "completionOpportunities": 1,
    "trace": [
      {
        "event": {
          "start": 0,
          "seconds": 28800
        },
        "before": {
          "creditSeconds": 0,
          "pendingSeconds": 0,
          "lostSeconds": 0,
          "activeSeconds": 0,
          "time": 0
        },
        "after": {
          "creditSeconds": 28800,
          "pendingSeconds": 0,
          "lostSeconds": 0,
          "activeSeconds": 28800,
          "time": 28800
        }
      }
    ]
  },
  "RP": 0,
  "noCastOrXP": true
}
```

## FT84-01-written-tutor-present

Rank-one learning uses its real route

**Scope:** SOURCE_QUALIFIED_ISOLATED_SPECIFICATION

```json
{
  "walletCp": 3150,
  "materialsConsumed": {
    "lines": [
      {
        "id": "paper-A",
        "category": "mundane",
        "quantity": 4,
        "unitCp": 25,
        "indivisible": true,
        "required": 3,
        "lineExactCp": 75,
        "reductionFactor": "3/4"
      },
      {
        "id": "ink-A",
        "category": "mundane",
        "quantity": 5,
        "unitCp": 100,
        "indivisible": false,
        "required": "15/4",
        "lineExactCp": 375,
        "reductionFactor": "3/4"
      },
      {
        "id": "rare-ink-R",
        "category": "rare",
        "quantity": 4,
        "unitCp": 100,
        "indivisible": false,
        "required": 4,
        "lineExactCp": 400,
        "reductionFactor": 1
      }
    ],
    "exactTotalCp": 850,
    "finalPurchaseCp": 850
  },
  "materialsRemaining": [
    {
      "id": "paper-A",
      "quantity": 1
    },
    {
      "id": "ink-A",
      "quantity": "5/4"
    },
    {
      "id": "rare-ink-R",
      "quantity": 0
    }
  ],
  "teacherFeeCp": 0,
  "bookEntries": [
    "Detect Magic ritual-record only"
  ],
  "normalWizardBookAcquisition": false,
  "credits": {
    "requiredSeconds": 14400,
    "creditedSeconds": 14400,
    "pendingSeconds": 0,
    "lostSeconds": 0,
    "actualActiveSeconds": 14400,
    "elapsedSeconds": 14400,
    "complete": true,
    "completionOpportunities": 1,
    "trace": [
      {
        "event": {
          "start": 0,
          "seconds": 14400
        },
        "before": {
          "creditSeconds": 0,
          "pendingSeconds": 0,
          "lostSeconds": 0,
          "activeSeconds": 0,
          "time": 0
        },
        "after": {
          "creditSeconds": 14400,
          "pendingSeconds": 0,
          "lostSeconds": 0,
          "activeSeconds": 14400,
          "time": 14400
        }
      }
    ]
  },
  "RP": 0,
  "noCastOrXP": true
}
```

## FT84-01-ambiguous-full-price

Unclassified material price does not block valid half-time work

**Scope:** SOURCE_QUALIFIED_ISOLATED_SPECIFICATION

```json
{
  "walletCp": 1000,
  "bookEntries": [
    "Detect Magic ritual-record"
  ],
  "activeSeconds": 14400,
  "materialDiscount": 0
}
```

## FT84-01-missing-source

No new prerequisite or stock from a discount

**Scope:** NEGATIVE_PREDICATE_NOT_WHOLE_LEARNING_IMPLEMENTATION

```json
{
  "walletCp": 2000,
  "creditSeconds": 0,
  "bookEntries": [],
  "adjudication": "no-learning-progress"
}
```

## FT84-01-no-readable-language

No new prerequisite or stock from a discount

**Scope:** NEGATIVE_PREDICATE_NOT_WHOLE_LEARNING_IMPLEMENTATION

```json
{
  "walletCp": 2000,
  "creditSeconds": 0,
  "bookEntries": [],
  "adjudication": "no-learning-progress"
}
```

## FT84-01-no-real-book

No new prerequisite or stock from a discount

**Scope:** NEGATIVE_PREDICATE_NOT_WHOLE_LEARNING_IMPLEMENTATION

```json
{
  "walletCp": 2000,
  "creditSeconds": 0,
  "bookEntries": [],
  "adjudication": "no-learning-progress"
}
```

## FT84-01-missing-rare-stock

No new prerequisite or stock from a discount

**Scope:** NEGATIVE_PREDICATE_NOT_WHOLE_LEARNING_IMPLEMENTATION

```json
{
  "walletCp": 2000,
  "creditSeconds": 0,
  "bookEntries": [],
  "adjudication": "no-learning-progress"
}
```

## FT84-01-unpaid-Spell-Scribe

No new prerequisite or stock from a discount

**Scope:** NEGATIVE_PREDICATE_NOT_WHOLE_LEARNING_IMPLEMENTATION

```json
{
  "walletCp": 2000,
  "creditSeconds": 0,
  "bookEntries": [],
  "adjudication": "no-copy-discount; use otherwise-legal baseline"
}
```

## FT84-01-unqualified-teacher

No new prerequisite or stock from a discount

**Scope:** NEGATIVE_PREDICATE_NOT_WHOLE_LEARNING_IMPLEMENTATION

```json
{
  "walletCp": 2000,
  "creditSeconds": 0,
  "bookEntries": [],
  "adjudication": "no-learning-progress"
}
```

## FT84-01-interruption

Written study retains completed15-minute credit and real used stock

**Scope:** SOURCE_QUALIFIED_ISOLATED_SPECIFICATION

```json
{
  "credit": {
    "requiredSeconds": 14400,
    "creditedSeconds": 14400,
    "pendingSeconds": 0,
    "lostSeconds": 600,
    "actualActiveSeconds": 15000,
    "elapsedSeconds": 15300,
    "complete": true,
    "completionOpportunities": 1,
    "trace": [
      {
        "event": {
          "start": 0,
          "seconds": 1500,
          "interrupt": true
        },
        "before": {
          "creditSeconds": 0,
          "pendingSeconds": 0,
          "lostSeconds": 0,
          "activeSeconds": 0,
          "time": 0
        },
        "after": {
          "creditSeconds": 900,
          "pendingSeconds": 0,
          "lostSeconds": 600,
          "activeSeconds": 1500,
          "time": 1500
        }
      },
      {
        "event": {
          "start": 1800,
          "seconds": 13500
        },
        "before": {
          "creditSeconds": 900,
          "pendingSeconds": 0,
          "lostSeconds": 600,
          "activeSeconds": 1500,
          "time": 1500
        },
        "after": {
          "creditSeconds": 14400,
          "pendingSeconds": 0,
          "lostSeconds": 600,
          "activeSeconds": 15000,
          "time": 15300
        }
      }
    ]
  },
  "inkConsumed": 4,
  "inkRemaining": 1,
  "bookEntries": [
    "Detect Magic ritual-record"
  ]
}
```

## FT84-01-rounding

Final purchase and time ceilings, not per-line or per-phase

**Scope:** PURE_ROUNDING_BOUNDARY_WITHOUT_NEW_COPY_PERMISSION

```json
{
  "minutes": 61,
  "bill": {
    "lines": [
      {
        "id": "tinyA",
        "category": "mundane",
        "quantity": 2,
        "unitCp": 1,
        "indivisible": false,
        "required": "3/2",
        "lineExactCp": "3/2",
        "reductionFactor": "3/4"
      },
      {
        "id": "tinyB",
        "category": "mundane",
        "quantity": 2,
        "unitCp": 1,
        "indivisible": false,
        "required": "3/2",
        "lineExactCp": "3/2",
        "reductionFactor": "3/4"
      },
      {
        "id": "protected",
        "category": "unique",
        "quantity": 1,
        "unitCp": 1,
        "indivisible": true,
        "required": 1,
        "lineExactCp": 1,
        "reductionFactor": 1
      }
    ],
    "exactTotalCp": 4,
    "finalPurchaseCp": 4
  },
  "oneIndivisibleSheetRequired": 1
}
```

## FT84-01-wizard-route

Wizard Spell Scribing remains its own found-spell procedure

**Scope:** EXISTING_SOURCE_WORKED_COMPARISON_NOT_CLASS_ACQUISITION_EXECUTION

```json
{
  "activeMinutes": 120,
  "costCp": 5000,
  "RitualBookEntryGranted": false
}
```

## FT84-01-method-switch

A later complete text changes only the unworked phase-aligned remainder

**Scope:** SOURCE_QUALIFIED_ISOLATED_SPECIFICATION

```json
{
  "actualWorkMinutes": 300,
  "completedRitualRecords": 1,
  "retroactiveRefundCp": 0
}
```

## FT84-02-translate

Named research preserves completed phase credit and exact single result

**Scope:** SOURCE_QUALIFIED_ISOLATED_SPECIFICATION

```json
{
  "progress": {
    "requiredSeconds": 14400,
    "creditedSeconds": 14400,
    "pendingSeconds": 0,
    "lostSeconds": 600,
    "actualActiveSeconds": 15000,
    "elapsedSeconds": 15300,
    "complete": true,
    "completionOpportunities": 1,
    "trace": [
      {
        "event": {
          "start": 0,
          "seconds": 1500,
          "interrupt": true
        },
        "before": {
          "creditSeconds": 0,
          "pendingSeconds": 0,
          "lostSeconds": 0,
          "activeSeconds": 0,
          "time": 0
        },
        "after": {
          "creditSeconds": 900,
          "pendingSeconds": 0,
          "lostSeconds": 600,
          "activeSeconds": 1500,
          "time": 1500
        }
      },
      {
        "event": {
          "start": 1800,
          "seconds": 13500
        },
        "before": {
          "creditSeconds": 900,
          "pendingSeconds": 0,
          "lostSeconds": 600,
          "activeSeconds": 1500,
          "time": 1500
        },
        "after": {
          "creditSeconds": 14400,
          "pendingSeconds": 0,
          "lostSeconds": 600,
          "activeSeconds": 15000,
          "time": 15300
        }
      }
    ]
  },
  "walletCp": 1500,
  "actualAgreedFeeCp": 500,
  "notesSheetsUsed": 1,
  "notesSheetsRemaining": 3,
  "completionCheck": {
    "die": 7,
    "INT": 3,
    "PB": 4,
    "assistant": 1,
    "total": 15,
    "DC": 15,
    "success": true
  },
  "result": "one supported preregistered passage",
  "XP": 0,
  "RP": 0,
  "manufactureInputsConsumed": 0,
  "newLanguageOrItem": false
}
```

## FT84-02-formula

Named research preserves completed phase credit and exact single result

**Scope:** SOURCE_QUALIFIED_ISOLATED_SPECIFICATION

```json
{
  "progress": {
    "requiredSeconds": 14400,
    "creditedSeconds": 14400,
    "pendingSeconds": 0,
    "lostSeconds": 600,
    "actualActiveSeconds": 15000,
    "elapsedSeconds": 15300,
    "complete": true,
    "completionOpportunities": 1,
    "trace": [
      {
        "event": {
          "start": 0,
          "seconds": 1500,
          "interrupt": true
        },
        "before": {
          "creditSeconds": 0,
          "pendingSeconds": 0,
          "lostSeconds": 0,
          "activeSeconds": 0,
          "time": 0
        },
        "after": {
          "creditSeconds": 900,
          "pendingSeconds": 0,
          "lostSeconds": 600,
          "activeSeconds": 1500,
          "time": 1500
        }
      },
      {
        "event": {
          "start": 1800,
          "seconds": 13500
        },
        "before": {
          "creditSeconds": 900,
          "pendingSeconds": 0,
          "lostSeconds": 600,
          "activeSeconds": 1500,
          "time": 1500
        },
        "after": {
          "creditSeconds": 14400,
          "pendingSeconds": 0,
          "lostSeconds": 600,
          "activeSeconds": 15000,
          "time": 15300
        }
      }
    ]
  },
  "walletCp": 1800,
  "actualAgreedFeeCp": 200,
  "notesSheetsUsed": 1,
  "notesSheetsRemaining": 3,
  "completionCheck": {
    "die": 5,
    "INT": 3,
    "PB": 3,
    "assistant": 0,
    "total": 11,
    "DC": 8,
    "success": true
  },
  "result": "usable exact recipe-121 transcription only",
  "XP": 0,
  "RP": 0,
  "manufactureInputsConsumed": 0,
  "newLanguageOrItem": false
}
```

## FT84-02-assistant-True

Assistant contribution requires all adjusted successful work

**Scope:** SOURCE_QUALIFIED_ISOLATED_SPECIFICATION

```json
{
  "total": 15,
  "success": true,
  "result": "supported passage",
  "retryWithoutNewEvidenceOrMethod": false
}
```

## FT84-02-assistant-False

Assistant contribution requires all adjusted successful work

**Scope:** SOURCE_QUALIFIED_ISOLATED_SPECIFICATION

```json
{
  "total": 14,
  "success": false,
  "result": "notes only",
  "retryWithoutNewEvidenceOrMethod": false
}
```

## FT84-02-final-fraction

A source-qualified final30seconds is a real shorter final phase

**Scope:** FINITE_PHASE_BOUNDARY_WITH_SOURCE_MINIMUM_PREMISE

```json
{
  "requiredSeconds": 14430,
  "creditedSeconds": 14430,
  "pendingSeconds": 0,
  "lostSeconds": 0,
  "actualActiveSeconds": 14430,
  "elapsedSeconds": 14430,
  "complete": true,
  "completionOpportunities": 1,
  "trace": [
    {
      "event": {
        "start": 0,
        "seconds": 14400
      },
      "before": {
        "creditSeconds": 0,
        "pendingSeconds": 0,
        "lostSeconds": 0,
        "activeSeconds": 0,
        "time": 0
      },
      "after": {
        "creditSeconds": 14400,
        "pendingSeconds": 0,
        "lostSeconds": 0,
        "activeSeconds": 14400,
        "time": 14400
      }
    },
    {
      "event": {
        "start": 14400,
        "seconds": 30
      },
      "before": {
        "creditSeconds": 14400,
        "pendingSeconds": 0,
        "lostSeconds": 0,
        "activeSeconds": 14400,
        "time": 14400
      },
      "after": {
        "creditSeconds": 14430,
        "pendingSeconds": 0,
        "lostSeconds": 0,
        "activeSeconds": 14430,
        "time": 14430
      }
    }
  ]
}
```

## FT84-02-real-progress-loss

A genuine prior loss leaves a5-minute final remainder

**Scope:** CONDITIONAL_PROGRESS_LOSS_BOUNDARY_NOT_NEW_LOSS_SOURCE

```json
{
  "requiredSeconds": 14400,
  "creditedSeconds": 14400,
  "pendingSeconds": 0,
  "lostSeconds": 0,
  "actualActiveSeconds": 300,
  "elapsedSeconds": 300,
  "complete": true,
  "completionOpportunities": 1,
  "trace": [
    {
      "event": {
        "start": 0,
        "seconds": 300
      },
      "before": {
        "creditSeconds": 14100,
        "pendingSeconds": 0,
        "lostSeconds": 0,
        "activeSeconds": 0,
        "time": 0
      },
      "after": {
        "creditSeconds": 14400,
        "pendingSeconds": 0,
        "lostSeconds": 0,
        "activeSeconds": 300,
        "time": 300
      }
    }
  ]
}
```

## FT84-02-exclude-ordinary-language-course

Named research completion does not leak into another procedure

**Scope:** SCOPED_CLASSIFICATION_BOUNDARY

```json
{
  "requiredMinutes": 19200,
  "newPhaseClockApplied": false,
  "newEvidenceGranted": false
}
```

## FT84-02-exclude-RitualCaster-teacher-learning

Named research completion does not leak into another procedure

**Scope:** SCOPED_CLASSIFICATION_BOUNDARY

```json
{
  "requiredMinutes": 480,
  "newPhaseClockApplied": false,
  "newEvidenceGranted": false
}
```

## FT84-02-exclude-ordinary-formula-copy

Named research completion does not leak into another procedure

**Scope:** SCOPED_CLASSIFICATION_BOUNDARY

```json
{
  "requiredMinutes": 60,
  "newPhaseClockApplied": false,
  "newEvidenceGranted": false
}
```

## FT84-02-exclude-Scribing-Insight-specific-spend

Named research completion does not leak into another procedure

**Scope:** SCOPED_CLASSIFICATION_BOUNDARY

```json
{
  "requiredMinutes": 480,
  "newPhaseClockApplied": false,
  "newEvidenceGranted": false
}
```

## FT84-02-exclude-fixed-curing-wait

Named research completion does not leak into another procedure

**Scope:** SCOPED_CLASSIFICATION_BOUNDARY

```json
{
  "requiredMinutes": 1440,
  "newPhaseClockApplied": false,
  "newEvidenceGranted": false
}
```

## FT84-02-exclude-unrelated-research-clock

Named research completion does not leak into another procedure

**Scope:** SCOPED_CLASSIFICATION_BOUNDARY

```json
{
  "requiredMinutes": null,
  "newPhaseClockApplied": false,
  "newEvidenceGranted": false
}
```

## FT84-02-invalid-unsupported-meaning

An actual project gate remains required

**Scope:** PREDICATE_DIAGNOSTIC_NOT_FULL_PROJECT_REJECTION_ENGINE

```json
{
  "creditSeconds": 0,
  "stock": 4,
  "extraRoll": false,
  "extraWorkWatch": false
}
```

## FT84-02-invalid-missing-archive-access

An actual project gate remains required

**Scope:** PREDICATE_DIAGNOSTIC_NOT_FULL_PROJECT_REJECTION_ENGINE

```json
{
  "creditSeconds": 0,
  "stock": 4,
  "extraRoll": false,
  "extraWorkWatch": false
}
```

## FT84-02-invalid-unchanged-evidence-retry

An actual project gate remains required

**Scope:** PREDICATE_DIAGNOSTIC_NOT_FULL_PROJECT_REJECTION_ENGINE

```json
{
  "creditSeconds": 0,
  "stock": 4,
  "extraRoll": false,
  "extraWorkWatch": false
}
```

## FT84-02-invalid-third-active-work-Watch

An actual project gate remains required

**Scope:** PREDICATE_DIAGNOSTIC_NOT_FULL_PROJECT_REJECTION_ENGINE

```json
{
  "creditSeconds": 0,
  "stock": 4,
  "extraRoll": false,
  "extraWorkWatch": false
}
```

## FT84-02-invalid-same-minute-training-and-research

An actual project gate remains required

**Scope:** PREDICATE_DIAGNOSTIC_NOT_FULL_PROJECT_REJECTION_ENGINE

```json
{
  "creditSeconds": 0,
  "stock": 4,
  "extraRoll": false,
  "extraWorkWatch": false
}
```

## FT84-03-gadget-False

Complete real gadget construction

**Scope:** SOURCE_QUALIFIED_ISOLATED_SPECIFICATION

```json
{
  "owner": "TEST-Gnome-maker",
  "partsLots": 1,
  "lotPriceCp": 500,
  "useSpent": 1,
  "nextUseAt": 86400,
  "receipts": [
    "build-1"
  ],
  "actualWorkSeconds": 600,
  "activeGadget": {
    "id": "build-1-body",
    "profile": "clamp (source worked-case d4=3; activation not tested)",
    "weightLb": 1,
    "AC": 10,
    "HP": 1,
    "createdAt": 600,
    "expiresAt": 4200,
    "holder": "TEST-Gnome-maker",
    "activationExecuted": false
  },
  "currencyCp": 0,
  "RP": 0,
  "otherItemCharges": 2
}
```

## FT84-03-gadget-True

Complete real gadget construction

**Scope:** SOURCE_QUALIFIED_ISOLATED_SPECIFICATION

```json
{
  "owner": "TEST-Gnome-maker",
  "partsLots": 1,
  "lotPriceCp": 500,
  "useSpent": 1,
  "nextUseAt": 86400,
  "receipts": [
    "build-1"
  ],
  "actualWorkSeconds": 300,
  "activeGadget": {
    "id": "build-1-body",
    "profile": "clamp (source worked-case d4=3; activation not tested)",
    "weightLb": 1,
    "AC": 10,
    "HP": 1,
    "createdAt": 300,
    "expiresAt": 3900,
    "holder": "TEST-Gnome-maker",
    "activationExecuted": false
  },
  "currencyCp": 0,
  "RP": 0,
  "otherItemCharges": 2
}
```

## FT84-03-gadget-interrupt

Four minutes cannot be banked into a later gadget

**Scope:** SOURCE_QUALIFIED_ISOLATED_SPECIFICATION

```json
{
  "owner": "TEST-Gnome-maker",
  "partsLots": 1,
  "lotPriceCp": 500,
  "useSpent": 1,
  "nextUseAt": 86400,
  "receipts": [
    "build-1"
  ],
  "actualWorkSeconds": 240,
  "activeGadget": null,
  "currencyCp": 0,
  "RP": 0,
  "otherItemCharges": 2
}
```

## FT84-03-gadget-immediate-retry

Remaining parts do not reset the spent24h use

**Scope:** SOURCE_QUALIFIED_ISOLATED_SPECIFICATION

```json
{
  "owner": "TEST-Gnome-maker",
  "partsLots": 1,
  "lotPriceCp": 500,
  "useSpent": 1,
  "nextUseAt": 86400,
  "receipts": [
    "build-1"
  ],
  "actualWorkSeconds": 240,
  "activeGadget": null,
  "currencyCp": 0,
  "RP": 0,
  "otherItemCharges": 2
}
```

## FT84-03-gadget-later-use

A real next24h use needs a fresh full5-minute job and parts

**Scope:** SOURCE_QUALIFIED_ISOLATED_SPECIFICATION

```json
{
  "owner": "TEST-Gnome-maker",
  "partsLots": 0,
  "lotPriceCp": 500,
  "useSpent": 2,
  "nextUseAt": 172800,
  "receipts": [
    "build-1",
    "build-2"
  ],
  "actualWorkSeconds": 540,
  "activeGadget": {
    "id": "build-2-body",
    "profile": "clamp (source worked-case d4=3; activation not tested)",
    "weightLb": 1,
    "AC": 10,
    "HP": 1,
    "createdAt": 86700,
    "expiresAt": 90300,
    "holder": "TEST-Gnome-maker",
    "activationExecuted": false
  },
  "currencyCp": 0,
  "RP": 0,
  "otherItemCharges": 2
}
```

## FT84-03-gadget-replay

A repeated build receipt does not roll or grant another body

**Scope:** SOURCE_QUALIFIED_ISOLATED_SPECIFICATION

```json
{
  "owner": "TEST-Gnome-maker",
  "partsLots": 1,
  "lotPriceCp": 500,
  "useSpent": 1,
  "nextUseAt": 86400,
  "receipts": [
    "build-1"
  ],
  "actualWorkSeconds": 300,
  "activeGadget": {
    "id": "build-1-body",
    "profile": "clamp (source worked-case d4=3; activation not tested)",
    "weightLb": 1,
    "AC": 10,
    "HP": 1,
    "createdAt": 300,
    "expiresAt": 3900,
    "holder": "TEST-Gnome-maker",
    "activationExecuted": false
  },
  "currencyCp": 0,
  "RP": 0,
  "otherItemCharges": 2
}
```

## FT84-03-gadget-custody

Actual transfer preserves identity, expiry and construction use

**Scope:** SOURCE_QUALIFIED_ISOLATED_SPECIFICATION

```json
{
  "owner": "TEST-Gnome-maker",
  "partsLots": 1,
  "lotPriceCp": 500,
  "useSpent": 1,
  "nextUseAt": 86400,
  "receipts": [
    "build-1"
  ],
  "actualWorkSeconds": 300,
  "activeGadget": {
    "id": "build-1-body",
    "profile": "clamp (source worked-case d4=3; activation not tested)",
    "weightLb": 1,
    "AC": 10,
    "HP": 1,
    "createdAt": 300,
    "expiresAt": 3900,
    "holder": "actual-recipient",
    "activationExecuted": false
  },
  "currencyCp": 0,
  "RP": 0,
  "otherItemCharges": 2
}
```

## FT84-03-gadget-missing-sourceGranted

No permission or stock generated by Craftsman

**Scope:** PREDICATE_DIAGNOSTIC_NOT_ACQUISITION_ENGINE

```json
{
  "owner": "TEST-Gnome-maker",
  "partsLots": 2,
  "lotPriceCp": 500,
  "useSpent": 0,
  "nextUseAt": 0,
  "receipts": [],
  "actualWorkSeconds": 0,
  "activeGadget": null,
  "currencyCp": 0,
  "RP": 0,
  "otherItemCharges": 2
}
```

## FT84-03-gadget-missing-gnome

No permission or stock generated by Craftsman

**Scope:** PREDICATE_DIAGNOSTIC_NOT_ACQUISITION_ENGINE

```json
{
  "owner": "TEST-Gnome-maker",
  "partsLots": 2,
  "lotPriceCp": 500,
  "useSpent": 0,
  "nextUseAt": 0,
  "receipts": [],
  "actualWorkSeconds": 0,
  "activeGadget": null,
  "currencyCp": 0,
  "RP": 0,
  "otherItemCharges": 2
}
```

## FT84-03-gadget-missing-tools

No permission or stock generated by Craftsman

**Scope:** PREDICATE_DIAGNOSTIC_NOT_ACQUISITION_ENGINE

```json
{
  "owner": "TEST-Gnome-maker",
  "partsLots": 2,
  "lotPriceCp": 500,
  "useSpent": 0,
  "nextUseAt": 0,
  "receipts": [],
  "actualWorkSeconds": 0,
  "activeGadget": null,
  "currencyCp": 0,
  "RP": 0,
  "otherItemCharges": 2
}
```

## FT84-03-gadget-missing-partsOwned

No permission or stock generated by Craftsman

**Scope:** PREDICATE_DIAGNOSTIC_NOT_ACQUISITION_ENGINE

```json
{
  "owner": "TEST-Gnome-maker",
  "partsLots": 2,
  "lotPriceCp": 500,
  "useSpent": 0,
  "nextUseAt": 0,
  "receipts": [],
  "actualWorkSeconds": 0,
  "activeGadget": null,
  "currencyCp": 0,
  "RP": 0,
  "otherItemCharges": 2
}
```

## FT84-03-gadget-missing-lawfulWork

No permission or stock generated by Craftsman

**Scope:** PREDICATE_DIAGNOSTIC_NOT_ACQUISITION_ENGINE

```json
{
  "owner": "TEST-Gnome-maker",
  "partsLots": 2,
  "lotPriceCp": 500,
  "useSpent": 0,
  "nextUseAt": 0,
  "receipts": [],
  "actualWorkSeconds": 0,
  "activeGadget": null,
  "currencyCp": 0,
  "RP": 0,
  "otherItemCharges": 2
}
```

## FT84-03-kit-success

Half-time prepared snare retains actual stock and check

**Scope:** SOURCE_QUALIFIED_ISOLATED_SPECIFICATION

```json
{
  "owner": "TEST-kit-maker",
  "cordLb": 0,
  "frameLb": 0,
  "fixtureKitNominalPriceCp": 500,
  "kits": [
    {
      "id": "kit-1",
      "type": "snare",
      "weightLb": 2,
      "armed": false,
      "setter": null
    }
  ],
  "actualWorkSeconds": 900,
  "quickPlacementUses": {
    "snare": 1,
    "caltrop": 1,
    "charge": 1
  },
  "armedSlots": {
    "snare": null,
    "caltrop": null,
    "charge": null
  },
  "hardDenialHistory": [
    "preserved-prior"
  ],
  "usableWorkSeconds": 900,
  "attemptClosed": true
}
```

## FT84-03-kit-failure

Half-time prepared snare retains actual stock and check

**Scope:** SOURCE_QUALIFIED_ISOLATED_SPECIFICATION

```json
{
  "owner": "TEST-kit-maker",
  "cordLb": 0,
  "frameLb": "1/2",
  "fixtureKitNominalPriceCp": 500,
  "kits": [],
  "actualWorkSeconds": 900,
  "quickPlacementUses": {
    "snare": 1,
    "caltrop": 1,
    "charge": 1
  },
  "armedSlots": {
    "snare": null,
    "caltrop": null,
    "charge": null
  },
  "hardDenialHistory": [
    "preserved-prior"
  ],
  "usableWorkSeconds": 900,
  "attemptClosed": true
}
```

## FT84-03-kit-interruption

Half-time prepared snare retains actual stock and check

**Scope:** SOURCE_QUALIFIED_ISOLATED_SPECIFICATION

```json
{
  "owner": "TEST-kit-maker",
  "cordLb": 0,
  "frameLb": 0,
  "fixtureKitNominalPriceCp": 500,
  "kits": [
    {
      "id": "kit-1",
      "type": "snare",
      "weightLb": 2,
      "armed": false,
      "setter": null
    }
  ],
  "actualWorkSeconds": 900,
  "quickPlacementUses": {
    "snare": 1,
    "caltrop": 1,
    "charge": 1
  },
  "armedSlots": {
    "snare": null,
    "caltrop": null,
    "charge": null
  },
  "hardDenialHistory": [
    "preserved-prior"
  ],
  "usableWorkSeconds": 900,
  "attemptClosed": true
}
```

## FT84-03-category-barricade

Actual source category controls the factor

**Scope:** CATEGORY_AND_ARITHMETIC_BOUNDARY_NOT_COMPLETE_MANUFACTURE

```json
{
  "activeMinutes": 30,
  "fixedWaitMinutes": 1440
}
```

## FT84-03-category-explicit-temper

Actual source category controls the factor

**Scope:** CATEGORY_AND_ARITHMETIC_BOUNDARY_NOT_COMPLETE_MANUFACTURE

```json
{
  "activeMinutes": 480,
  "fixedWaitMinutes": 1440
}
```

## FT84-03-category-explicit-killzone

Actual source category controls the factor

**Scope:** CATEGORY_AND_ARITHMETIC_BOUNDARY_NOT_COMPLETE_MANUFACTURE

```json
{
  "activeMinutes": 10,
  "fixedWaitMinutes": 1440
}
```

## FT84-03-category-collect-caltrops

Actual source category controls the factor

**Scope:** CATEGORY_AND_ARITHMETIC_BOUNDARY_NOT_COMPLETE_MANUFACTURE

```json
{
  "activeMinutes": 1,
  "fixedWaitMinutes": 1440
}
```

## FT84-03-category-authorized-full-repair

Actual source category controls the factor

**Scope:** CATEGORY_AND_ARITHMETIC_BOUNDARY_NOT_COMPLETE_MANUFACTURE

```json
{
  "activeMinutes": 120,
  "fixedWaitMinutes": 1440
}
```

## FT84-03-category-recipe121

Actual source category controls the factor

**Scope:** CATEGORY_AND_ARITHMETIC_BOUNDARY_NOT_COMPLETE_MANUFACTURE

```json
{
  "activeMinutes": 120,
  "fixedWaitMinutes": 1440
}
```

## FT84-03-recipe121-phases

Research and short kits do not erase actual manufacture incorporation

**Scope:** COMPLETE_WORK_LEDGER_ONLY_NO_MANUFACTURE_ROLL_OR_OUTPUT

```json
{
  "creditedSeconds": 7200,
  "actualSeconds": 9600,
  "completionCheckNowDue": true,
  "outputsAlreadyGranted": 0
}
```

## FT84-03-rest-whole-20

FA13 whole-job boundary remains unchanged

**Scope:** RETAINED_WHOLE_JOB_BOUNDARY_NOT_REST_OR_REPAIR_ENGINE

```json
{
  "HP": 7,
  "maxHP": 10,
  "charges": 1,
  "service": 4,
  "fuel": 3,
  "materialCp": 80,
  "beneficialRestGrantedByThisTest": false
}
```

## FT84-03-rest-whole-30

FA13 whole-job boundary remains unchanged

**Scope:** RETAINED_WHOLE_JOB_BOUNDARY_NOT_REST_OR_REPAIR_ENGINE

```json
{
  "HP": 7,
  "maxHP": 10,
  "charges": 1,
  "service": 4,
  "fuel": 3,
  "materialCp": 80,
  "beneficialRestGrantedByThisTest": false
}
```

## FT84-03-rest-whole-31

FA13 whole-job boundary remains unchanged

**Scope:** RETAINED_WHOLE_JOB_BOUNDARY_NOT_REST_OR_REPAIR_ENGINE

```json
{
  "HP": 4,
  "maxHP": 10,
  "charges": 1,
  "service": 4,
  "fuel": 3,
  "materialCp": 80,
  "beneficialRestGrantedByThisTest": false
}
```

## FT84-03-rest-whole-480

FA13 whole-job boundary remains unchanged

**Scope:** RETAINED_WHOLE_JOB_BOUNDARY_NOT_REST_OR_REPAIR_ENGINE

```json
{
  "HP": 4,
  "maxHP": 10,
  "charges": 1,
  "service": 4,
  "fuel": 3,
  "materialCp": 80,
  "beneficialRestGrantedByThisTest": false
}
```

