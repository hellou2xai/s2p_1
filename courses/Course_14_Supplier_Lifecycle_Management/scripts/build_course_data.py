"""Generate the practice data set for Course 14: Supplier Lifecycle Management.

Scenario: Crestview Industries, US-based manufacturer with $38.6M in annual
supplier spend across 30 suppliers. The Supplier Relationship Manager (the
student) builds a Claude Code system that tracks every supplier from
onboarding to exit.

Produces, under practice/:
  Master/supplier-master.csv          (30 suppliers, read-only source)
  Master/performance-history.csv      (120 rows, 4 quarters)
  Master/compliance-status.csv        (30 rows)
  Master/development-plans.csv        (10 active plans)
  Master/open-orders.csv              (active POs, used in Lesson 5)
  Master/Onboarding_Checklist_Template.docx
  Master/Heartland_Polymers_Dev_Plan.docx
  Master/CAP_Template.docx
  Drafts/                             (empty; lessons write working files here)
  Outputs/                            (empty; lessons write final files here)
  state/                              (empty; Lesson 6 populates it at runtime)
  skills/assess-lifecycle-stage.md
  skills/detect-risk-triggers.md
  .claude/settings.json
  .claude/commands/lifecycle-status.md
  .claude/commands/onboard-supplier.md
  .claude/commands/trigger-exit.md

Folder convention (matches the lessons):
  Master/   read-only source data and templates
  Drafts/   working files the student creates during a lesson
  Outputs/  signed-off final files

Deterministic: all values are hardcoded. No random.seed reliance.
All currency USD, US geography, US dates (YYYY-MM-DD in data, MM/DD/YYYY in prose).
"""

from __future__ import annotations

import csv
import json
import shutil
from datetime import date
from pathlib import Path

from docx import Document

ROOT = Path(__file__).resolve().parent.parent
PRACTICE = ROOT / "practice"
TODAY = date(2026, 4, 25)


# 30 suppliers. Tuple shape:
#   (supplier_id, supplier_name, category, tier, lifecycle_stage,
#    annual_spend_usd, onboard_date, last_review_date, risk_tier, region)
# Stage distribution (matches COURSE_OVERVIEW.md):
#   3 onboarding, 15 active, 3 strategic, 3 at_risk,
#   2 corrective_action, 2 exit, 2 under_review
# Apex Electronics (SUP004) annual spend = $1,200,000 (matches Lesson 4 text).
SUPPLIERS = [
    ("SUP001", "Great Lakes Steel", "raw-materials", "strategic", "active",
     4200000, "2019-03-12", "2026-01-15", "low", "Midwest"),
    ("SUP002", "Heartland Polymers", "raw-materials", "strategic", "strategic",
     3800000, "2018-07-22", "2026-02-10", "low", "Midwest"),
    ("SUP003", "Pacific Aluminum", "raw-materials", "preferred", "active",
     3100000, "2020-05-08", "2026-01-22", "low", "West"),
    ("SUP004", "Apex Electronics", "components", "preferred", "at_risk",
     1200000, "2021-02-14", "2026-03-05", "high", "Northeast"),
    ("SUP005", "Cascade Fasteners", "components", "approved", "active",
     1800000, "2020-11-03", "2026-01-30", "low", "West"),
    ("SUP006", "Continental Freight", "logistics", "strategic", "strategic",
     3600000, "2017-09-19", "2026-02-18", "low", "Midwest"),
    ("SUP007", "Patriot Logistics", "logistics", "preferred", "active",
     2900000, "2019-06-25", "2026-02-02", "low", "Southeast"),
    ("SUP008", "Eagle Transport", "logistics", "preferred", "active",
     2100000, "2020-08-11", "2026-01-19", "medium", "Midwest"),
    ("SUP009", "Horizon Carriers", "logistics", "approved", "active",
     1700000, "2021-04-30", "2026-02-25", "low", "South"),
    ("SUP010", "Coastal Coatings", "components", "preferred", "under_review",
     1500000, "2019-12-04", "2026-03-01", "medium", "Southeast"),
    ("SUP011", "TechForward Solutions", "it-services", "strategic", "strategic",
     2800000, "2018-03-17", "2026-02-12", "low", "West"),
    ("SUP012", "CloudBridge Systems", "it-services", "preferred", "active",
     2500000, "2019-10-09", "2026-01-28", "low", "West"),
    ("SUP013", "Nexus IT Services", "it-services", "preferred", "at_risk",
     1900000, "2020-06-21", "2026-03-08", "high", "Northeast"),
    ("SUP014", "Pinnacle Software", "it-services", "approved", "active",
     1500000, "2021-01-15", "2026-02-05", "low", "West"),
    ("SUP015", "Frontier Machining", "components", "approved", "corrective_action",
     480000, "2020-09-28", "2026-03-26", "high", "Midwest"),
    ("SUP016", "National Facilities", "facilities", "strategic", "active",
     2200000, "2018-11-12", "2026-01-25", "low", "South"),
    ("SUP017", "Metro Building Svcs", "facilities", "preferred", "active",
     1800000, "2019-04-08", "2026-02-08", "low", "Northeast"),
    ("SUP018", "Whitfield Consulting", "professional-services", "strategic", "active",
     2600000, "2018-08-30", "2026-01-31", "low", "Northeast"),
    ("SUP019", "Sterling Advisory", "professional-services", "preferred", "active",
     2100000, "2020-02-19", "2026-02-15", "low", "Midwest"),
    ("SUP020", "Meridian Legal", "professional-services", "preferred", "active",
     1600000, "2019-07-14", "2026-02-20", "low", "Northeast"),
    ("SUP021", "Crestline Accounting", "professional-services", "approved", "active",
     1200000, "2021-05-26", "2026-02-22", "low", "Midwest"),
    ("SUP022", "Catalyst Training", "professional-services", "approved", "active",
     700000, "2022-03-11", "2026-03-12", "low", "West"),
    ("SUP023", "Regional Supply Co", "mro-supplies", "approved", "exit",
     280000, "2017-10-04", "2026-02-14", "high", "South"),
    ("SUP024", "Heritage Painting", "facilities", "approved", "exit",
     210000, "2020-01-22", "2026-02-28", "high", "Southeast"),
    ("SUP025", "Summit Electrical", "components", "approved", "onboarding",
     400000, "2026-02-05", "2026-04-10", "medium", "Midwest"),
    ("SUP026", "Greenfield Maintenance", "facilities", "approved", "onboarding",
     350000, "2026-02-20", "2026-04-12", "medium", "Northeast"),
    ("SUP027", "Agile Platforms", "it-services", "approved", "onboarding",
     200000, "2026-03-08", "2026-04-15", "medium", "West"),
    ("SUP028", "Midland Packaging", "packaging", "approved", "at_risk",
     320000, "2021-03-19", "2026-03-15", "high", "Midwest"),
    ("SUP029", "Ironside Recruiting", "professional-services", "approved", "corrective_action",
     380000, "2020-12-05", "2026-03-22", "high", "Northeast"),
    ("SUP030", "Precision Plumbing", "facilities", "approved", "under_review",
     420000, "2019-08-17", "2026-02-26", "medium", "South"),
]


# Performance scores, hardcoded by stage. Each supplier gets 4 quarters.
# Quarter labels follow the lesson convention: "Q3 2025" (not "2025-Q3").
# Lessons reference specific values, so use them exactly:
#   Apex Electronics: Q3 2025 = 84, Q4 2025 = 66 (drop of 18)
#   Frontier Machining: Q3 2025 = 71, Q4 2025 = 69 (small drop, CAP open)
#   Heartland Polymers: stable around 91, with delivery 87 to 93%, defect from 2.1% to 1.4%
#   Great Lakes Steel: stable around 79
#   Midland Packaging: drop of 13 in Q3-Q4
PERFORMANCE = {
    # supplier_id: [(quarter, quality, delivery, responsiveness, cost, overall), x4]
    "SUP001": [  # Great Lakes Steel: stable
        ("Q2 2025", 79, 81, 78, 77, 79),
        ("Q3 2025", 80, 79, 79, 78, 79),
        ("Q4 2025", 78, 80, 80, 79, 79),
        ("Q1 2026", 81, 80, 79, 78, 80),
    ],
    "SUP002": [  # Heartland Polymers: strategic, improving
        ("Q2 2025", 88, 85, 90, 86, 87),
        ("Q3 2025", 90, 91, 92, 88, 90),
        ("Q4 2025", 92, 93, 93, 89, 92),
        ("Q1 2026", 93, 94, 94, 90, 93),
    ],
    "SUP003": [  # Pacific Aluminum
        ("Q2 2025", 75, 78, 76, 80, 77),
        ("Q3 2025", 78, 79, 78, 79, 78),
        ("Q4 2025", 80, 81, 79, 78, 80),
        ("Q1 2026", 81, 80, 80, 79, 80),
    ],
    "SUP004": [  # Apex Electronics: AT RISK, drops 18 pts Q3 to Q4
        ("Q2 2025", 86, 84, 85, 82, 84),
        ("Q3 2025", 85, 83, 86, 82, 84),
        ("Q4 2025", 64, 68, 67, 65, 66),
        ("Q1 2026", 65, 66, 68, 64, 66),
    ],
    "SUP005": [  # Cascade Fasteners: stable
        ("Q2 2025", 76, 77, 75, 78, 77),
        ("Q3 2025", 77, 78, 76, 77, 77),
        ("Q4 2025", 78, 77, 77, 78, 78),
        ("Q1 2026", 79, 78, 78, 77, 78),
    ],
    "SUP006": [  # Continental Freight: strategic
        ("Q2 2025", 86, 88, 89, 84, 87),
        ("Q3 2025", 88, 89, 90, 85, 88),
        ("Q4 2025", 90, 91, 91, 86, 90),
        ("Q1 2026", 91, 92, 92, 87, 91),
    ],
    "SUP007": [  # Patriot Logistics
        ("Q2 2025", 78, 80, 79, 77, 79),
        ("Q3 2025", 79, 81, 80, 78, 80),
        ("Q4 2025", 80, 82, 81, 78, 80),
        ("Q1 2026", 81, 82, 81, 79, 81),
    ],
    "SUP008": [  # Eagle Transport
        ("Q2 2025", 73, 75, 74, 76, 75),
        ("Q3 2025", 74, 76, 75, 76, 75),
        ("Q4 2025", 75, 76, 75, 75, 75),
        ("Q1 2026", 76, 77, 76, 75, 76),
    ],
    "SUP009": [  # Horizon Carriers
        ("Q2 2025", 70, 72, 71, 73, 72),
        ("Q3 2025", 71, 73, 72, 72, 72),
        ("Q4 2025", 72, 73, 72, 72, 72),
        ("Q1 2026", 73, 74, 73, 72, 73),
    ],
    "SUP010": [  # Coastal Coatings: under review, audit pending
        ("Q2 2025", 71, 70, 73, 72, 72),
        ("Q3 2025", 70, 69, 72, 71, 71),
        ("Q4 2025", 70, 70, 71, 71, 71),
        ("Q1 2026", 70, 70, 71, 71, 71),
    ],
    "SUP011": [  # TechForward Solutions: strategic
        ("Q2 2025", 87, 86, 88, 84, 86),
        ("Q3 2025", 89, 88, 90, 85, 88),
        ("Q4 2025", 91, 90, 91, 86, 90),
        ("Q1 2026", 92, 91, 92, 87, 91),
    ],
    "SUP012": [  # CloudBridge Systems
        ("Q2 2025", 80, 81, 82, 78, 80),
        ("Q3 2025", 81, 82, 83, 79, 81),
        ("Q4 2025", 82, 83, 83, 79, 82),
        ("Q1 2026", 83, 83, 84, 80, 83),
    ],
    "SUP013": [  # Nexus IT Services: AT RISK
        ("Q2 2025", 74, 76, 75, 73, 75),
        ("Q3 2025", 73, 74, 74, 72, 73),
        ("Q4 2025", 60, 61, 63, 60, 61),
        ("Q1 2026", 60, 60, 62, 59, 60),
    ],
    "SUP014": [  # Pinnacle Software
        ("Q2 2025", 76, 77, 78, 75, 76),
        ("Q3 2025", 77, 78, 78, 75, 77),
        ("Q4 2025", 78, 78, 79, 76, 78),
        ("Q1 2026", 79, 79, 80, 76, 79),
    ],
    "SUP015": [  # Frontier Machining: corrective action open, small Q3-Q4 drop
        ("Q2 2025", 72, 70, 73, 71, 72),
        ("Q3 2025", 71, 69, 72, 70, 71),
        ("Q4 2025", 69, 67, 71, 69, 69),
        ("Q1 2026", 70, 68, 71, 69, 70),
    ],
    "SUP016": [  # National Facilities
        ("Q2 2025", 81, 83, 82, 79, 81),
        ("Q3 2025", 82, 84, 83, 80, 82),
        ("Q4 2025", 83, 84, 84, 80, 83),
        ("Q1 2026", 83, 85, 84, 81, 84),
    ],
    "SUP017": [  # Metro Building Svcs
        ("Q2 2025", 75, 76, 75, 77, 76),
        ("Q3 2025", 76, 77, 76, 77, 76),
        ("Q4 2025", 77, 77, 77, 77, 77),
        ("Q1 2026", 77, 78, 77, 76, 77),
    ],
    "SUP018": [  # Whitfield Consulting
        ("Q2 2025", 84, 83, 85, 80, 83),
        ("Q3 2025", 85, 84, 86, 81, 84),
        ("Q4 2025", 85, 84, 86, 81, 84),
        ("Q1 2026", 86, 85, 86, 82, 85),
    ],
    "SUP019": [  # Sterling Advisory
        ("Q2 2025", 78, 79, 80, 76, 78),
        ("Q3 2025", 79, 80, 81, 77, 79),
        ("Q4 2025", 80, 80, 81, 77, 80),
        ("Q1 2026", 81, 81, 82, 78, 81),
    ],
    "SUP020": [  # Meridian Legal
        ("Q2 2025", 76, 77, 78, 75, 77),
        ("Q3 2025", 77, 78, 78, 75, 77),
        ("Q4 2025", 78, 78, 79, 76, 78),
        ("Q1 2026", 78, 79, 79, 76, 78),
    ],
    "SUP021": [  # Crestline Accounting
        ("Q2 2025", 73, 74, 75, 73, 74),
        ("Q3 2025", 74, 75, 75, 74, 75),
        ("Q4 2025", 75, 75, 76, 74, 75),
        ("Q1 2026", 76, 76, 76, 74, 76),
    ],
    "SUP022": [  # Catalyst Training
        ("Q2 2025", 71, 72, 73, 70, 72),
        ("Q3 2025", 72, 73, 73, 71, 72),
        ("Q4 2025", 73, 73, 74, 71, 73),
        ("Q1 2026", 73, 74, 74, 72, 73),
    ],
    "SUP023": [  # Regional Supply Co: exit, declining
        ("Q2 2025", 65, 64, 66, 67, 66),
        ("Q3 2025", 63, 62, 64, 65, 64),
        ("Q4 2025", 60, 60, 62, 64, 62),
        ("Q1 2026", 58, 59, 61, 63, 60),
    ],
    "SUP024": [  # Heritage Painting: exit
        ("Q2 2025", 62, 64, 63, 65, 64),
        ("Q3 2025", 60, 62, 62, 64, 62),
        ("Q4 2025", 58, 60, 60, 63, 60),
        ("Q1 2026", 56, 58, 59, 62, 59),
    ],
    "SUP025": [  # Summit Electrical: onboarding (limited history)
        ("Q2 2025", 0, 0, 0, 0, 0),
        ("Q3 2025", 0, 0, 0, 0, 0),
        ("Q4 2025", 0, 0, 0, 0, 0),
        ("Q1 2026", 75, 76, 78, 74, 76),
    ],
    "SUP026": [  # Greenfield Maintenance: onboarding
        ("Q2 2025", 0, 0, 0, 0, 0),
        ("Q3 2025", 0, 0, 0, 0, 0),
        ("Q4 2025", 0, 0, 0, 0, 0),
        ("Q1 2026", 72, 74, 75, 73, 74),
    ],
    "SUP027": [  # Agile Platforms: onboarding
        ("Q2 2025", 0, 0, 0, 0, 0),
        ("Q3 2025", 0, 0, 0, 0, 0),
        ("Q4 2025", 0, 0, 0, 0, 0),
        ("Q1 2026", 73, 75, 76, 74, 75),
    ],
    "SUP028": [  # Midland Packaging: AT RISK, drop of 13 Q3 to Q4
        ("Q2 2025", 78, 76, 77, 75, 77),
        ("Q3 2025", 77, 76, 78, 75, 77),
        ("Q4 2025", 64, 63, 65, 62, 64),
        ("Q1 2026", 63, 62, 64, 61, 63),
    ],
    "SUP029": [  # Ironside Recruiting: corrective_action
        ("Q2 2025", 68, 70, 69, 71, 70),
        ("Q3 2025", 67, 68, 68, 70, 68),
        ("Q4 2025", 65, 66, 66, 69, 67),
        ("Q1 2026", 66, 67, 67, 69, 67),
    ],
    "SUP030": [  # Precision Plumbing: under_review
        ("Q2 2025", 72, 73, 74, 70, 72),
        ("Q3 2025", 72, 73, 73, 71, 72),
        ("Q4 2025", 71, 72, 73, 71, 72),
        ("Q1 2026", 72, 72, 73, 71, 72),
    ],
}


# Compliance fields per supplier. Lessons reference these onboarding documents
# (Lesson 2 worked example):
#   W-9, NDA (legacy field, kept implicitly via Quality Agreement and
#   Code of Conduct), Certificate of Insurance (COI), ACH banking form,
#   Supplier Code of Conduct acknowledgment, and Quality Agreement signature.
#
# We model each as one of: Received, Pending, Expired, "" (blank = never sent).
# Values mirror the original CSV's intent:
#   - active/strategic suppliers: all Received
#   - onboarding suppliers (Summit Electrical, Greenfield, Agile): mix of
#     Pending and blank, matching the original "missing" gaps
#   - at_risk and corrective_action suppliers: a couple Pending or Expired
#   - exit suppliers (Regional Supply Co, Heritage Painting): Expired insurance
#
# Summit Electrical (SUP025) row matches Lesson 2 Step 4: W-9 Received,
# NDA Received (mapped to Code of Conduct here), COI blank, ACH blank,
# Code of Conduct Pending, Quality Agreement blank, Last_Review_Date blank.
COMPLIANCE = {
    # supplier_id: (W9, COI, ACH_Banking_Form, Code_of_Conduct,
    #               Quality_Agreement, Last_Review_Date)
    "SUP001": ("Received", "Received", "Received", "Received", "Received", "2026-01-15"),
    "SUP002": ("Received", "Received", "Received", "Received", "Received", "2026-02-10"),
    "SUP003": ("Received", "Received", "Received", "Received", "Received", "2026-01-22"),
    "SUP004": ("Received", "Received", "Received", "Received", "Received", "2026-03-05"),
    "SUP005": ("Received", "Received", "Received", "Received", "Received", "2026-01-30"),
    "SUP006": ("Received", "Received", "Received", "Received", "Received", "2026-02-18"),
    "SUP007": ("Received", "Received", "Received", "Received", "Received", "2026-02-02"),
    "SUP008": ("Received", "Received", "Received", "Received", "Received", "2026-01-19"),
    "SUP009": ("Received", "Received", "Received", "Received", "Received", "2026-02-25"),
    "SUP010": ("Received", "Received", "Received", "Received", "Pending", "2026-03-01"),
    "SUP011": ("Received", "Received", "Received", "Received", "Received", "2026-02-12"),
    "SUP012": ("Received", "Received", "Received", "Received", "Received", "2026-01-28"),
    "SUP013": ("Received", "Received", "Received", "Received", "Expired", "2026-03-08"),
    "SUP014": ("Received", "Received", "Received", "Received", "Received", "2026-02-05"),
    "SUP015": ("Received", "Expired", "Received", "Received", "Pending", "2026-03-26"),
    "SUP016": ("Received", "Received", "Received", "Received", "Received", "2026-01-25"),
    "SUP017": ("Received", "Received", "Received", "Received", "Received", "2026-02-08"),
    "SUP018": ("Received", "Received", "Received", "Received", "Received", "2026-01-31"),
    "SUP019": ("Received", "Received", "Received", "Received", "Received", "2026-02-15"),
    "SUP020": ("Received", "Received", "Received", "Received", "Received", "2026-02-20"),
    "SUP021": ("Received", "Received", "Received", "Received", "Received", "2026-02-22"),
    "SUP022": ("Received", "Received", "Received", "Received", "Received", "2026-03-12"),
    "SUP023": ("Received", "Expired", "Received", "Received", "Expired", "2026-02-14"),
    "SUP024": ("Received", "Expired", "Received", "Pending", "Expired", "2026-02-28"),
    "SUP025": ("Received", "", "", "Pending", "", ""),  # Summit Electrical: gaps
    "SUP026": ("Received", "Pending", "Received", "Pending", "", "2026-03-15"),
    "SUP027": ("Received", "Received", "Pending", "Pending", "", "2026-03-22"),
    "SUP028": ("Received", "Received", "Received", "Received", "Pending", "2026-03-15"),
    "SUP029": ("Received", "Pending", "Received", "Received", "Expired", "2026-03-22"),
    "SUP030": ("Received", "Received", "Received", "Received", "Pending", "2026-02-26"),
}


# 10 active development plans. Heartland Polymers (SUP002) row referenced by
# Lesson 3: targets include delivery on-time rate 87% to 94%, defect rate
# 2.1% to below 1.0%, supplier portal adoption 40% to 100%. Review_Date 2026-05-08.
DEV_PLANS = [
    ("SUP002", "Heartland Polymers", "growth",
     "Delivery on-time 87% to 94%, defect rate 2.1% to below 1.0%, portal adoption 40% to 100%",
     "on_track", "2026-01-08", "2026-05-08"),
    ("SUP006", "Continental Freight", "capability",
     "Reduce average transit time from 4.2 to 3.5 days by Q4 2026",
     "on_track", "2026-02-12", "2026-06-15"),
    ("SUP011", "TechForward Solutions", "innovation",
     "Launch joint AI-driven inventory pilot by Q3 2026",
     "on_track", "2026-01-22", "2026-05-20"),
    ("SUP001", "Great Lakes Steel", "capability",
     "Achieve ISO 14001 certification by Q3 2026",
     "behind", "2026-02-05", "2026-05-15"),
    ("SUP003", "Pacific Aluminum", "growth",
     "Increase capacity by 20% by Q4 2026",
     "on_track", "2026-01-30", "2026-06-30"),
    ("SUP016", "National Facilities", "capability",
     "Consolidate 3 regional contracts into 1 MSA by Q4 2026",
     "on_track", "2026-02-18", "2026-07-10"),
    ("SUP018", "Whitfield Consulting", "growth",
     "Reduce engagement lead time from 14 to 10 days by Q2 2026",
     "completed", "2026-01-15", "2026-05-25"),
    ("SUP012", "CloudBridge Systems", "innovation",
     "Migrate Crestview workloads to multi-region failover by Q3 2026",
     "on_track", "2026-02-22", "2026-06-05"),
    ("SUP019", "Sterling Advisory", "capability",
     "Add 2 senior consultants with manufacturing experience by Q3 2026",
     "behind", "2026-02-10", "2026-05-30"),
    ("SUP007", "Patriot Logistics", "growth",
     "Expand cold chain capability to 3 new lanes by Q4 2026",
     "on_track", "2026-01-28", "2026-06-20"),
]


# Open POs for Lesson 5. Regional Supply Co has exactly three open POs totaling $48,000.
OPEN_ORDERS = [
    # PO_Number, Supplier_Name, Amount_USD, Delivery_Date, Status
    ("PO-4412", "Regional Supply Co", 18000, "2026-05-02", "Open"),
    ("PO-4487", "Regional Supply Co", 22000, "2026-05-10", "Open"),
    ("PO-4501", "Regional Supply Co", 8000, "2026-05-14", "Open"),
    ("PO-4520", "Great Lakes Steel", 145000, "2026-05-20", "Open"),
    ("PO-4521", "Heartland Polymers", 92000, "2026-05-08", "Open"),
    ("PO-4522", "Pacific Aluminum", 68000, "2026-05-12", "Open"),
    ("PO-4523", "Apex Electronics", 56000, "2026-05-15", "Open"),
    ("PO-4524", "Continental Freight", 48000, "2026-05-18", "Open"),
    ("PO-4525", "Cascade Fasteners", 32000, "2026-05-22", "Open"),
    ("PO-4526", "Eagle Transport", 28000, "2026-05-25", "Open"),
    ("PO-4527", "Frontier Machining", 18000, "2026-05-09", "Open"),
    ("PO-4528", "Heritage Painting", 12000, "2026-05-30", "Open"),
    ("PO-4529", "Midland Packaging", 14000, "2026-05-11", "Open"),
    ("PO-4530", "TechForward Solutions", 75000, "2026-06-01", "Open"),
    ("PO-4380", "Regional Supply Co", 9500, "2026-04-10", "Closed"),
    ("PO-4395", "Regional Supply Co", 11200, "2026-04-15", "Closed"),
]


def write_csv(path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(fieldnames)
        w.writerows(rows)
    print(f"  {path.relative_to(PRACTICE)}: {len(rows)} rows")


def build_supplier_master(path):
    rows = [list(s) for s in SUPPLIERS]
    fieldnames = [
        "Supplier_ID", "Supplier_Name", "Category", "Tier", "Lifecycle_Stage",
        "Annual_Spend_USD", "Onboarded_Date", "Last_Review_Date", "Risk_Tier", "Region",
    ]
    write_csv(path, fieldnames, rows)


def build_performance_history(path):
    rows = []
    name_lookup = {s[0]: s[1] for s in SUPPLIERS}
    for sid, scores in PERFORMANCE.items():
        name = name_lookup[sid]
        for q, qual, deliv, resp, cost, overall in scores:
            rows.append([sid, name, q, qual, deliv, resp, cost, overall])
    fieldnames = [
        "Supplier_ID", "Supplier_Name", "Quarter",
        "Quality_Score", "Delivery_Score", "Responsiveness_Score",
        "Cost_Score", "Overall_Score",
    ]
    write_csv(path, fieldnames, rows)


def build_compliance_status(path):
    rows = []
    name_lookup = {s[0]: s[1] for s in SUPPLIERS}
    for sid, fields in COMPLIANCE.items():
        w9, coi, ach, coc, qa, last = fields
        rows.append([sid, name_lookup[sid], w9, coi, ach, coc, qa, last])
    fieldnames = [
        "Supplier_ID", "Supplier_Name", "W9", "COI", "ACH_Banking_Form",
        "Code_of_Conduct", "Quality_Agreement", "Last_Review_Date",
    ]
    write_csv(path, fieldnames, rows)


def build_development_plans(path):
    fieldnames = [
        "Supplier_ID", "Supplier_Name", "Plan_Type", "Target",
        "Status", "Plan_Start_Date", "Review_Date",
    ]
    rows = [list(p) for p in DEV_PLANS]
    write_csv(path, fieldnames, rows)


def build_open_orders(path):
    fieldnames = ["PO_Number", "Supplier_Name", "Amount_USD", "Delivery_Date", "Status"]
    rows = [list(o) for o in OPEN_ORDERS]
    write_csv(path, fieldnames, rows)


def build_onboarding_template(path):
    """Crestview's standard 12-item onboarding checklist."""
    doc = Document()
    doc.add_heading("Crestview Industries Supplier Onboarding Checklist", level=1)
    doc.add_paragraph(
        "Standard 12-item onboarding checklist. Complete every item before moving "
        "the supplier from Onboarding to Active status. Owner: Supplier Relationship Manager."
    )
    doc.add_heading("Supplier Information", level=2)
    info = doc.add_table(rows=4, cols=2)
    info.style = "Light Grid Accent 1"
    info.cell(0, 0).text = "Supplier Name"
    info.cell(0, 1).text = "[Supplier Name]"
    info.cell(1, 0).text = "Supplier ID"
    info.cell(1, 1).text = "[SUP-NNN]"
    info.cell(2, 0).text = "Category"
    info.cell(2, 1).text = "[Category]"
    info.cell(3, 0).text = "Onboarding Start Date"
    info.cell(3, 1).text = "[YYYY-MM-DD]"

    doc.add_heading("Checklist Items", level=2)
    items = [
        ("1", "W-9 Tax Form", "Received signed W-9 with current EIN."),
        ("2", "Non-Disclosure Agreement (NDA)", "Mutual NDA executed and on file."),
        ("3", "Certificate of Insurance (COI)", "General liability $2M, auto $1M, workers comp."),
        ("4", "ACH Banking Form", "Bank account, routing number, voided check."),
        ("5", "Supplier Code of Conduct Acknowledgment", "Signed acknowledgment of Crestview Code of Conduct."),
        ("6", "Quality Agreement Signature", "Signed quality agreement (for components and raw materials)."),
        ("7", "ISO 9001 or Equivalent", "ISO certificate or equivalent quality system documentation."),
        ("8", "Financial Review", "Dun and Bradstreet report or equivalent. Score above 70."),
        ("9", "Background Check", "Beneficial owner background screening complete."),
        ("10", "Sanctions and Watchlist Screening", "OFAC, EU, and UK list screening clear."),
        ("11", "Diversity Certification (if applicable)", "MBE, WBE, VBE, or other certification on file."),
        ("12", "First Order Test", "Test PO placed and delivery accepted."),
    ]
    table = doc.add_table(rows=len(items) + 1, cols=4)
    table.style = "Light Grid Accent 1"
    table.cell(0, 0).text = "#"
    table.cell(0, 1).text = "Checklist Item"
    table.cell(0, 2).text = "Description"
    table.cell(0, 3).text = "Status"
    for i, (num, item, desc) in enumerate(items, start=1):
        table.cell(i, 0).text = num
        table.cell(i, 1).text = item
        table.cell(i, 2).text = desc
        table.cell(i, 3).text = ""

    doc.add_heading("Sign-off", level=2)
    doc.add_paragraph(
        "Supplier Relationship Manager: ________________________   Date: ____________\n"
        "Director of Procurement: ________________________________   Date: ____________"
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(path))
    print(f"  {path.relative_to(PRACTICE)}")


def build_heartland_dev_plan(path):
    """Heartland Polymers development plan, referenced by Lesson 3."""
    doc = Document()
    doc.add_heading("Heartland Polymers: Strategic Development Plan", level=1)
    doc.add_paragraph(
        "Effective Date: 2026-01-08. Next Review: 2026-05-08. Plan Owner: "
        "Supplier Relationship Manager, Crestview Industries."
    )

    doc.add_heading("Background", level=2)
    doc.add_paragraph(
        "Heartland Polymers is a strategic supplier in the raw materials category, "
        "with annual spend of $3.8M. Performance has been strong, with overall scores "
        "consistently above 87. This development plan tracks three growth targets "
        "agreed at the January 2026 strategic review."
    )

    doc.add_heading("Improvement Targets", level=2)
    targets = doc.add_table(rows=4, cols=3)
    targets.style = "Light Grid Accent 1"
    targets.cell(0, 0).text = "Target"
    targets.cell(0, 1).text = "Goal"
    targets.cell(0, 2).text = "Deadline"
    targets.cell(1, 0).text = "Delivery on-time rate"
    targets.cell(1, 1).text = "Increase from 87% to 94%"
    targets.cell(1, 2).text = "2026-06-30"
    targets.cell(2, 0).text = "Defect rate"
    targets.cell(2, 1).text = "Reduce from 2.1% to below 1.0%"
    targets.cell(2, 2).text = "2026-09-30"
    targets.cell(3, 0).text = "Supplier portal adoption"
    targets.cell(3, 1).text = "Increase from 40% to 100%"
    targets.cell(3, 2).text = "2026-09-30"

    doc.add_heading("Milestones", level=2)
    milestones = doc.add_table(rows=5, cols=3)
    milestones.style = "Light Grid Accent 1"
    milestones.cell(0, 0).text = "Milestone"
    milestones.cell(0, 1).text = "Target Date"
    milestones.cell(0, 2).text = "Status"
    milestones.cell(1, 0).text = "Joint quality review and root cause workshop"
    milestones.cell(1, 1).text = "2026-02-15"
    milestones.cell(1, 2).text = "Complete"
    milestones.cell(2, 0).text = "Portal training for 100% of Heartland sales staff"
    milestones.cell(2, 1).text = "2026-04-01"
    milestones.cell(2, 2).text = "Complete"
    milestones.cell(3, 0).text = "Mid-year review"
    milestones.cell(3, 1).text = "2026-05-08"
    milestones.cell(3, 2).text = "Pending"
    milestones.cell(4, 0).text = "Defect rate validation in incoming inspection"
    milestones.cell(4, 1).text = "2026-08-01"
    milestones.cell(4, 2).text = "Pending"

    doc.add_heading("Quarterly Check-In Notes", level=2)
    doc.add_paragraph(
        "Q4 2025: Delivery on-time rate at 91%. Defect rate at 1.6%. Portal adoption at 55%."
    )
    doc.add_paragraph(
        "Q1 2026: Delivery on-time rate at 93%. Defect rate at 1.4%. Portal adoption at 72%."
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(path))
    print(f"  {path.relative_to(PRACTICE)}")


def build_cap_template(path):
    """Crestview standard CAP template referenced by Lesson 4."""
    doc = Document()
    doc.add_heading("Crestview Industries Corrective Action Plan (CAP)", level=1)
    doc.add_paragraph(
        "Standard template. Issue this CAP when a supplier's performance score drops "
        "10 or more points across two consecutive quarters, or when a critical compliance "
        "or quality incident is documented."
    )

    doc.add_heading("Supplier Details", level=2)
    sup = doc.add_table(rows=5, cols=2)
    sup.style = "Light Grid Accent 1"
    sup.cell(0, 0).text = "Supplier Name"
    sup.cell(0, 1).text = "[Supplier Name]"
    sup.cell(1, 0).text = "Supplier ID"
    sup.cell(1, 1).text = "[SUP-NNN]"
    sup.cell(2, 0).text = "Category"
    sup.cell(2, 1).text = "[Category]"
    sup.cell(3, 0).text = "Annual Spend"
    sup.cell(3, 1).text = "[$Amount USD]"
    sup.cell(4, 0).text = "CAP Issue Date"
    sup.cell(4, 1).text = "[YYYY-MM-DD]"

    doc.add_heading("Incident Summary", level=2)
    doc.add_paragraph(
        "[Describe the performance drop or incident. Include quarterly scores, "
        "the specific dimensions affected (quality, delivery, responsiveness, cost), "
        "and the spend impact.]"
    )

    doc.add_heading("Root Cause", level=2)
    doc.add_paragraph(
        "[Root Cause TBC. To be completed by supplier within 14 days of CAP issue.]"
    )

    doc.add_heading("Required Actions", level=2)
    actions = doc.add_table(rows=4, cols=3)
    actions.style = "Light Grid Accent 1"
    actions.cell(0, 0).text = "#"
    actions.cell(0, 1).text = "Action"
    actions.cell(0, 2).text = "Deadline"
    actions.cell(1, 0).text = "1"
    actions.cell(1, 1).text = "Submit root cause analysis"
    actions.cell(1, 2).text = "[YYYY-MM-DD]"
    actions.cell(2, 0).text = "2"
    actions.cell(2, 1).text = "Submit corrective action response"
    actions.cell(2, 2).text = "[YYYY-MM-DD]"
    actions.cell(3, 0).text = "3"
    actions.cell(3, 1).text = "Achieve target performance score"
    actions.cell(3, 2).text = "[Target Quarter]"

    doc.add_heading("Sign-off", level=2)
    doc.add_paragraph(
        "Plan Issued By: Supplier Relationship Manager, Crestview Industries\n"
        "Issue Date: [YYYY-MM-DD]\n"
        "Supplier Acknowledgment: ________________________   Date: ____________"
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(path))
    print(f"  {path.relative_to(PRACTICE)}")


def build_skills(skills_dir):
    skills_dir.mkdir(parents=True, exist_ok=True)

    assess = """# Skill: Assess Lifecycle Stage

Use this skill when classifying any Crestview Industries supplier into one of the seven lifecycle stages.

## Inputs

- `Master/supplier-master.csv` (Lifecycle_Stage column, Onboarded_Date, Last_Review_Date)
- `Master/performance-history.csv` (4 quarters of Overall_Score)
- `Master/compliance-status.csv` (W9, COI, ACH_Banking_Form, Code_of_Conduct, Quality_Agreement)
- `Master/development-plans.csv` (active plan flag)

## Stage rules, in order

Apply the rules from top to bottom. Stop at the first match.

1. **Exit.** Lifecycle_Stage in supplier-master is `exit`, or supplier_master shows an exit flag with an off-boarding date.
2. **Corrective Action.** Lifecycle_Stage is `corrective_action`, or an open CAP exists.
3. **Under Review.** Lifecycle_Stage is `under_review`, or an audit is pending, or a stage dispute is unresolved.
4. **At Risk.** Overall_Score dropped 10 or more points between Q3 2025 and Q4 2025, or any compliance field is Expired.
5. **Onboarding.** Onboarded_Date within last 90 days from today (2026-04-25), or any compliance field is blank or Pending.
6. **Strategic.** Active development plan on file, Tier is `strategic`, and Overall_Score above 85 for the last 3 quarters.
7. **Active.** All compliance fields Received, no open issues, Overall_Score above 60.

## Output

A row per supplier with: Supplier_Name, Stage, Reason. Save to `Outputs/segmentation-report.md` or to `Drafts/Supplier_Segmentation_v1.csv`, depending on the calling lesson.
"""

    detect = """# Skill: Detect Risk Triggers

Use this skill to find suppliers whose performance is sliding toward at-risk before a delivery failure.

## Inputs

- `Master/performance-history.csv` (Overall_Score, by Quarter)
- `Master/supplier-master.csv` (Annual_Spend_USD, Lifecycle_Stage)

## Triggers

Flag a supplier as at risk if any of these conditions hold:

1. Overall_Score dropped 10 or more points between the last two quarters on file.
2. Overall_Score below 60 for two consecutive quarters.
3. Quality_Score below 65 in the most recent quarter, regardless of trend.
4. Delivery_Score below 65 in the most recent quarter and Annual_Spend_USD above $500,000.

## Output

A ranked list (by point drop, descending) with these columns:
- Supplier_Name
- Q3_Score (or earliest of the two compared quarters)
- Q4_Score (or latest of the two compared quarters)
- Point_Drop
- Annual_Spend_USD

Save to `Drafts/At_Risk_Report_v1.csv` or to `Outputs/corrective-action-plans/at-risk-summary.md`, depending on the calling lesson.
"""

    (skills_dir / "assess-lifecycle-stage.md").write_text(assess, encoding="utf-8")
    print(f"  skills/assess-lifecycle-stage.md")
    (skills_dir / "detect-risk-triggers.md").write_text(detect, encoding="utf-8")
    print(f"  skills/detect-risk-triggers.md")


def build_claude_dir(claude_dir):
    claude_dir.mkdir(parents=True, exist_ok=True)
    commands_dir = claude_dir / "commands"
    commands_dir.mkdir(parents=True, exist_ok=True)

    settings = {
        "permissions": {
            "allow": [
                "Read(./Master/**)",
                "Read(./Drafts/**)",
                "Read(./Outputs/**)",
                "Read(./state/**)",
                "Read(./skills/**)",
                "Write(./Drafts/**)",
                "Write(./Outputs/**)",
                "Write(./state/**)",
                "Edit(./Drafts/**)",
                "Edit(./Outputs/**)",
                "Edit(./state/**)",
            ],
            "deny": [
                "Write(./Master/**)",
                "Edit(./Master/**)",
            ],
        },
    }
    (claude_dir / "settings.json").write_text(
        json.dumps(settings, indent=2), encoding="utf-8"
    )
    print(f"  .claude/settings.json")

    lifecycle_status = """# /lifecycle-status

Produce a full portfolio status report covering every supplier in `Master/supplier-master.csv`.

## Steps

1. Read `state/lifecycle-state.json` if it exists. That is the current truth for stages and decisions.
2. Read `Master/supplier-master.csv`, `Master/performance-history.csv`, `Master/compliance-status.csv`, and `Master/development-plans.csv`.
3. Apply the rules in `skills/assess-lifecycle-stage.md` to confirm or correct the stage on every supplier.
4. Group suppliers by stage. Report a count per stage.
5. List every supplier with a Decision_Status of `Deferred` or `CAP Issued` from the state file.
6. Save the full report to `Outputs/segmentation-report.md`.

## Output format

A markdown report with these sections:
- Header: today's date, total suppliers, total annual spend.
- Stage distribution table: Stage, Count, Total Spend.
- Per-stage supplier lists.
- Open decisions section (Deferred and CAP Issued).
- Recommendations: at most three.
"""

    onboard = """# /onboard-supplier

Run the onboarding compliance check for a single supplier and produce a checklist.

## Inputs

- The supplier name (passed as an argument).
- `Master/compliance-status.csv`
- `Master/Onboarding_Checklist_Template.docx`

## Steps

1. Find the supplier row in `Master/compliance-status.csv`.
2. Read every field in the row.
3. Compare each field to the 12-item checklist in the Word template.
4. Produce a two-column table: Checklist Item, Status (Complete, Missing, or Expired).
5. If any item is Missing or Expired, draft a follow-up email to the supplier with a 7-day deadline.
6. Save the checklist to `Outputs/onboarding-checklists/<supplier-name>-checklist.md`.

## Output format

A markdown file with the supplier name, the date, the 12-row checklist table, and the draft follow-up email at the bottom.
"""

    trigger_exit = """# /trigger-exit

Initiate the exit workflow for a supplier flagged for off-boarding.

## Inputs

- The supplier name (passed as an argument).
- `Master/supplier-master.csv`
- `Master/open-orders.csv`

## Steps

1. Find the supplier row in `Master/supplier-master.csv`. Confirm Lifecycle_Stage is `exit`.
2. Find every row in `Master/open-orders.csv` for the supplier where Status is not Closed or Cancelled. Sum the Amount_USD.
3. Build a seven-milestone transition timeline starting from today's date.
4. Draft a formal supplier exit notification letter listing every open PO and the deadlines.
5. Save the timeline and letter to `Outputs/exit-plans/<supplier-name>-exit-plan.md`.
6. Append a Decision_Log entry to `state/lifecycle-state.json` for that supplier.

## Output format

A markdown file with the supplier name, transition timeline table, exit letter, and a list of open POs with values and dates.
"""

    (commands_dir / "lifecycle-status.md").write_text(lifecycle_status, encoding="utf-8")
    print(f"  .claude/commands/lifecycle-status.md")
    (commands_dir / "onboard-supplier.md").write_text(onboard, encoding="utf-8")
    print(f"  .claude/commands/onboard-supplier.md")
    (commands_dir / "trigger-exit.md").write_text(trigger_exit, encoding="utf-8")
    print(f"  .claude/commands/trigger-exit.md")


def remove_stale_folders():
    """Drop folders the lessons no longer use.

    Earlier versions shipped data/ and outputs/ (lowercase). The lessons use
    Master/, Drafts/, Outputs/ instead. Remove the old layout so the student
    sees one clean tree.
    """
    for stale in ["data", "outputs"]:
        stale_path = PRACTICE / stale
        if stale_path.exists():
            shutil.rmtree(stale_path)
            print(f"  removed stale folder: {stale}/")


def main():
    print("Building Course 14 practice data...")
    print()

    PRACTICE.mkdir(parents=True, exist_ok=True)

    # Drop any leftover lowercase data/ or outputs/ folders from earlier builds.
    remove_stale_folders()

    # Master/ (read-only source)
    master_dir = PRACTICE / "Master"
    build_supplier_master(master_dir / "supplier-master.csv")
    build_performance_history(master_dir / "performance-history.csv")
    build_compliance_status(master_dir / "compliance-status.csv")
    build_development_plans(master_dir / "development-plans.csv")
    build_open_orders(master_dir / "open-orders.csv")
    build_onboarding_template(master_dir / "Onboarding_Checklist_Template.docx")
    build_heartland_dev_plan(master_dir / "Heartland_Polymers_Dev_Plan.docx")
    build_cap_template(master_dir / "CAP_Template.docx")

    # Drafts/ (working files; lessons fill it)
    drafts_dir = PRACTICE / "Drafts"
    drafts_dir.mkdir(parents=True, exist_ok=True)
    (drafts_dir / ".gitkeep").write_text("", encoding="utf-8")
    print(f"  Drafts/ (empty)")

    # Outputs/ (signed-off final files; lessons fill it)
    outputs_dir = PRACTICE / "Outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)
    (outputs_dir / ".gitkeep").write_text("", encoding="utf-8")
    print(f"  Outputs/ (empty)")

    # state/ (Lesson 6 generates lifecycle-state.json at runtime)
    state_dir = PRACTICE / "state"
    state_dir.mkdir(parents=True, exist_ok=True)
    (state_dir / ".gitkeep").write_text("", encoding="utf-8")
    print(f"  state/ (empty)")

    # skills/ (kept for student reference)
    build_skills(PRACTICE / "skills")

    # .claude/
    build_claude_dir(PRACTICE / ".claude")

    print()
    print("Done. All files in practice/.")


if __name__ == "__main__":
    main()
