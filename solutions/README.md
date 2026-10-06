# Reference programs

`tutor/task-notes.json` maps every active task to its reference program and records the date and submission of physical validation where available. The same programs feed the simulator audit and AI context. A passing simulator audit alone does not establish physical validation; entries marked `pending` still require a real-robot check.

Lesson prose and student-facing parameter hints are maintained in the lesson files. Validation dates, submission IDs and internal status stay in tutor metadata and are not inserted into lessons. Run `python3 scripts/build_tutor_context.py` after updating lessons, templates, references, checks or validation evidence.
