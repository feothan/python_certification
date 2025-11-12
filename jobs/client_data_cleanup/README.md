# Client Data Cleanup

Problem:
The raw CSV had inconsistent name formats, inconsistent date formats, duplicate entries, and missing required fields.

Solution:
Used pandas to normalize name formats, convert dates to ISO format, remove duplicate rows, and drop incomplete entries.

Outcome:
Produced a clean, uniform CSV suitable for reporting, import, or CRM upload.
